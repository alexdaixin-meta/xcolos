# 08 coder

- time: 2026-10-27T18:00:26+00:00 (138.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 42da090bdf17badb, reply sha256 cb06713707f62742

## Sent

````
# Task: write the XColos game file for "Wizard Triad"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

DECK: 28 cards. Three suits (Red, Blue, Green), each with ranks 1 to 8 (24 cards), plus 2 Wizards and 2 Jesters.

STRUCTURE: The game is 12 hands. Each hand is 3 tricks and each trick is one round, so the game is 36 rounds. Players are P1, P2 and P3, seated in that order. Play always proceeds P1 -> P2 -> P3 -> P1. There is no talk phase.

START OF A HAND (on the first trick of each hand only):
(1) Shuffle all 28 cards. Deal 3 cards face down to each player. Each player sees only their own cards.
(2) Turn the next card (the 10th) face up as the trump card. If it is a suited card, that suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.
(3) Bidding: all three players at the same moment secretly choose a bid of 0, 1, 2 or 3 tricks. A missing or invalid bid counts as 1. Then all bids are revealed to everyone. Bids need not add up to 3.
(4) The first lead of hand h goes to P1 if h is 1, 4, 7 or 10; to P2 if h is 2, 5, 8 or 11; and to P3 if h is 3, 6, 9 or 12.

EACH TRICK:
(5) The leader plays one card face up. Then the next player in seat order plays one card face up, then the third player.
(6) Led suit: the led suit is the suit of the first suited card played in the trick, but only if no Wizard was played before that card. If a Wizard is played before any suited card (for example, a Wizard is led, or a Jester is led and then a Wizard is played), the trick has no led suit. Until a suited card is played, there is no led suit yet.
(7) Legal plays: a Wizard or a Jester may always be played. If there is a led suit and the player holds a card of it, they must play a Wizard, a Jester or a card of the led suit. Otherwise they may play any card they hold.
(8) Illegal or unknown choices: if a player names a card they do not hold, or a card they may not legally play, the engine plays a card for them using this priority, checked in order:
   (a) if there is a led suit and the player holds a card of it, their lowest-ranked card of the led suit;
   (b) otherwise, a Jester, if they hold one;
   (c) otherwise, their lowest-ranked suited card, with ties between equal ranks broken Red before Blue before Green (for example, Red 2 is played before Blue 2);
   (d) otherwise, a Wizard.
   Step (a) is skipped whenever there is no led suit at that moment.
(9) Winning the trick:
   - If any Wizard was played, the first Wizard played wins.
   - Otherwise, if any trump card was played, the highest-ranked trump wins.
   - Otherwise, the highest-ranked card of the led suit wins.
   - With only 2 Jesters in the deck, a trick of three Jesters cannot occur. If no card qualifies under the rules above, the first Jester played wins.
(10) All played cards stay visible to everyone for the rest of the hand. The trick winner adds 1 to their tricks taken this hand and leads the next trick of the hand.

END OF A HAND (after the third trick):
(11) Each player compares their tricks taken with their bid.
   - Exact: they score 30 + 5 x bid. So bid 0 scores 30, bid 1 scores 35, bid 2 scores 40 and bid 3 scores 45.
   - Not exact: they score -10 x |tricks taken - bid|.
(12) Scores and all bids and tricks taken are announced. Tricks taken reset to 0 and all cards are collected for the next shuffle.

END OF GAME: after hand 12 (round 36).

How the winner is decided: After hand 12, the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Wizard Triad (3 to 3 players, best with 3)

A three-player trick-taking game over 12 hands of 3 tricks each. Players secretly bid how many tricks they will take, then follow suit, with Wizards, Jesters and trump, and score for hitting the bid exactly.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards the player holds this hand, such as 'R5', 'B1', 'G8', 'W1', 'W2', 'J1', 'J2'.
  - each player: bid (number, starts 0); everyone sees it. The player's bid this hand (0-3). It is revealed after the simultaneous poll.
  - each player: tricks_taken (number, starts 0); everyone sees it. Tricks won so far this hand.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played in the current trick (empty if not yet played).
  - each player: score (number, starts 0); everyone sees it. Running total score.
  - the table: deck (list, starts ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2']); hidden from all players. The undealt cards.
  - the table: trump_card (text, starts ''); everyone sees it. The face-up 10th card of this hand.
  - the table: trump_suit (text, starts ''); everyone sees it. 'R', 'B' or 'G' if the trump card is suited; 'none' if it is a Wizard or a Jester.
  - the table: hand_number (number, starts 0); everyone sees it. The current hand, 1-12.
  - the table: hands_done (number, starts 0); everyone sees it. Number of hands fully scored.
  - the table: trick_in_hand (number, starts 1); everyone sees it. Which trick of the hand is being played (1-3).
  - the table: leader (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: led_suit (text, starts ''); everyone sees it. '' means no led suit yet; 'R', 'B' or 'G' is the led suit; 'none' means a Wizard came before any suited card.
  - the table: wizard_played (bool, starts False); everyone sees it. Whether a Wizard has been played in the current trick.
  - the table: best_value (number, starts -1); hidden from all players. Strength of the card currently winning the trick.
  - the table: best_seat (number, starts 0); hidden from all players. The seat currently winning the trick.
  - the table: played_cards (list, starts []); everyone sees it. All cards played so far this hand, visible to everyone.
  - parameters, each kept as a table attribute: deck_size = 28, suits = 3, rank_min = 1, rank_max = 8, wizards = 2, jesters = 2, hands = 12, tricks_per_hand = 3, total_rounds = 36, cards_dealt_per_player = 3, trump_card_position = 10, bid_min = 0, bid_max = 3, default_bid = 1, exact_base = 30, exact_per_bid = 5, miss_penalty_per_trick = 10, wizard_strength = 100, trump_strength_bonus = 20, jester_strength = 0, offsuit_strength = -1, no_card_strength = -1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 are P1, P2 and P3. Play order is always 1 -> 2 -> 3 -> 1.
  2. Every score is set to 0, hand_number to 0, hands_done to 0, and trick_in_hand to 1.
  3. There is no talk phase.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_hand == 1: hand_number += 1. All 28 cards are returned to deck; every hand, played_card, bid and tricks_taken is reset to empty or 0; played_cards is cleared. Then 3 random draws are made from deck into each player's hand (remove from deck, append to hand). Then one random card is drawn from deck into trump_card. trump_suit = that card's suit letter if it is suited, else 'none'. leader = ((hand_number - 1) mod 3) + 1.
  2. [sync] all players. What happens: When trick_in_hand == 1: each player is sent their own hand, plus trump_card, trump_suit, hand_number and leader.
  3. [poll] all players answers: a whole number from 0 to 3. What happens: When trick_in_hand == 1: each player's bid is set to their answer. A missing or invalid answer sets bid = 1. Nobody sees any bid until all are in.
  4. [tell] all players. What happens: When trick_in_hand == 1: all bids are announced (Seat 1, Seat 2, Seat 3).
  5. [update] all players. What happens: Start of trick: led_suit = '', wizard_played = false, best_value = -1, best_seat = 0, and every played_card = ''.
  6. [ask] seat leader answers: one card from the offered legal cards in their hand. What happens: The card (or the fallback card from rule R9 if the answer is missing or invalid) is removed from hand, set as played_card and appended to played_cards. If it is a Wizard: strength = 100, and if led_suit == '' then led_suit = 'none'; wizard_played = true. If it is a Jester: strength = 0. If it is suited with suit s and rank r: if led_suit == '' and wizard_played == false then led_suit = s; strength = 20 + r if s == trump_suit, else r if s == led_suit, else -1. If strength > best_value, then best_value = strength and best_seat = this seat. Announced to all.
  7. [ask] seat (leader mod 3) + 1 answers: one card from the offered legal cards in their hand. What happens: Same processing as the leader's play: remove from hand, set played_card, append to played_cards, update led_suit, wizard_played, best_value and best_seat. Announced to all.
  8. [ask] seat ((leader + 1) mod 3) + 1 answers: one card from the offered legal cards in their hand. What happens: Same processing as the leader's play: remove from hand, set played_card, append to played_cards, update led_suit, wizard_played, best_value and best_seat. Announced to all.
  9. [update] all players. What happens: tricks_taken of seat best_seat += 1; leader = best_seat. The trick winner is announced.
  10. [update] all players. What happens: When trick_in_hand == 3: for each player, if tricks_taken == bid then score += 30 + 5 * bid, else score -= 10 * |tricks_taken - bid|. hands_done += 1. Scores, bids and tricks_taken are announced. Then tricks_taken = 0 for everyone.
  11. [update] all players. What happens: trick_in_hand = (trick_in_hand mod 3) + 1.
  12. [check] all players. What happens: End the game if hands_done == 12; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand starts (trick_in_hand == 1), then all 28 cards are shuffled into deck and each player is dealt exactly 3 cards into their hand, seen only by them.
  R2. When the 10th card (the trump card) is suited, then trump_suit is its suit; when it is a Wizard or a Jester, then trump_suit is 'none' for that hand.
  R3. When bidding, then all three players bid 0, 1, 2 or 3 simultaneously, and a missing or invalid bid becomes 1; all bids are then revealed, and they need not sum to 3.
  R4. When hand h starts, then the first leader is seat ((h - 1) mod 3) + 1: P1 for hands 1, 4, 7, 10; P2 for hands 2, 5, 8, 11; P3 for hands 3, 6, 9, 12.
  R5. When a trick is played, then the leader plays first, then the next seat in order 1 -> 2 -> 3 -> 1, then the third seat, each card face up.
  R6. When the first suited card of a trick is played and no Wizard was played before it, then its suit becomes the led suit; when a Wizard is played before any suited card, then the trick has no led suit.
  R7. When there is a led suit and a player holds a card of it, then they may play only a Wizard, a Jester or a card of the led suit; otherwise any card they hold is legal.
  R8. When a Wizard or a Jester is played, then it is always legal.
  R9. When a player's choice is missing or not a legal card they hold, then the engine plays, in order of priority: (a) their lowest led-suit card if a led suit exists and they hold one; (b) else a Jester; (c) else their lowest suited card, with ties broken Red, then Blue, then Green; (d) else a Wizard.
  R10. When any Wizard is played in a trick, then the first Wizard played wins the trick.
  R11. When no Wizard is played but at least one trump-suit card is, then the highest-ranked trump card wins the trick.
  R12. When no Wizard and no trump is played, then the highest-ranked card of the led suit wins the trick.
  R13. When no card qualifies under R10-R12, then the first Jester played wins the trick.
  R14. When a trick ends, then its winner's tricks_taken increases by 1 and that player leads the next trick of the hand.
  R15. When a card is played, then it stays visible in played_cards for the rest of the hand.
  R16. When a hand ends and a player's tricks_taken equals their bid, then they score 30 + 5 x bid (bid 0 = 30, 1 = 35, 2 = 40, 3 = 45).
  R17. When a hand ends and a player's tricks_taken differs from their bid, then they lose 10 x |tricks_taken - bid| points (for example, bid 2 and take 0 = -20).
  R18. When a hand ends, then scores, bids and tricks taken are announced, and tricks_taken resets to 0.
  R19. When hand 12 (round 36) has been scored, then the game ends and the highest total score wins; a tie for the highest total is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid at the start of each hand | asked: all three seats, simultaneously | options: 0, 1, 2 or 3
  - Card to play in a trick | asked: the seat whose turn it is (leader, then the next seat, then the third) | options: If led_suit is 'R', 'B' or 'G' and the seat holds a card of that suit: only their cards of the led suit plus any Wizards and Jesters they hold. Otherwise (no led suit yet, led_suit 'none', or no card of the led suit held): every card in their hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hands_done == 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after hand 12. The highest total wins; if two or three players tie for the highest total, they share the result (a draw).
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

- each player: `bid` (number, visible: public, starts 0): The player's bid this hand (0-3). It is revealed after the simultaneous poll.
- each player: `tricks_taken` (number, visible: public, starts 0): Tricks won so far this hand.
- each player: `played_card` (text, visible: public, starts ''): The card this player played in the current trick (empty if not yet played).
- each player: `score` (number, visible: public, starts 0): Running total score.
- the table: `trump_card` (text, visible: public, starts ''): The face-up 10th card of this hand.
- the table: `trump_suit` (text, visible: public, starts ''): 'R', 'B' or 'G' if the trump card is suited; 'none' if it is a Wizard or a Jester.
- the table: `hand_number` (number, visible: public, starts 0): The current hand, 1-12.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 28, suits = 3, rank_min = 1, rank_max = 8, wizards = 2, jesters = 2, hands = 12, tricks_per_hand = 3, total_rounds = 36, cards_dealt_per_player = 3, trump_card_position = 10, bid_min = 0, bid_max = 3, default_bid = 1, exact_base = 30, exact_per_bid = 5, miss_penalty_per_trick = 10, wizard_strength = 100, trump_strength_bonus = 20, jester_strength = 0, offsuit_strength = -1, no_card_strength = -1
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "wizard_triad",
    "name": "Wizard Triad",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, twelve hands of three tricks: bid in secret, follow suit, and score for hitting your bid exactly."
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
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "number",
        "initial": -1
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "W1", "W2", "J1", "J2"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "fallback_order",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_strength",
        "visible": "none",
        "type": "number",
        "initial": -1
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
        "initial": ""
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "wizard_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "best_value",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
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
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "suits",
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
        "initial": 8
      },
      {
        "key": "wizards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "jesters",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "initial": 3
      },
      {
        "key": "trump_card_position",
        "visible": "public",
        "type": "number",
        "initial": 10
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
        "key": "default_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_base",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "exact_per_bid",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "miss_penalty_per_trick",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "wizard_strength",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "trump_strength_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "jester_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offsuit_strength",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "no_card_strength",
        "visible": "public",
        "type": "number",
        "initial": -1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "prepare the table",
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
            "key": "hand_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hands_done",
            "value": 0
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
            "key": "fallback_order",
            "value": ["R1", "B1", "G1", "R2", "B2", "G2", "R3", "B3", "G3", "R4", "B4", "G4", "R5", "B5", "G5", "R6", "B6", "G6", "R7", "B7", "G7", "R8", "B8", "G8"]
          }
        }
      ],
      "text": "Seats 1, 2 and 3 are P1, P2 and P3. Play always goes 1 -> 2 -> 3 -> 1. There is no talk."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "trick_in_hand == 1"
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
              "calc": "deck + played_cards + ([trump_card] if trump_card != '' else [])"
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
            "key": "played_card",
            "value": ""
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
            "key": "bid_said",
            "value": -1
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
            "key": "played_cards",
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
              "calc": "pick[0] if pick[0] in ['R', 'B', 'G'] else 'none'"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "(hand_number - 1) % 3 + 1"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands}: the cards are shuffled and dealt. Trump card: {trump_card} (trump suit: {trump_suit}). Seat {leader} leads first."
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
      "text": "Hand {hand_number}: your cards. Trump card {trump_card}, trump suit {trump_suit}; seat {leader} leads."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bidding",
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
      "text": "Hand {hand_number}, trump card {trump_card} (trump suit {trump_suit}). Bid in secret how many of the {tricks_per_hand} tricks you will take: a whole number from {bid_min} to {bid_max}. Nobody sees a bid until all are in."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "record bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "you.bid_said if (you.bid_said >= bid_min and you.bid_said <= bid_max) else default_bid"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bid",
      "label": "bids revealed",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "all",
      "text": "Bids for hand {hand_number}: Seat 1 bids {players[0].bid}, Seat 2 bids {players[1].bid}, Seat 3 bids {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "start of trick",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": ""
          }
        },
        {
          "set": {
            "key": "wizard_played",
            "value": false
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "no_card_strength"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
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
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ],
      "text": "Trick {trick_in_hand} of hand {hand_number}. Seat {leader} leads."
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
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "card_a"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": {
                "calc": "$answer if $answer in players[$seat - 1].offer else (sorted([c for c in players[$seat - 1].hand if c[0] == led_suit])[0] if (led_suit in ['R', 'B', 'G'] and len([c for c in players[$seat - 1].hand if c[0] == led_suit]) > 0) else (sorted([c for c in players[$seat - 1].hand if c[0] == 'J'])[0] if len([c for c in players[$seat - 1].hand if c[0] == 'J']) > 0 else ([c for c in fallback_order if c in players[$seat - 1].hand][0] if len([c for c in fallback_order if c in players[$seat - 1].hand]) > 0 else players[$seat - 1].hand[0])))"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "pick"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": {
                "calc": "pick"
              },
              "text": "Seat {player} plays {pick}."
            }
          },
          {
            "append": {
              "key": "played_cards",
              "value": {
                "calc": "pick"
              }
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "(('none' if pick[0] == 'W' else (pick[0] if (pick[0] in ['R', 'B', 'G'] and not wizard_played) else ''))) if led_suit == '' else led_suit"
              }
            }
          },
          {
            "set": {
              "key": "wizard_played",
              "value": {
                "calc": "wizard_played or pick[0] == 'W'"
              }
            }
          },
          {
            "set": {
              "key": "card_strength",
              "value": {
                "calc": "wizard_strength if pick[0] == 'W' else (jester_strength if pick[0] == 'J' else ((trump_strength_bonus + int(pick[1])) if pick[0] == trump_suit else (int(pick[1]) if pick[0] == led_suit else offsuit_strength)))"
              }
            }
          },
          {
            "set": {
              "key": "best_seat",
              "value": "$seat",
              "if": {
                "calc": "card_strength > best_value"
              }
            }
          },
          {
            "set": {
              "key": "best_value",
              "value": {
                "calc": "max(best_value, card_strength)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_suit or c[0] == 'W' or c[0] == 'J'] if (led_suit in ['R', 'B', 'G'] and len([c for c in you.hand if c[0] == led_suit]) > 0) else you.hand"
              }
            }
          }
        ]
      },
      "text": "You lead trick {trick_in_hand} of hand {hand_number}. Trump suit: {trump_suit}. Play one card from your hand face up."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the second card",
      "to": {
        "where": "you.seat == leader % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "card_b"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": {
                "calc": "$answer if $answer in players[$seat - 1].offer else (sorted([c for c in players[$seat - 1].hand if c[0] == led_suit])[0] if (led_suit in ['R', 'B', 'G'] and len([c for c in players[$seat - 1].hand if c[0] == led_suit]) > 0) else (sorted([c for c in players[$seat - 1].hand if c[0] == 'J'])[0] if len([c for c in players[$seat - 1].hand if c[0] == 'J']) > 0 else ([c for c in fallback_order if c in players[$seat - 1].hand][0] if len([c for c in fallback_order if c in players[$seat - 1].hand]) > 0 else players[$seat - 1].hand[0])))"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "pick"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": {
                "calc": "pick"
              },
              "text": "Seat {player} plays {pick}."
            }
          },
          {
            "append": {
              "key": "played_cards",
              "value": {
                "calc": "pick"
              }
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "(('none' if pick[0] == 'W' else (pick[0] if (pick[0] in ['R', 'B', 'G'] and not wizard_played) else ''))) if led_suit == '' else led_suit"
              }
            }
          },
          {
            "set": {
              "key": "wizard_played",
              "value": {
                "calc": "wizard_played or pick[0] == 'W'"
              }
            }
          },
          {
            "set": {
              "key": "card_strength",
              "value": {
                "calc": "wizard_strength if pick[0] == 'W' else (jester_strength if pick[0] == 'J' else ((trump_strength_bonus + int(pick[1])) if pick[0] == trump_suit else (int(pick[1]) if pick[0] == led_suit else offsuit_strength)))"
              }
            }
          },
          {
            "set": {
              "key": "best_seat",
              "value": "$seat",
              "if": {
                "calc": "card_strength > best_value"
              }
            }
          },
          {
            "set": {
              "key": "best_value",
              "value": {
                "calc": "max(best_value, card_strength)"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_suit or c[0] == 'W' or c[0] == 'J'] if (led_suit in ['R', 'B', 'G'] and len([c for c in you.hand if c[0] == led_suit]) > 0) else you.hand"
              }
            }
          }
        ]
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Trump suit: {trump_suit}; led suit: {led_suit} ('' = none yet, 'none' = no led suit). Cards played this hand: {played_cards}. Play one card face up from those offered."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the third card",
      "to": {
        "where": "you.seat == (leader + 1) % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "card_c"
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "pick",
              "value": {
                "calc": "$answer if $answer in players[$seat - 1].offer else (sorted([c for c in players[$seat - 1].hand if c[0] == led_suit])[0] if (led_suit in ['R', 'B', 'G'] and len([c for c in players[$seat - 1].hand if c[0] == led_suit]) > 0) else (sorted([c for c in players[$seat - 1].hand if c[0] == 'J'])[0] if len([c for c in players[$seat - 1].hand if c[0] == 'J']) > 0 else ([c for c in fallback_order if c in players[$seat - 1].hand][0] if len([c for c in fallback_order if c in players[$seat - 1].hand]) > 0 else players[$seat - 1].hand[0])))"
              }
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "pick"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": {
                "calc": "pick"
              },
              "text": "Seat {player} plays {pick}."
            }
          },
          {
            "append": {
              "key": "played_cards",
              "value": {
                "calc": "pick"
              }
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "(('none' if pick[0] == 'W' else (pick[0] if (pick[0] in ['R', 'B', 'G'] and not wizard_played) else ''))) if led_suit == '' else led_suit"
              }
            }
          },
          {
            "set": {
              "key": "wizard_played",
              "value": {
                "calc": "wizard_played or pick[0] == 'W'"
              }
            }
          },
          {
            "set": {
              "key": "card_strength",
              "value": {
                "calc": "wizard_strength if pick[0] == 'W' else (jester_strength if pick[0] == 'J' else ((trump_strength_bonus + int(pick[1])) if pick[0] == trump_suit else (int(pick[1]) if pick[0] == led_suit else offsuit_strength)))"
              }
            }
          },
          {
            "set": {
              "key": "best_seat",
              "value": "$seat",
              "if": {
                "calc": "card_strength > best_value"
              }
            }
          },
          {
            "set": {
              "key": "best_value",
              "value": {
                "calc": "max(best_value, card_strength)"
              }
            }
          }
        ]
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Trump suit: {trump_suit}; led suit: {led_suit} ('' = none yet, 'none' = no led suit). Cards played this hand: {played_cards}. Play one card face up from those offered."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "trick winner",
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "best_seat"
            },
            "key": "tricks_taken",
            "value": 1,
            "if": {
              "calc": "best_seat > 0"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "best_seat"
            },
            "if": {
              "calc": "best_seat > 0"
            }
          }
        }
      ],
      "text": "Seat {leader} wins trick {trick_in_hand} and leads next. Tricks taken: Seat 1 {players[0].tricks_taken}, Seat 2 {players[1].tricks_taken}, Seat 3 {players[2].tricks_taken}."
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
              "calc": "(exact_base + exact_per_bid * you.bid) if you.tricks_taken == you.bid else (0 - miss_penalty_per_trick * abs(you.tricks_taken - you.bid))"
            }
          }
        },
        {
          "adjust": {
            "key": "hands_done",
            "value": 1
          }
        }
      ],
      "text": "Hand {hand_number} scored. Seat 1: bid {players[0].bid}, took {players[0].tricks_taken}, score {players[0].score}. Seat 2: bid {players[1].bid}, took {players[1].tricks_taken}, score {players[1].score}. Seat 3: bid {players[2].bid}, took {players[2].tricks_taken}, score {players[2].score}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "next trick",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "tricks_taken",
            "value": 0,
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "trick_in_hand % tricks_per_hand + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last hand",
      "when": {
        "calc": "hands_done >= hands"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hands_done >= hands"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "Wizard Triad: three players (P1, P2, P3 in seats 1, 2, 3); play always goes 1 -> 2 -> 3 -> 1. There is no talk. The deck has {deck_size} cards: {suits} suits (Red R, Blue B, Green G) with ranks {rank_min} to {rank_max}, plus {wizards} Wizards (W1, W2) and {jesters} Jesters (J1, J2). The game is {hands} hands of {tricks_per_hand} tricks; each trick is one round ({total_rounds} rounds).\n\nSTART OF A HAND: (1) All {deck_size} cards are shuffled and {cards_dealt_per_player} are dealt face down to each player; you see only your own. (2) The next card (card {trump_card_position}) is turned face up as the trump card. If it is suited, that suit is trump for the hand; if it is a Wizard or a Jester, there is no trump this hand. (3) Bidding: all three players at the same moment secretly bid {bid_min} to {bid_max} tricks. A missing or invalid bid counts as {default_bid}. Then all bids are revealed to everyone. Bids need not add up to {tricks_per_hand}. (4) The first lead of hand h goes to P1 if h is 1, 4, 7 or 10; to P2 if h is 2, 5, 8 or 11; to P3 if h is 3, 6, 9 or 12.\n\nEACH TRICK: (5) The leader plays one card face up, then the next player in seat order, then the third. (6) The led suit is the suit of the first suited card played in the trick, but only if no Wizard was played before it. If a Wizard is played before any suited card (a Wizard is led, or a Jester is led and then a Wizard is played), the trick has no led suit. Until a suited card is played there is no led suit yet. (7) A Wizard or a Jester may always be played. If there is a led suit and you hold a card of it, you must play a Wizard, a Jester or a card of the led suit; otherwise you may play any card you hold. You are only offered legal cards. (8) If a choice is missing or not a legal card you hold, the engine plays for you, checked in order: (a) if there is a led suit and you hold it, your lowest card of the led suit; (b) otherwise a Jester if you hold one; (c) otherwise your lowest-ranked suited card, ties broken Red before Blue before Green; (d) otherwise a Wizard. Step (a) is skipped when there is no led suit at that moment. (9) Winning the trick: if any Wizard was played, the first Wizard played wins. Otherwise, if any trump was played, the highest trump wins. Otherwise the highest card of the led suit wins. If no card qualifies, the first Jester played wins. (10) Played cards stay visible to everyone for the rest of the hand. The trick winner adds 1 to their tricks taken and leads the next trick of the hand.\n\nEND OF A HAND: (11) If your tricks taken equal your bid exactly, you score {exact_base} + {exact_per_bid} x bid (bid 0 = 30, 1 = 35, 2 = 40, 3 = 45). If not, you lose {miss_penalty_per_trick} x |tricks taken - bid| (e.g. bid 2, take 0 = -20). (12) Scores, bids and tricks taken are announced; tricks taken reset to 0 and all cards are collected for the next shuffle.\n\nEND OF GAME: after hand {hands}, the highest total score wins. If two or three players tie for the highest total, they share the result (a draw)."
}
```
````
