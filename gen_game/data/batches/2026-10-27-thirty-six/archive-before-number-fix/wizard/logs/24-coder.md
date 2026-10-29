# 24 coder

- time: 2026-10-27T18:24:14+00:00 (98.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 3a764e337a6138c2, reply sha256 b80d9880de2d93eb

## Sent

````
# Task: write the XColos game file for "Three-Card Wizard"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. The deck has 28 cards:
- Red R1-R8, Blue B1-B8 and Green G1-G8 (the suit is the letter, the rank is the number);
- two Wizards, W1 and W2;
- two Jesters, J1 and J2.

SEATS. Players sit in seats 1, 2 and 3. Everyone starts with a score of 0.

STRUCTURE. The game has 12 hands of 3 tricks each. Each round is one trick, so there are 36 rounds.
- The table tracks hand_number (starting at 0) and trick_in_hand (starting at 1).
- Each player has: hand (a list, private to them), bid, tricks_taken, played_card, offer (a list) and score.

RULE 1 (new hand: deal). Only when trick_in_hand = 1:
- add 1 to hand_number;
- shuffle all 28 cards into the deck (this is the round's only random event);
- empty every hand and set every tricks_taken to 0;
- deal the top 3 cards of the deck to seat 1, the next 3 to seat 2 and the next 3 to seat 3, each seen only by its owner;
- remove the 10th card from the deck and place it face up as trump_card, announced to all. After this, 18 cards remain in the deck.

RULE 2 (trump). If trump_card is suited, trump_suit is its suit letter. If it is a Wizard or a Jester, trump_suit is 'none' for the whole hand.

RULE 3 (first leader). Only when trick_in_hand = 1, leader = ((hand_number - 1) mod 3) + 1:
- seat 1 leads in hands 1, 4, 7 and 10;
- seat 2 leads in hands 2, 5, 8 and 11;
- seat 3 leads in hands 3, 6, 9 and 12.

RULE 4 (bidding). Only when trick_in_hand = 1, all three players answer one simultaneous poll.
- The options are exactly the fixed list 0, 1, 2, 3, offered to every seat.
- Each player's answer is stored in their bid exactly as given, and a 0 stays 0.
- Only if an answer is missing or not one of 0, 1, 2, 3 does that bid become 1.
- All bids are then announced. They need not sum to 3.
- Bids are not changed again until Rule 10.

RULE 5 (trick setup). Every round, set:
- led_suit = 'none';
- wizard_played = false;
- best_value = -1;
- best_seat = 0;
- played_cards empty.

RULE 6 (play order). Three players play one card each, one after another:
- first the seat in leader;
- then the seat (leader mod 3) + 1;
- then the seat ((leader + 1) mod 3) + 1.
Each player sees the cards already played to the trick.

RULE 7 (legal cards). Before a player chooses, build their offer list, keeping the order the cards sit in their hand:
- if led_suit is not 'none' and they hold at least one card of led_suit, the offer is their cards of led_suit plus any Wizards and Jesters they hold;
- otherwise, the offer is every card in their hand.
The player picks one card from the offer.

RULE 8 (fallback). If the answer is missing or not in the offer, the engine plays the first card of the offer list.

RULE 9 (resolving each played card). As each card is played, remove it from the hand, record it as played_card and append it to played_cards. Then work out the led suit and the card's strength.

Led suit:
- If the card is suited, led_suit is 'none' and wizard_played is false, then led_suit becomes that card's suit.
- If the card is a Wizard, set wizard_played = true.
- A Wizard or Jester never sets led_suit. Once any Wizard is played, later cards do not set led_suit.

Strength:
- Wizard: 100.
- Suited card whose suit equals trump_suit: 20 + rank.
- Other suited card whose suit equals led_suit: its rank.
- Anything else: 0. This includes Jesters and off-suit non-trump cards.

If strength > best_value (strictly), set best_value = strength and best_seat = this seat. As a result:
- the first Wizard wins the trick;
- otherwise the highest trump wins;
- otherwise the highest card of the led suit wins;
- if all three cards are Jesters, the first Jester wins.

RULE 10 (end of trick). Add 1 to tricks_taken of best_seat, announce the winner, and set leader = best_seat.
- If trick_in_hand = 3, score the hand. A player whose tricks_taken equals their bid gains 20 + 10 × tricks_taken. Otherwise they lose 10 × |tricks_taken - bid|. Announce all scores, then set every bid to 0 and trick_in_hand = 1.
- Otherwise add 1 to trick_in_hand.

RULE 11 (end). The game ends after round 36, which is the end of hand 12.

How the winner is decided: After hand 12, the player with the highest score wins. If two or three players tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Three-Card Wizard (3 to 3 players, best with 3)

A three-player trick-taking game of 12 hands with 3 tricks each: players bid exactly how many tricks they will take, then play Wizards, Jesters and suited cards to hit that number.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards this player holds in the current hand. Only the owner sees them.
  - each player: bid (number, starts 0); everyone sees it. The number of tricks bid this hand. It is collected by a simultaneous poll and then announced, and it is reset to 0 after scoring.
  - each player: tricks_taken (number, starts 0); everyone sees it. Tricks won so far in the current hand.
  - each player: played_card (text, starts ''); everyone sees it. The card this player played to the current trick.
  - each player: offer (list, starts []); only its owner sees it. The legal cards this player may play now, in hand order.
  - each player: score (number, starts 0); everyone sees it. Cumulative score.
  - the table: deck (list, starts ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'W1', 'W2', 'J1', 'J2']); hidden from all players. The undealt cards, refilled with all 28 cards and shuffled at the start of each hand.
  - the table: trump_card (text, starts ''); everyone sees it. The face-up 10th card of the shuffled deck.
  - the table: trump_suit (text, starts 'none'); everyone sees it. The suit letter of trump_card, or 'none' if it is a Wizard or a Jester.
  - the table: hand_number (number, starts 0); everyone sees it. The current hand, 1 to 12.
  - the table: trick_in_hand (number, starts 1); everyone sees it. The current trick within the hand, 1 to 3.
  - the table: leader (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: led_suit (text, starts 'none'); everyone sees it. The suit led in this trick, or 'none'.
  - the table: wizard_played (bool, starts False); everyone sees it. Whether a Wizard has been played in this trick.
  - the table: best_value (number, starts -1); everyone sees it. The strength of the currently winning card in the trick.
  - the table: best_seat (number, starts 0); everyone sees it. The seat currently winning the trick.
  - the table: played_cards (list, starts []); everyone sees it. The cards played to the current trick, in order.
  - parameters, each kept as a table attribute: deck_size = 28, suits = 3, ranks_per_suit = 8, wizards = 2, jesters = 2, hands = 12, tricks_per_hand = 3, rounds = 36, cards_dealt_per_player = 3, trump_card_position = 10, cards_left_in_deck_after_deal = 18, bid_min = 0, bid_max = 3, default_bid = 1, wizard_strength = 100, trump_strength_bonus = 20, jester_or_offsuit_strength = 0, initial_best_value = -1, exact_bid_bonus = 20, points_per_trick_when_exact = 10, penalty_per_trick_off = 10, starting_score = 0, starting_hand_number = 0, starting_trick_in_hand = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 are filled, and every score is set to 0.
  2. hand_number is set to 0, trick_in_hand to 1 and every bid to 0.
  3. The deck list holds the 28 cards R1-R8, B1-B8, G1-G8, W1, W2, J1 and J2.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_hand = 1: add 1 to hand_number; refill deck with all 28 cards and shuffle it; empty every hand and set every tricks_taken to 0; draw 3 cards at random from deck into seat 1's hand, then 3 into seat 2's, then 3 into seat 3's (each removed from deck); remove the next random card from deck and set it as trump_card (18 cards stay in deck); set trump_suit to the suit letter of trump_card if it is suited, otherwise 'none'; set leader = ((hand_number - 1) mod 3) + 1.
  2. [sync] all players. What happens: When trick_in_hand = 1: each player sees their own hand; trump_card, trump_suit, hand_number and leader are announced to all.
  3. [poll] all players answers: one of 0, 1, 2, 3. What happens: When trick_in_hand = 1: each player's bid is set to their answer exactly (a 0 stays 0); a missing or invalid answer sets that bid to 1. All bids are then announced.
  4. [update] all players. What happens: Every round: led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0, played_cards = [].
  5. [update] seat leader. What happens: Build the leader's offer from their hand, in hand order: if led_suit != 'none' and they hold a card of led_suit, the offer is those cards plus any W or J cards they hold; otherwise it is the whole hand.
  6. [ask] seat leader answers: one card from their offer. What happens: The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0].
  7. [update] seat leader. What happens: Resolve the card. If it is suited and led_suit = 'none' and wizard_played = false, set led_suit to its suit. If it is a Wizard, set wizard_played = true. Strength is 100 for a Wizard, 20 + rank for a suit equal to trump_suit, rank for a suit equal to led_suit, and 0 otherwise. If strength > best_value, set best_value = strength and best_seat = this seat. The played card is announced.
  8. [update] seat (leader mod 3) + 1. What happens: Build this player's offer with the same rule as above.
  9. [ask] seat (leader mod 3) + 1 answers: one card from their offer. What happens: The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0].
  10. [update] seat (leader mod 3) + 1. What happens: Resolve the card with the same led-suit and strength rule as above, then announce it.
  11. [update] seat ((leader + 1) mod 3) + 1. What happens: Build this player's offer with the same rule as above.
  12. [ask] seat ((leader + 1) mod 3) + 1 answers: one card from their offer. What happens: The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0].
  13. [update] seat ((leader + 1) mod 3) + 1. What happens: Resolve the card with the same led-suit and strength rule as above, then announce it.
  14. [update] all players. What happens: Add 1 to tricks_taken of best_seat; announce best_seat as the trick winner; set leader = best_seat.
  15. [update] all players. What happens: When trick_in_hand = 3: for each player, if tricks_taken = bid, add 20 + 10 * tricks_taken to score; otherwise subtract 10 * |tricks_taken - bid|. Announce all scores, set every bid to 0 and set trick_in_hand = 1. Otherwise (trick_in_hand < 3) add 1 to trick_in_hand.
  16. [check] all players. What happens: End the game if hand_number >= 12 and trick_in_hand = 1 (hand 12 has just been scored); otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When trick_in_hand = 1 at the start of a round, then hand_number increases by 1, the deck is refilled to 28 cards and shuffled, every tricks_taken becomes 0, and each seat receives exactly 3 cards in its hand.
  R2. When a hand is dealt, then one further card is removed from the deck and becomes trump_card, leaving exactly 18 cards in the deck.
  R3. When trump_card is suited (for example G5), then trump_suit is its letter (G); when trump_card is W1, W2, J1 or J2, then trump_suit is 'none'.
  R4. When a hand begins, then leader = ((hand_number - 1) mod 3) + 1: seat 1 leads in hands 1, 4, 7 and 10, seat 2 in hands 2, 5, 8 and 11, and seat 3 in hands 3, 6, 9 and 12.
  R5. When trick_in_hand = 1, then all three players bid at once from {0, 1, 2, 3}, and each bid is stored exactly as given (a 0 stays 0).
  R6. When a bid answer is missing or not in {0, 1, 2, 3}, then that bid is 1.
  R7. When bidding is done, then all bids are announced, and they need not sum to 3.
  R8. When a trick starts, then led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0 and played_cards is empty.
  R9. When a trick is played, then the order is leader, then (leader mod 3) + 1, then ((leader + 1) mod 3) + 1.
  R10. When led_suit is not 'none' and the player holds a card of led_suit, then the offer is their led-suit cards plus any Wizards and Jesters they hold, in hand order; otherwise the offer is the whole hand.
  R11. When a play answer is missing or not in the offer, then the first card of the offer is played.
  R12. When a card is played, then it is removed from the hand, recorded as played_card and appended to played_cards.
  R13. When a suited card is played while led_suit = 'none' and wizard_played = false, then led_suit becomes its suit.
  R14. When a Wizard is played, then wizard_played = true and led_suit does not change; when a Jester is played, then led_suit does not change.
  R15. When a card is played, then its strength is 100 for a Wizard, 20 + rank for a trump-suit card, its rank for a led-suit card, and 0 for a Jester or an off-suit non-trump card.
  R16. When a card's strength is strictly greater than best_value, then best_value becomes that strength and best_seat becomes that seat; equal strength does not take the lead, so the first Wizard wins and three Jesters are won by the first Jester.
  R17. When a trick ends, then best_seat's tricks_taken increases by 1 and leader becomes best_seat.
  R18. When trick_in_hand = 3 at the end of a trick and a player's tricks_taken equals their bid, then they gain 20 + 10 * tricks_taken (for example bid 0 and 0 tricks gains 20, bid 2 and 2 tricks gains 40).
  R19. When trick_in_hand = 3 at the end of a trick and a player's tricks_taken differs from their bid, then they lose 10 * |tricks_taken - bid| (for example bid 3 and 1 trick loses 20).
  R20. When a hand is scored, then all scores are announced, every bid is set to 0 and trick_in_hand becomes 1; after tricks 1 and 2 of a hand, trick_in_hand increases by 1 instead.
  R21. When hand 12 has been scored (after round 36), then the game ends and the highest score wins, with players tied at the top sharing the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid for this hand (poll, only when trick_in_hand = 1) | asked: seats 1, 2 and 3 | options: every seat: 0, 1, 2, 3
  - Card to play to the trick | asked: the leader, then (leader mod 3) + 1, then ((leader + 1) mod 3) + 1 | options: the leader, or any later player when led_suit is 'none' (a Wizard was led, or only Wizards and Jesters have been played so far): every card in their hand; a later player when led_suit is set and they hold a card of led_suit: their led-suit cards plus any W1, W2, J1, J2 they hold; a later player when led_suit is set and they hold none of it: every card in their hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.hand_number >= 12 and game.trick_in_hand = 1
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final score after hand 12. The highest score wins, and players tied at the top share the win (the source calls this a draw).
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

