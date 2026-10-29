# 13 coder

- time: 2026-10-27T17:29:33+00:00 (122.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 b0c44cedb80f3aca, reply sha256 4567a85a43094fdb

## Sent

````
# Task: write the XColos game file for "Biblios: Scriptorium"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP

The deck has 24 cards, and its full contents are public knowledge:
- Red: 1, 1, 2, 2, 3, 4 (6 cards)
- Blue: 1, 1, 2, 2, 3, 4 (6 cards)
- Green: 1, 1, 2, 2, 3, 4 (6 cards)
- Gold: 2, 2, 3, 3 (4 cards)
- Church (2 cards)

Shuffle the deck. Every player starts with 4 Gold. Each player's Gold amount is private. Each colour has a public VP value that starts at 3 (Red 3, Blue 3, Green 3); a VP value can never go below 1 or above 5. Seat 1 is the active player in round 1. The game lasts exactly 12 rounds, and the active player rotates by seat each round (seat 1, 2, 3, 1, ... or seat 1-4 with 4 players). The deck is exactly used up.

EACH ROUND

1. Draw. Draw the top 2 cards. Only the active player sees them.

2. Keep. The active player secretly chooses one card to keep.
   - A kept colour card goes face-down into the active player's private hand. Its value counts for that colour at the end.
   - A kept Gold card adds its value to the active player's private Gold immediately.
   - A kept Church card is played at step 9.
   - Nobody else learns what was kept, except that a Church card is revealed when it is played.

3. Offer. The other card is revealed to everyone as the lot.

4. Talk. Every player, including the active player, writes one short message at the same time. All messages are then shown to everyone. Talk is not binding.

5. Bid. Every non-active player at the same time submits a whole-number bid from 0 up to their current Gold.

6. Resolve.
   - If one player made the single highest bid and it is at least 1, that player pays the bid from their Gold to the active player's Gold.
   - If the highest bid is tied, or all bids are 0, nobody pays and the lot is discarded.

7. Take. The winner takes the lot face-up, so its colour and value are public.
   - A Gold lot adds its value to the winner's Gold.
   - A Church lot is played at step 9.

8. Announce. The sale price (or 'discarded') is announced.

9. Church. Each player who gained a Church card this round, whether kept or bought, chooses at the same time one colour and either +1 or -1. Apply all changes, limited to the range 1-5. A colour may receive two changes. The new VP values are announced.

10. End check. After round 12, the game ends.

END SCORING

For each colour, each player sums the values of all their colour cards in that colour (kept and bought). The player with the highest sum gains that colour's current VP value. If several players tie for highest, they split the value equally (fractions allowed). A colour in which everyone has 0 scores for no one. Gold scores no VP.

How the winner is decided: The player with the most VP wins. If VP totals tie for first, the tied player with the most leftover Gold wins. If that also ties, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Biblios: Scriptorium (3 to 4 players, best with 3)

Over 12 rounds, the active player draws 2 cards, secretly keeps one and auctions the other in a sealed bid. Church cards shift colour values, and the most cards in a colour wins that colour's VP.

STATE (every item below must exist in the file):
  - each player: gold (number, starts 4); only its owner sees it. Private Gold. It pays bids, receives sale proceeds and Gold cards, and breaks VP ties.
  - each player: hand (list, starts []); only its owner sees it. Kept cards, face-down and private (colour cards and kept Church cards)
  - each player: kept_red (number, starts 0); only its owner sees it. Sum of values of kept Red cards
  - each player: kept_blue (number, starts 0); only its owner sees it. Sum of values of kept Blue cards
  - each player: kept_green (number, starts 0); only its owner sees it. Sum of values of kept Green cards
  - each player: bought (list, starts []); everyone sees it. Lots won at auction, face-up
  - each player: bought_red (number, starts 0); everyone sees it. Sum of values of bought Red cards
  - each player: bought_blue (number, starts 0); everyone sees it. Sum of values of bought Blue cards
  - each player: bought_green (number, starts 0); everyone sees it. Sum of values of bought Green cards
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid
  - each player: church_pending (bool, starts False); only its owner sees it. True if the player gained a Church card this round (kept or bought); revealed when it is played at step 9
  - each player: church_choice (text, starts ''); everyone sees it. This round's Church play: a colour and +1 or -1
  - each player: vp (number, starts 0); everyone sees it. Victory points, calculated at end scoring
  - the table: deck (list, starts ['red-1', 'red-1', 'red-2', 'red-2', 'red-3', 'red-4', 'blue-1', 'blue-1', 'blue-2', 'blue-2', 'blue-3', 'blue-4', 'green-1', 'green-1', 'green-2', 'green-2', 'green-3', 'green-4', 'gold-2', 'gold-2', 'gold-3', 'gold-3', 'church', 'church']); hidden from all players. Undrawn cards; the composition is public knowledge but the order is hidden
  - the table: drawn (list, starts []); hidden from all players. The 2 cards drawn this round; shown only to the active player, as the options of the keep question
  - the table: lot (text, starts ''); everyone sees it. The card offered at auction this round
  - the table: discard (list, starts []); everyone sees it. Lots that went unsold
  - the table: vp_red (number, starts 3); everyone sees it. Red VP value, 1-5
  - the table: vp_blue (number, starts 3); everyone sees it. Blue VP value, 1-5
  - the table: vp_green (number, starts 3); everyone sees it. Green VP value, 1-5
  - the table: round (number, starts 0); everyone sees it. Current round number
  - the table: active_seat (number, starts 1); everyone sees it. Seat of the active player: ((round-1) mod player_count)+1
  - the table: high_bid (number, starts 0); hidden from all players. Scratch: highest bid this round
  - the table: high_count (number, starts 0); hidden from all players. Scratch: number of bidders at the highest bid
  - the table: winner_seat (number, starts 0); everyone sees it. Seat that won the lot this round (0 if discarded)
  - the table: sale_price (number, starts 0); everyone sees it. Price paid this round (0 if discarded)
  - parameters, each kept as a table attribute: deck_size = 24, colour_cards_per_colour = 6, colour_cards_value_1_per_colour = 2, colour_cards_value_2_per_colour = 2, colour_cards_value_3_per_colour = 1, colour_cards_value_4_per_colour = 1, gold_cards = 4, gold_cards_value_2 = 2, gold_cards_value_3 = 2, church_cards = 2, starting_gold = 4, vp_start = 3, vp_min = 1, vp_max = 5, rounds = 12, cards_drawn_per_round = 2, cards_kept_per_round = 1, min_bid = 0, min_winning_bid = 1, church_change = 1, rank_vp_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Put the 24 cards listed above in the table list deck. The order is random because each draw takes a random card.
  2. Every player starts with gold = 4 (private), an empty hand, an empty bought list and all colour sums at 0.
  3. Set vp_red = vp_blue = vp_green = 3 (public).
  4. Set round = 0. Seat 1 will be the active player in round 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; active_seat = ((round-1) mod player_count) + 1; reset every player's bid = 0, church_pending = false, church_choice = ''; winner_seat = 0, sale_price = 0, high_bid = 0, high_count = 0, lot = ''
  2. [update] table. What happens: Draw: move 2 random cards from deck into drawn (remove from deck, append to drawn)
  3. [ask] the active seat (active_seat) answers: one card from drawn (only the active player sees these options). What happens: Kept colour card <c>-<v>: append it to the active player's hand and add v to kept_<c>. Kept gold-<v>: add v to the active player's gold. Kept church: append it to hand and set church_pending = true. The other card in drawn becomes lot, then drawn is cleared.
  4. [tell] all players. What happens: Offer: announce 'The lot is {lot}.'
  5. [poll] all players answers: short text message. What happens: Talk: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}; talk is not binding
  6. [poll] every seat except active_seat answers: whole number from 0 to the bidder's current gold. What happens: Set each bidder's bid; no one sees a bid until all are in
  7. [update] table. What happens: high_bid = max bid among non-active seats; high_count = number of non-active seats with bid == high_bid. If high_count == 1 and high_bid >= 1: winner_seat = that seat, sale_price = high_bid, winner's gold -= high_bid, active player's gold += high_bid. Otherwise: winner_seat = 0, sale_price = 0, append lot to discard.
  8. [update] the winner (when winner_seat > 0). What happens: Take: append lot to the winner's bought (public). Colour lot <c>-<v>: bought_<c> += v. Gold lot gold-<v>: winner's gold += v. Church lot: winner's church_pending = true.
  9. [tell] all players. What happens: Announce: 'Seat {winner_seat} bought {lot} for {sale_price} Gold.', or 'The lot {lot} was discarded.' when winner_seat == 0
  10. [poll] every player with church_pending == true (skipped if none) answers: one of: red+1, red-1, blue+1, blue-1, green+1, green-1. What happens: Set church_choice and reveal that the player played a Church card. Then apply every choice one after another: vp_<c> = min(5, max(1, vp_<c> ± 1)), so a colour may receive two changes.
  11. [tell] all players. What happens: Announce each church_choice made this round and the VP values: 'Red {vp_red}, Blue {vp_blue}, Green {vp_green}.'
  12. [update] table (end scoring, only when round == 12). What happens: For each colour c: each player's total_c = kept_c + bought_c; m_c = max total_c over players. If m_c > 0, each player with total_c == m_c adds vp_c / (number of players with total_c == m_c) to vp. Gold adds no VP. Reveal all hands.
  13. [check] table. What happens: If round == 12, end the game; otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, the deck holds 24 cards: Red, Blue and Green each 1,1,2,2,3,4, Gold 2,2,3,3, and 2 Church. Each player has 4 Gold, and the Red, Blue and Green VP values are each 3.
  R2. When round r begins, the active seat is ((r-1) mod player_count)+1, so round 1 is seat 1.
  R3. When a round begins, 2 cards are removed from the deck, and only the active player sees them.
  R4. When the active player keeps a colour card of value v, it goes into their private hand and adds v to their kept sum for that colour.
  R5. When the active player keeps a Gold card of value v, their gold increases by v immediately.
  R6. When the active player keeps a Church card, they play it at step 9 that round.
  R7. When a card is kept, the other drawn card becomes the public lot.
  R8. When the talk step runs, every player including the active player sends one message at once, and all messages are shown to everyone.
  R9. When bidding, every non-active player at once bids a whole number from 0 to their current gold, and the active player does not bid.
  R10. When exactly one player has the highest bid and it is at least 1, that player pays the bid from their gold to the active player's gold and takes the lot.
  R11. When the highest bid is tied or all bids are 0, nobody pays and the lot is discarded.
  R12. When a colour lot of value v is won, it is public in the winner's bought cards and adds v to their bought sum for that colour.
  R13. When a Gold lot of value v is won, the winner's gold increases by v.
  R14. When a Church lot is won, the winner plays it at step 9 that round.
  R15. When the auction resolves, the sale price, or that the lot was discarded, is announced.
  R16. When players gained a Church card this round, each chooses at once one colour and +1 or -1. All changes apply, each VP value is limited to 1-5, and a colour may receive two changes.
  R17. When a Church card is played, it and the chosen change are revealed, and the new VP values are announced.
  R18. When round 12 ends, the game ends and the deck is empty.
  R19. When scoring a colour, each player's total is their kept plus bought values in it, and the sole highest total gains that colour's VP value.
  R20. When several players tie for the highest total in a colour, they split its VP value equally, and fractions are allowed.
  R21. When every player has 0 in a colour, that colour scores for no one.
  R22. When scoring, Gold scores no VP.
  R23. When VP totals tie for first, the tied player with more leftover gold wins; if gold also ties, those players draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Keep: which drawn card to keep | asked: the active seat only | options: exactly the 2 cards in drawn
  - Talk: short message | asked: every seat, including the active seat | options: free short text
  - Bid | asked: every seat except the active seat | options: whole numbers from 0 to that seat's current gold; the active seat is not asked
  - Church: colour and direction | asked: only seats with church_pending == true this round | options: red+1, red-1, blue+1, blue-1, green+1, green-1; seats without a Church card this round are not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12 after the step 9 Church resolution and end scoring
  - each player's standing: you.vp * 1000 + you.gold (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Most VP wins. A tie on VP is broken by the most leftover Gold. Players still tied on both share the win, which is a draw.
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

