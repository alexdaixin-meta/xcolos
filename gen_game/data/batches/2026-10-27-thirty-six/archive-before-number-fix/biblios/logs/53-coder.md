# 53 coder

- time: 2026-10-27T18:14:27+00:00 (136.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 cf023610d962a59e, reply sha256 f86c159220deb69e

## Sent

````
# Task: write the XColos game file for "Biblios: The Scriptorium (revised)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. The deck has 36 cards:
- Colour cards (21): for each of Red, Green and Blue, values 1, 1, 2, 2, 3, 3, 4. Each colour totals 16.
- Gold cards (9): values 1, 1, 1, 2, 2, 2, 3, 3, 3. These total 18 Gold.
- Church cards (6): each simply named 'Church'.
The deck composition is public. The deck is shuffled once at setup and kept face-down, its order hidden from everyone.
Each player starts with:
- 4 Gold, private (only that player sees it);
- an empty hand, private;
- church_count 0.
Three public dice, vp_red, vp_green and vp_blue, each start at 3 and always stay between 1 and 5.
Players sit P1, P2, P3. Clockwise order is P1 -> P2 -> P3 -> P1. The player next clockwise after P1 is P2, after P2 is P3, and after P3 is P1.
The game lasts 12 rounds. 12 rounds x 3 cards uses the whole deck exactly.

EACH ROUND (r = 1 to 12):
1. Active player. P1 is active in rounds 1, 4, 7 and 10; P2 in rounds 2, 5, 8 and 11; P3 in rounds 3, 6, 9 and 12. This is announced to everyone.
2. Deal. The top 3 cards of the deck are removed and shown privately to the active player as positions 1, 2 and 3.
3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone with their authors. Talk is not binding and may be a bluff.
4. Split. The active player chooses one of: 'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'. The keep card goes face-down into the active player's hand. The sell card becomes the lot. The remaining card becomes the gift.
5. Reveal. The lot and the gift are shown face-up to everyone. The kept card stays secret.
6. Bid. All three players, including the active player, privately bid a whole number of Gold from 0 upward, all at the same moment. A bid above a player's current Gold counts as exactly that player's whole Gold.
7. Sale. The highest bid wins the lot.
- On a tie for highest: the active player wins if among the tied; otherwise the tied player who comes first clockwise after the active player wins. (If all bid 0, the active player wins.)
- The winner loses Gold equal to their bid (paid to the bank) and takes the lot into their hand.
- All three bids are then revealed to everyone.
8. Gift.
- If a non-active player won the lot, the gift goes to the other non-active player.
- If the active player won the lot, the gift goes to whichever non-active player bid lower. On a tie it goes to the player next clockwise after the active player.
9. Gold cards. Every Gold card that entered a hand this round is removed from that hand, and its value is added to that player's Gold.
10. Church cards. For each player, church_count is set to the number of Church cards that entered their hand this round (0, 1 or 2; only the active player can reach 2). Those Church cards are removed from the hand. Each player's church_count is announced.
11. Church choice. Every player with church_count of 1 or more privately makes exactly ONE choice at the same moment, from: 'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'. Players with church_count 0 do not choose.
12. Red die. net = (sum of church_count over players who chose 'red up') minus (sum of church_count over players who chose 'red down'). Set vp_red = min(5, max(1, vp_red + net)).
13. Green die. Same calculation with 'green up' and 'green down': vp_green = min(5, max(1, vp_green + net)).
14. Blue die. Same calculation with 'blue up' and 'blue down': vp_blue = min(5, max(1, vp_blue + net)). The three die values and each player's Church choice are announced.
15. Reset. Every church_count is set to 0, and bids are cleared.
16. End check. After round 12, go to scoring; otherwise start the next round.

SCORING. For each colour, each player's sum is the total value of that colour's cards in their hand. The player with the strictly highest sum in a colour scores VP equal to that colour's die value. If two or more players tie for highest, nobody scores that colour. A player's VP is the total over the three colours.

How the winner is decided: The player with the most VP wins. If players tie on VP, the tied player with the most remaining Gold wins. If they are still tied, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Biblios: The Scriptorium (revised) (3 to 3 players, best with 3)

Three scribes take turns splitting a three-card deal into a kept card, a lot that everyone bids on and a gift for a rival. They collect colour cards to win colours and play Church cards to move each colour's VP die.

STATE (every item below must exist in the file):
  - each player: gold (number, starts 4); only its owner sees it. Gold coins held. Only the owner sees it.
  - each player: hand (list, starts []); only its owner sees it. Colour cards held face-down, such as 'Red 3'
  - each player: offer (list, starts []); only its owner sees it. The 3 dealt cards in positions 1, 2 and 3. Filled only for the active player during the deal.
  - each player: new_cards (list, starts []); only its owner sees it. Cards that entered this player's hand this round (keep, lot or gift)
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid. Revealed to all after the sale.
  - each player: effective_bid (number, starts 0); only its owner sees it. min(bid, gold): the bid as it counts
  - each player: church_count (number, starts 0); everyone sees it. Church cards that entered this player's hand this round (0, 1 or 2)
  - each player: church_choice (text, starts ''); only its owner sees it. This round's Church choice. Announced after the dice move.
  - each player: red_sum (number, starts 0); only its owner sees it. Total value of Red cards in hand, computed at scoring
  - each player: green_sum (number, starts 0); only its owner sees it. Total value of Green cards in hand, computed at scoring
  - each player: blue_sum (number, starts 0); only its owner sees it. Total value of Blue cards in hand, computed at scoring
  - each player: vp (number, starts 0); everyone sees it. Victory points scored at the end
  - the table: deck (list, starts 'the 36 cards: Red/Green/Blue 1,1,2,2,3,3,4; Gold 1,1,1,2,2,2,3,3,3; Church x6'); hidden from all players. Face-down shuffled deck
  - the table: round (number, starts 0); everyone sees it. Current round, 1 to 12
  - the table: active_seat (number, starts 0); everyone sees it. Seat of the active player this round
  - the table: lot (text, starts ''); everyone sees it. The card being auctioned this round
  - the table: gift (text, starts ''); everyone sees it. The card given away this round
  - the table: lot_winner (number, starts 0); everyone sees it. Seat that won the lot this round
  - the table: gift_receiver (number, starts 0); everyone sees it. Seat that received the gift this round
  - the table: vp_red (number, starts 3); everyone sees it. Red VP die, from 1 to 5
  - the table: vp_green (number, starts 3); everyone sees it. Green VP die, from 1 to 5
  - the table: vp_blue (number, starts 3); everyone sees it. Blue VP die, from 1 to 5
  - parameters, each kept as a table attribute: deck_size = 36, colours = 3, colour_cards_per_colour = 7, colour_value_1_copies = 2, colour_value_2_copies = 2, colour_value_3_copies = 2, colour_value_4_copies = 1, colour_total_per_colour = 16, gold_cards = 9, gold_value_1_copies = 3, gold_value_2_copies = 3, gold_value_3_copies = 3, gold_cards_total = 18, church_cards = 6, starting_gold = 4, die_start = 3, die_min = 1, die_max = 5, rounds = 12, cards_per_round = 3, bid_min = 0, bid_max = 22, max_church_per_player_per_round = 2, rank_vp_weight = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The deck list is filled with the 36 cards: 'Red 1', 'Red 1', 'Red 2', 'Red 2', 'Red 3', 'Red 3', 'Red 4' and the same for Green and Blue; 'Gold 1' x3, 'Gold 2' x3, 'Gold 3' x3; and 'Church' x6. Everyone is told the composition, but the order is hidden.
  2. Each player gets gold 4, an empty hand and church_count 0.
  3. vp_red, vp_green and vp_blue are set to 3.
  4. Seats are P1, P2 and P3. Clockwise order is P1 -> P2 -> P3 -> P1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; active_seat = ((round - 1) mod 3) + 1. Announce 'Round {round}: seat {active_seat} is active.'
  2. [update] seat active_seat. What happens: Draw 3 cards at random from deck into the active player's offer, as positions 1, 2 and 3, and remove them from deck. Only the active player sees offer.
  3. [poll] all players answers: short text. What happens: Each message is broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding.
  4. [ask] seat active_seat answers: one of: 'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'. What happens: The keep card is appended to the active player's hand and new_cards. lot = the sell card. gift = the remaining card. offer = [].
  5. [tell] all players. What happens: Announce 'Lot: {lot}. Gift: {gift}.' The kept card stays secret.
  6. [poll] all players answers: whole number 0 to 22. What happens: bid = answer; effective_bid = min(bid, gold).
  7. [update] all players. What happens: lot_winner = the seat with the highest effective_bid. On a tie, the active seat wins if it is among the tied; otherwise the tied seat that comes first clockwise after the active seat wins. If all bid 0, the active seat wins. The winner's gold -= the winner's effective_bid. lot is appended to the winner's hand and new_cards. All three bids are announced.
  8. [update] all players. What happens: If lot_winner != active_seat: gift_receiver = the non-active seat that is not lot_winner. Otherwise gift_receiver = the non-active seat with the lower effective_bid; on a tie, the seat next clockwise after active_seat. gift is appended to gift_receiver's hand and new_cards. Announce the receiver.
  9. [update] all players. What happens: For each player, each 'Gold N' card in new_cards is removed from hand, and gold += N.
  10. [update] all players. What happens: For each player, church_count = the number of 'Church' cards in new_cards, and those cards are removed from hand. Announce each church_count.
  11. [poll] each player with church_count >= 1 answers: one of: 'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'. What happens: church_choice = answer.
  12. [update] all players. What happens: net = the sum of church_count over players with church_choice 'red up' minus the sum over players with 'red down'; vp_red = min(5, max(1, vp_red + net)).
  13. [update] all players. What happens: net = the sum of church_count over 'green up' minus the sum over 'green down'; vp_green = min(5, max(1, vp_green + net)).
  14. [update] all players. What happens: net = the sum of church_count over 'blue up' minus the sum over 'blue down'; vp_blue = min(5, max(1, vp_blue + net)). Announce vp_red, vp_green, vp_blue and each player's church_choice.
  15. [update] all players. What happens: For every player: church_count = 0, bid = 0, effective_bid = 0, church_choice = '', new_cards = []. Set lot = '', gift = '', lot_winner = 0 and gift_receiver = 0.
  16. [update] all players. What happens: Runs only when round == 12. For each player: red_sum, green_sum and blue_sum = the totals of that colour's card values in hand. For each colour, the player with the strictly highest sum gets vp += that colour's die value (vp_red, vp_green or vp_blue). If the highest is tied, nobody scores that colour. Announce each vp and gold.
  17. [check] all players. What happens: If round == 12, end the game; otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, the deck holds 36 cards: Red, Green and Blue each 1,1,2,2,3,3,4; Gold 1,1,1,2,2,2,3,3,3; and 6 Church cards.
  R2. At setup, each player has 4 gold, an empty hand and church_count 0, and vp_red, vp_green and vp_blue are each 3.
  R3. When the round is 1, 4, 7 or 10, then P1 is active; when it is 2, 5, 8 or 11, then P2 is active; when it is 3, 6, 9 or 12, then P3 is active.
  R4. At the start of each round, 3 cards are removed from the deck and shown only to the active player, so after round r the deck holds 36 - 3r cards.
  R5. When the active player chooses 'keep X sell Y', then card X goes into their hand, card Y becomes the lot, and the third card becomes the gift.
  R6. Each round, every player sends one talk message at the same time, and all messages are shown to everyone with their authors.
  R7. When a player bids more than their gold, then the bid counts as exactly their gold.
  R8. The highest effective bid wins the lot, and the winner's gold drops by that bid.
  R9. When the highest bid is tied and the active player is among the tied, then the active player wins the lot; otherwise the tied player first clockwise after the active player wins.
  R10. When all three players bid 0, then the active player wins the lot and pays 0.
  R11. When a non-active player wins the lot, then the gift goes to the other non-active player.
  R12. When the active player wins the lot, then the gift goes to the non-active player with the lower bid, or on a tie to the player next clockwise after the active player.
  R13. When a Gold N card enters a hand, then it is removed from that hand and the player's gold rises by N.
  R14. When Church cards enter a player's hand in a round, then church_count equals their number (0 to 2) and they are removed from the hand.
  R15. Each player with church_count >= 1 makes exactly one choice among red, green or blue, up or down; players with church_count 0 do not choose.
  R16. Each die moves by the summed church_count of its 'up' choosers minus that of its 'down' choosers, clamped to between 1 and 5 (for example 4 + 2 -> 5, and 2 - 2 -> 1).
  R17. At the end of each round, every church_count, bid and church_choice is reset.
  R18. When round 12 ends, then the game ends and scoring happens.
  R19. At scoring, the player with the strictly highest sum in a colour gains VP equal to that colour's die value; when the highest is tied, nobody scores that colour.
  R20. The most VP wins, ties are broken by the most gold, and players still tied share a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all players | options: any short text
  - Split | asked: the active seat only | options: 'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'
  - Bid | asked: all players, including the active seat | options: a whole number from 0 to 22
  - Church choice | asked: only seats with church_count >= 1; seats with church_count 0 are not asked | options: 'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12
  - each player's standing: you.vp * 100 + you.gold (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The most VP wins. A VP tie is broken by the most remaining Gold. Players still tied share the win, which is a draw among them.
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

- each player: `church_count` (number, visible: public, starts 0): Church cards that entered this player's hand this round (0, 1 or 2)
- each player: `vp` (number, visible: public, starts 0): Victory points scored at the end
- the table: `round` (number, visible: public, starts 0): Current round, 1 to 12
- the table: `active_seat` (number, visible: public, starts 0): Seat of the active player this round
- the table: `lot` (text, visible: public, starts ''): The card being auctioned this round
- the table: `gift` (text, visible: public, starts ''): The card given away this round
- the table: `vp_red` (number, visible: public, starts 3): Red VP die, from 1 to 5
- the table: `vp_green` (number, visible: public, starts 3): Green VP die, from 1 to 5
- the table: `vp_blue` (number, visible: public, starts 3): Blue VP die, from 1 to 5
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, colours = 3, colour_cards_per_colour = 7, colour_value_1_copies = 2, colour_value_2_copies = 2, colour_value_3_copies = 2, colour_value_4_copies = 1, colour_total_per_colour = 16, gold_cards = 9, gold_value_1_copies = 3, gold_value_2_copies = 3, gold_value_3_copies = 3, gold_cards_total = 18, church_cards = 6, starting_gold = 4, die_start = 3, die_min = 1, die_max = 5, rounds = 12, cards_per_round = 3, bid_min = 0, bid_max = 22, max_church_per_player_per_round = 2, rank_vp_weight = 100
- the game ends with ONE ending whose `rank_by` is `you.vp * 100 + you.gold`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Stop putting per-player data into prompt text, since a prompt can only fill in {value} and {seat}.
(1) Gold: store each player's Gold as a private player attribute (visible to its owner only). The state that player is shown will then display it. Make the bid prompt generic, e.g. 'Bid a whole number of Gold from 0 to 22; your current Gold is shown in your state.'
(2) The three dealt cards: during the Deal, move the top 3 deck cards into private player attributes of the active player only (e.g. offer_1, offer_2, offer_3, visible to that player alone). The split prompt then says 'Your three cards are shown in your state as offer_1..offer_3.' Clear those attributes (or set them to a placeholder text such as 'none') after the split.
(3) Blank lot and gift: never let a public field print empty. At the start of each round, before any state is shown, set lot and gift to an explicit text such as 'not chosen yet', and overwrite them at the Split. Alternatively, do not display table state in show_the_offer, which is a private step for the active player. Any other scratch attributes must be marked hidden (`none` visibility).
(4) Do not reuse a text placeholder like {gold} anywhere else, including the bid prompt that mentions the lot. Use {value} only where the step actually supplies a value.
Keep every parameter as an attribute. Keep the single ending with rank_by `you.vp * 100 + you.gold`.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "biblios_scriptorium_revised",
    "name": "Biblios: The Scriptorium (revised)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three scribes split three-card deals into a kept card, an auctioned lot and a gift, then move the colour dice with Church cards."
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
        "key": "gold",
        "visible": "ally",
        "type": "number",
        "initial": 4
      },
      {
        "key": "hand",
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
        "key": "new_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "effective_bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "church_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "church_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "red_sum",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_sum",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_sum",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "vp",
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
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lot",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "gift",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "lot_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gift_receiver",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "vp_red",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_green",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_blue",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "keep_pos",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sell_pos",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "keep_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "high_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "next_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "other_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "colour_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "colour_value_1_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_value_2_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_value_3_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_value_4_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "colour_total_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "gold_cards",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "gold_value_1_copies",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "gold_value_2_copies",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "gold_value_3_copies",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "gold_cards_total",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "church_cards",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "die_start",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "die_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "die_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "initial": 22
      },
      {
        "key": "max_church_per_player_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_vp_weight",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "fill the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "['Red 1', 'Red 1', 'Red 2', 'Red 2', 'Red 3', 'Red 3', 'Red 4', 'Green 1', 'Green 1', 'Green 2', 'Green 2', 'Green 3', 'Green 3', 'Green 4', 'Blue 1', 'Blue 1', 'Blue 2', 'Blue 2', 'Blue 3', 'Blue 3', 'Blue 4', 'Gold 1', 'Gold 1', 'Gold 1', 'Gold 2', 'Gold 2', 'Gold 2', 'Gold 3', 'Gold 3', 'Gold 3', 'Church', 'Church', 'Church', 'Church', 'Church', 'Church']"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the players and the dice",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "starting_gold"
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
            "key": "church_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "die_start"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "die_start"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "die_start"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the deck",
      "to": "all",
      "text": "The deck has {deck_size} cards, shuffled face-down: Red, Green and Blue each 1, 1, 2, 2, 3, 3, 4; Gold 1, 1, 1, 2, 2, 2, 3, 3, 3; and {church_cards} Church cards. Each of you starts with {starting_gold} Gold, kept private. The dice for Red, Green and Blue start at {die_start}. Seats sit clockwise 1 -> 2 -> 3 -> 1."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "active player",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "((round - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": "not chosen yet"
          }
        },
        {
          "set": {
            "key": "gift",
            "value": "not chosen yet"
          }
        }
      ],
      "text": "Round {round}: seat {active_seat} is active."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "deal",
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
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "offer",
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
            "player": {
              "calc": "active_seat"
            },
            "key": "offer",
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
            "player": {
              "calc": "active_seat"
            },
            "key": "offer",
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
        }
      ]
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "show the offer",
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "fields": [
        "offer"
      ],
      "text": "Your three dealt cards, in positions 1, 2 and 3:"
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
      "text": "Say one short thing to the table. Everyone writes at the same moment; talk is not binding and may be a bluff."
    },
    {
      "use": "ask",
      "phase": "split",
      "label": "split",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "keep 1 sell 2",
          "keep 1 sell 3",
          "keep 2 sell 1",
          "keep 2 sell 3",
          "keep 3 sell 1",
          "keep 3 sell 2"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "keep_pos",
              "value": {
                "calc": "0 if $answer in ['keep 1 sell 2', 'keep 1 sell 3'] else (1 if $answer in ['keep 2 sell 1', 'keep 2 sell 3'] else 2)"
              }
            }
          },
          {
            "set": {
              "key": "sell_pos",
              "value": {
                "calc": "0 if $answer in ['keep 2 sell 1', 'keep 3 sell 1'] else (1 if $answer in ['keep 1 sell 2', 'keep 3 sell 2'] else 2)"
              }
            }
          },
          {
            "set": {
              "key": "keep_card",
              "value": {
                "calc": "[p.offer[keep_pos] for p in players if p.seat == active_seat][0]"
              }
            }
          },
          {
            "set": {
              "key": "lot",
              "value": {
                "calc": "[p.offer[sell_pos] for p in players if p.seat == active_seat][0]"
              }
            }
          },
          {
            "set": {
              "key": "gift",
              "value": {
                "calc": "[p.offer[int(cards_per_round * (cards_per_round - 1) / 2) - keep_pos - sell_pos] for p in players if p.seat == active_seat][0]"
              }
            }
          },
          {
            "append": {
              "player": "$seat",
              "key": "hand",
              "value": {
                "calc": "keep_card"
              }
            }
          },
          {
            "append": {
              "player": "$seat",
              "key": "new_cards",
              "value": {
                "calc": "keep_card"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "offer",
              "value": []
            }
          }
        ]
      },
      "text": "Split your three cards, shown in your state as offer (positions 1, 2 and 3). Choose 'keep X sell Y': card X goes face-down into your hand, card Y becomes the lot everyone bids on, and the remaining card becomes the gift."
    },
    {
      "use": "tell",
      "phase": "split",
      "label": "reveal",
      "to": "all",
      "text": "Lot: {lot}. Gift: {gift}. The kept card stays secret."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
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
      "text": "Bid a whole number of Gold from 0 to 22 for the lot, in secret; everyone bids at the same moment. Your current Gold is shown in your state. A bid above your Gold counts as exactly your whole Gold."
    },
    {
      "use": "update",
      "phase": "sale",
      "label": "sale",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "effective_bid",
            "value": {
              "calc": "min(you.bid, you.gold)"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.effective_bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "lot_winner",
            "value": {
              "calc": "((active_seat - 1 + min([(p.seat - active_seat + len(players)) % len(players) for p in players if p.effective_bid == high_bid])) % len(players)) + 1"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "lot_winner"
            },
            "key": "gold",
            "value": {
              "calc": "-high_bid"
            },
            "if": {
              "calc": "high_bid > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "lot_winner"
            },
            "key": "hand",
            "value": {
              "calc": "lot"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "lot_winner"
            },
            "key": "new_cards",
            "value": {
              "calc": "lot"
            }
          }
        }
      ],
      "text": "Seat {lot_winner} wins the lot ({lot}) and pays {high_bid} Gold. Bids: seat 1 {players[0].bid}, seat 2 {players[1].bid}, seat 3 {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "gift",
      "label": "gift",
      "do": [
        {
          "set": {
            "key": "next_seat",
            "value": {
              "calc": "(active_seat % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "other_seat",
            "value": {
              "calc": "((active_seat + 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "key": "gift_receiver",
            "value": {
              "calc": "([p.seat for p in players if p.seat != active_seat and p.seat != lot_winner][0]) if lot_winner != active_seat else (other_seat if [p.effective_bid for p in players if p.seat == other_seat][0] < [p.effective_bid for p in players if p.seat == next_seat][0] else next_seat)"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "gift_receiver"
            },
            "key": "hand",
            "value": {
              "calc": "gift"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "gift_receiver"
            },
            "key": "new_cards",
            "value": {
              "calc": "gift"
            }
          }
        }
      ],
      "text": "Seat {gift_receiver} receives the gift ({gift})."
    },
    {
      "use": "update",
      "phase": "cards",
      "label": "gold cards",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "sum([1 if c == 'Gold 1' else (2 if c == 'Gold 2' else (3 if c == 'Gold 3' else 0)) for c in you.new_cards])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in you.hand if c not in ['Gold 1', 'Gold 2', 'Gold 3']]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "cards",
      "label": "church cards",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "church_count",
            "value": {
              "calc": "min(max_church_per_player_per_round, count(c == 'Church' for c in you.new_cards))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in you.hand if c != 'Church']"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_choice",
            "value": "none"
          }
        }
      ],
      "text": "Church cards this round: seat 1 {players[0].church_count}, seat 2 {players[1].church_count}, seat 3 {players[2].church_count}."
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "church choice",
      "when": {
        "calc": "sum([p.church_count for p in players]) >= 1"
      },
      "to": {
        "where": "you.church_count >= 1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "red up",
          "red down",
          "green up",
          "green down",
          "blue up",
          "blue down"
        ]
      },
      "store": "church_choice",
      "text": "You played Church cards this round (your church_count is in your state). Make exactly one secret choice: move one die up or down. The die moves by your church_count in that direction, combined with the other players' choices, and stays between 1 and 5."
    },
    {
      "use": "update",
      "phase": "church",
      "label": "red die",
      "do": [
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "min(die_max, max(die_min, vp_red + sum([p.church_count for p in players if p.church_choice == 'red up']) - sum([p.church_count for p in players if p.church_choice == 'red down'])))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "church",
      "label": "green die",
      "do": [
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "min(die_max, max(die_min, vp_green + sum([p.church_count for p in players if p.church_choice == 'green up']) - sum([p.church_count for p in players if p.church_choice == 'green down'])))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "church",
      "label": "blue die",
      "do": [
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "min(die_max, max(die_min, vp_blue + sum([p.church_count for p in players if p.church_choice == 'blue up']) - sum([p.church_count for p in players if p.church_choice == 'blue down'])))"
            }
          }
        }
      ],
      "text": "Dice: red {vp_red}, green {vp_green}, blue {vp_blue}. Church choices: seat 1 {players[0].church_choice}, seat 2 {players[1].church_choice}, seat 3 {players[2].church_choice}."
    },
    {
      "use": "update",
      "phase": "reset",
      "label": "reset",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "church_count",
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
            "key": "effective_bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "new_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "lot",
            "value": ""
          }
        },
        {
          "set": {
            "key": "gift",
            "value": ""
          }
        },
        {
          "set": {
            "key": "lot_winner",
            "value": 0
          }
        },
        {
          "set": {
            "key": "gift_receiver",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "red_sum",
            "value": {
              "calc": "count(c == 'Red 1' for c in you.hand) + 2 * count(c == 'Red 2' for c in you.hand) + 3 * count(c == 'Red 3' for c in you.hand) + 4 * count(c == 'Red 4' for c in you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green_sum",
            "value": {
              "calc": "count(c == 'Green 1' for c in you.hand) + 2 * count(c == 'Green 2' for c in you.hand) + 3 * count(c == 'Green 3' for c in you.hand) + 4 * count(c == 'Green 4' for c in you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue_sum",
            "value": {
              "calc": "count(c == 'Blue 1' for c in you.hand) + 2 * count(c == 'Blue 2' for c in you.hand) + 3 * count(c == 'Blue 3' for c in you.hand) + 4 * count(c == 'Blue 4' for c in you.hand)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "count(p.red_sum >= you.red_sum for p in players) == 1"
            },
            "key": "vp",
            "value": {
              "calc": "vp_red"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "count(p.green_sum >= you.green_sum for p in players) == 1"
            },
            "key": "vp",
            "value": {
              "calc": "vp_green"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "count(p.blue_sum >= you.blue_sum for p in players) == 1"
            },
            "key": "vp",
            "value": {
              "calc": "vp_blue"
            }
          }
        }
      ],
      "text": "Scoring: seat 1 {players[0].vp} VP and {players[0].gold} Gold; seat 2 {players[1].vp} VP and {players[1].gold} Gold; seat 3 {players[2].vp} VP and {players[2].gold} Gold."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "end check",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.vp * 100 + you.gold",
      "reveal": [
        "hand",
        "gold"
      ],
      "text": "Winner: {result}. Final: Seat 1 {players[0].vp} VP, {players[0].gold} Gold; Seat 2 {players[1].vp} VP, {players[1].gold} Gold; Seat 3 {players[2].vp} VP, {players[2].gold} Gold. Dice: red {vp_red}, green {vp_green}, blue {vp_blue}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 13,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "SETUP. The deck has {deck_size} cards: Colour cards (21): for each of Red, Green and Blue, values 1, 1, 2, 2, 3, 3, 4 (each colour totals {colour_total_per_colour}). Gold cards ({gold_cards}): values 1, 1, 1, 2, 2, 2, 3, 3, 3, totalling {gold_cards_total} Gold. Church cards ({church_cards}): each simply named 'Church'. The deck composition is public; the deck is shuffled once and kept face-down, its order hidden from everyone. Each player starts with {starting_gold} Gold (private: only that player sees it), an empty private hand, and church_count 0. Three public dice, vp_red, vp_green and vp_blue, each start at {die_start} and always stay between {die_min} and {die_max}. Players sit P1, P2, P3; clockwise order is P1 -> P2 -> P3 -> P1. The game lasts {rounds} rounds, which uses the whole deck exactly.\n\nEACH ROUND:\n1. Active player. P1 is active in rounds 1, 4, 7 and 10; P2 in rounds 2, 5, 8 and 11; P3 in rounds 3, 6, 9 and 12. This is announced to everyone.\n2. Deal. The top {cards_per_round} cards of the deck are removed and shown privately to the active player as positions 1, 2 and 3.\n3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone with their authors. Talk is not binding and may be a bluff.\n4. Split. The active player chooses one of 'keep 1 sell 2', 'keep 1 sell 3', 'keep 2 sell 1', 'keep 2 sell 3', 'keep 3 sell 1', 'keep 3 sell 2'. The keep card goes face-down into the active player's hand. The sell card becomes the lot. The remaining card becomes the gift.\n5. Reveal. The lot and the gift are shown face-up to everyone. The kept card stays secret.\n6. Bid. All three players, including the active player, privately bid a whole number of Gold from {bid_min} to {bid_max}, all at the same moment. A bid above a player's current Gold counts as exactly that player's whole Gold; a bid at or below it counts as bid.\n7. Sale. The highest bid wins the lot. On a tie for highest: the active player wins if among the tied; otherwise the tied player who comes first clockwise after the active player wins. If all bid 0, the active player wins and pays 0. The winner loses Gold equal to their bid (paid to the bank) and takes the lot into their hand; the others pay nothing. All three bids are then revealed to everyone.\n8. Gift. If a non-active player won the lot, the gift goes to the other non-active player. If the active player won the lot, the gift goes to whichever non-active player bid lower; on a tie it goes to the player next clockwise after the active player.\n9. Gold cards. Every Gold card that entered a hand this round is removed from that hand, and its value is added to that player's Gold.\n10. Church cards. For each player, church_count is set to the number of Church cards that entered their hand this round (0, 1 or 2; only the active player can reach {max_church_per_player_per_round}). Those Church cards are removed from the hand. Each player's church_count is announced.\n11. Church choice. Every player with church_count of 1 or more privately makes exactly ONE choice at the same moment, from 'red up', 'red down', 'green up', 'green down', 'blue up', 'blue down'. Players with church_count 0 do not choose.\n12-14. Dice. For each colour, net = (sum of church_count over players who chose that colour 'up') minus (sum of church_count over players who chose it 'down'); the die becomes min({die_max}, max({die_min}, die + net)). For example 4 + 2 -> 5, and 2 - 2 -> 1. A die nobody chose stays where it is. The three die values and each player's Church choice are announced.\n15. Reset. Every church_count is set to 0, and bids and Church choices are cleared.\n16. End check. After round {rounds}, go to scoring; otherwise start the next round.\n\nSCORING. For each colour, each player's sum is the total value of that colour's cards in their hand. The player with the strictly highest sum in a colour scores VP equal to that colour's die value. If two or more players tie for highest, nobody scores that colour. A player's VP is the total over the three colours. The player with the most VP wins. If players tie on VP, the tied player with the most remaining Gold wins. If they are still tied, the game is a draw among them (they share the win)."
}
```
````
