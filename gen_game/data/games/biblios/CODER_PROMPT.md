# Task: write the XColos game file for "Biblios: Scriptorium Lots (revised)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- 3 players, seats 1, 2 and 3.
- The deck has 36 cards, and its makeup is public knowledge:
  - Colour cards in five colours (Red, Blue, Green, Yellow, Purple). Each colour has values 1, 1, 2, 2, 3, 4, making 30 cards.
  - 3 Gold cards, worth 2, 3 and 4 gold.
  - 3 Church cards.
- The deck is shuffled once.
- Each player starts with 8 gold, 0 in every colour, an empty public record and a church flag set to No.
- Five colour dice each start at 3. A die can never go below 1 or above 6.

TURN ORDER
- The game lasts exactly 12 rounds.
- The active player in rounds 1 to 12 is, in order: seat 1, 2, 3, 2, 3, 1, 3, 1, 2, 1, 2, 3.
- The active player's 'next seat' is cyclic: 1 to 2, 2 to 3, 3 to 1.

CARD EFFECTS (used whenever a player receives a card)
- A colour card adds its value to that player's total in its colour.
- A Gold card adds its gold to that player's purse.
- A Church card sets that player's church flag to Yes. If the flag is already Yes, the card has no further effect this round. A player gets at most one church action per round, no matter how many Church cards they acquire.