- each player: `bought` (list, visible: public, starts []): Lots won at auction, face-up
- each player: `bought_red` (number, visible: public, starts 0): Sum of values of bought Red cards
- each player: `bought_blue` (number, visible: public, starts 0): Sum of values of bought Blue cards
- each player: `bought_green` (number, visible: public, starts 0): Sum of values of bought Green cards
- each player: `church_choice` (text, visible: public, starts ''): This round's Church play: a colour and +1 or -1
- each player: `vp` (number, visible: public, starts 0): Victory points, calculated at end scoring
- the table: `lot` (text, visible: public, starts ''): The card offered at auction this round
- the table: `vp_red` (number, visible: public, starts 3): Red VP value, 1-5
- the table: `vp_blue` (number, visible: public, starts 3): Blue VP value, 1-5
- the table: `vp_green` (number, visible: public, starts 3): Green VP value, 1-5
- the table: `round` (number, visible: public, starts 0): Current round number
- the table: `active_seat` (number, visible: public, starts 1): Seat of the active player: ((round-1) mod player_count)+1
- the table: `sale_price` (number, visible: public, starts 0): Price paid this round (0 if discarded)
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, colour_cards_per_colour = 6, colour_cards_value_1_per_colour = 2, colour_cards_value_2_per_colour = 2, colour_cards_value_3_per_colour = 1, colour_cards_value_4_per_colour = 1, gold_cards = 4, gold_cards_value_2 = 2, gold_cards_value_3 = 2, church_cards = 2, starting_gold = 4, vp_start = 3, vp_min = 1, vp_max = 5, rounds = 12, cards_drawn_per_round = 2, cards_kept_per_round = 1, min_bid = 0, min_winning_bid = 1, church_change = 1, rank_vp_multiplier = 1000
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

