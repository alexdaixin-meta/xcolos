# 49 coder

- time: 2026-10-27T17:44:31+00:00 (105.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 08c2caf9a19dea22, reply sha256 9f35654523203edf

## Sent

````
# Task: write the XColos game file for "Modern Art: Sealed Gallery"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

R1 SETUP (once, before round 1). There are three players, seats 1, 2 and 3, and three artists: Red, Blue and Green.
- Every player starts with money 60 and with owned_red, owned_blue and owned_green all 0.
- Each artist starts with season count 0 and value 0.
- The auctioneer is seat 1. The round counter is 0. The flag season_over is 0.
- Money is public: every bid, price and payout is announced, and anyone may track every balance. Each player's hand is private.

R2 DEAL (once, before round 1). The game rolls one six-sided die (deal_roll, 1 to 6).
- The three compositions are:
  - A: Red 4, Blue 2, Green 1.
  - B: Red 1, Blue 4, Green 2.
  - C: Red 2, Blue 1, Green 4.
- Seats 1, 2 and 3 receive compositions by roll:
  - Roll 1: A, B, C.
  - Roll 2: A, C, B.
  - Roll 3: B, A, C.
  - Roll 4: B, C, A.
  - Roll 5: C, A, B.
  - Roll 6: C, B, A.
- Exactly one case applies. It SETS each seat's hand_red, hand_blue and hand_green to the listed numbers.
- Each player sees only their own hand. Each player knows the other two seats hold the other two compositions, but not which seat holds which.

Each round runs R3 to R16 in order.

R3 START (every round). The round counter rises by 1. season_over is set to 0.

R4 PLAY (every round). The auctioneer chooses one artist X for which their own hand count is above 0. Only those artists are options.

R5 UPDATE (every round).
- The auctioneer's hand_X falls by 1.
- season_X rises by 1.
- current_artist is set to X and announced to all.

R6 SEASON-ENDING CARD (every round). If season_X is now 3, season_over is set to 1, the card is discarded unsold, and this is announced. Otherwise season_over stays 0.

R7 TALK (only if season_over = 0). Every player, including the auctioneer, writes one short message at the same time without seeing the others. All three messages are then shown to everyone, labelled by seat. Messages are free text and bind no one.

R8 BID (only if season_over = 0). All three players, including the auctioneer, bid at the same moment.
- Each bids a whole number from 0 up to their own current money.
- Bids are hidden until all are in, then all three are announced.

R9 WINNER (only if season_over = 0).
- The highest bid wins, and the price is the winning bid.
- If the highest bid is 0, the auctioneer takes the painting at price 0.
- Ties at a positive bid go to the tied seat that comes first in this order: the seat after the auctioneer, then the next seat, with the auctioneer last. (Auctioneer 1: order 2, 3, 1. Auctioneer 2: order 3, 1, 2. Auctioneer 3: order 1, 2, 3.)

R10 SETTLE (only if season_over = 0).
- If the winner is not the auctioneer, the winner's money falls by the price and the auctioneer's money rises by the price.
- If the winner is the auctioneer, the auctioneer's money falls by the price, which goes to the bank.
- The winner's owned_X rises by 1.
- The winner and price are announced.

R11 FINAL-ROUND FLAG (every round). If the round counter is 18, season_over is set to 1.

R12 SEASON SCORING (only if season_over = 1). Only artists with season count at least 1 can score.
- If one artist has the strictly highest season count, its value rises by 6. Then, if one of the other two artists has a strictly higher season count than the third and at least 1, that artist's value rises by 3.
- If two or three artists tie for the highest season count (at least 1), each of them gains value +3, and no other artist scores.

R13 PAYOUT (only if season_over = 1). For each artist that scored in R12 this round, every player's money rises by (their owned count of that artist) × (that artist's new cumulative value). Artists that did not score pay nothing, but keep their value.

R14 RESET (only if season_over = 1).
- Every player's owned_red, owned_blue and owned_green become 0 (paintings are discarded).
- Every artist's season count becomes 0.
- Values are kept.

R15 ANNOUNCE (only if season_over = 1). The scoring artists, their new values, each player's payout and each player's money are announced.

