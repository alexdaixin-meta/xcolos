# 44 coder

- time: 2026-10-27T18:51:50+00:00 (89.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1d4db30765cd1603, reply sha256 e62d32c20bb28f6d

## Sent

````
# Task: write the XColos game file for "Pocket Wizard"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. The deck has 28 cards: suits R, B and G, each with ranks 1 to 8 (written R1..R8, B1..B8, G1..G8), plus two Wizards (W1, W2) and two Jesters (J1, J2). The full deck in order is R1-R8, B1-B8, G1-G8, W1, W2, J1, J2.

STATE. Each seat has: hand (an ordered list of cards, private to that seat), bid, tricks_taken, played_card, offer, score, bid_answer. The table has: deck, trump_card, trump_suit, hand_number, trick_in_hand, leader, led_suit, best_value, best_seat, cur_card, cur_seat, cur_strength. At setup: every score is 0, every bid is 0, every tricks_taken is 0, hand_number is 0, trick_in_hand is 1, leader is 1, and the deck holds all 28 cards.

The game lasts 27 rounds. Each round is one trick, and every 3 rounds make one hand.

R1 New hand. This happens only at the start of a round in which trick_in_hand is 1. In rounds where trick_in_hand is 2 or 3, nothing is dealt and hands are left exactly as they are.
- hand_number increases by 1.
- The deck is refilled to the full 28 cards and shuffled. This is the round's only random draw.
- Every tricks_taken becomes 0.
- Starting with seat 1, then seat 2, then seat 3, each seat takes the top 3 cards in turn. They are appended to its hand in the order taken, so each seat holds exactly 3 cards.
- leader becomes seat ((hand_number - 1) mod 3) + 1.

R2 Trump. When a hand is dealt, one further card is taken from the deck and becomes trump_card, leaving exactly 18 cards in the deck. If trump_card is an R, B or G card, trump_suit is that suit. If it is a Wizard or a Jester, trump_suit is 'none' (no trump). trump_card and trump_suit are announced to everyone.

R3 Bidding (only when trick_in_hand is 1). All three seats answer at the same moment, each seeing only its own hand and the trump card: 'How many tricks will you take this hand? Answer 0, 1, 2 or 3.'

R4 Bid validation. An answer that is exactly 0, 1, 2 or 3 becomes that seat's bid unchanged. A legal 0 stays 0. If an answer is missing or is anything else, that seat's bid is 1. All three bids are then announced.

R5 Start of trick. led_suit becomes 'none', best_value becomes -1, and best_seat becomes the leader.

R6 Play order. Seats play one at a time, in the order leader, then the next seat up (after seat 3 comes seat 1), then the next. Every played card is shown to all players at once.

R7 Offer. Just before a seat plays, its offer is built from its hand in hand order.
- If led_suit is a suit and the seat holds at least one card of that suit, the offer is every card of that suit plus every Wizard and Jester, kept in the order they appear in the hand.
- Otherwise the offer is the whole hand, in hand order.

R8 Play. The seat is asked to choose one card from its offer. If the answer is missing or not in the offer, the first card of the offer is played. The played card is removed from the hand, and the remaining cards keep their order. It becomes played_card, and is recorded as cur_card with cur_seat.

R9 Led suit. If led_suit is 'none', best_value is below 100, and the card just played is an R, B or G card, led_suit becomes that card's suit. This is checked before strength is computed.

R10 Strength. The strength of the card just played is:
- 100 if it is a Wizard and best_value is below 100;
- 0 if it is a Wizard and a Wizard was already played this trick;
- 0 if it is a Jester;
- 20 + rank if its suit equals trump_suit;
- its rank if its suit equals led_suit (and that is not the trump suit);
- 0 for any other card.
If the strength is strictly greater than best_value, best_value becomes that strength and best_seat becomes the seat that played it. A tie never changes the winner. As a result, the first Wizard always wins; if only Jesters are played, the first Jester wins; and after a Jester lead, the first suited card sets the led suit.

R11 Trick award. After all three seats have played, best_seat's tricks_taken increases by 1 and best_seat becomes the leader of the next trick.

R12 Hand scoring (when trick_in_hand is 3, after R11). For each seat:
- if tricks_taken equals bid, score increases by 20 + 10 × tricks_taken;
- otherwise score decreases by 10 × |tricks_taken - bid|.
All scores are announced.

R13 Advance. trick_in_hand increases by 1. If it would become 4, it becomes 1 instead.

R14 End. After round 27 (9 hands), the game ends.

How the winner is decided: After 27 rounds, the seat with the highest score wins. If two or three seats tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Pocket Wizard (3 to 3 players, best with 3)

A three-player Wizard-style trick-taking game: 9 hands of 3 tricks each, where every seat bids how many tricks it will take and scores for hitting its bid exactly.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Ordered list of the cards this seat holds.
  - each player: bid (number, starts 0); everyone sees it. Tricks this seat bid for the current hand (0 to 3).
  - each player: bid_answer (text, starts ''); only its owner sees it. This seat's raw answer to the bidding question, before validation.
  - each player: tricks_taken (number, starts 0); everyone sees it. Tricks this seat has won in the current hand.
  - each player: played_card (text, starts ''); everyone sees it. The card this seat played to the current trick.
  - each player: offer (list, starts []); only its owner sees it. The legal cards this seat may play right now, in hand order.
  - each player: score (number, starts 0); everyone sees it. This seat's running score.
  - the table: deck (list, starts ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2']); hidden from all players. The cards not yet dealt.
  - the table: trump_card (text, starts ''); everyone sees it. The card turned up after the deal.
  - the table: trump_suit (text, starts 'none'); everyone sees it. R, B, G or none.
  - the table: hand_number (number, starts 0); everyone sees it. Which hand is being played (1 to 9).
  - the table: trick_in_hand (number, starts 1); everyone sees it. Which trick of the hand this round is (1 to 3).
  - the table: leader (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: led_suit (text, starts 'none'); everyone sees it. The suit led in this trick, or none.
  - the table: best_value (number, starts -1); everyone sees it. The highest strength played so far in this trick.
  - the table: best_seat (number, starts 1); everyone sees it. The seat currently winning the trick.
  - the table: cur_card (text, starts ''); everyone sees it. The card just played.
  - the table: cur_seat (number, starts 0); everyone sees it. The seat that just played.
  - the table: cur_strength (number, starts 0); everyone sees it. The strength of the card just played.
  - parameters, each kept as a table attribute: deck_size = 28, suits = 3, ranks_per_suit = 8, wizards = 2, jesters = 2, total_rounds = 27, tricks_per_hand = 3, hands = 9, cards_dealt_per_seat = 3, trump_cards_turned = 1, deck_left_after_deal = 18, bid_min = 0, bid_max = 3, default_bid = 1, best_value_start = -1, wizard_strength = 100, jester_strength = 0, second_wizard_strength = 0, trump_bonus = 20, exact_bid_bonus = 20, points_per_trick_on_exact_bid = 10, penalty_per_trick_off = 10, first_leader = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every seat's score, bid and tricks_taken are set to 0, and every hand is empty.
  2. hand_number is set to 0, trick_in_hand to 1 and leader to 1.
  3. The deck is filled with all 28 cards in the order R1-R8, B1-B8, G1-G8, W1, W2, J1, J2.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_hand == 1: hand_number += 1. The deck is reset to the full 28 cards. Every tricks_taken = 0. Dealing goes seat 1, then seat 2, then seat 3: each seat draws 3 cards at random from the deck, one at a time, and each card is appended to its hand in the order drawn and removed from the deck. leader = ((hand_number - 1) mod 3) + 1.
  2. [update] all players. What happens: When trick_in_hand == 1: one card is drawn at random from the deck into trump_card and removed from the deck, leaving 18 cards. trump_suit = the first letter of trump_card if that letter is R, B or G, otherwise 'none'. Announce trump_card and trump_suit to everyone.
  3. [sync] all players. What happens: When trick_in_hand == 1: each seat is shown its own hand, trump_card and trump_suit.
  4. [poll] all players answers: a whole number from 0 to 3: 'How many tricks will you take this hand?'. What happens: When trick_in_hand == 1: each answer is stored in that seat's bid_answer.
  5. [update] all players. What happens: When trick_in_hand == 1: bid = bid_answer if it is exactly 0, 1, 2 or 3; otherwise bid = 1. Announce all three bids.
  6. [update] all players. What happens: Start of trick: led_suit = 'none', best_value = -1, best_seat = leader.
  7. [update] seat leader. What happens: Build the leader's offer. If led_suit is not 'none' and the hand holds at least one card of led_suit, offer = the cards of led_suit plus every W and J card, in hand order. Otherwise offer = the whole hand, in hand order.
  8. [ask] seat leader answers: one card from that seat's offer. What happens: If the answer is missing or not in the offer, the first card of the offer is used. The card is removed from the hand, and the remaining cards keep their order. played_card = that card, cur_card = that card, cur_seat = this seat. The card is shown to all players.
  9. [update] all players. What happens: If led_suit == 'none' and best_value < 100 and cur_card is an R, B or G card, then led_suit = the suit of cur_card. Then set cur_strength: 100 if cur_card is a W and best_value < 100; 0 if cur_card is a W and best_value >= 100; 0 if cur_card is a J; 20 + rank if the suit of cur_card == trump_suit; rank if the suit of cur_card == led_suit; otherwise 0. If cur_strength > best_value, then best_value = cur_strength and best_seat = cur_seat.
  10. [update] seat (leader mod 3) + 1. What happens: Build that seat's offer by the same rule as for the leader.
  11. [ask] seat (leader mod 3) + 1 answers: one card from that seat's offer. What happens: Same as the leader's play: an invalid answer plays the first card of the offer; the card is removed from the hand; played_card, cur_card and cur_seat are set; the card is shown to all.
  12. [update] all players. What happens: Apply the led-suit and strength rules to cur_card, exactly as after the leader's play.
  13. [update] seat ((leader + 1) mod 3) + 1. What happens: Build that seat's offer by the same rule as for the leader.
  14. [ask] seat ((leader + 1) mod 3) + 1 answers: one card from that seat's offer. What happens: Same as the leader's play: an invalid answer plays the first card of the offer; the card is removed from the hand; played_card, cur_card and cur_seat are set; the card is shown to all.
  15. [update] all players. What happens: Apply the led-suit and strength rules to cur_card, exactly as after the leader's play.
  16. [update] all players. What happens: Trick award: the tricks_taken of seat best_seat += 1; leader = best_seat. Announce the trick winner.
  17. [update] all players. What happens: When trick_in_hand == 3: for each seat, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |tricks_taken - bid|. Announce all scores.
  18. [update] all players. What happens: trick_in_hand += 1; if trick_in_hand == 4, then trick_in_hand = 1.
  19. [check] all players. What happens: End the game if hand_number == 9 and trick_in_hand == 1 (27 rounds have been played); otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a round starts with trick_in_hand == 1, then hand_number increases by 1, the deck is refilled to 28 cards, every tricks_taken becomes 0, and seats 1, 2 and 3 each receive 3 cards in that order.
  R1b. When a round starts with trick_in_hand == 2 or 3, then no cards are dealt and no hand changes except through play.
  R1c. When a hand is dealt, then leader becomes ((hand_number - 1) mod 3) + 1, so hand 1 is led by seat 1, hand 2 by seat 2 and hand 4 by seat 1.
  R2. When a hand is dealt, then one more card becomes trump_card and exactly 18 cards remain in the deck.
  R2b. When trump_card is an R, B or G card, then trump_suit is that suit; when it is W1, W2, J1 or J2, then trump_suit is 'none'.
  R3. When trick_in_hand == 1, then all three seats are asked for a bid at the same time, and none sees another's bid before answering.
  R4. When a bid answer is exactly 0, 1, 2 or 3, then bid equals that answer (a 0 stays 0); when it is missing or anything else, then bid is 1.
  R5. When a trick starts, then led_suit is 'none', best_value is -1 and best_seat is the leader.
  R6. When a trick is played, then the seats play in the order leader, (leader mod 3) + 1, ((leader + 1) mod 3) + 1, so a trick led by seat 3 is played by seats 3, 1, 2.
  R7. When led_suit is a suit and the seat holds a card of that suit, then its offer is exactly its cards of that suit plus its W and J cards, in hand order; otherwise its offer is its whole hand.
  R8. When a seat's answer is missing or not in its offer, then the first card of the offer is played; the played card leaves the hand and the other cards keep their order.
  R9. When led_suit is 'none', best_value < 100 and an R, B or G card is played, then led_suit becomes that card's suit (so after a Jester lead, the first suited card sets the led suit, but after a Wizard lead it does not).
  R10a. When a Wizard is played and best_value < 100, then its strength is 100, so the first Wizard always wins the trick.
  R10b. When a Wizard is played after another Wizard in the same trick, or a Jester is played, then its strength is 0.
  R10c. When a card of trump_suit is played, then its strength is 20 + rank (for example, trump 3 = 23).
  R10d. When a card of led_suit that is not trump is played, then its strength is its rank; any other card has strength 0.
  R10e. When a strength is strictly greater than best_value, then best_value and best_seat update; a tie never changes best_seat, so if only Jesters are played, the first Jester wins.
  R11. When all three seats have played, then best_seat's tricks_taken increases by 1 and best_seat leads the next trick.
  R12a. When trick_in_hand == 3 and a seat's tricks_taken equals its bid, then its score increases by 20 + 10 * tricks_taken (bid 0 and took 0 gives +20; bid 2 and took 2 gives +40).
  R12b. When trick_in_hand == 3 and tricks_taken differs from bid, then score decreases by 10 * |tricks_taken - bid| (bid 3 and took 1 gives -20).
  R13. When a round ends, then trick_in_hand increases by 1, wrapping from 3 back to 1.
  R14. When 27 rounds (9 hands) have been played, then the game ends and the highest score wins; seats tied at the top share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid: how many tricks will you take this hand? | asked: all three seats, at the same time, when trick_in_hand == 1 | options: a whole number 0, 1, 2 or 3
  - Play a card | asked: the seat whose turn it is in the trick | options: The leader, or any seat while led_suit is 'none': every card in its hand. A follower holding at least one card of led_suit: those cards plus its Wizards and Jesters, in hand order. A follower holding no card of led_suit: every card in its hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number == 9 and trick_in_hand == 1
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 27 rounds (9 hands), each seat's standing is its score. The highest score wins, and seats tied for the highest score share the result (the source calls this a draw).
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

- each player: `bid` (number, visible: public, starts 0): Tricks this seat bid for the current hand (0 to 3).
- each player: `tricks_taken` (number, visible: public, starts 0): Tricks this seat has won in the current hand.
- each player: `played_card` (text, visible: public, starts ''): The card this seat played to the current trick.
- each player: `score` (number, visible: public, starts 0): This seat's running score.
- the table: `trump_card` (text, visible: public, starts ''): The card turned up after the deal.
- the table: `trump_suit` (text, visible: public, starts 'none'): R, B, G or none.
- the table: `hand_number` (number, visible: public, starts 0): Which hand is being played (1 to 9).
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 28, suits = 3, ranks_per_suit = 8, wizards = 2, jesters = 2, total_rounds = 27, tricks_per_hand = 3, hands = 9, cards_dealt_per_seat = 3, trump_cards_turned = 1, deck_left_after_deal = 18, bid_min = 0, bid_max = 3, default_bid = 1, best_value_start = -1, wizard_strength = 100, jester_strength = 0, second_wizard_strength = 0, trump_bonus = 20, exact_bid_bonus = 20, points_per_trick_on_exact_bid = 10, penalty_per_trick_off = 10, first_leader = 1
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
    "id": "pocket_wizard",
    "name": "Pocket Wizard",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three-player Wizard-style trick-taking: 9 hands of 3 tricks, bid your tricks and score for hitting the bid exactly."
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
        "key": "bid_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "score",
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
        "initial": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "W1", "W2", "J1", "J2"]
      },
      {
        "key": "full_deck",
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
        "key": "trump_card",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "trump_suit",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "hand_number",
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
        "initial": "none"
      },
      {
        "key": "best_value",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cur_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
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
        "key": "ranks_per_suit",
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
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 27
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_dealt_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "trump_cards_turned",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_left_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 18
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
        "key": "best_value_start",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "wizard_strength",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "jester_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_wizard_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
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
        "key": "first_leader",
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
            "key": "hand",
            "value": []
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
            "key": "trick_in_hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "first_leader"
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
      "label": "new hand",
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
              "calc": "full_deck"
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
            "key": "leader",
            "value": {
              "calc": "hand_number - 3 * int((hand_number - 1) / 3)"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands} is dealt: {cards_dealt_per_seat} cards to each seat. Seat {leader} leads."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "trump",
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
              "calc": "trump_card[0] if trump_card[0] in ['R', 'B', 'G'] else 'none'"
            }
          }
        }
      ],
      "text": "The trump card is {trump_card}. Trump suit: {trump_suit}."
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
      "text": "Hand {hand_number}: trump card {trump_card}, trump suit {trump_suit}. Your cards:"
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
      "store": "bid_answer",
      "text": "Trump card {trump_card} (trump suit {trump_suit}). How many tricks will you take this hand? Answer 0, 1, 2 or 3."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_answer) if (you.bid_answer in ['0', '1', '2', '3'] or you.bid_answer in [0, 1, 2, 3]) else default_bid"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_answer",
            "value": ""
          }
        }
      ],
      "text": "Bids: Seat 1 {players[0].bid}, Seat 2 {players[1].bid}, Seat 3 {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "start of trick",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "best_value_start"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "leader"
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
      ],
      "text": "Trick {trick_in_hand} of hand {hand_number}. Seat {leader} leads."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "leader's offer",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == leader"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader plays",
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
        "bind": "p1"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Trump suit: {trump_suit}. You lead: play one card from your offer."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "leader's card counts",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "leader"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "$p1 if $p1 in players[cur_seat - 1].offer else players[cur_seat - 1].offer[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "played_card",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "cur_card[0]"
            },
            "if": {
              "calc": "led_suit == 'none' and best_value < wizard_strength and cur_card[0] in ['R', 'B', 'G']"
            }
          }
        },
        {
          "set": {
            "key": "cur_strength",
            "value": {
              "calc": "wizard_strength if (cur_card[0] == 'W' and best_value < wizard_strength) else (second_wizard_strength if cur_card[0] == 'W' else (jester_strength if cur_card[0] == 'J' else ((trump_bonus + int(cur_card[1])) if cur_card[0] == trump_suit else (int(cur_card[1]) if cur_card[0] == led_suit else 0))))"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "cur_seat"
            },
            "if": {
              "calc": "cur_strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "max(best_value, cur_strength)"
            }
          }
        }
      ],
      "text": "Led suit: {led_suit}. Seat {best_seat} is winning the trick."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second seat's offer",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == (1 if leader == 3 else leader + 1)"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second seat plays",
      "to": {
        "where": "you.seat == (1 if leader == 3 else leader + 1)"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "p2"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Led suit: {led_suit}; trump suit: {trump_suit}; seat {best_seat} is winning. Play one card from your offer."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second card counts",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "1 if leader == 3 else leader + 1"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "$p2 if $p2 in players[cur_seat - 1].offer else players[cur_seat - 1].offer[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "played_card",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "cur_card[0]"
            },
            "if": {
              "calc": "led_suit == 'none' and best_value < wizard_strength and cur_card[0] in ['R', 'B', 'G']"
            }
          }
        },
        {
          "set": {
            "key": "cur_strength",
            "value": {
              "calc": "wizard_strength if (cur_card[0] == 'W' and best_value < wizard_strength) else (second_wizard_strength if cur_card[0] == 'W' else (jester_strength if cur_card[0] == 'J' else ((trump_bonus + int(cur_card[1])) if cur_card[0] == trump_suit else (int(cur_card[1]) if cur_card[0] == led_suit else 0))))"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "cur_seat"
            },
            "if": {
              "calc": "cur_strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "max(best_value, cur_strength)"
            }
          }
        }
      ],
      "text": "Led suit: {led_suit}. Seat {best_seat} is winning the trick."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third seat's offer",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == (3 if leader == 1 else leader - 1)"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third seat plays",
      "to": {
        "where": "you.seat == (3 if leader == 1 else leader - 1)"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "p3"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Led suit: {led_suit}; trump suit: {trump_suit}; seat {best_seat} is winning. You play last: play one card from your offer."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "
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
    "id": "pocket_wizard",
    "name": "Pocket Wizard",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three-player Wizard-style trick-taking: 9 hands of 3 tricks, bid your tricks and score for hitting the bid exactly."
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
        "key": "bid_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "score",
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
          "R1",
          "R2",
          "R3",
          "R4",
          "R5",
          "R6",
          "R7",
          "R8",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "B6",
          "B7",
          "B8",
          "G1",
          "G2",
          "G3",
          "G4",
          "G5",
          "G6",
          "G7",
          "G8",
          "W1",
          "W2",
          "J1",
          "J2"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
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
        "key": "hand_number",
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
        "initial": "none"
      },
      {
        "key": "best_value",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cur_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
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
        "key": "ranks_per_suit",
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
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 27
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "cards_dealt_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "trump_cards_turned",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_left_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 18
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
        "key": "best_value_start",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "wizard_strength",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "jester_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_wizard_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
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
        "key": "first_leader",
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
            "key": "hand",
            "value": []
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
            "key": "trick_in_hand",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "first_leader"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": [
              "R1",
              "R2",
              "R3",
              "R4",
              "R5",
              "R6",
              "R7",
              "R8",
              "B1",
              "B2",
              "B3",
              "B4",
              "B5",
              "B6",
              "B7",
              "B8",
              "G1",
              "G2",
              "G3",
              "G4",
              "G5",
              "G6",
              "G7",
              "G8",
              "W1",
              "W2",
              "J1",
              "J2"
            ]
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
      "label": "new hand",
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
            "value": [
              "R1",
              "R2",
              "R3",
              "R4",
              "R5",
              "R6",
              "R7",
              "R8",
              "B1",
              "B2",
              "B3",
              "B4",
              "B5",
              "B6",
              "B7",
              "B8",
              "G1",
              "G2",
              "G3",
              "G4",
              "G5",
              "G6",
              "G7",
              "G8",
              "W1",
              "W2",
              "J1",
              "J2"
            ]
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
            "key": "bid_answer",
            "value": ""
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
            "key": "leader",
            "value": {
              "calc": "hand_number - 3 * int((hand_number - 1) / 3)"
            }
          }
        }
      ],
      "text": "Hand {hand_number} of {hands} is dealt: {cards_dealt_per_seat} cards to each seat. Seat {leader} leads."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "trump",
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
              "calc": "trump_card[0] if trump_card[0] in ['R', 'B', 'G'] else 'none'"
            }
          }
        }
      ],
      "text": "The trump card is {trump_card}. Trump suit: {trump_suit}."
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
      "text": "Hand {hand_number}: trump card {trump_card}, trump suit {trump_suit}. Your cards:"
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
      "store": "bid_answer",
      "text": "Trump card {trump_card} (trump suit {trump_suit}). How many tricks will you take this hand? Answer 0, 1, 2 or 3."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_answer) if (you.bid_answer in ['0', '1', '2', '3'] or you.bid_answer in [0, 1, 2, 3]) else default_bid"
            }
          }
        }
      ],
      "text": "Bids: Seat 1 {players[0].bid}, Seat 2 {players[1].bid}, Seat 3 {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "start of trick",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "best_value_start"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "leader"
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
      ],
      "text": "Trick {trick_in_hand} of hand {hand_number}. Seat {leader} leads."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "leader's offer",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == leader"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader plays",
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
        "bind": "p1"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Trump suit: {trump_suit}. You lead: play one card from your offer."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "leader's card counts",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "leader"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "$p1 if $p1 in players[cur_seat - 1].offer else players[cur_seat - 1].offer[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "played_card",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "cur_card[0]"
            },
            "if": {
              "calc": "led_suit == 'none' and best_value < wizard_strength and cur_card[0] in ['R', 'B', 'G']"
            }
          }
        },
        {
          "set": {
            "key": "cur_strength",
            "value": {
              "calc": "wizard_strength if (cur_card[0] == 'W' and best_value < wizard_strength) else (second_wizard_strength if cur_card[0] == 'W' else (jester_strength if cur_card[0] == 'J' else ((trump_bonus + int(cur_card[1])) if cur_card[0] == trump_suit else (int(cur_card[1]) if cur_card[0] == led_suit else 0))))"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "cur_seat"
            },
            "if": {
              "calc": "cur_strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "max(best_value, cur_strength)"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} played {cur_card}. Led suit: {led_suit}. Seat {best_seat} is winning the trick."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second seat's offer",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == (1 if leader == 3 else leader + 1)"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second seat plays",
      "to": {
        "where": "you.seat == (1 if leader == 3 else leader + 1)"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "p2"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Led suit: {led_suit}; trump suit: {trump_suit}; seat {best_seat} is winning. Play one card from your offer."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second card counts",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "1 if leader == 3 else leader + 1"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "$p2 if $p2 in players[cur_seat - 1].offer else players[cur_seat - 1].offer[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "played_card",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "cur_card[0]"
            },
            "if": {
              "calc": "led_suit == 'none' and best_value < wizard_strength and cur_card[0] in ['R', 'B', 'G']"
            }
          }
        },
        {
          "set": {
            "key": "cur_strength",
            "value": {
              "calc": "wizard_strength if (cur_card[0] == 'W' and best_value < wizard_strength) else (second_wizard_strength if cur_card[0] == 'W' else (jester_strength if cur_card[0] == 'J' else ((trump_bonus + int(cur_card[1])) if cur_card[0] == trump_suit else (int(cur_card[1]) if cur_card[0] == led_suit else 0))))"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "cur_seat"
            },
            "if": {
              "calc": "cur_strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "max(best_value, cur_strength)"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} played {cur_card}. Led suit: {led_suit}. Seat {best_seat} is winning the trick."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third seat's offer",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == (3 if leader == 1 else leader - 1)"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third seat plays",
      "to": {
        "where": "you.seat == (3 if leader == 1 else leader - 1)"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "p3"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Trick {trick_in_hand} of hand {hand_number}. Led suit: {led_suit}; trump suit: {trump_suit}; seat {best_seat} is winning. You play last: play one card from your offer."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third card counts and trick award",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "3 if leader == 1 else leader - 1"
            }
          }
        },
        {
          "set": {
            "key": "cur_card",
            "value": {
              "calc": "$p3 if $p3 in players[cur_seat - 1].offer else players[cur_seat - 1].offer[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "hand",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "cur_seat"
            },
            "key": "played_card",
            "value": {
              "calc": "cur_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "cur_card[0]"
            },
            "if": {
              "calc": "led_suit == 'none' and best_value < wizard_strength and cur_card[0] in ['R', 'B', 'G']"
            }
          }
        },
        {
          "set": {
            "key": "cur_strength",
            "value": {
              "calc": "wizard_strength if (cur_card[0] == 'W' and best_value < wizard_strength) else (second_wizard_strength if cur_card[0] == 'W' else (jester_strength if cur_card[0] == 'J' else ((trump_bonus + int(cur_card[1])) if cur_card[0] == trump_suit else (int(cur_card[1]) if cur_card[0] == led_suit else 0))))"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "cur_seat"
            },
            "if": {
              "calc": "cur_strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "max(best_value, cur_strength)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "best_seat"
            },
            "key": "tricks_taken",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "best_seat"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} played {cur_card}. Seat {best_seat} wins the trick and leads next. Tricks taken: Seat 1 {players[0].tricks_taken}, Seat 2 {players[1].tricks_taken}, Seat 3 {players[2].tricks_taken}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "hand scoring",
      "when": {
        "calc": "trick_in_hand == 3"
      },
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(exact_bid_bonus + points_per_trick_on_exact_bid * you.tricks_taken) if you.tricks_taken == you.bid else (0 - penalty_per_trick_off * abs(you.tricks_taken - you.bid))"
            }
          }
        }
      ],
      "text": "Hand {hand_number} scored. Scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "advance",
      "do": [
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
      "phase": "score",
      "label": "after the last hand",
      "when": {
        "calc": "hand_number >= hands and trick_in_hand == 1"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number >= hands and trick_in_hand == 1"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 27,
    "rounds_max": 27,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Pocket Wizard is for 3 players. The deck has {deck_size} cards: {suits} suits R, B and G, each with ranks 1 to {ranks_per_suit} (R1..R8, B1..B8, G1..G8), plus {wizards} Wizards (W1, W2) and {jesters} Jesters (J1, J2). The game lasts {total_rounds} rounds: each round is one trick, and every {tricks_per_hand} rounds make one hand, so there are {hands} hands. Everyone starts with score 0.\n\nNew hand: at the start of a hand the deck is refilled to all {deck_size} cards and shuffled, every tricks_taken returns to 0, and seats 1, 2 and 3 in turn each take {cards_dealt_per_seat} cards into their private hand. Hand 1 is led by seat 1, hand 2 by seat 2, hand 3 by seat 3, hand 4 by seat 1, and so on. In the second and third trick of a hand nothing is dealt.\n\nTrump: after the deal, {trump_cards_turned} more card is turned up as the trump card, leaving {deck_left_after_deal} cards in the deck. If it is an R, B or G card, that suit is trump; if it is a Wizard or a Jester, there is no trump (trump suit 'none'). The trump card is shown to everyone.\n\nBidding: at the start of each hand all three seats bid at the same moment, each seeing only its own hand and the trump card: how many tricks will you take this hand, {bid_min} to {bid_max}? An answer of exactly 0, 1, 2 or 3 is your bid (0 stays 0); a missing or other answer becomes a bid of {default_bid}. All bids are then announced.\n\nPlaying a trick: the leader plays first, then the next seat up, then the next (after seat 3 comes seat 1), so a trick led by seat 3 is played 3, 1, 2. Every card played is shown to all. You must choose from your offer: if a suit has been led and you hold at least one card of it, your offer is your cards of that suit plus all your Wizards and Jesters; otherwise you may play any card in your hand. A missing answer or a card not in your offer plays the first card of your offer. The played card leaves your hand.\n\nLed suit: the first R, B or G card played sets the led suit, unless a Wizard was played before it in that trick (then there is no led suit). After a Jester lead, the first suited card sets the led suit.\n\nStrength: the first Wizard in a trick has strength {wizard_strength}; a later Wizard has {second_wizard_strength}; a Jester has {jester_strength}; a trump card has {trump_bonus} + rank (trump 3 = 23); a card of the led suit that is not trump has its rank; any other card has 0. A card takes the lead only if its strength is strictly greater than the best so far; a tie never changes who is winning. So the first Wizard always wins, and if only Jesters are played the first Jester wins.\n\nAfter all three have played, the winner of the trick adds 1 to tricks_taken and leads the next trick.\n\nScoring after the third trick of each hand: if your tricks_taken equals your bid, you gain {exact_bid_bonus} + {points_per_trick_on_exact_bid} x tricks taken (bid 0 and took 0 gives +20; bid 2 and took 2 gives +40). If not, you lose {penalty_per_trick_off} x the difference (bid 3 and took 1 gives -20). Scores are announced.\n\nAfter {total_rounds} rounds ({hands} hands) the game ends. The highest score wins; seats tied for the highest score share the result."
}
```
````