1) Draw: at round start, remove the first two entries of the deck list in order (deck[0], deck[1]) into `drawn`. Offer both, as named options such as 'red-1' and 'red-2', to the active seat only. Do not pick at random from the deck or re-shuffle after setup, because the rules say draw the TOP 2 of the already-shuffled deck. The other drawn card becomes `lot`.
2) Bid: run one simultaneous poll in which every non-active seat chooses from the whole numbers min_bid (0) up to that seat's current gold. With 4 gold the options are 0, 1, 2, 3 and 4. Do not ask the active seat. Store each choice in that player's `bid`.
3) Resolve from those bids: compute high_bid and how many seats bid it. If exactly one seat holds the high bid and it is at least min_winning_bid, move that amount from the winner's gold to the active seat's gold and set `sale_price` to it. Append the lot to the winner's `bought`, add its value to the matching bought_red, bought_blue or bought_green, and add a Gold lot's value to gold. Otherwise set `sale_price` to 0 and discard the lot.
4) Reset `bid` and `drawn` each round, keep all parameters as attributes, and check that a given deck or gold in a scenario is used as given.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "biblios_scriptorium",
    "name": "Biblios: Scriptorium",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Twelve rounds: draw two, keep one in secret, auction the other by sealed bid, and shift colour values with Church cards."
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
        "key": "kept_red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "kept_blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "kept_green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bought",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "bought_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bought_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bought_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "church_pending",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "church_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
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
        "initial": [
          "red-1",
          "red-1",
          "red-2",
          "red-2",
          "red-3",
          "red-4",
          "blue-1",
          "blue-1",
          "blue-2",
          "blue-2",
          "blue-3",
          "blue-4",
          "green-1",
          "green-1",
          "green-2",
          "green-2",
          "green-3",
          "green-4",
          "gold-2",
          "gold-2",
          "gold-3",
          "gold-3",
          "church",
          "church"
        ]
      },
      {
        "key": "drawn",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "lot",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "vp_red",
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
        "key": "vp_green",
        "visible": "public",
        "type": "number",
        "initial": 3
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
        "initial": 1
      },
      {
        "key": "high_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sale_price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "colour_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "colour_cards_value_1_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_cards_value_2_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "colour_cards_value_3_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "colour_cards_value_4_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "gold_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "gold_cards_value_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_cards_value_3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "church_cards",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "vp_start",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "vp_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "vp_max",
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
        "key": "cards_drawn_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "cards_kept_per_round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_winning_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "church_change",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_vp_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "shuffle and seat the table",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[pair[1] for pair in sorted([[uniform(0, 1), c] for c in deck])]"
            }
          }
        },
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
            "key": "bought",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "kept_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "kept_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "kept_green",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bought_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bought_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bought_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "vp_start"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "vp_start"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "vp_start"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
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
      "phase": "draw",
      "label": "a new round",
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
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "church_pending",
            "value": false
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
            "key": "winner_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "sale_price",
            "value": 0
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": 0
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
            "key": "drawn",
            "value": []
          }
        }
      ],
      "text": "Round {round} of {rounds}. Seat {active_seat} is the active player."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "draw the top two",
      "do": [
        {
          "set": {
            "key": "drawn",
            "value": {
              "calc": "[deck[0], deck[1]]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "drawn[0]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "drawn[1]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "keep",
      "label": "keep",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "drawn"
        }
      },
      "each": {
        "do": [
          {
            "append": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer",
              "if": {
                "calc": "$answer not in ['gold-2', 'gold-3']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "kept_red",
              "value": {
                "calc": "int($answer[-1])"
              },
              "if": {
                "calc": "$answer in ['red-1', 'red-2', 'red-3', 'red-4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "kept_blue",
              "value": {
                "calc": "int($answer[-1])"
              },
              "if": {
                "calc": "$answer in ['blue-1', 'blue-2', 'blue-3', 'blue-4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "kept_green",
              "value": {
                "calc": "int($answer[-1])"
              },
              "if": {
                "calc": "$answer in ['green-1', 'green-2', 'green-3', 'green-4']"
              }
            }
          },
          {
            "adjust": {
              "player": "$seat",
              "key": "gold",
              "value": {
                "calc": "int($answer[-1])"
              },
              "if": {
                "calc": "$answer in ['gold-2', 'gold-3']"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "church_pending",
              "value": true,
              "if": {
                "calc": "$answer == 'church'"
              }
            }
          },
          {
            "set": {
              "key": "lot",
              "value": {
                "calc": "drawn[1] if drawn[0] == $answer else drawn[0]"
              }
            }
          },
          {
            "set": {
              "key": "drawn",
              "value": []
            }
          }
        ]
      },
      "text": "You drew {drawn}. Keep one card in secret; the other goes up for auction. A kept colour card goes into your private hand, a kept Gold card adds its value to your Gold now, and a kept Church card is played after the auction."
    },
    {
      "use": "tell",
      "phase": "offer",
      "label": "the offer",
      "to": "all",
      "text": "The lot is {lot}."
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
      "text": "The lot is {lot}. Say one short thing to the table. Talk is not binding."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "to": {
        "where": "you.seat != active_seat and you.gold > min_bid"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Sealed bid for the lot {lot}: a whole number from {min_bid} up to your Gold. If yours is the single highest bid and at least {min_winning_bid}, you pay it to seat {active_seat} and take the lot. If the highest bid is tied or all bids are 0, nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the auction",
      "do": [
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players if p.seat != active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": {
              "calc": "count(p.seat != active_seat and p.bid == high_bid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat != active_seat and p.bid == high_bid]) if high_count == 1 and high_bid >= min_winning_bid else 0"
            }
          }
        },
        {
          "set": {
            "key": "sale_price",
            "value": {
              "calc": "high_bid if winner_seat > 0 else 0"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "gold",
            "value": {
              "calc": "-sale_price"
            },
            "if": {
              "calc": "winner_seat > 0 and players[winner_seat - 1].gold >= sale_price"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "gold",
            "value": {
              "calc": "sale_price"
            },
            "if": {
              "calc": "winner_seat > 0"
            }
          }
        },
        {
          "append": {
            "key": "discard",
            "value": {
              "calc": "lot"
            },
            "if": {
              "calc": "winner_seat == 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "take",
      "label": "the winner takes the lot",
      "when": {
        "calc": "winner_seat > 0"
      },
      "do": [
        {
          "append": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "bought",
            "value": {
              "calc": "lot"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "bought_red",
            "value": {
              "calc": "int(lot[-1])"
            },
            "if": {
              "calc": "lot in ['red-1', 'red-2', 'red-3', 'red-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "bought_blue",
            "value": {
              "calc": "int(lot[-1])"
            },
            "if": {
              "calc": "lot in ['blue-1', 'blue-2', 'blue-3', 'blue-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "bought_green",
            "value": {
              "calc": "int(lot[-1])"
            },
            "if": {
              "calc": "lot in ['green-1', 'green-2', 'green-3', 'green-4']"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "gold",
            "value": {
              "calc": "int(lot[-1])"
            },
            "if": {
              "calc": "lot in ['gold-2', 'gold-3']"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "church_pending",
            "value": true,
            "if": {
              "calc": "lot == 'church'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "sold",
      "when": {
        "calc": "winner_seat > 0"
      },
      "to": "all",
      "text": "Seat {winner_seat} bought {lot} for {sale_price} Gold."
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "discarded",
      "when": {
        "calc": "winner_seat == 0"
      },
      "to": "all",
      "text": "The lot {lot} was discarded. Nobody pays."
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "church",
      "to": {
        "where": "you.church_pending == True"
      },
      "answer": {
        "type": "choice",
        "options": [
          "red+1",
          "red-1",
          "blue+1",
          "blue-1",
          "green+1",
          "green-1"
        ]
      },
      "store": "church_choice",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays a Church card: {value}."
      },
      "text": "You gained a Church card this round. Choose one colour and +1 or -1 to its VP value (limited to {vp_min}-{vp_max})."
    },
    {
      "use": "update",
      "phase": "church",
      "label": "apply church changes",
      "when": {
        "calc": "any(p.church_choice != '' for p in players)"
      },
      "do": [
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_red + (church_change if players[0].church_choice == 'red+1' else -church_change)))"
            },
            "if": {
              "calc": "players[0].church_choice in ['red+1', 'red-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_blue + (church_change if players[0].church_choice == 'blue+1' else -church_change)))"
            },
            "if": {
              "calc": "players[0].church_choice in ['blue+1', 'blue-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_green + (church_change if players[0].church_choice == 'green+1' else -church_change)))"
            },
            "if": {
              "calc": "players[0].church_choice in ['green+1', 'green-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_red + (church_change if players[1].church_choice == 'red+1' else -church_change)))"
            },
            "if": {
              "calc": "players[1].church_choice in ['red+1', 'red-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_blue + (church_change if players[1].church_choice == 'blue+1' else -church_change)))"
            },
            "if": {
              "calc": "players[1].church_choice in ['blue+1', 'blue-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_green + (church_change if players[1].church_choice == 'green+1' else -church_change)))"
            },
            "if": {
              "calc": "players[1].church_choice in ['green+1', 'green-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_red + (church_change if players[2].church_choice == 'red+1' else -church_change)))"
            },
            "if": {
              "calc": "players[2].church_choice in ['red+1', 'red-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_blue + (church_change if players[2].church_choice == 'blue+1' else -church_change)))"
            },
            "if": {
              "calc": "players[2].church_choice in ['blue+1', 'blue-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_green + (church_change if players[2].church_choice == 'green+1' else -church_change)))"
            },
            "if": {
              "calc": "players[2].church_choice in ['green+1', 'green-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_red",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_red + (church_change if players[3].church_choice == 'red+1' else -church_change)))"
            },
            "if": {
              "calc": "len(players) >= 4 and players[3].church_choice in ['red+1', 'red-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_blue",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_blue + (church_change if players[3].church_choice == 'blue+1' else -church_change)))"
            },
            "if": {
              "calc": "len(players) >= 4 and players[3].church_choice in ['blue+1', 'blue-1']"
            }
          }
        },
        {
          "set": {
            "key": "vp_green",
            "value": {
              "calc": "max(vp_min, min(vp_max, vp_green + (church_change if players[3].church_choice == 'green+1' else -church_change)))"
            },
            "if": {
              "calc": "len(players) >= 4 and players[3].church_choice in ['green+1', 'green-1']"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "church",
      "label": "vp values",
      "to": "all",
      "text": "VP values now: Red {vp_red}, Blue {vp_blue}, Green {vp_green}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "end scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "key": "top_red",
            "value": {
              "calc": "max([p.kept_red + p.bought_red for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_blue",
            "value": {
              "calc": "max([p.kept_blue + p.bought_blue for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_green",
            "value": {
              "calc": "max([p.kept_green + p.bought_green for p in players])"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "vp",
            "value": {
              "calc": "vp_red / count(p.kept_red + p.bought_red == top_red for p in players) if top_red > 0 and you.kept_red + you.bought_red == top_red else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "vp",
            "value": {
              "calc": "vp_blue / count(p.kept_blue + p.bought_blue == top_blue for p in players) if top_blue > 0 and you.kept_blue + you.bought_blue == top_blue else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "vp",
            "value": {
              "calc": "vp_green / count(p.kept_green + p.bought_green == top_green for p in players) if top_green > 0 and you.kept_green + you.bought_green == top_green else 0"
            }
          }
        }
      ],
      "text": "Final scoring: Red {vp_red}, Blue {vp_blue}, Green {vp_green}."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after round twelve",
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
      "rank_by": "you.vp * rank_vp_multiplier + you.gold",
      "reveal": [
        "hand",
        "gold",
        "kept_red",
        "kept_blue",
        "kept_green"
      ],
      "text": "Winner: {result}. Final [seat, VP, Gold]: {[[p.seat, p.vp, p.gold] for p in players]}; colour values Red {vp_red}, Blue {vp_blue}, Green {vp_green}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "The deck has {deck_size} cards and its contents are public: Red, Blue and Green each 1, 1, 2, 2, 3, 4 ({colour_cards_per_colour} cards per colour); Gold 2, 2, 3, 3 ({gold_cards} cards); and {church_cards} Church cards. The deck is shuffled. Every player starts with {starting_gold} Gold, and each player's Gold is private. Each colour has a public VP value that starts at {vp_start}; a VP value can never go below {vp_min} or above {vp_max}. The game lasts exactly {rounds} rounds and the active player rotates by seat each round, starting with seat 1. The deck is exactly used up.\n\nEach round:\n1. Draw. The top {cards_drawn_per_round} cards are drawn. Only the active player sees them.\n2. Keep. The active player secretly keeps {cards_kept_per_round} card. A kept colour card goes face-down into their private hand and its value counts for that colour at the end. A kept Gold card adds its value to their private Gold immediately. A kept Church card is played at step 9. Nobody else learns what was kept, except that a Church card is revealed when it is played.\n3. Offer. The other card is revealed to everyone as the lot.\n4. Talk. Every player, including the active player, writes one short message at the same time; all messages are shown to everyone. Talk is not binding.\n5. Bid. Every non-active player at the same time submits a whole-number bid from {min_bid} up to their current Gold. The active player does not bid.\n6. Resolve. If one player made the single highest bid and it is at least {min_winning_bid}, that player pays the bid from their Gold to the active player's Gold and takes the lot. If the highest bid is tied, or all bids are 0, nobody pays and the lot is discarded.\n7. Take. The winner takes the lot face-up, so its colour and value are public. A Gold lot adds its value to the winner's Gold. A Church lot is played at step 9.\n8. Announce. The sale price, or that the lot was discarded, is announced.\n9. Church. Each player who gained a Church card this round, kept or bought, chooses at the same time one colour and either +{church_change} or -{church_change}. All changes apply, each limited to the range {vp_min}-{vp_max}; a colour may receive two changes. The Church plays and the new VP values are announced.\n10. End check. After round {rounds}, the game ends.\n\nEnd scoring: for each colour, each player sums the values of all their colour cards in that colour (kept and bought). The player with the highest sum gains that colour's current VP value. If several players tie for highest, they split the value equally (fractions allowed). A colour in which everyone has 0 scores for no one. Gold scores no VP.\n\nThe player with the most VP wins. If VP totals tie for first, the tied player with the most leftover Gold wins. If that also ties, the game is a draw and those players share the win."
}
```
````