R16 ROTATE AND END (every round).
- The auctioneer passes to the next seat (1 to 2, 2 to 3, 3 to 1).
- If the round counter is 18, the game ends. Otherwise the next round begins at R3.
- Each seat is auctioneer exactly 6 times and plays 6 of its 7 cards, so the R4 options are never empty.

How the winner is decided: After round 18, including the final season's scoring and payout, the player with the strictly highest money wins. If two or three players tie for the highest money, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Modern Art: Sealed Gallery (3 to 3 players, best with 3)

Three players take turns as auctioneer of 18 paintings by three artists. Everyone bids at once in sealed bids, artists gain value at each season's end, owned paintings pay out, and the richest player after round 18 wins.

STATE (every item below must exist in the file):
  - each player: money (number, starts 60); everyone sees it. Coins held. Every bid, price and payout is announced.
  - each player: hand_red (number, starts 0); only its owner sees it. Red cards in this player's private hand.
  - each player: hand_blue (number, starts 0); only its owner sees it. Blue cards in this player's private hand.
  - each player: hand_green (number, starts 0); only its owner sees it. Green cards in this player's private hand.
  - each player: owned_red (number, starts 0); everyone sees it. Red paintings bought this season.
  - each player: owned_blue (number, starts 0); everyone sees it. Blue paintings bought this season.
  - each player: owned_green (number, starts 0); everyone sees it. Green paintings bought this season.
  - each player: message (text, starts ''); everyone sees it. This round's talk message.
  - each player: bid (number, starts 0); everyone sees it. This round's sealed bid, revealed once all bids are in.
  - each player: last_payout (number, starts 0); everyone sees it. Money received at the most recent season scoring.
  - the table: round (number, starts 0); everyone sees it. Round counter, from 1 to 18.
  - the table: auctioneer (number, starts 1); everyone sees it. Seat of the current auctioneer.
  - the table: season_over (number, starts 0); everyone sees it. Set to 1 when the season ends this round.
  - the table: deal_roll (number, starts 0); hidden from all players. Hidden die roll (1 to 6) that decides which seat gets which composition.
  - the table: season_red (number, starts 0); everyone sees it. Red cards played this season.
  - the table: season_blue (number, starts 0); everyone sees it. Blue cards played this season.
  - the table: season_green (number, starts 0); everyone sees it. Green cards played this season.
  - the table: value_red (number, starts 0); everyone sees it. Cumulative value of Red.
  - the table: value_blue (number, starts 0); everyone sees it. Cumulative value of Blue.
  - the table: value_green (number, starts 0); everyone sees it. Cumulative value of Green.
  - the table: current_artist (text, starts ''); everyone sees it. Artist played this round (red, blue or green).
  - the table: high_bid (number, starts 0); everyone sees it. Highest bid this round.
  - the table: winner (number, starts 0); everyone sees it. Seat that won this round's painting.
  - the table: price (number, starts 0); everyone sees it. Price paid this round.
  - the table: scored_red (number, starts 0); everyone sees it. 1 if Red scored at this season's end, else 0.
  - the table: scored_blue (number, starts 0); everyone sees it. 1 if Blue scored at this season's end, else 0.
  - the table: scored_green (number, starts 0); everyone sees it. 1 if Green scored at this season's end, else 0.
  - parameters, each kept as a table attribute: start_money = 60, artist_count = 3, die_sides = 6, composition_major = 4, composition_middle = 2, composition_minor = 1, cards_per_hand = 7, auctions_per_seat = 6, season_end_count = 3, first_place_value = 6, second_place_value = 3, tie_value = 3, min_season_count_to_score = 1, total_rounds = 18, first_auctioneer = 1, min_bid = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 each get money 60, and owned_red, owned_blue and owned_green 0.
  2. season_red, season_blue and season_green are set to 0, and value_red, value_blue and value_green to 0.
  3. auctioneer is set to 1, round to 0 and season_over to 0.
  4. deal_roll is set to a random whole number from 1 to 6 (seeded).
  5. Composition A is Red 4, Blue 2, Green 1. Composition B is Red 1, Blue 4, Green 2. Composition C is Red 2, Blue 1, Green 4.
  6. The compositions go to seats 1, 2 and 3 by roll: roll 1 gives A,B,C; roll 2 gives A,C,B; roll 3 gives B,A,C; roll 4 gives B,C,A; roll 5 gives C,A,B; roll 6 gives C,B,A. This sets each seat's hand_red, hand_blue and hand_green.
  7. Each player is shown only their own hand and is told that the other two seats hold the other two compositions.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; season_over = 0.
  2. [ask] the seat equal to auctioneer answers: one artist from red, blue, green, offering only those whose hand count for this seat is above 0. What happens: The chosen artist is X.
  3. [update] the seat equal to auctioneer. What happens: That seat's hand_X -= 1; season_X += 1; current_artist = X. Announce current_artist to all.
  4. [update] all players. What happens: If season_X == 3, then season_over = 1 and announce that the card is discarded unsold and the season ends. Otherwise season_over stays 0.
  5. [poll] all players, when season_over == 0 answers: short free text. What happens: Set each player's message, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
  6. [poll] all players, when season_over == 0 answers: a whole number from 0 to your own money. What happens: Set each player's bid. Once all bids are in, announce all three bids.
  7. [update] all players, when season_over == 0. What happens: high_bid = max of the bids. If high_bid == 0: winner = auctioneer and price = 0. Otherwise price = high_bid and winner = the first seat with bid == high_bid in this order: auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer.
  8. [update] all players, when season_over == 0. What happens: If winner != auctioneer: the winner's money -= price and the auctioneer's money += price. If winner == auctioneer: the auctioneer's money -= price (paid to the bank). The winner's owned_X += 1. Announce winner and price.
  9. [update] all players. What happens: If round == 18, then season_over = 1.
  10. [update] all players, when season_over == 1. What happens: Set scored_red, scored_blue and scored_green to 0. Let top = the largest season count. If top >= 1 and exactly one artist has season == top, that artist gets value += 6 and scored = 1; then let s = the larger season count of the other two, and if s >= 1 and exactly one of them has season == s, that artist gets value += 3 and scored = 1. If top >= 1 and two or three artists have season == top, each of them gets value += 3 and scored = 1, and no other artist scores.
  11. [update] all players, when season_over == 1. What happens: For each player: last_payout = owned_red*value_red*scored_red + owned_blue*value_blue*scored_blue + owned_green*value_green*scored_green; money += last_payout.
  12. [update] all players, when season_over == 1. What happens: Every player's owned_red, owned_blue and owned_green = 0; season_red, season_blue and season_green = 0. Values are kept.
  13. [tell] all players, when season_over == 1. What happens: Announce the scoring artists, value_red, value_blue, value_green, and each player's last_payout and money.
  14. [update] all players. What happens: auctioneer = auctioneer % 3 + 1.
  15. [check] all players. What happens: If round == 18, end the game. Otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has money 60 and owned_red, owned_blue and owned_green 0; every season count and every value is 0; auctioneer is 1; round is 0.
  R2. When deal_roll is 1, then seats 1, 2 and 3 get compositions A, B and C, where A is Red 4/Blue 2/Green 1, B is Red 1/Blue 4/Green 2, and C is Red 2/Blue 1/Green 4.
  R3. When deal_roll is 2, 3, 4, 5 or 6, then seats 1, 2 and 3 get A,C,B or B,A,C or B,C,A or C,A,B or C,B,A respectively.
  R4. When hands are dealt, then each player sees only their own hand_red, hand_blue and hand_green.
  R5. When a round starts, then round rises by 1 and season_over is set to 0.
  R6. When the auctioneer chooses an artist, then only artists with the auctioneer's hand count above 0 are offered.
  R7. When artist X is played, then the auctioneer's hand_X falls by 1, season_X rises by 1, and current_artist is announced as X.
  R8. When season_X reaches 3 after a play, then season_over is 1, the card is discarded unsold, and no talk, bid or sale happens that round.
  R9. When season_over is 0, then all three players write one message at the same time, and all are shown labelled by seat.
  R10. When season_over is 0, then all three players, including the auctioneer, bid simultaneously a whole number from 0 to their own money, and all bids are announced.
  R11. When the highest bid is positive, then the highest bidder wins at a price equal to that bid.
  R12. When all bids are 0, then the auctioneer takes the painting at price 0.
  R13. When a positive top bid is tied, then the winner is the tied seat that comes first in the order: seat after the auctioneer, the next seat, then the auctioneer (for example, with auctioneer 1 the order is 2, 3, 1).
  R14. When the winner is not the auctioneer, then the winner pays the price to the auctioneer; for example, a price of 10 moves 10 from the winner's money to the auctioneer's.
  R15. When the winner is the auctioneer, then the auctioneer's money falls by the price, paid to the bank.
  R16. When a painting of X is sold, then the winner's owned_X rises by 1 and the winner and price are announced.
  R17. When round is 18, then season_over is set to 1 after the sale.
  R18. When a season ends and one artist has the strictly highest season count (at least 1), then its value rises by 6.
  R19. When a single artist was top, and one of the other two has a season count strictly higher than the third and at least 1, then that artist's value rises by 3; otherwise no second artist scores.
  R20. When two or three artists tie for the highest season count (at least 1), then each of them gains 3 value and no other artist scores.
  R21. When a season ends, then for each artist that scored, every player's money rises by their owned count of it times its new cumulative value; artists that did not score pay nothing but keep their value.
  R22. When a season's payout is done, then every owned count and every season count is reset to 0, and values are kept.
  R23. When a season ends, then the scoring artists, new values, each player's payout and each player's money are announced.
  R24. When a round ends, then the auctioneer passes 1 to 2, 2 to 3, and 3 to 1.
  R25. When round 18 has ended, then the game ends and the player with the most money wins; players tied for the most money share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Which artist do you play? | asked: the auctioneer only | options: each of red, blue and green for which the auctioneer's own hand count is above 0; other seats are not asked
  - Your message to the table | asked: all three seats, only when season_over == 0 | options: short free text
  - Your sealed bid | asked: all three seats including the auctioneer, only when season_over == 0 | options: a whole number from 0 to that seat's current money

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 18
  - each player's standing: you.money (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After round 18, including the last season's scoring and payout, the player with the most money wins. Players tied for the most money share the result, which is the source's draw.
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

