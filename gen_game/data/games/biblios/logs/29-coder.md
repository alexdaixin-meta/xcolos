# 29 coder

- time: 2026-10-27T21:21:43+00:00 (128.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1794aea09b5b4be1, reply sha256 e3983c71d1d0ed22

## Sent

````
# Task: write the XColos game file for "Biblios: Sealed Scriptorium (revised)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP.
The deck has 36 cards.
- There are 30 colour cards: for each of the five colours (Red, Blue, Green, Yellow, Purple), one card each of values 1, 1, 2, 2, 3 and 4.
- There are 6 Church cards.
Shuffle the deck once. Its order is hidden from everyone.

Each player starts with 8 gold. Each colour has a public die worth, starting at 4. A public worth can never go below 2 or above 8.

Every player has two collections:
- A hidden collection, seen only by its owner. It holds the colour cards and Church cards they kept, and their secret marks.
- A public collection, seen by all. It holds the colour cards they won.
Gold totals and public die worths are public. The worths shown during play never include secret marks.

ROUNDS.
There are 12 rounds. The active player is seat 1, 2, 3, 1, 2, 3 in rounds 1-6, and seat 3, 2, 1, 3, 2, 1 in rounds 7-12. Each round has these steps:

1. Announce the round number, the active player, all public die worths, all gold totals and all public collections.
2. Remove the top two cards of the deck. Show them privately to the active player only, as Card A (the top card) and Card B (the next card).
3. The active player privately chooses Keep A or Keep B.
4. The kept card goes into the active player's hidden collection. Nothing about it is announced. The other card is announced publicly as this round's lot.
5. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
6. Sealed bid: all three players, including the active player, at the same time bid a whole number of gold from 0 up to the gold they hold.
7. Reveal all bids. If the highest bid is at least 1 and no other player bid the same amount, that player wins the lot and pays their bid to the bank (the gold leaves the game). Otherwise nobody pays and the lot is discarded face-up.
8. A won colour card goes into the winner's public collection.
9. Church and secret mark, answered at the same time:
   (a) The active player always privately names one colour and a direction (+1 or -1). This is recorded secretly in their hidden collection as this round's mark. It counts at scoring only if the card they kept this round is a Church card. Otherwise it is void. This question is asked every round, so being asked reveals nothing.
   (b) If the lot was a Church card and someone won it, the winner publicly names one colour and a direction (+1 or -1).
   If the active player is also the winner, they answer both parts.
10. If part (b) was answered, change that colour's public worth by the named direction. If this would take it below 2 or above 8, it has no effect. The won Church card is then discarded face-up. Secret marks change nothing now.
11. Every player gains 1 gold.
12. If this was round 12, go to scoring. Otherwise begin the next round.

SCORING.
1. Final worths. Start from each colour's public worth. Reveal all hidden collections. Take every mark that counts (made in a round where that player kept a Church card) and apply them one at a time in round order, earliest round first. Each mark changes its colour's worth by 1 in its direction, checked against the worth as already changed by earlier marks. A mark that would take a worth below 2 or above 8 has no effect.
2. Majorities. For each colour, add up the values of each player's cards of that colour, hidden and public together.
   - If one player has the strictly highest total and it is at least 1, they score VP equal to that colour's final worth.
   - If two or more players tie for the highest total (at least 1), each of them scores half the final worth, rounded down.
   - If no one has a card of that colour, nobody scores it.
   Church cards have no value at scoring.
3. Gold. Each player scores 1 VP for every full 5 gold they hold.

How the winner is decided: The player with the most VP after scoring wins. If two or more players tie for the most VP, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Biblios: Sealed Scriptorium (revised) (3 to 3 players, best with 3)

Three scribes each round secretly keep one of two cards, then sealed-bid for the other, while public Church cards and secret marks shift the worth of five colours that score by majority.

STATE (every item below must exist in the file):
  - each player: gold (number, starts 8); everyone sees it. Gold held. Bids are paid from it, it gains 1 each round, and 1 VP is scored for every full 5 at the end.
  - each player: hidden_cards (list, starts []); only its owner sees it. Hidden collection: the cards this player kept as active player (colour cards such as 'Red 3', or 'Church'). It is revealed to all at scoring.
  - each player: public_cards (list, starts []); everyone sees it. Public collection: the colour cards won at auction.
  - each player: marks (list, starts []); only its owner sees it. Secret marks, part of the hidden collection. There is one entry per round in which this player was active, recorded as 'round:colour:direction:counts', where counts is yes if the card kept that round was Church.
  - each player: offer_a (text, starts ''); only its owner sees it. Card A (the top card) shown privately to this player while active.
  - each player: offer_b (text, starts ''); only its owner sees it. Card B (the next card) shown privately to this player while active.
  - each player: kept_card (text, starts ''); only its owner sees it. The card this player kept in the current round as active player.
  - each player: message (text, starts ''); everyone sees it. This round's non-binding talk message.
  - each player: bid (number, starts 0); everyone sees it. This round's sealed bid. It is revealed only after all bids are in.
  - each player: total_red (number, starts 0); everyone sees it. Sum of Red card values in the hidden and public collections, computed at scoring.
  - each player: total_blue (number, starts 0); everyone sees it. Sum of Blue card values, computed at scoring.
  - each player: total_green (number, starts 0); everyone sees it. Sum of Green card values, computed at scoring.
  - each player: total_yellow (number, starts 0); everyone sees it. Sum of Yellow card values, computed at scoring.
  - each player: total_purple (number, starts 0); everyone sees it. Sum of Purple card values, computed at scoring.
  - each player: vp (number, starts 0); everyone sees it. Victory points, computed at scoring.
  - the table: deck (list, starts ['Red 1', 'Red 1', 'Red 2', 'Red 2', 'Red 3', 'Red 4', 'Blue 1', 'Blue 1', 'Blue 2', 'Blue 2', 'Blue 3', 'Blue 4', 'Green 1', 'Green 1', 'Green 2', 'Green 2', 'Green 3', 'Green 4', 'Yellow 1', 'Yellow 1', 'Yellow 2', 'Yellow 2', 'Yellow 3', 'Yellow 4', 'Purple 1', 'Purple 1', 'Purple 2', 'Purple 2', 'Purple 3', 'Purple 4', 'Church', 'Church', 'Church', 'Church', 'Church', 'Church']); hidden from all players. The draw pile, shuffled once at setup. Index 0 is the top card.
  - the table: round (number, starts 0); everyone sees it. The current round number, from 1 to 12.
  - the table: active_seat (number, starts 0); everyone sees it. The seat of this round's active player.
  - the table: worth_red (number, starts 4); everyone sees it. Red public die worth, from 2 to 8.
  - the table: worth_blue (number, starts 4); everyone sees it. Blue public die worth, from 2 to 8.
  - the table: worth_green (number, starts 4); everyone sees it. Green public die worth, from 2 to 8.
  - the table: worth_yellow (number, starts 4); everyone sees it. Yellow public die worth, from 2 to 8.
  - the table: worth_purple (number, starts 4); everyone sees it. Purple public die worth, from 2 to 8.
  - the table: lot (text, starts ''); everyone sees it. The card put up for auction this round.
  - the table: discard (list, starts []); everyone sees it. Face-up discards: unwon lots and won Church cards.
  - the table: high_bid (number, starts 0); everyone sees it. The highest bid this round.
  - the table: high_count (number, starts 0); everyone sees it. How many players bid the highest amount this round.
  - the table: winner_seat (number, starts 0); everyone sees it. The seat that won this round's lot, or 0 if nobody won it.
  - the table: final_worth_red (number, starts 4); everyone sees it. Red worth after the counting marks are applied at scoring.
  - the table: final_worth_blue (number, starts 4); everyone sees it. Blue final worth.
  - the table: final_worth_green (number, starts 4); everyone sees it. Green final worth.
  - the table: final_worth_yellow (number, starts 4); everyone sees it. Yellow final worth.
  - the table: final_worth_purple (number, starts 4); everyone sees it. Purple final worth.
  - parameters, each kept as a table attribute: deck_size = 36, colour_cards = 30, church_cards = 6, colours = 5, cards_per_colour = 6, value_1_cards_per_colour = 2, value_2_cards_per_colour = 2, value_3_cards_per_colour = 1, value_4_cards_per_colour = 1, starting_gold = 8, starting_worth = 4, worth_min = 2, worth_max = 8, rounds = 12, cards_revealed_to_active = 2, bid_min = 0, min_winning_bid = 1, gold_income_per_round = 1, mark_step = 1, church_step = 1, tie_share_divisor = 2, gold_per_vp = 5, min_majority_total = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck list of 36 cards: for each of Red, Blue, Green, Yellow and Purple, the cards '<Colour> 1', '<Colour> 1', '<Colour> 2', '<Colour> 2', '<Colour> 3' and '<Colour> 4', plus six 'Church' cards.
  2. Shuffle the deck once into a random order. Its order is hidden from everyone (visibility none).
  3. Set every player's gold to 8, set hidden_cards, public_cards and marks to empty, and set vp to 0.
  4. Set worth_red, worth_blue, worth_green, worth_yellow and worth_purple to 4, round to 0 and discard to empty.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. If round <= 6, active_seat = ((round - 1) mod 3) + 1; otherwise active_seat = 3 - ((round - 7) mod 3). This gives seats 1,2,3,1,2,3,3,2,1,3,2,1. Reset winner_seat = 0, high_bid = 0, high_count = 0 and every bid = 0.
  2. [tell] all players. What happens: Announce round, active_seat, worth_red, worth_blue, worth_green, worth_yellow, worth_purple, every player's gold and every player's public_cards.
  3. [update] seat {active_seat}. What happens: Set the active player's offer_a = deck[0] and offer_b = deck[1]. Remove both from deck. Nothing is announced.
  4. [sync] seat {active_seat}. What happens: The active player privately sees offer_a as Card A and offer_b as Card B.
  5. [ask] seat {active_seat} answers: choice: Keep A | Keep B. What happens: The answer is private. If Keep A, kept_card = offer_a and lot = offer_b; if Keep B, kept_card = offer_b and lot = offer_a. Append kept_card to the active player's hidden_cards.
  6. [tell] all players. What happens: Announce publicly: 'This round's lot is {lot}.' Nothing about the kept card is announced.
  7. [poll] all players answers: short text. What happens: message = the answer. Once all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding.
  8. [poll] all players answers: whole number from 0 to you.gold. What happens: bid = the answer. No bid is seen until all three are in.
  9. [update] all players. What happens: Reveal every bid publicly. high_bid = max of bid over players; high_count = number of players with bid == high_bid. If high_bid >= 1 and high_count == 1, then winner_seat = the seat with that bid, and that player's gold -= high_bid (paid to the bank and removed from the game). Otherwise winner_seat = 0, nobody pays, and lot is appended to discard (face-up).
  10. [update] seat {winner_seat}. What happens: when winner_seat != 0 and lot != 'Church': append lot to the winner's public_cards.
  11. [poll] seat {active_seat}; also seat {winner_seat} when winner_seat != 0 and lot == 'Church' answers: (a) for the active seat, privately: a choice of colour and direction from Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1; (b) for the Church winner, publicly: the same ten options. A seat that is both answers both questions.. What happens: (a) Append 'round:colour:direction:counts' to the active player's marks, where counts = yes if kept_card == 'Church', otherwise no. This changes no worth now. (b) The answer is recorded for the next step and announced publicly.
  12. [update] all players. What happens: when winner_seat != 0 and lot == 'Church': for the named colour, if worth + direction is between 2 and 8 inclusive, then worth_<colour> += direction; otherwise no change. Append the Church card to discard (face-up). Announce the new worth.
  13. [update] all players. What happens: Every player's gold += 1.
  14. [update] all players. What happens: when round == 12: reveal every player's hidden_cards and marks to all. Set each final_worth_<colour> = worth_<colour>. Then take every mark with counts = yes, from all players, sorted by round ascending, and apply them one at a time: if final_worth_<colour> + direction is between 2 and 8 inclusive, final_worth_<colour> += direction; otherwise the mark has no effect. Each mark is checked against the worth as already changed by earlier marks.
  15. [update] all players. What happens: when round == 12: for each player and each colour, total_<colour> = sum of the numeric values of that colour's cards in hidden_cards and public_cards together. Church cards count 0.
  16. [update] all players. What happens: when round == 12: for each colour, M = max of total_<colour> over players and K = number of players with total_<colour> == M. If M >= 1 and K == 1, that player's vp += final_worth_<colour>. If M >= 1 and K >= 2, each tied player's vp += floor(final_worth_<colour> / 2). If M == 0, nobody scores the colour. Then every player's vp += floor(gold / 5). Announce every player's final worths, totals and vp.
  17. [check] all players. What happens: If round == 12, end the game; otherwise begin the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup the deck holds 36 cards: for each of 5 colours, values 1,1,2,2,3,4 (30 colour cards), plus 6 Church cards. It is shuffled once and hidden from everyone.
  R2. At setup every player has 8 gold and every colour's public worth is 4.
  R3. The game lasts exactly 12 rounds.
  R4. The active seat in rounds 1 to 12 is 1, 2, 3, 1, 2, 3, 3, 2, 1, 3, 2, 1.
  R5. At the start of each round, the round number, active seat, all five public worths, all gold totals and all public collections are announced.
  R6. Each round the top two deck cards are removed from the deck and shown only to the active player, as Card A (top) and Card B (next).
  R7. When the active player chooses Keep A, Card A goes to their hidden collection and Card B becomes the publicly announced lot; Keep B does the reverse.
  R8. The identity of the kept card is never announced during play.
  R9. Each round every player writes one short message simultaneously, and all messages are then shown to everyone; they bind no one.
  R10. Each round all three players, including the active player, bid simultaneously a whole number from 0 to their current gold.
  R11. When the highest bid is at least 1 and no other player bid that amount, that player wins the lot and loses gold equal to their bid, which leaves the game.
  R12. When the highest bid is 0, or two or more players tie for the highest bid, nobody pays and the lot is discarded face-up.
  R13. When the won lot is a colour card, it goes into the winner's public collection.
  R14. Every round the active player privately names one colour and a direction (+1 or -1), which is recorded secretly in their marks.
  R15. A mark counts at scoring only if the card the active player kept that round is a Church card; otherwise it is void.
  R16. When a Church lot is won, the winner publicly names a colour and a direction (+1 or -1), and that colour's public worth changes by 1 in that direction.
  R17. When a public worth change would take a worth below 2 or above 8, it has no effect.
  R18. A won Church card is discarded face-up after its effect, and an unwon Church lot changes no worth.
  R19. When the active player also wins a Church lot, they answer both the secret mark and the public Church question.
  R20. Secret marks change no public worth during play.
  R21. At the end of every round each player gains 1 gold.
  R22. At scoring, all hidden collections are revealed, and counting marks are applied to the public worths one at a time in round order, earliest first, each by 1 in its direction; any mark that would go below 2 or above 8 has no effect.
  R23. At scoring, each player's colour total is the sum of that colour's card values in their hidden and public collections; Church cards count 0.
  R24. When one player has the strictly highest total of a colour and it is at least 1, they score VP equal to that colour's final worth.
  R25. When two or more players tie for the highest total of a colour (at least 1), each scores floor(final worth / 2) VP.
  R26. When no player has a card of a colour, nobody scores that colour.
  R27. At scoring each player gains floor(gold / 5) VP.
  R28. After scoring in round 12 the game ends, and the player with the most VP wins; players tied for most VP share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Keep a card | asked: the active seat only | options: Keep A, Keep B
  - Talk message | asked: every seat | options: a short free-text message
  - Sealed bid | asked: every seat | options: a whole number from 0 to that seat's current gold
  - Secret mark (part a) | asked: the active seat, every round | options: Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1
  - Church effect (part b) | asked: the seat that won a Church lot, only in a round where a Church lot was won | options: Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1, Yellow +1, Yellow -1, Purple +1, Purple -1; any other seat is not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 12
  - each player's standing: you.vp (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their VP after scoring: colour majorities at final worths plus 1 VP per full 5 gold. The highest VP wins; players tied at the top share the result (the source calls this a draw).
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

- each player: `gold` (number, visible: public, starts 8): Gold held. Bids are paid from it, it gains 1 each round, and 1 VP is scored for every full 5 at the end.
- each player: `public_cards` (list, visible: public, starts []): Public collection: the colour cards won at auction.
- each player: `vp` (number, visible: public, starts 0): Victory points, computed at scoring.
- the table: `round` (number, visible: public, starts 0): The current round number, from 1 to 12.
- the table: `active_seat` (number, visible: public, starts 0): The seat of this round's active player.
- the table: `worth_red` (number, visible: public, starts 4): Red public die worth, from 2 to 8.
- the table: `worth_blue` (number, visible: public, starts 4): Blue public die worth, from 2 to 8.
- the table: `worth_green` (number, visible: public, starts 4): Green public die worth, from 2 to 8.
- the table: `worth_yellow` (number, visible: public, starts 4): Yellow public die worth, from 2 to 8.
- the table: `worth_purple` (number, visible: public, starts 4): Purple public die worth, from 2 to 8.
- the table: `lot` (text, visible: public, starts ''): The card put up for auction this round.
- the table: `winner_seat` (number, visible: public, starts 0): The seat that won this round's lot, or 0 if nobody won it.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, colour_cards = 30, church_cards = 6, colours = 5, cards_per_colour = 6, value_1_cards_per_colour = 2, value_2_cards_per_colour = 2, value_3_cards_per_colour = 1, value_4_cards_per_colour = 1, starting_gold = 8, starting_worth = 4, worth_min = 2, worth_max = 8, rounds = 12, cards_revealed_to_active = 2, bid_min = 0, min_winning_bid = 1, gold_income_per_round = 1, mark_step = 1, church_step = 1, tie_share_divisor = 2, gold_per_vp = 5, min_majority_total = 1
- the game ends with ONE ending whose `rank_by` is `you.vp`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "biblios_sealed_scriptorium_revised",
    "name": "Biblios: Sealed Scriptorium (revised)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three scribes secretly keep one of two cards, sealed-bid for the other, and shift five colour worths with public Church cards and secret marks."
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
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hidden_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "public_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "marks",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer_a",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer_b",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kept_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_purple",
        "visible": "public",
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
        "initial": [
          "Red 1",
          "Red 1",
          "Red 2",
          "Red 2",
          "Red 3",
          "Red 4",
          "Blue 1",
          "Blue 1",
          "Blue 2",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Green 1",
          "Green 1",
          "Green 2",
          "Green 2",
          "Green 3",
          "Green 4",
          "Yellow 1",
          "Yellow 1",
          "Yellow 2",
          "Yellow 2",
          "Yellow 3",
          "Yellow 4",
          "Purple 1",
          "Purple 1",
          "Purple 2",
          "Purple 2",
          "Purple 3",
          "Purple 4",
          "Church",
          "Church",
          "Church",
          "Church",
          "Church",
          "Church"
        ]
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
        "key": "worth_red",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_blue",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_green",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_yellow",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_purple",
        "visible": "public",
        "type": "number",
        "initial": 4
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
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_count",
        "visible": "public",
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
        "key": "final_worth_red",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_blue",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_green",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_yellow",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_purple",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "church_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "church_dir",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mark_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "mark_dir",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "mark_counts",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "counting_marks",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "mark_idx",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_dir",
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
        "key": "colour_cards",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "church_cards",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "value_1_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_3_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_4_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "starting_worth",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "worth_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_revealed_to_active",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bid_min",
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
        "key": "gold_income_per_round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "mark_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "church_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tie_share_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_per_vp",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "min_majority_total",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "Red 1",
              "Red 1",
              "Red 2",
              "Red 2",
              "Red 3",
              "Red 4",
              "Blue 1",
              "Blue 1",
              "Blue 2",
              "Blue 2",
              "Blue 3",
              "Blue 4",
              "Green 1",
              "Green 1",
              "Green 2",
              "Green 2",
              "Green 3",
              "Green 4",
              "Yellow 1",
              "Yellow 1",
              "Yellow 2",
              "Yellow 2",
              "Yellow 3",
              "Yellow 4",
              "Purple 1",
              "Purple 1",
              "Purple 2",
              "Purple 2",
              "Purple 3",
              "Purple 4",
              "Church",
              "Church",
              "Church",
              "Church",
              "Church",
              "Church"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), c] for c in deck])]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the scribes",
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
            "key": "hidden_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "public_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "marks",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "vp",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table",
      "do": [
        {
          "set": {
            "key": "worth_red",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_blue",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_green",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_yellow",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_purple",
            "value": {
              "calc": "starting_worth"
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
            "key": "discard",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your start",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "new round",
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
              "calc": "((round - 1) % len(players)) + 1 if round * 2 <= rounds else len(players) - ((round - 1 - int(rounds / 2)) % len(players))"
            }
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
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "kept_card",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "round announcement",
      "to": "all",
      "text": "Round {round} of {rounds}: seat {active_seat} is active. Public worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}, Yellow {worth_yellow}, Purple {worth_purple}. Gold: seat 1 {players[0].gold}, seat 2 {players[1].gold}, seat 3 {players[2].gold}. Public collections: seat 1 {players[0].public_cards}, seat 2 {players[1].public_cards}, seat 3 {players[2].public_cards}."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "draw two cards",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer_a",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer_b",
            "value": {
              "calc": "deck[1]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "deck[0]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "draw",
      "label": "show the cards",
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "fields": [
        "offer_a",
        "offer_b"
      ],
      "text": "Your two cards, seen only by you: Card A (offer_a, the top card) and Card B (offer_b, the next card)."
    },
    {
      "use": "ask",
      "phase": "draw",
      "label": "keep a card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Keep A",
          "Keep B"
        ]
      },
      "verify": {
        "bind": "keep"
      },
      "text": "You were just shown Card A (offer_a) and Card B (offer_b) privately. Keep one secretly in your hidden collection; the other becomes this round's lot for auction."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the kept card",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "kept_card",
            "value": {
              "calc": "you.offer_a if $keep == 'Keep A' else you.offer_b"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "[p.offer_b if $keep == 'Keep A' else p.offer_a for p in players if p.seat == active_seat][0]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "hidden_cards",
            "value": {
              "calc": "you.kept_card"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "auction",
      "label": "the lot",
      "to": "all",
      "text": "This round's lot is {lot}."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table about the lot {lot}. Everyone writes at once; messages are shown afterwards and bind no one."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "sealed bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Sealed bid for the lot {lot}: a whole number of gold from {bid_min} up to the gold you hold. A unique highest bid of at least {min_winning_bid} wins and pays; otherwise nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "reveal bids",
      "do": [
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": {
              "calc": "count(p.bid == high_bid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[p.seat for p in players if p.bid == high_bid][0] if high_bid >= min_winning_bid and high_count == 1 else 0"
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
              "calc": "-high_bid"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} wins {lot} and pays {high_bid} gold to the bank."
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
            },
            "text": "Nobody wins the lot; {lot} is discarded face-up and nobody pays."
          }
        }
      ],
      "text": "Bids: seat 1 {players[0].bid}, seat 2 {players[1].bid}, seat 3 {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "won colour card",
      "when": {
        "calc": "winner_seat != 0 and lot != 'Church'"
      },
      "do": [
        {
          "append": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "public_cards",
            "value": {
              "calc": "lot"
            },
            "text": "{lot} goes into seat {player}'s public collection."
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "secret mark",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Red +1",
          "Red -1",
          "Blue +1",
          "Blue -1",
          "Green +1",
          "Green -1",
          "Yellow +1",
          "Yellow -1",
          "Purple +1",
          "Purple -1"
        ]
      },
      "verify": {
        "bind": "mark"
      },
      "text": "Secretly name a colour and a direction as this round's mark. It counts at scoring only if the card you kept this round is a Church card; otherwise it is void. It changes nothing now."
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "church effect",
      "when": {
        "calc": "winner_seat != 0 and lot == 'Church'"
      },
      "to": {
        "where": "you.seat == winner_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Red +1",
          "Red -1",
          "Blue +1",
          "Blue -1",
          "Green +1",
          "Green -1",
          "Yellow +1",
          "Yellow -1",
          "Purple +1",
          "Purple -1"
        ]
      },
      "verify": {
        "bind": "church"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} uses the Church card: {value}."
      },
      "text": "You won the Church card. Publicly name a colour and a direction: that colour's public worth moves by {church_step}, unless it would go below {worth_min} or above {worth_max}."
    },
    {
      "use": "update",
      "phase": "church",
      "label": "apply church",
      "when": {
        "calc": "winner_seat != 0 and lot == 'Church'"
      },
      "do": [
        {
          "set": {
            "key": "church_colour",
            "value": {
              "calc": "[c for c in ['Red', 'Blue', 'Green', 'Yellow', 'Purple'] if c in $church][0]"
            }
          }
        },
        {
          "set": {
            "key": "church_dir",
            "value": {
              "calc": "church_step if '+1' in $church else -church_step"
            }
          }
        },
        {
          "set": {
            "key": "worth_red",
            "value": {
              "calc": "worth_red + church_dir if church_colour == 'Red' and worth_red + church_dir >= worth_min and worth_red + church_dir <= worth_max else worth_red"
            }
          }
        },
        {
          "set": {
            "key": "worth_blue",
            "value": {
              "calc": "worth_blue + church_dir if church_colour == 'Blue' and worth_blue + church_dir >= worth_min and worth_blue + church_dir <= worth_max else worth_blue"
            }
          }
        },
        {
          "set": {
            "key": "worth_green",
            "value": {
              "calc": "worth_green + church_dir if church_colour == 'Green' and worth_green + church_dir >= worth_min and worth_green + church_dir <= worth_max else worth_green"
            }
          }
        },
        {
          "set": {
            "key": "worth_yellow",
            "value": {
              "calc": "worth_yellow + church_dir if church_colour == 'Yellow' and worth_yellow + church_dir >= worth_min and worth_yellow + church_dir <= worth_max else worth_yellow"
            }
          }
        },
        {
          "set": {
            "key": "worth_purple",
            "value": {
              "calc": "worth_purple + church_dir if church_colour == 'Purple' and worth_purple + church_dir >= worth_min and worth_purple + church_dir <= worth_ma
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (kept_card, message, offer_a, offer_b) in `your_start`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "biblios_sealed_scriptorium_revised",
    "name": "Biblios: Sealed Scriptorium (revised)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three scribes secretly keep one of two cards, sealed-bid for the other, and shift five colour worths with public Church cards and secret marks."
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
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hidden_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "public_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "marks",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer_a",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer_b",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kept_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_purple",
        "visible": "public",
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
        "initial": [
          "Red 1",
          "Red 1",
          "Red 2",
          "Red 2",
          "Red 3",
          "Red 4",
          "Blue 1",
          "Blue 1",
          "Blue 2",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Green 1",
          "Green 1",
          "Green 2",
          "Green 2",
          "Green 3",
          "Green 4",
          "Yellow 1",
          "Yellow 1",
          "Yellow 2",
          "Yellow 2",
          "Yellow 3",
          "Yellow 4",
          "Purple 1",
          "Purple 1",
          "Purple 2",
          "Purple 2",
          "Purple 3",
          "Purple 4",
          "Church",
          "Church",
          "Church",
          "Church",
          "Church",
          "Church"
        ]
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
        "key": "worth_red",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_blue",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_green",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_yellow",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_purple",
        "visible": "public",
        "type": "number",
        "initial": 4
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
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_count",
        "visible": "public",
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
        "key": "final_worth_red",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_blue",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_green",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_yellow",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "final_worth_purple",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "church_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "church_dir",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "mark_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "mark_dir",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "mark_counts",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "counting_marks",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "mark_idx",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cur_dir",
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
        "key": "colour_cards",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "church_cards",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "value_1_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_3_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_4_cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_gold",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "starting_worth",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "worth_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "worth_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "cards_revealed_to_active",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bid_min",
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
        "key": "gold_income_per_round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "mark_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "church_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tie_share_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "gold_per_vp",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "min_majority_total",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "Red 1",
              "Red 1",
              "Red 2",
              "Red 2",
              "Red 3",
              "Red 4",
              "Blue 1",
              "Blue 1",
              "Blue 2",
              "Blue 2",
              "Blue 3",
              "Blue 4",
              "Green 1",
              "Green 1",
              "Green 2",
              "Green 2",
              "Green 3",
              "Green 4",
              "Yellow 1",
              "Yellow 1",
              "Yellow 2",
              "Yellow 2",
              "Yellow 3",
              "Yellow 4",
              "Purple 1",
              "Purple 1",
              "Purple 2",
              "Purple 2",
              "Purple 3",
              "Purple 4",
              "Church",
              "Church",
              "Church",
              "Church",
              "Church",
              "Church"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), c] for c in deck])]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the scribes",
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
            "key": "hidden_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "public_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "marks",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "vp",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table",
      "do": [
        {
          "set": {
            "key": "worth_red",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_blue",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_green",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_yellow",
            "value": {
              "calc": "starting_worth"
            }
          }
        },
        {
          "set": {
            "key": "worth_purple",
            "value": {
              "calc": "starting_worth"
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
            "key": "discard",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your start",
      "mode": "self",
      "to": "all",
      "fields": [
        "gold",
        "hidden_cards",
        "public_cards",
        "marks",
        "vp"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "new round",
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
              "calc": "((round - 1) % len(players)) + 1 if round * 2 <= rounds else len(players) - ((round - 1 - int(rounds / 2)) % len(players))"
            }
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
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "kept_card",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "round announcement",
      "to": "all",
      "text": "Round {round} of {rounds}: seat {active_seat} is active. Public worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}, Yellow {worth_yellow}, Purple {worth_purple}. Gold: seat 1 {players[0].gold}, seat 2 {players[1].gold}, seat 3 {players[2].gold}. Public collections: seat 1 {players[0].public_cards}, seat 2 {players[1].public_cards}, seat 3 {players[2].public_cards}."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "draw two cards",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer_a",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer_b",
            "value": {
              "calc": "deck[1]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "deck[0]"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "deck[0]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "draw",
      "label": "show the cards",
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "fields": [
        "offer_a",
        "offer_b"
      ],
      "text": "Your two cards, seen only by you: Card A (offer_a, the top card) and Card B (offer_b, the next card)."
    },
    {
      "use": "ask",
      "phase": "draw",
      "label": "keep a card",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Keep A",
          "Keep B"
        ]
      },
      "verify": {
        "bind": "keep"
      },
      "text": "You were just shown Card A (offer_a) and Card B (offer_b) privately. Keep one secretly in your hidden collection; the other becomes this round's lot for auction."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the kept card",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "kept_card",
            "value": {
              "calc": "you.offer_a if $keep == 'Keep A' else you.offer_b"
            }
          }
        },
        {
          "set": {
            "key": "lot",
            "value": {
              "calc": "[p.offer_b if $keep == 'Keep A' else p.offer_a for p in players if p.seat == active_seat][0]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "hidden_cards",
            "value": {
              "calc": "you.kept_card"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "auction",
      "label": "the lot",
      "to": "all",
      "text": "This round's lot is {lot}."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table about the lot {lot}. Everyone writes at once; messages are shown afterwards and bind no one."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "sealed bid",
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_min"
        },
        "max": {
          "calc": "you.gold"
        }
      },
      "store": "bid",
      "text": "Sealed bid for the lot {lot}: a whole number of gold from {bid_min} up to the gold you hold. A unique highest bid of at least {min_winning_bid} wins and pays; otherwise nobody pays and the lot is discarded."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "reveal bids",
      "do": [
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "high_count",
            "value": {
              "calc": "count(p.bid == high_bid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[p.seat for p in players if p.bid == high_bid][0] if high_bid >= min_winning_bid and high_count == 1 else 0"
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
              "calc": "-high_bid"
            },
            "if": {
              "calc": "winner_seat > 0"
            },
            "text": "Seat {player} wins {lot} and pays {high_bid} gold to the bank."
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
            },
            "text": "Nobody wins the lot; {lot} is discarded face-up and nobody pays."
          }
        }
      ],
      "text": "Bids: seat 1 {players[0].bid}, seat 2 {players[1].bid}, seat 3 {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "won colour card",
      "when": {
        "calc": "winner_seat != 0 and lot != 'Church'"
      },
      "do": [
        {
          "append": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "public_cards",
            "value": {
              "calc": "lot"
            },
            "text": "{lot} goes into seat {player}'s public collection."
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "secret mark",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Red +1",
          "Red -1",
          "Blue +1",
          "Blue -1",
          "Green +1",
          "Green -1",
          "Yellow +1",
          "Yellow -1",
          "Purple +1",
          "Purple -1"
        ]
      },
      "verify": {
        "bind": "mark"
      },
      "text": "Secretly name a colour and a direction as this round's mark. It counts at scoring only if the card you kept this round is a Church card; otherwise it is void. It changes nothing now."
    },
    {
      "use": "poll",
      "phase": "church",
      "label": "church effect",
      "when": {
        "calc": "winner_seat != 0 and lot == 'Church'"
      },
      "to": {
        "where": "you.seat == winner_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Red +1",
          "Red -1",
          "Blue +1",
          "Blue -1",
          "Green +1",
          "Green -1",
          "Yellow +1",
          "Yellow -1",
          "Purple +1",
          "Purple -1"
        ]
      },
      "verify": {
        "bind": "church"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} uses the Church card: {value}."
      },
      "text": "You won the Church card. Publicly name a colour and a direction: that colour's public worth moves by {church_step}, unless it would go below {worth_min} or above {worth_max}."
    },
    {
      "use": "update",
      "phase": "church",
      "label": "apply church",
      "when": {
        "calc": "winner_seat != 0 and lot == 'Church'"
      },
      "do": [
        {
          "set": {
            "key": "church_colour",
            "value": {
              "calc": "[c for c in ['Red', 'Blue', 'Green', 'Yellow', 'Purple'] if c in $church][0]"
            }
          }
        },
        {
          "set": {
            "key": "church_dir",
            "value": {
              "calc": "church_step if '+1' in $church else -church_step"
            }
          }
        },
        {
          "set": {
            "key": "worth_red",
            "value": {
              "calc": "worth_red + church_dir if church_colour == 'Red' and worth_red + church_dir >= worth_min and worth_red + church_dir <= worth_max else worth_red"
            }
          }
        },
        {
          "set": {
            "key": "worth_blue",
            "value": {
              "calc": "worth_blue + church_dir if church_colour == 'Blue' and worth_blue + church_dir >= worth_min and worth_blue + church_dir <= worth_max else worth_blue"
            }
          }
        },
        {
          "set": {
            "key": "worth_green",
            "value": {
              "calc": "worth_green + church_dir if church_colour == 'Green' and worth_green + church_dir >= worth_min and worth_green + church_dir <= worth_max else worth_green"
            }
          }
        },
        {
          "set": {
            "key": "worth_yellow",
            "value": {
              "calc": "worth_yellow + church_dir if church_colour == 'Yellow' and worth_yellow + church_dir >= worth_min and worth_yellow + church_dir <= worth_max else worth_yellow"
            }
          }
        },
        {
          "set": {
            "key": "worth_purple",
            "value": {
              "calc": "worth_purple + church_dir if church_colour == 'Purple' and worth_purple + church_dir >= worth_min and worth_purple + church_dir <= worth_max else worth_purple"
            }
          }
        },
        {
          "append": {
            "key": "discard",
            "value": "Church"
          }
        }
      ],
      "text": "The Church card is discarded face-up. Public worths now: Red {worth_red}, Blue {worth_blue}, Green {worth_green}, Yellow {worth_yellow}, Purple {worth_purple}."
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "record mark and income",
      "do": [
        {
          "set": {
            "key": "mark_colour",
            "value": {
              "calc": "[c for c in ['Red', 'Blue', 'Green', 'Yellow', 'Purple'] if c in $mark][0]"
            }
          }
        },
        {
          "set": {
            "key": "mark_dir",
            "value": {
              "calc": "'+1' if '+1' in $mark else '-1'"
            }
          }
        },
        {
          "set": {
            "key": "mark_counts",
            "value": {
              "calc": "'yes' if [p.kept_card for p in players if p.seat == active_seat][0] == 'Church' else 'no'"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "marks",
            "value": {
              "calc": "['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'][round - 1] + ':' + mark_colour + ':' + mark_dir + ':' + mark_counts"
            }
          }
        },
        {
          "append": {
            "key": "counting_marks",
            "value": {
              "calc": "mark_colour + ' ' + mark_dir"
            },
            "if": {
              "calc": "mark_counts == 'yes'"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "gold",
            "value": {
              "calc": "gold_income_per_round"
            }
          }
        }
      ],
      "text": "Every player gains {gold_income_per_round} gold."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "reveal and final worths",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "disclose": {
            "of": 1,
            "attribute": "hidden_cards",
            "to": "all",
            "text": "Seat {subject}'s hidden collection: {value}."
          }
        },
        {
          "disclose": {
            "of": 1,
            "attribute": "marks",
            "to": "all",
            "text": "Seat {subject}'s marks: {value}."
          }
        },
        {
          "disclose": {
            "of": 2,
            "attribute": "hidden_cards",
            "to": "all",
            "text": "Seat {subject}'s hidden collection: {value}."
          }
        },
        {
          "disclose": {
            "of": 2,
            "attribute": "marks",
            "to": "all",
            "text": "Seat {subject}'s marks: {value}."
          }
        },
        {
          "disclose": {
            "of": 3,
            "attribute": "hidden_cards",
            "to": "all",
            "text": "Seat {subject}'s hidden collection: {value}."
          }
        },
        {
          "disclose": {
            "of": 3,
            "attribute": "marks",
            "to": "all",
            "text": "Seat {subject}'s marks: {value}."
          }
        },
        {
          "set": {
            "key": "final_worth_red",
            "value": {
              "calc": "worth_red"
            }
          }
        },
        {
          "set": {
            "key": "final_worth_blue",
            "value": {
              "calc": "worth_blue"
            }
          }
        },
        {
          "set": {
            "key": "final_worth_green",
            "value": {
              "calc": "worth_green"
            }
          }
        },
        {
          "set": {
            "key": "final_worth_yellow",
            "value": {
              "calc": "worth_yellow"
            }
          }
        },
        {
          "set": {
            "key": "final_worth_purple",
            "value": {
              "calc": "worth_purple"
            }
          }
        },
        {
          "set": {
            "key": "mark_idx",
            "value": 0
          }
        }
      ],
      "text": "Scoring: all hidden collections are revealed. Counting marks are now applied in round order."
    },
    {
      "use": "repeat",
      "phase": "scoring",
      "label": "apply counting marks",
      "when": {
        "calc": "round >= rounds"
      },
      "until": {
        "calc": "mark_idx >= len(counting_marks)"
      },
      "max": 13,
      "steps": [
        {
          "use": "update",
          "label": "apply one mark",
          "do": [
            {
              "set": {
                "key": "cur_colour",
                "value": {
                  "calc": "[c for c in ['Red', 'Blue', 'Green', 'Yellow', 'Purple'] if c in counting_marks[mark_idx]][0]"
                }
              }
            },
            {
              "set": {
                "key": "cur_dir",
                "value": {
                  "calc": "mark_step if '+1' in counting_marks[mark_idx] else -mark_step"
                }
              }
            },
            {
              "set": {
                "key": "final_worth_red",
                "value": {
                  "calc": "final_worth_red + cur_dir if cur_colour == 'Red' and final_worth_red + cur_dir >= worth_min and final_worth_red + cur_dir <= worth_max else final_worth_red"
                }
              }
            },
            {
              "set": {
                "key": "final_worth_blue",
                "value": {
                  "calc": "final_worth_blue + cur_dir if cur_colour == 'Blue' and final_worth_blue + cur_dir >= worth_min and final_worth_blue + cur_dir <= worth_max else final_worth_blue"
                }
              }
            },
            {
              "set": {
                "key": "final_worth_green",
                "value": {
                  "calc": "final_worth_green + cur_dir if cur_colour == 'Green' and final_worth_green + cur_dir >= worth_min and final_worth_green + cur_dir <= worth_max else final_worth_green"
                }
              }
            },
            {
              "set": {
                "key": "final_worth_yellow",
                "value": {
                  "calc": "final_worth_yellow + cur_dir if cur_colour == 'Yellow' and final_worth_yellow + cur_dir >= worth_min and final_worth_yellow + cur_dir <= worth_max else final_worth_yellow"
                }
              }
            },
            {
              "set": {
                "key": "final_worth_purple",
                "value": {
                  "calc": "final_worth_purple + cur_dir if cur_colour == 'Purple' and final_worth_purple + cur_dir >= worth_min and final_worth_purple + cur_dir <= worth_max else final_worth_purple"
                }
              }
            },
            {
              "adjust": {
                "key": "mark_idx",
                "value": 1
              }
            }
          ]
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "totals and victory points",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total_red",
            "value": {
              "calc": "count(c == 'Red 1' for c in you.hidden_cards + you.public_cards) + 2 * count(c == 'Red 2' for c in you.hidden_cards + you.public_cards) + 3 * count(c == 'Red 3' for c in you.hidden_cards + you.public_cards) + 4 * count(c == 'Red 4' for c in you.hidden_cards + you.public_cards)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total_blue",
            "value": {
              "calc": "count(c == 'Blue 1' for c in you.hidden_cards + you.public_cards) + 2 * count(c == 'Blue 2' for c in you.hidden_cards + you.public_cards) + 3 * count(c == 'Blue 3' for c in you.hidden_cards + you.public_cards) + 4 * count(c == 'Blue 4' for c in you.hidden_cards + you.public_cards)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total_green",
            "value": {
              "calc": "count(c == 'Green 1' for c in you.hidden_cards + you.public_cards) + 2 * count(c == 'Green 2' for c in you.hidden_cards + you.public_cards) + 3 * count(c == 'Green 3' for c in you.hidden_cards + you.public_cards) + 4 * count(c == 'Green 4' for c in you.hidden_cards + you.public_cards)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total_yellow",
            "value": {
              "calc": "count(c == 'Yellow 1' for c in you.hidden_cards + you.public_cards) + 2 * count(c == 'Yellow 2' for c in you.hidden_cards + you.public_cards) + 3 * count(c == 'Yellow 3' for c in you.hidden_cards + you.public_cards) + 4 * count(c == 'Yellow 4' for c in you.hidden_cards + you.public_cards)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total_purple",
            "value": {
              "calc": "count(c == 'Purple 1' for c in you.hidden_cards + you.public_cards) + 2 * count(c == 'Purple 2' for c in you.hidden_cards + you.public_cards) + 3 * count(c == 'Purple 3' for c in you.hidden_cards + you.public_cards) + 4 * count(c == 'Purple 4' for c in you.hidden_cards + you.public_cards)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.total_red == max([p.total_red for p in players]) and you.total_red >= min_majority_total"
            },
            "key": "vp",
            "value": {
              "calc": "final_worth_red if count(p.total_red == you.total_red for p in players) == 1 else int(final_worth_red / tie_share_divisor)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.total_blue == max([p.total_blue for p in players]) and you.total_blue >= min_majority_total"
            },
            "key": "vp",
            "value": {
              "calc": "final_worth_blue if count(p.total_blue == you.total_blue for p in players) == 1 else int(final_worth_blue / tie_share_divisor)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.total_green == max([p.total_green for p in players]) and you.total_green >= min_majority_total"
            },
            "key": "vp",
            "value": {
              "calc": "final_worth_green if count(p.total_green == you.total_green for p in players) == 1 else int(final_worth_green / tie_share_divisor)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.total_yellow == max([p.total_yellow for p in players]) and you.total_yellow >= min_majority_total"
            },
            "key": "vp",
            "value": {
              "calc": "final_worth_yellow if count(p.total_yellow == you.total_yellow for p in players) == 1 else int(final_worth_yellow / tie_share_divisor)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.total_purple == max([p.total_purple for p in players]) and you.total_purple >= min_majority_total"
            },
            "key": "vp",
            "value": {
              "calc": "final_worth_purple if count(p.total_purple == you.total_purple for p in players) == 1 else int(final_worth_purple / tie_share_divisor)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "vp",
            "value": {
              "calc": "int(you.gold / gold_per_vp)"
            }
          }
        }
      ],
      "text": "Final worths: Red {final_worth_red}, Blue {final_worth_blue}, Green {final_worth_green}, Yellow {final_worth_yellow}, Purple {final_worth_purple}. Totals (R/B/G/Y/P): seat 1 {players[0].total_red}/{players[0].total_blue}/{players[0].total_green}/{players[0].total_yellow}/{players[0].total_purple}, seat 2 {players[1].total_red}/{players[1].total_blue}/{players[1].total_green}/{players[1].total_yellow}/{players[1].total_purple}, seat 3 {players[2].total_red}/{players[2].total_blue}/{players[2].total_green}/{players[2].total_yellow}/{players[2].total_purple}. VP: seat 1 {players[0].vp}, seat 2 {players[1].vp}, seat 3 {players[2].vp}."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last round",
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
      "rank_by": "you.vp",
      "text": "Winner: {result}. Final VP: Seat 1 {players[0].vp}, Seat 2 {players[1].vp}, Seat 3 {players[2].vp}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 600,
    "deadline_s": 120
  },
  "rules": "SETUP. The deck has {deck_size} cards: {colour_cards} colour cards (for each of the {colours} colours Red, Blue, Green, Yellow and Purple, one card each of values 1, 1, 2, 2, 3 and 4) and {church_cards} Church cards. The deck is shuffled once; its order is hidden from everyone. Each player starts with {starting_gold} gold. Each colour has a public die worth, starting at {starting_worth}. A public worth can never go below {worth_min} or above {worth_max}. Every player has a hidden collection, seen only by its owner (the cards they kept and their secret marks), and a public collection, seen by all (the colour cards they won). Gold totals and public worths are public; the worths shown during play never include secret marks.\n\nROUNDS. There are {rounds} rounds. The active player is seat 1, 2, 3, 1, 2, 3 in rounds 1-6 and seat 3, 2, 1, 3, 2, 1 in rounds 7-12. Each round:\n1. The round number, the active player, all public worths, all gold totals and all public collections are announced.\n2. The top {cards_revealed_to_active} cards of the deck are removed and shown privately to the active player only, as Card A (the top card) and Card B (the next card).\n3. The active player privately chooses Keep A or Keep B.\n4. The kept card goes into the active player's hidden collection; nothing about it is announced. The other card is announced publicly as this round's lot.\n5. Talk: every player writes one short message at the same time; all messages are then shown to everyone. Messages are not binding.\n6. Sealed bid: all three players, including the active player, at the same time bid a whole number of gold from {bid_min} up to the gold they hold.\n7. All bids are revealed. If the highest bid is at least {min_winning_bid} and no other player bid the same amount, that player wins the lot and pays their bid to the bank (the gold leaves the game). Otherwise (highest bid 0, or a tie for highest) nobody pays and the lot is discarded face-up.\n8. A won colour card goes into the winner's public collection.\n9. Church and secret mark: (a) the active player always privately names one colour and a direction (+1 or -1), recorded secretly as this round's mark. It counts at scoring only if the card they kept this round is a Church card; otherwise it is void. This is asked every round, so being asked reveals nothing. (b) If the lot was a Church card and someone won it, the winner publicly names one colour and a direction (+1 or -1). If the active player is also the winner, they answer both parts. If the Church lot was not won, nobody is asked part (b) and no worth changes.\n10. If part (b) was answered, that colour's public worth changes by {church_step} in the named direction; if this would take it below {worth_min} or above {worth_max}, it has no effect. The won Church card is then discarded face-up. Secret marks change nothing now.\n11. Every player gains {gold_income_per_round} gold.\n12. After round {rounds}, scoring follows; otherwise the next round begins.\n\nSCORING.\n1. Final worths: start from each colour's public worth. All hidden collections are revealed. Every mark that counts (made in a round where that player kept a Church card) is applied one at a time in round order, earliest first, changing its colour's worth by {mark_step} in its direction, checked against the worth as already changed by earlier marks. A mark that would take a worth below {worth_min} or above {worth_max} has no effect.\n2. Majorities: for each colour, add up the values of each player's cards of that colour, hidden and public together. If one player has the strictly highest total and it is at least {min_majority_total}, they score VP equal to that colour's final worth. If two or more players tie for the highest total (at least {min_majority_total}), each scores the final worth divided by {tie_share_divisor}, rounded down. If no one has a card of that colour, nobody scores it. Church cards have no value at scoring.\n3. Gold: each player scores 1 VP for every full {gold_per_vp} gold they hold.\n\nThe player with the most VP wins. If two or more players tie for the most VP, they share the result (a draw)."
}
```
````