EACH ROUND
1. The round number and active player are announced.
2. The top 3 cards of the deck are dealt and shown only to the active player.
3. SPLIT (active player's choice): the active player assigns the three cards, one each, to KEEP, AUCTION and GIVE. There are 6 possible assignments, each offered as one option.
4. The KEEP card goes to the active player face-down and takes effect (see CARD EFFECTS). Only that player knows what it was. Purses are public, so a gold gain reveals a kept Gold card.
5. The GIVE card is revealed, goes to the active player's next seat, takes effect, and is added to that player's public record.
6. The AUCTION card is revealed to everyone.
7. TALK: all three players write one short message at the same time. All messages are then shown together. Talk is not binding.
8. BID: all three players secretly and at the same time bid a whole number from 0 up to their current gold.
9. All bids are revealed. If exactly one player made the highest bid and it is above 0, that player pays that much gold, which leaves the game. That player takes the auction card, which takes effect and is added to their public record. Otherwise (a tie for the top bid, or all bids 0) the card is discarded and nobody pays.
10. CHURCH: every player whose church flag is Yes chooses, all at the same time, exactly one of 10 options: raise Red, lower Red, raise Blue, lower Blue, raise Green, lower Green, raise Yellow, lower Yellow, raise Purple, lower Purple, each by 1. Choices are applied in seat order 1, 2, 3, each clamped to the range 1-6. If no flag is Yes, this step is skipped.
11. All church flags are reset to No.
12. Public state is announced: the five die values, each player's gold, and each player's public record. Kept cards and true colour totals are not shown.

END OF GAME (after round 12; all 36 cards have been dealt)
- For each colour, compare the three players' true totals in that colour, kept cards included.
- If one player alone has the highest total, that player scores VP equal to that colour's final die value. If the highest total is tied, nobody scores that colour.
- Each player's VP is the sum of the colours they won.

ENGINE ATTRIBUTES (18)
- Per player (8): Red total, Blue total, Green total, Yellow total, Purple total (all hidden), gold, church flag, public record (text).
- Table (10): five dice, round number, active seat, deck (list), dealt cards (list of 3), auction card.

How the winner is decided: The player with the most VP wins. If VP is tied at the top, the tied player with the most remaining gold wins. If that is also tied, the game is a draw among those players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Biblios: Scriptorium Lots (revised) (3 to 3 players, best with 3)

Three scribes take turns splitting three cards among keep, give and auction. They bid gold for the auction cards and use Church cards to push colour dice, then score each colour they alone lead at its final die value.

STATE (every item below must exist in the file):
  - each player: red (number, starts 0); only its owner sees it. true Red total, kept cards included
  - each player: blue (number, starts 0); only its owner sees it. true Blue total, kept cards included
  - each player: green (number, starts 0); only its owner sees it. true Green total, kept cards included
  - each player: yellow (number, starts 0); only its owner sees it. true Yellow total, kept cards included
  - each player: purple (number, starts 0); only its owner sees it. true Purple total, kept cards included
  - each player: gold (number, starts 8); everyone sees it. purse; the public tie-break
  - each player: church (bool, starts False); only its owner sees it. church flag; Yes gives one church action this round
  - each player: kept (list, starts []); only its owner sees it. cards this player kept face-down
  - each player: public_record (text, starts ''); everyone sees it. cards received openly (given or won at auction)
  - each player: vp (number, starts 0); everyone sees it. victory points, computed after round 12
  - the table: die_red (number, starts 3); everyone sees it. Red die, 1-6
  - the table: die_blue (number, starts 3); everyone sees it. Blue die, 1-6
  - the table: die_green (number, starts 3); everyone sees it. Green die, 1-6
  - the table: die_yellow (number, starts 3); everyone sees it. Yellow die, 1-6
  - the table: die_purple (number, starts 3); everyone sees it. Purple die, 1-6
  - the table: round (number, starts 0); everyone sees it. current round number
  - the table: active_seat (number, starts 0); everyone sees it. seat of the active player this round
  - the table: active_order (list, starts [1, 2, 3, 2, 3, 1, 3, 1, 2, 1, 2, 3]); everyone sees it. active seat for rounds 1-12
  - the table: deck (list, starts ['Red 1', 'Red 1', 'Red 2', 'Red 2', 'Red 3', 'Red 4', 'Blue 1', 'Blue 1', 'Blue 2', 'Blue 2', 'Blue 3', 'Blue 4', 'Green 1', 'Green 1', 'Green 2', 'Green 2', 'Green 3', 'Green 4', 'Yellow 1', 'Yellow 1', 'Yellow 2', 'Yellow 2', 'Yellow 3', 'Yellow 4', 'Purple 1', 'Purple 1', 'Purple 2', 'Purple 2', 'Purple 3', 'Purple 4', 'Gold 2', 'Gold 3', 'Gold 4', 'Church', 'Church', 'Church']); hidden from all players. shuffled draw pile; its makeup is public, its order hidden
  - the table: dealt (list, starts []); hidden from all players. the 3 cards dealt this round, shown privately to the active player only
  - the table: auction_card (text, starts ''); everyone sees it. the card up for auction this round
  - the table: discard (list, starts []); everyone sees it. auction cards nobody won
  - parameters, each kept as a table attribute: player_count = 3, deck_size = 36, colours = 5, colour_cards_per_colour = 6, colour_value_1_copies = 2, colour_value_2_copies = 2, colour_value_3_copies = 1, colour_value_4_copies = 1, colour_cards_total = 30, gold_card_small = 2, gold_card_mid = 3, gold_card_large = 4, gold_cards = 3, church_cards = 3, starting_gold = 8, starting_colour_total = 0, die_start = 3, die_min = 1, die_max = 6, die_step = 1, rounds = 12, cards_per_round = 3, split_options = 6, church_options = 10, max_church_actions_per_round = 1, min_bid = 0, winning_bid_must_exceed = 0, active_seat_round_1 = 1, active_seat_round_2 = 2, active_seat_round_3 = 3, active_seat_round_4 = 2, active_seat_round_5 = 3, active_seat_round_6 = 1, active_seat_round_7 = 3, active_seat_round_8 = 1, active_seat_round_9 = 2, active_seat_round_10 = 1, active_seat_round_11 = 2, active_seat_round_12 = 3, rank_gold_weight = 1, rank_vp_weight = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 are filled.
  2. The 36-card deck is placed in `deck` and shuffled once by the seeded random draw. It holds 30 colour cards (Red, Blue, Green, Yellow and Purple, each with values 1, 1, 2, 2, 3, 4), Gold 2, Gold 3, Gold 4 and three Church cards.
  3. Each player starts with gold 8, all five colour totals 0, an empty kept list, an empty public_record, church No and vp 0.
  4. All five dice start at 3.
  5. The deck makeup is announced to everyone.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; active_seat = active_order[round-1]; announce 'Round {round}: seat {active_seat} is active.'
  2. [update] seat active_seat. What happens: Draw 3 cards at random from deck into dealt, removing them from deck. Reveal dealt privately to the active seat only.
  3. [ask] seat active_seat answers: one of the 6 assignments of the three dealt cards to KEEP / AUCTION / GIVE, each listed as an option naming the cards (e.g. 'KEEP Red 3, AUCTION Gold 2, GIVE Church'). What happens: records which dealt card is keep_card, auction_card and give_card
  4. [update] seat active_seat. What happens: keep_card is appended to the active player's kept list and takes effect for them. A colour card adds its value to that colour total, a Gold card adds to gold, and a Church card sets church = true (no extra effect if already true). Nothing is announced except the public change in gold.
  5. [update] next seat of active_seat (1->2, 2->3, 3->1). What happens: give_card is revealed to everyone, takes effect for the next seat (colour total, gold or church = true), and is appended to that player's public_record.
  6. [update] all players. What happens: auction_card = the AUCTION card; announce it to everyone. dealt is emptied.
  7. [poll] all players answers: short text message. What happens: broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all are in; non-binding
  8. [poll] all players answers: whole number from 0 to that player's gold. What happens: records each player's secret bid
  9. [update] all players. What happens: All bids are revealed and top = max bid. If top > 0 and exactly one player bid top, that player's gold -= top (the gold leaves the game), auction_card takes effect for them (colour total, gold or church = true) and is appended to their public_record. Otherwise auction_card is appended to discard and nobody pays.
  10. [poll] every player whose church is true (step skipped if none) answers: one of: raise Red, lower Red, raise Blue, lower Blue, raise Green, lower Green, raise Yellow, lower Yellow, raise Purple, lower Purple. What happens: Choices are applied in seat order 1, 2, 3: the named die is changed by +1 or -1 and clamped to 1..6.
  11. [update] all players. What happens: church = false for every player.
  12. [tell] all players. What happens: Announce the five die values, each player's gold and each player's public_record. Kept cards and true colour totals are not shown.
  13. [update] all players. What happens: when round == 12: for each colour, a player whose total in that colour is strictly greater than both other players' totals gets vp += that colour's die value; a tied top scores nobody.
  14. [check] all players. What happens: end the game if round == 12, otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has gold 8, all colour totals 0, church No and an empty public_record, and every die is 3.
  R2. When the game starts, then the deck holds 36 cards: values 1, 1, 2, 2, 3, 4 in each of five colours, Gold 2, Gold 3, Gold 4 and 3 Church cards.
  R3. When round r (1-12) begins, then the active seat is entry r of the order 1, 2, 3, 2, 3, 1, 3, 1, 2, 1, 2, 3.
  R4. When a round begins, then 3 cards are removed from the deck and shown only to the active seat.
  R5. When the active seat splits the cards, then they choose one of exactly 6 assignments of the 3 cards to KEEP, AUCTION and GIVE.
  R6. When a player receives a colour card of value v, then their total in that colour rises by v.
  R7. When a player receives a Gold card worth g, then their gold rises by g.
  R8. When a player receives a Church card, then their church flag becomes Yes, and a second Church card in the same round has no further effect.
  R9. When the KEEP card is applied, then it goes to the active seat's kept list, is not revealed, and is not added to the public record.
  R10. When the GIVE card is applied, then it is revealed, goes to the next seat (1->2, 2->3, 3->1), takes effect and is added to that seat's public_record.
  R11. When the AUCTION card is chosen, then it is revealed to everyone before talk and bidding.
  R12. When talk happens, then all three players submit one short message at the same time and all are shown together; talk is not binding.
  R13. When bidding happens, then each player secretly bids a whole number from 0 to their current gold, all at the same time.
  R14. When exactly one player has the highest bid and it is above 0, then that player loses that much gold (the gold leaves the game), gets the auction card's effect, and the card is added to their public_record.
  R15. When the top bid is tied or all bids are 0, then the auction card is discarded and nobody pays.
  R16. When at least one church flag is Yes, then each such player picks one of 10 options (raise or lower one of the five dice by 1), all at the same time.
  R17. When church choices are applied, then they are applied in seat order 1, 2, 3, and each die is clamped to between 1 and 6 (raising a 6 or lowering a 1 does nothing).
  R18. When no church flag is Yes, then the church step is skipped.
  R19. When a round ends, then every church flag is reset to No and the dice, every player's gold and every public_record are announced.
  R20. When round 12 ends, then the game ends and all 36 cards have been dealt.
  R21. When the game ends, then for each colour the single player with the strictly highest true total gains VP equal to that colour's die, and a tied top scores nobody.
  R22. When the game ends, then the player with the most VP wins; a VP tie goes to the most gold; players still level share the win as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - SPLIT | asked: the active seat only | options: the 6 permutations assigning this round's 3 dealt cards to KEEP, AUCTION and GIVE, each naming the cards
  - TALK | asked: all three seats | options: one short free-text message
  - BID | asked: all three seats | options: a whole number from 0 to that seat's current gold
  - CHURCH | asked: only seats whose church flag is Yes; seats with No are not asked | options: raise Red, lower Red, raise Blue, lower Blue, raise Green, lower Green, raise Yellow, lower Yellow, raise Purple, lower Purple

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12
  - each player's standing: you.vp * 1000 + you.gold (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Most VP wins. A tie on VP goes to the tied player with the most gold. Players still level share the win (a draw).
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

- each player: `gold` (number, visible: public, starts 8): purse; the public tie-break
- each player: `public_record` (text, visible: public, starts ''): cards received openly (given or won at auction)
- each player: `vp` (number, visible: public, starts 0): victory points, computed after round 12
- the table: `die_red` (number, visible: public, starts 3): Red die, 1-6
- the table: `die_blue` (number, visible: public, starts 3): Blue die, 1-6
- the table: `die_green` (number, visible: public, starts 3): Green die, 1-6
- the table: `die_yellow` (number, visible: public, starts 3): Yellow die, 1-6
- the table: `die_purple` (number, visible: public, starts 3): Purple die, 1-6
- the table: `round` (number, visible: public, starts 0): current round number
- the table: `active_seat` (number, visible: public, starts 0): seat of the active player this round
- the table: `auction_card` (text, visible: public, starts ''): the card up for auction this round
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, deck_size = 36, colours = 5, colour_cards_per_colour = 6, colour_value_1_copies = 2, colour_value_2_copies = 2, colour_value_3_copies = 1, colour_value_4_copies = 1, colour_cards_total = 30, gold_card_small = 2, gold_card_mid = 3, gold_card_large = 4, gold_cards = 3, church_cards = 3, starting_gold = 8, starting_colour_total = 0, die_start = 3, die_min = 1, die_max = 6, die_step = 1, rounds = 12, cards_per_round = 3, split_options = 6, church_options = 10, max_church_actions_per_round = 1, min_bid = 0, winning_bid_must_exceed = 0, active_seat_round_1 = 1, active_seat_round_2 = 2, active_seat_round_3 = 3, active_seat_round_4 = 2, active_seat_round_5 = 3, active_seat_round_6 = 1, active_seat_round_7 = 3, active_seat_round_8 = 1, active_seat_round_9 = 2, active_seat_round_10 = 1, active_seat_round_11 = 2, active_seat_round_12 = 3, rank_gold_weight = 1, rank_vp_weight = 1000
- the game ends with ONE ending whose `rank_by` is `you.vp * 1000 + you.gold`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Auction resolution: the condition 'auction_winner > 0 and you.gold >= top_bid' sits in a table-level step where there is no `you`. Bids are capped at current gold, so drop the gold check entirely. Resolve the winner with table attributes: compute top_bid and a count of players at top_bid, and set auction_winner only when the count is 1 and top_bid > winning_bid_must_exceed. Then apply payment and the card effect in a per-player step whose `when` is `you.seat == auction_winner`. 2) Remove attributes that nothing writes: active_order, card_table and perms. Alternatively, actually use active_order, by setting active_seat each round from the active_seat_round_N parameters with `if` conditions on round. Do not keep dead attributes. 3) Church dice: check that each of the 10 church options maps to a step whose `if` tests the exact option text the poll returns. Spell the key exactly die_blue. Apply raise as min(die + die_step, die_max) and lower as max(die - die_step, die_min). Apply choices in seat order 1, 2, 3, only for players whose church flag is Yes. Make sure the church flag is really set when a Church card is kept, given or won at auction, because that is the only way any die changes. Reset the flags only after the church step. 4) Keep hiding bookkeeping (give_card, top_bid, auction_winner, counts) from the shown state, as attempt 1 required, so empty fields are not printed.