- each player: `money` (number, visible: public, starts 60): Coins held. Every bid, price and payout is announced.
- each player: `bid` (number, visible: public, starts 0): This round's sealed bid, revealed once all bids are in.
- the table: `round` (number, visible: public, starts 0): Round counter, from 1 to 18.
- the table: `auctioneer` (number, visible: public, starts 1): Seat of the current auctioneer.
- the table: `season_red` (number, visible: public, starts 0): Red cards played this season.
- the table: `season_blue` (number, visible: public, starts 0): Blue cards played this season.
- the table: `season_green` (number, visible: public, starts 0): Green cards played this season.
- the table: `value_red` (number, visible: public, starts 0): Cumulative value of Red.
- the table: `value_blue` (number, visible: public, starts 0): Cumulative value of Blue.
- the table: `value_green` (number, visible: public, starts 0): Cumulative value of Green.
- parameters (each must be an attribute holding this value, never a number buried in a step): start_money = 60, artist_count = 3, die_sides = 6, composition_major = 4, composition_middle = 2, composition_minor = 1, cards_per_hand = 7, auctions_per_seat = 6, season_end_count = 3, first_place_value = 6, second_place_value = 3, tie_value = 3, min_season_count_to_score = 1, total_rounds = 18, first_auctioneer = 1, min_bid = 0
- the game ends with ONE ending whose `rank_by` is `you.money`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Make R8 a single simultaneous numeric bid. All three seats, including the auctioneer, enter a whole number from min_bid up to their own money in one poll, and each value is stored in that seat's `bid`. Do not offer a choice list such as the `offer` list of artist names. The player's numeric answer must be what reaches `bid`.
2) After the poll, compute high_bid as the maximum bid. If high_bid is 0, the auctioneer wins at price 0. Otherwise the winner is the top bidder, breaking ties in the order seat after the auctioneer, then the next seat, then the auctioneer.
3) Settle: the winner pays the price to the auctioneer, or to the bank if the winner is the auctioneer, and the winner's owned_X rises by 1.
4) Fix the deal. For each roll, exactly one case should set each seat's hand_red, hand_blue and hand_green, and later cases must not overwrite earlier ones. Guard each step with a `when deal_roll == k` condition. With roll 6, seat 1 must end with C (2, 1, 4), not green 1.
5) Keep all parameters as attributes. Make sure R6–R16 run with the right `when season_over` conditions.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "modern_art_sealed_gallery",
    "name": "Modern Art: Sealed Gallery",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players auction 18 paintings by three artists in sealed bids; artists gain value each season and the richest player after round 18 wins."
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
        "key": "money",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "hand_red",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_blue",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_green",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "owned_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "owned_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "owned_green",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "last_payout",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "auctioneer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "season_over",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_roll",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "season_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_artist",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "scored_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "scored_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "scored_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_ties",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "second_count",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gain_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gain_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gain_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_money",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "artist_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "die_sides",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "composition_major",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "composition_middle",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "composition_minor",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "auctions_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "season_end_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "first_place_value",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "second_place_value",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tie_value",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_season_count_to_score",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 18
      },
      {
        "key": "first_auctioneer",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting money",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "start_money"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_green",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "artists start at zero",
      "do": [
        {
          "set": {
            "key": "season_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "value_green",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first auctioneer",
      "do": [
        {
          "set": {
            "key": "auctioneer",
            "value": {
              "calc": "first_auctioneer"
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
            "key": "season_over",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "roll the deal die",
      "do": [
        {
          "set": {
            "key": "deal_roll",
            "value": {
              "calc": "min(die_sides, max(1, int(uniform(1, die_sides + 1))))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the compositions",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand_red",
            "value": {
              "calc": "[composition_major, composition_minor, composition_middle][[[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]][deal_roll - 1][you.seat - 1]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_blue",
            "value": {
              "calc": "[composition_middle, composition_major, composition_minor][[[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]][deal_roll - 1][you.seat - 1]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_green",
            "value": {
              "calc": "[composition_minor, composition_middle, composition_major][[[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]][deal_roll - 1][you.seat - 1]]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand_red",
        "hand_blue",
        "hand_green",
        "money"
      ],
      "text": "Your private hand: Red {hand_red}, Blue {hand_blue}, Green {hand_green}. The other two seats hold the other two compositions, but you do not know which seat holds which."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the round starts",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "season_over",
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
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(['red'] if you.hand_red > 0 else []) + (['blue'] if you.hand_blue > 0 else []) + (['green'] if you.hand_green > 0 else [])"
            }
          }
        }
      ],
      "text": "Round {round} of {total_rounds}. Seat {auctioneer} is the auctioneer."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the auctioneer plays a card",
      "to": {
        "where": "you.seat == auctioneer"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "artist"
      },
      "text": "You are the auctioneer. Choose one artist from your hand to put up for auction."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the card is played",
      "do": [
        {
          "set": {
            "key": "current_artist",
            "value": "$artist"
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand_red",
            "value": -1,
            "if": {
              "calc": "$artist == 'red'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand_blue",
            "value": -1,
            "if": {
              "calc": "$artist == 'blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "hand_green",
            "value": -1,
            "if": {
              "calc": "$artist == 'green'"
            }
          }
        },
        {
          "adjust": {
            "key": "season_red",
            "value": 1,
            "if": {
              "calc": "$artist == 'red'"
            }
          }
        },
        {
          "adjust": {
            "key": "season_blue",
            "value": 1,
            "if": {
              "calc": "$artist == 'blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "season_green",
            "value": 1,
            "if": {
              "calc": "$artist == 'green'"
            }
          }
        }
      ],
      "text": "Seat {auctioneer} plays a {current_artist} painting. Season counts: Red {season_red}, Blue {season_blue}, Green {season_green}."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "season-ending card",
      "do": [
        {
          "set": {
            "key": "season_over",
            "value": 1,
            "if": {
              "calc": "(season_red if current_artist == 'red' else (season_blue if current_artist == 'blue' else season_green)) >= season_end_count"
            },
            "text": "That is the third {current_artist} card this season: it is discarded unsold and the season ends now."
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "when": {
        "calc": "season_over == 0"
      },
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
      "text": "A {current_artist} painting is up for auction. Write one short message to the table. Everyone writes at the same time; nothing said binds anyone."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "when": {
        "calc": "season_over == 0"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.money"
        }
      },
      "store": "bid",
      "text": "Sealed bid for the {current_artist} painting: a whole number from {min_bid} up to your money. All three seats, the auctioneer included, bid at once; bids are revealed together."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the winner",
      "when": {
        "calc": "season_over == 0"
      },
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
            "key": "price",
            "value": {
              "calc": "high_bid"
            }
          }
        },
        {
          "set": {
            "key": "winner",
            "value": {
              "calc": "auctioneer if high_bid == 0 else [s for s in [auctioneer % len(players) + 1, (auctioneer + 1) % len(players) + 1, auctioneer] if players[s - 1].bid == high_bid][0]"
            }
          }
        }
      ],
      "text": "Bids revealed: Seat 1 {players[0].bid}, Seat 2 {players[1].bid}, Seat 3 {players[2].bid}."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "settle",
      "when": {
        "calc": "season_over == 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "winner"
            },
            "key": "money",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "winner != auctioneer"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "money",
            "value": {
              "calc": "price"
            },
            "if": {
              "calc": "winner != auctioneer"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "auctioneer"
            },
            "key": "money",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "winner == auctioneer"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner"
            },
            "key": "owned_red",
            "value": 1,
            "if": {
              "calc": "current_artist == 'red'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner"
            },
            "key": "owned_blue",
            "value": 1,
            "if": {
              "calc": "current_artist == 'blue'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner"
            },
            "key": "owned_green",
            "value": 1,
            "if": {
              "calc": "current_artist == 'green'"
            }
          }
        }
      ],
      "text": "Seat {winner} wins the {current_artist} painting for {price}. Money: Seat 1 {players[0].money}, Seat 2 {players[1].money}, Seat 3 {players[2].money}."
    },
    {
      "use": "update",
      "phase": "season",
      "label": "final-round flag",
      "do": [
        {
          "set": {
            "key": "season_over",
            "value": 1,
            "if": {
              "calc": "round == total_rounds"
            },
            "text": "Round {round} was the last: the final season ends now."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "season",
      "label": "season scoring",
      "when": {
        "calc": "season_over == 1"
      },
      "do": [
        {
          "set": {
            "key": "scored_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "scored_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "scored_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "max([season_red, season_blue, season_green])"
            }
          }
        },
        {
          "set": {
            "key": "top_ties",
            "value": {
              "calc": "count(c == top_count for c in [season_red, season_blue, season_green])"
            }
          }
        },
        {
          "set": {
            "key": "second_count",
            "value": {
              "calc": "max([c for c in [season_red, season_blue, season_green] if c < top_count] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "gain_red",
            "value": {
              "calc": "0 if top_count < min_season_count_to_score else (first_place_value if season_red == top_count and top_ties == 1 else (tie_value if season_red == top_count else (second_place_value if top_ties == 1 and season_red == second_count and second_count >= min_season_count_to_score and count(c == second_count for c in [season_red, season_blue, season_green]) == 1 else 0)))"
            }
          }
        },
        {
          "set": {
            "key": "gain_blue",
            "value": {
              "calc": "0 if top_count < min_season_count_to_score else (first_place_value if season_blue == top_count and top_ties == 1 else (tie_value if season_blue == top_count else (second_place_value if top_ties == 1 and season_blue == second_count and second_count >= min_season_count_to_score and count(c == second_count for c in [season_red, season_blue, season_green]) == 1 else 0)))"
            }
          }
        },
        {
          "set": {
            "key": "gain_green",
            "value": {
              "calc": "0 if top_count < min_season_count_to_score else (first_place_value if season_green == top_count and top_ties == 1 else (tie_value if season_green == top_count else (second_place_value if top_ties == 1 and season_green == second_count and second_count >= min_season_count_to_score and count(c == second_count for c in [season_red, season_blue, season_green]) == 1 else 0)))"
            }
          }
        },
        {
          "adjust": {
            "key": "value_red",
            "value": {
              "calc": "gain_red"
            }
          }
        },
        {
          "adjust": {
            "key": "value_blue",
            "value": {
              "calc": "gain_blue"
            }
          }
        },
        {
          "adjust": {
            "key": "value_green",
            "value": {
              "calc": "gain_green"
            }
          }
        },
        {
          "set": {
            "key": "scored_red",
            "value": {
              "calc": "1 if gain_red > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "scored_blue",
            "value": {
              "calc": "1 if gain_blue > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "scored_green",
            "value": {
              "calc": "1 if gain_green > 0 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "season",
      "label": "payout",
      "when": {
        "calc": "season_over == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "last_payout",
            "value": {
              "calc": "you.owned_red * value_red * scored_red + you.owned_blue * value_blue * scored_blue + you.owned_green * value_green * scored_green"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "you.last_payout"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "season",
      "label": "reset the season",
      "when": {
        "calc": "season_over == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "owned_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "owned_green",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_red",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_blue",
            "value": 0
          }
        },
        {
          "set": {
            "key": "season_green",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "season",
      "label": "season results",
      "when": {
        "calc": "season_over == 1"
      },
      "to": "all",
      "text": "Season scored (1 = scored): Red {scored_red}, Blue {scored_blue}, Green {scored_green}. Values now: Red {value_red}, Blue {value_blue}, Green {value_green}. Payouts: Seat 1 {players[0].last_payout}, Seat 2 {players[1].last_payout}, Seat 3 {players[2].last_payout}. Money: Seat 1 {players[0].money}, Seat 2 {players[1].money}, Seat 3 {players[2].money}. Paintings are discarded and season counts reset."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "rotate the auctioneer",
      "do": [
        {
          "set": {
            "key": "auctioneer",
            "value": {
              "calc": "auctioneer % len(players) + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after the last round",
      "when": {
        "calc": "round >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= total_rounds"
      },
      "rank_by": "you.money",
      "text": "Winner: {result}. Final money: Seat 1 {players[0].money}, Seat 2 {players[1].money}, Seat 3 {players[2].money}."
    }
  },
  "limits": {
    "rounds": 18,
    "rounds_max": 20,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Three players (seats 1, 2, 3) and three artists: Red, Blue and Green. Everyone starts with {start_money} money and no paintings. Each artist starts with season count 0 and value 0. Seat {first_auctioneer} is the first auctioneer. Money is public: every bid, price and payout is announced. Your hand is private.\n\nDeal: a hidden {die_sides}-sided die decides which seat gets which of three compositions of {cards_per_hand} cards: A is Red 4, Blue 2, Green 1; B is Red 1, Blue 4, Green 2; C is Red 2, Blue 1, Green 4. Roll 1 gives seats 1, 2, 3 A, B, C; roll 2 A, C, B; roll 3 B, A, C; roll 4 B, C, A; roll 5 C, A, B; roll 6 C, B, A. You see only your own hand; the other two seats hold the other two compositions, but you do not know which seat holds which.\n\nEach of the {total_rounds} rounds: the round counter rises by 1. The auctioneer plays one card from their hand (only artists they still hold are offered); their hand count for it falls by 1 and that artist's season count rises by 1. If that season count is now {season_end_count}, the card is discarded unsold, the season ends, and there is no talk, bid or sale that round. Otherwise: every player, the auctioneer included, writes one short message at the same time; all three are shown labelled by seat and bind no one. Then all three players, the auctioneer included, bid at the same moment a whole number from {min_bid} up to their own money; bids are hidden until all are in, then all are announced. The highest bid wins and the price is that bid. If the highest bid is 0, the auctioneer takes the painting at price 0. A tie at a positive bid goes to the tied seat that comes first in this order: the seat after the auctioneer, then the next seat, with the auctioneer last (auctioneer 1: 2, 3, 1; auctioneer 2: 3, 1, 2; auctioneer 3: 1, 2, 3). If the winner is not the auctioneer, the winner pays the price to the auctioneer; if the winner is the auctioneer, the auctioneer pays the price to the bank. The winner owns one more painting of that artist. In round {total_rounds} the season also ends after the sale.\n\nSeason scoring: only artists with season count at least {min_season_count_to_score} can score. If one artist has the strictly highest season count, its value rises by {first_place_value}; then, if one of the other two has a strictly higher season count than the third and at least {min_season_count_to_score}, its value rises by {second_place_value}, otherwise no second artist scores. If two or three artists tie for the highest season count, each of them gains {tie_value} value and no other artist scores. For each artist that scored, every player's money rises by their owned count of that artist times its new cumulative value; artists that did not score pay nothing but keep their value. Then all owned paintings are discarded and every season count returns to 0; values are kept. The scoring artists, new values, payouts and money are announced.\n\nAt the end of each round the auctioneer passes 1 to 2, 2 to 3, 3 to 1, so each seat is auctioneer {auctions_per_seat} times. After round {total_rounds}, including the final season's scoring and payout, the player with the most money wins; players tied for the most money share the result (a draw)."
}
```
````