- each player: `bid` (number, visible: public, starts 0): The number of tricks bid this hand. It is collected by a simultaneous poll and then announced, and it is reset to 0 after scoring.
- each player: `tricks_taken` (number, visible: public, starts 0): Tricks won so far in the current hand.
- each player: `score` (number, visible: public, starts 0): Cumulative score.
- the table: `trump_card` (text, visible: public, starts ''): The face-up 10th card of the shuffled deck.
- the table: `hand_number` (number, visible: public, starts 0): The current hand, 1 to 12.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 28, suits = 3, ranks_per_suit = 8, wizards = 2, jesters = 2, hands = 12, tricks_per_hand = 3, rounds = 36, cards_dealt_per_player = 3, trump_card_position = 10, cards_left_in_deck_after_deal = 18, bid_min = 0, bid_max = 3, default_bid = 1, wizard_strength = 100, trump_strength_bonus = 20, jester_or_offsuit_strength = 0, initial_best_value = -1, exact_bid_bonus = 20, points_per_trick_when_exact = 10, penalty_per_trick_off = 10, starting_score = 0, starting_hand_number = 0, starting_trick_in_hand = 1
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
    "id": "three_card_wizard",
    "name": "Three-Card Wizard",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Twelve hands of three tricks: bid exactly how many tricks you will take, then play Wizards, Jesters and suited cards to hit it."
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
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "wizard_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "best_value",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
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
        "key": "cur_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "strength",
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
        "key": "rounds",
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
        "key": "cards_left_in_deck_after_deal",
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
        "key": "jester_or_offsuit_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_best_value",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "points_per_trick_when_exact",
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
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_trick_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "set up the table",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": {
              "calc": "starting_hand_number"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "starting_trick_in_hand"
            }
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
            "key": "deck",
            "value": {
              "calc": "full_deck"
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
      "label": "deal a new hand",
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
            "key": "hand",
            "value": []
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
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "hand_number - 1 - 3 * int((hand_number - 1) / 3) + 1"
            }
          }
        }
      ],
      "text": "Hand {hand_number} is dealt. Trump card: {trump_card} (trump suit: {trump_suit}). Seat {leader} leads."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your new hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "text": "Hand {hand_number}: trump card {trump_card}, trump suit {trump_suit}, seat {leader} leads. Your cards:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid for this hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": ["0", "1", "2", "3"]
      },
      "store": "bid_said",
      "text": "Hand {hand_number}. Trump card {trump_card}, trump suit {trump_suit}. Your hand: {hand}. Bid how many of the 3 tricks you will take: 0, 1, 2 or 3. Exactly right scores 20 + 10 per trick; otherwise you lose 10 per trick you are off."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "record the bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_said) if you.bid_said in ['0', '1', '2', '3'] else default_bid"
            },
            "text": "Seat {player} bids {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "trick setup",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": "none"
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
              "calc": "initial_best_value"
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
            "key": "played_cards",
            "value": []
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
      "use": "update",
      "phase": "trick",
      "label": "leader's offer",
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
            "players": {
              "where": "you.seat == cur_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        },
        {
          "set": {
            "key": "cur_offer",
            "value": {
              "calc": "[p.offer for p in players if p.seat == cur_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader plays",
      "when": {
        "calc": "len(cur_offer) > 1"
      },
      "to": {
        "where": "you.seat == cur_seat"
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
      "text": "Trick {trick_in_hand} of hand {hand_number}. You lead. Trump suit {trump_suit}. Your bid {bid}, tricks taken {tricks_taken}. Play one card from: {offer}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "resolve the lead",
      "do": [
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "$p1 if $p1 in cur_offer else cur_offer[0]"
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
              "calc": "last_card"
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
              "calc": "last_card"
            }
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "last_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "last_card[0]"
            },
            "if": {
              "calc": "last_card[0] in ['R', 'B', 'G'] and led_suit == 'none' and not wizard_played"
            }
          }
        },
        {
          "set": {
            "key": "wizard_played",
            "value": true,
            "if": {
              "calc": "last_card[0] == 'W'"
            }
          }
        },
        {
          "set": {
            "key": "strength",
            "value": {
              "calc": "wizard_strength if last_card[0] == 'W' else (trump_strength_bonus + int(last_card[1]) if last_card[0] == trump_suit else (int(last_card[1]) if last_card[0] == led_suit else jester_or_offsuit_strength))"
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
              "calc": "strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "strength"
            },
            "if": {
              "calc": "strength > best_value"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} plays {last_card}. Cards played: {played_cards}. Led suit: {led_suit}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second player's offer",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "leader + 1 if leader < 3 else 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        },
        {
          "set": {
            "key": "cur_offer",
            "value": {
              "calc": "[p.offer for p in players if p.seat == cur_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second player plays",
      "when": {
        "calc": "len(cur_offer) > 1"
      },
      "to": {
        "where": "you.seat == cur_seat"
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
      "text": "Trick {trick_in_hand} of hand {hand_number}. Cards played so far: {played_cards}. Led suit {led_suit}, trump suit {trump_suit}. Your bid {bid}, tricks taken {tricks_taken}. Play one card from: {offer}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "resolve the second card",
      "do": [
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "$p2 if $p2 in cur_offer else cur_offer[0]"
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
              "calc": "last_card"
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
              "calc": "last_card"
            }
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "last_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "last_card[0]"
            },
            "if": {
              "calc": "last_card[0] in ['R', 'B', 'G'] and led_suit == 'none' and not wizard_played"
            }
          }
        },
        {
          "set": {
            "key": "wizard_played",
            "value": true,
            "if": {
              "calc": "last_card[0] == 'W'"
            }
          }
        },
        {
          "set": {
            "key": "strength",
            "value": {
              "calc": "wizard_strength if last_card[0] == 'W' else (trump_strength_bonus + int(last_card[1]) if last_card[0] == trump_suit else (int(last_card[1]) if last_card[0] == led_suit else jester_or_offsuit_strength))"
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
              "calc": "strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "strength"
            },
            "if": {
              "calc": "strength > best_value"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} plays {last_card}. Cards played: {played_cards}. Led suit: {led_suit}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third player's offer",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "leader + 2 if leader < 2 else leader - 1"
            }
          }
        },
        {
          "set": {
           
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Hand 1. Trump card R2, trump suit R. Your hand: {hand}. Bid how many of the 3 tricks you w'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Hand 1. Trump card R2, trump suit R. Your hand: {hand}. Bid how many of the 3 tricks you w'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Hand 1. Trump card R2, trump suit R. Your hand: {hand}. Bid how many of the 3 tricks you w'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
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
      "max": 3,
      "suggested": 3
    },
    "blurb": "Twelve hands of three tricks: bid exactly how many tricks you will take, then play Wizards, Jesters and suited cards to hit it."
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
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "key": "full_deck",
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
        "key": "wizard_played",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "best_value",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "best_seat",
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
        "key": "cur_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "strength",
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
        "key": "rounds",
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
        "key": "cards_left_in_deck_after_deal",
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
        "key": "jester_or_offsuit_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_best_value",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "exact_bid_bonus",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "points_per_trick_when_exact",
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
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hand_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_trick_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "set up the table",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": {
              "calc": "starting_hand_number"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "starting_trick_in_hand"
            }
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
            "key": "deck",
            "value": {
              "calc": "full_deck"
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
      "label": "deal a new hand",
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
            "key": "hand",
            "value": []
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
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "hand_number - 1 - 3 * int((hand_number - 1) / 3) + 1"
            }
          }
        }
      ],
      "text": "Hand {hand_number} is dealt. Trump card: {trump_card} (trump suit: {trump_suit}). Seat {leader} leads."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your new hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "text": "Hand {hand_number}: trump card {trump_card}, trump suit {trump_suit}, seat {leader} leads. Your cards:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid for this hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "0",
          "1",
          "2",
          "3"
        ]
      },
      "store": "bid_said",
      "text": "Hand {hand_number}. Trump card {trump_card}, trump suit {trump_suit}. Look at the cards in your hand and bid how many of the 3 tricks you will take: 0, 1, 2 or 3. Exactly right scores 20 + 10 per trick taken; otherwise you lose 10 per trick you are off."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "record the bids",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid_said) if you.bid_said in ['0', '1', '2', '3'] else default_bid"
            },
            "text": "Seat {player} bids {value}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "trick setup",
      "do": [
        {
          "set": {
            "key": "led_suit",
            "value": "none"
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
              "calc": "initial_best_value"
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
            "key": "played_cards",
            "value": []
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
      "use": "update",
      "phase": "trick",
      "label": "leader's offer",
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
            "players": {
              "where": "you.seat == cur_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        },
        {
          "set": {
            "key": "cur_offer",
            "value": {
              "calc": "[p.offer for p in players if p.seat == cur_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "leader plays",
      "when": {
        "calc": "len(cur_offer) > 1"
      },
      "to": {
        "where": "you.seat == cur_seat"
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
      "text": "Trick {trick_in_hand} of hand {hand_number}. You lead. Trump suit {trump_suit}. Play one card from your offer list (your legal cards)."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "resolve the lead",
      "do": [
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "$p1 if $p1 in cur_offer else cur_offer[0]"
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
              "calc": "last_card"
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
              "calc": "last_card"
            }
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "last_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "last_card[0]"
            },
            "if": {
              "calc": "last_card[0] in ['R', 'B', 'G'] and led_suit == 'none' and not wizard_played"
            }
          }
        },
        {
          "set": {
            "key": "wizard_played",
            "value": true,
            "if": {
              "calc": "last_card[0] == 'W'"
            }
          }
        },
        {
          "set": {
            "key": "strength",
            "value": {
              "calc": "wizard_strength if last_card[0] == 'W' else (trump_strength_bonus + int(last_card[1]) if last_card[0] == trump_suit else (int(last_card[1]) if last_card[0] == led_suit else jester_or_offsuit_strength))"
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
              "calc": "strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "strength"
            },
            "if": {
              "calc": "strength > best_value"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} plays {last_card}. Cards played: {played_cards}. Led suit: {led_suit}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second player's offer",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "leader + 1 if leader < 3 else 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        },
        {
          "set": {
            "key": "cur_offer",
            "value": {
              "calc": "[p.offer for p in players if p.seat == cur_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second player plays",
      "when": {
        "calc": "len(cur_offer) > 1"
      },
      "to": {
        "where": "you.seat == cur_seat"
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
      "text": "Trick {trick_in_hand} of hand {hand_number}. Cards played so far: {played_cards}. Led suit {led_suit}, trump suit {trump_suit}. Play one card from your offer list (your legal cards)."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "resolve the second card",
      "do": [
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "$p2 if $p2 in cur_offer else cur_offer[0]"
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
              "calc": "last_card"
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
              "calc": "last_card"
            }
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "last_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "last_card[0]"
            },
            "if": {
              "calc": "last_card[0] in ['R', 'B', 'G'] and led_suit == 'none' and not wizard_played"
            }
          }
        },
        {
          "set": {
            "key": "wizard_played",
            "value": true,
            "if": {
              "calc": "last_card[0] == 'W'"
            }
          }
        },
        {
          "set": {
            "key": "strength",
            "value": {
              "calc": "wizard_strength if last_card[0] == 'W' else (trump_strength_bonus + int(last_card[1]) if last_card[0] == trump_suit else (int(last_card[1]) if last_card[0] == led_suit else jester_or_offsuit_strength))"
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
              "calc": "strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "strength"
            },
            "if": {
              "calc": "strength > best_value"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} plays {last_card}. Cards played: {played_cards}. Led suit: {led_suit}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third player's offer",
      "do": [
        {
          "set": {
            "key": "cur_seat",
            "value": {
              "calc": "leader + 2 if leader < 2 else leader - 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == cur_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[c for c in you.hand if c[0] == led_suit or c[0] in ['W', 'J']] if (led_suit != 'none' and count(c[0] == led_suit for c in you.hand) > 0) else you.hand"
            }
          }
        },
        {
          "set": {
            "key": "cur_offer",
            "value": {
              "calc": "[p.offer for p in players if p.seat == cur_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third player plays",
      "when": {
        "calc": "len(cur_offer) > 1"
      },
      "to": {
        "where": "you.seat == cur_seat"
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
      "text": "Trick {trick_in_hand} of hand {hand_number}. Cards played so far: {played_cards}. Led suit {led_suit}, trump suit {trump_suit}. Play one card from your offer list (your legal cards)."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "resolve the third card",
      "do": [
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "$p3 if $p3 in cur_offer else cur_offer[0]"
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
              "calc": "last_card"
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
              "calc": "last_card"
            }
          }
        },
        {
          "append": {
            "key": "played_cards",
            "value": {
              "calc": "last_card"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "last_card[0]"
            },
            "if": {
              "calc": "last_card[0] in ['R', 'B', 'G'] and led_suit == 'none' and not wizard_played"
            }
          }
        },
        {
          "set": {
            "key": "wizard_played",
            "value": true,
            "if": {
              "calc": "last_card[0] == 'W'"
            }
          }
        },
        {
          "set": {
            "key": "strength",
            "value": {
              "calc": "wizard_strength if last_card[0] == 'W' else (trump_strength_bonus + int(last_card[1]) if last_card[0] == trump_suit else (int(last_card[1]) if last_card[0] == led_suit else jester_or_offsuit_strength))"
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
              "calc": "strength > best_value"
            }
          }
        },
        {
          "set": {
            "key": "best_value",
            "value": {
              "calc": "strength"
            },
            "if": {
              "calc": "strength > best_value"
            }
          }
        }
      ],
      "text": "Seat {cur_seat} plays {last_card}. Cards played: {played_cards}. Led suit: {led_suit}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "end of trick",
      "do": [
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
      "text": "Seat {best_seat} wins trick {trick_in_hand} with the cards {played_cards}, and leads next."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "score the hand or move on",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(exact_bid_bonus + points_per_trick_when_exact * you.tricks_taken) if you.tricks_taken == you.bid else -penalty_per_trick_off * abs(you.tricks_taken - you.bid)"
            },
            "if": {
              "calc": "trick_in_hand == tricks_per_hand"
            },
            "text": "Seat {player} scores {value} for this hand."
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
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
              "calc": "starting_trick_in_hand if trick_in_hand == tricks_per_hand else trick_in_hand + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after hand 12",
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
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "Three-Card Wizard is for three players in seats 1, 2 and 3. Everyone starts with a score of {starting_score}.\n\nCARDS. The deck has {deck_size} cards: Red R1-R8, Blue B1-B8 and Green G1-G8 (the letter is the suit, the number is the rank), two Wizards (W1, W2) and two Jesters (J1, J2).\n\nSTRUCTURE. The game has {hands} hands of {tricks_per_hand} tricks each, one trick per round, {rounds} rounds in all.\n\nNEW HAND. At the start of each hand, hand_number goes up by 1, all {deck_size} cards are shuffled into the deck, every hand is emptied and every tricks_taken is set to 0. Each player is dealt {cards_dealt_per_player} cards (seat 1 first, then seat 2, then seat 3), seen only by their owner. The {trump_card_position}th card is turned face up as the trump card, leaving {cards_left_in_deck_after_deal} cards in the deck.\n\nTRUMP. If the trump card is suited, its suit letter is the trump suit. If it is a Wizard or a Jester, there is no trump suit ('none') for the whole hand.\n\nFIRST LEADER. Seat 1 leads the first trick in hands 1, 4, 7 and 10; seat 2 in hands 2, 5, 8 and 11; seat 3 in hands 3, 6, 9 and 12.\n\nBIDDING. At the start of each hand all three players bid at the same moment, choosing from {bid_min}, 1, 2 or {bid_max}: the number of tricks they will take. Your bid is stored exactly as given (a 0 stays 0). If your answer is missing or not one of those, your bid is {default_bid}. All bids are then announced; they need not add up to 3.\n\nPLAYING A TRICK. The leader plays first, then the next seat round (seat after 3 is seat 1), then the seat after that. Each player sees the cards already played. Legal cards: if a suit has been led and you hold at least one card of that suit, you must play a card of that suit or a Wizard or a Jester; otherwise you may play any card in your hand. You are offered exactly your legal cards. If your answer is missing or not legal, the first legal card in your hand order is played for you; if you have only one legal card, it is played automatically.\n\nLED SUIT. The first suited card played sets the led suit, unless a Wizard has already been played in the trick, in which case no suit is led for that trick. Wizards and Jesters never set the led suit.\n\nWINNING A TRICK. Each card has a strength: a Wizard is {wizard_strength}; a card of the trump suit is {trump_strength_bonus} + its rank; another card of the led suit is its rank; anything else (a Jester or an off-suit non-trump card) is {jester_or_offsuit_strength}. A card takes the lead only if its strength is strictly greater than the best so far; an equal strength does not. So the first Wizard wins; otherwise the highest trump; otherwise the highest card of the led suit; if all three are Jesters, the first Jester wins. The trick winner adds 1 to tricks_taken and leads the next trick.\n\nSCORING. After the third trick of a hand: if your tricks_taken equals your bid, you gain {exact_bid_bonus} + {points_per_trick_when_exact} x tricks taken (bid 0 and take 0 gains 20). If not, you lose {penalty_per_trick_off} x the difference between tricks taken and your bid. Scores are announced, every bid is reset to 0 and the next hand begins. After the first or second trick, play simply moves to the next trick.\n\nEND. The game ends after hand {hands} is scored. The highest score wins; players tied for the highest score share the win (a draw)."
}
```
````
