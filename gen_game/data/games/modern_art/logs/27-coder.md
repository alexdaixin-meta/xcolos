# 27 coder

- time: 2026-10-27T18:45:36+00:00 (126.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 b6cf36ec1c98036d, reply sha256 9f9b16cffe3bdc2e

## Sent

````
# Task: write the XColos game file for "Modern Art: Four Seasons"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP.
- Four players sit in seats 1-4.
- The deck has 24 cards: 6 each of Red, Blue, Green and Yellow.
- Shuffle the deck and deal each player 5 cards as a hidden hand. The remaining 4 cards are set aside unseen.
- Each player starts with 100 money. Money is hidden; each player sees only their own.
- Every artist starts with cumulative value 0 and season count 0.

STRUCTURE.
- There are 16 auctions in 4 seasons. Season s contains auctions 4s-3 to 4s.
- In auction k of season s, where k is 1 to 4 within the season, the auctioneer is seat ((s + k - 2) mod 4) + 1.
- This gives the order: Season 1: 1,2,3,4. Season 2: 2,3,4,1. Season 3: 3,4,1,2. Season 4: 4,1,2,3.
- Each player is auctioneer exactly once per season (4 times in all) and ends with 1 unused card.

EACH AUCTION.
(1) The auctioneer privately chooses one card from their hand and removes it from the hand. Its artist is announced to all.
(2) That artist's season count rises by 1, whether or not the painting sells.
(3) Talk: every player writes one short message at the same time, without seeing the others' messages. All messages are then shown to everyone. Messages are not binding.
(4) Every player, including the auctioneer, submits a sealed bid at the same time. A bid is a whole number from 0 to the bidder's current money.
(5) Resolution.
  - If the highest bid is 0, the painting is unsold and discarded.
  - Otherwise the highest bidder buys it. If several players tie for highest, the buyer is the first of them in the order: seat (A mod 4)+1, seat ((A+1) mod 4)+1, seat ((A+2) mod 4)+1, then the auctioneer, where A is the auctioneer's seat.
  - The buyer pays the bid. If the buyer is not the auctioneer, the auctioneer receives the bid divided by 2, rounded down, and the rest goes to the bank. If the auctioneer buys, the whole bid goes to the bank.
  - The painting joins the buyer's collection, and the buyer's paintings-bought count rises by 1.
(6) Announcement.
  - Everyone is told the artist and the buyer, or that the painting went unsold.
  - The price is told privately to the buyer and to the auctioneer only.
  - Losing bids are never revealed.

SEASON END (after the 4th auction of each season).
(a) Nomination. Every player at the same time secretly names one of the four artists. Each nomination adds 1 to that artist's season count. All nominations are then revealed.
(b) Ranking. Rank the artists by season count, higher first. Break ties first by higher cumulative value, then by this season's priority: Season 1 R>B>G>Y; Season 2 B>G>Y>R; Season 3 G>Y>R>B; Season 4 Y>R>B>G. An artist with season count 0 cannot place.
(c) Values. Add 30 to the cumulative value of the 1st artist, 20 to the 2nd and 10 to the 3rd. The 4th artist gains nothing.
(d) Payout. For each painting a player owns of an artist that placed in the top three this season, the bank pays that player the artist's cumulative value (after step c). Paintings of an artist that did not place pay 0. Each player is told their own payout privately. The artists' cumulative values are public.
(e) All owned paintings are discarded, and all season counts reset to 0.

GAME END. The game ends after the Season 4 payout. Final money totals are then revealed.

How the winner is decided: Only players who bought at least 3 paintings during the game are eligible. Among eligible players, the one with the most money wins. If two or more eligible players tie for most money, the game is a draw. If no player is eligible, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Modern Art: Four Seasons (4 to 4 players, best with 4)

Four dealers auction paintings by four artists over four seasons with sealed bids. Each season the artists are ranked and pay out on paintings held. The richest player who bought at least 3 paintings wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Hidden hand of artist cards (Red, Blue, Green, Yellow), 5 dealt at setup
  - each player: money (number, starts 100); only its owner sees it. The player's money, seen only by its owner until it is revealed at game end; this is the score
  - each player: paintings_bought (number, starts 0); everyone sees it. Paintings bought during the whole game; at least 3 are needed to be eligible to win
  - each player: collection (list, starts []); everyone sees it. Artists of the paintings owned this season (buyers are announced publicly); emptied at season end
  - each player: bid (number, starts 0); only its owner sees it. This auction's sealed bid; losing bids are never revealed
  - each player: nomination (text, starts ''); only its owner sees it. The artist this player names at season end; all nominations are revealed after the poll
  - each player: message (text, starts ''); everyone sees it. This auction's non-binding talk message
  - each player: payout_last (number, starts 0); only its owner sees it. The player's payout from the last season end, told privately
  - the table: deck (list, starts ['Red', 'Red', 'Red', 'Red', 'Red', 'Red', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Yellow']); hidden from all players. The 24-card deck
  - the table: set_aside (list, starts []); hidden from all players. The 4 cards set aside unseen after the deal
  - the table: season (number, starts 1); everyone sees it. Current season, 1 to 4
  - the table: auction_in_season (number, starts 1); everyone sees it. k, the auction's number within the season, 1 to 4
  - the table: auctions_done (number, starts 0); everyone sees it. Auctions completed so far, 0 to 16
  - the table: auctioneer (number, starts 1); everyone sees it. Seat of this auction's auctioneer
  - the table: current_card (text, starts ''); everyone sees it. Artist of the painting being auctioned
  - the table: high_bid (number, starts 0); hidden from all players. Highest bid this auction (the price); told privately to the buyer and the auctioneer only
  - the table: buyer (number, starts 0); everyone sees it. Seat of this auction's buyer, 0 if unsold
  - the table: count_red (number, starts 0); everyone sees it. Red's season count
  - the table: count_blue (number, starts 0); everyone sees it. Blue's season count
  - the table: count_green (number, starts 0); everyone sees it. Green's season count
  - the table: count_yellow (number, starts 0); everyone sees it. Yellow's season count
  - the table: value_red (number, starts 0); everyone sees it. Red's cumulative value
  - the table: value_blue (number, starts 0); everyone sees it. Blue's cumulative value
  - the table: value_green (number, starts 0); everyone sees it. Green's cumulative value
  - the table: value_yellow (number, starts 0); everyone sees it. Yellow's cumulative value
  - the table: place_red (number, starts 0); everyone sees it. Red's place this season: 1-3 = placed in the top three, 0 = did not place
  - the table: place_blue (number, starts 0); everyone sees it. Blue's place this season, as above
  - the table: place_green (number, starts 0); everyone sees it. Green's place this season, as above
  - the table: place_yellow (number, starts 0); everyone sees it. Yellow's place this season, as above
  - parameters, each kept as a table attribute: deck_size = 24, cards_per_artist = 6, hand_size = 5, set_aside_cards = 4, starting_money = 100, seasons = 4, auctions_per_season = 4, total_auctions = 16, value_first = 30, value_second = 20, value_third = 10, value_fourth = 0, auctioneer_share_divisor = 2, min_paintings_to_be_eligible = 3, min_bid = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Four players sit in seats 1 to 4.
  2. The deck list holds 24 cards: 6 each of Red, Blue, Green and Yellow.
  3. Each player draws 5 cards at random from the deck into their hand. Each draw removes the card from the deck.
  4. The remaining 4 cards are moved from the deck to set_aside, unseen.
  5. Each player's money is set to 100 and their paintings_bought to 0.
  6. Every artist's cumulative value and season count are set to 0. Season is 1, auction_in_season is 1 and auctions_done is 0.
  7. Sync: each player is sent their own hand and money.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: auctioneer = ((season + auction_in_season - 2) mod 4) + 1; every player's bid = 0 and message = ''; buyer = 0; high_bid = 0
  2. [ask] the seat equal to auctioneer answers: one card from the auctioneer's hand. What happens: Remove the chosen card from the auctioneer's hand and set current_card to its artist. Tell all players: 'Seat {auctioneer} auctions a {current_card} painting.'
  3. [update] all players. What happens: The season count of current_card's artist (count_red, count_blue, count_green or count_yellow) rises by 1, whether or not the painting sells
  4. [poll] all players answers: a short text message. What happens: Set each player's message, then broadcast to all: 'Seat {seat} says: {value}'. Messages are not binding.
  5. [poll] all players answers: a whole number from 0 to your current money. What happens: Set each player's bid; no bid is shown to anyone
  6. [update] all players. What happens: high_bid = the highest bid. If high_bid = 0: buyer = 0 and the card is discarded. Otherwise buyer = the seat with the highest bid*4 + (3 - ((seat - auctioneer - 1) mod 4)), which breaks ties in the order auctioneer+1, auctioneer+2, auctioneer+3, then the auctioneer. Buyer's money -= high_bid. If buyer != auctioneer, auctioneer's money += floor(high_bid / 2), and the rest goes to the bank. current_card is appended to the buyer's collection, and the buyer's paintings_bought += 1.
  7. [tell] all players. What happens: Public: 'Seat {buyer} bought the {current_card} painting', or 'The {current_card} painting went unsold' when buyer = 0. Private to the buyer and to the auctioneer only: 'The price was {high_bid}.' Losing bids are never revealed.
  8. [poll] all players answers: one of Red, Blue, Green, Yellow. What happens: Set each player's nomination. Each nomination adds 1 to that artist's season count. All nominations are then revealed to everyone.
  9. [update] all players. What happens: Each artist gets a key = count*10000 + value*10 + priority, where priority (3 highest) follows the season order: S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G. An artist's place = 1 + the number of artists with a higher key. An artist with count 0, or with place 4, gets place 0. Then value += 30 if place 1, 20 if place 2, 10 if place 3.
  10. [update] all players. What happens: For each player: payout_last = the sum, over the paintings in their collection, of that artist's value (after this season's increase) if the artist's place is 1 to 3, else 0. The player's money += payout_last. Tell each player privately: 'Your payout this season is {payout_last}.' Tell all players the four cumulative values.
  11. [update] all players. What happens: Every player's collection = []; count_red, count_blue, count_green and count_yellow = 0; every place = 0
  12. [update] all players. What happens: auctions_done += 1. If auction_in_season == 4, then season += 1 and auction_in_season = 1; otherwise auction_in_season += 1.
  13. [check] all players. What happens: If auctions_done == 16, the game ends and every player's final money is revealed to all; otherwise continue with the next auction

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the 4 players is dealt 5 hidden cards from a 24-card deck of 6 Red, 6 Blue, 6 Green and 6 Yellow, and the remaining 4 cards are set aside unseen.
  R2. At setup, each player has 100 money, and every artist has cumulative value 0 and season count 0.
  R3. In auction k of season s, the auctioneer is seat ((s + k - 2) mod 4) + 1, giving Season 1: 1,2,3,4; Season 2: 2,3,4,1; Season 3: 3,4,1,2; Season 4: 4,1,2,3.
  R4. When the auctioneer chooses a card, it is removed from their hand and its artist is announced to all.
  R5. When a card is auctioned, its artist's season count rises by 1, whether or not it sells.
  R6. Every auction, all players send one talk message at the same time, and the messages are then shown to everyone.
  R7. Every player, including the auctioneer, bids a whole number from 0 to their current money, sealed and at the same time.
  R8. When the highest bid is 0, the painting is unsold and discarded, and no money changes hands.
  R9. When bids tie for highest, the buyer is the first tied seat in the order auctioneer+1, auctioneer+2, auctioneer+3 (wrapping round), then the auctioneer; for example, with auctioneer 2 and seats 1 and 4 tied at 30, seat 4 buys.
  R10. When a non-auctioneer buys for bid b, the buyer pays b and the auctioneer receives floor(b/2); for example, a bid of 25 gives the auctioneer 12.
  R11. When the auctioneer buys their own painting for b, they pay b to the bank and receive nothing.
  R12. When a painting sells, it is added to the buyer's collection and the buyer's paintings_bought rises by 1.
  R13. After each auction, the artist and the buyer (or 'unsold') are announced to all, the price is told only to the buyer and the auctioneer, and losing bids are never revealed.
  R14. After the 4th auction of a season, every player secretly nominates one artist, each nomination adds 1 to that artist's season count, and all nominations are then revealed.
  R15. Artists are ranked by season count, higher first; ties are broken by higher cumulative value, then by the season priority (S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G), and an artist with season count 0 cannot place.
  R16. At season end, the 1st artist gains 30 cumulative value, the 2nd gains 20, the 3rd gains 10, and the 4th gains nothing.
  R17. At season end, each owned painting of a top-three artist pays its owner that artist's cumulative value after the increase, and a painting of an artist that did not place pays 0.
  R18. Each player's payout is told only to them, while the artists' cumulative values are public.
  R19. After the payout, all collections are emptied and all season counts reset to 0.
  R20. The game ends after the 16th auction and the Season 4 payout, and all final money is then revealed.
  R21. Only a player with paintings_bought >= 3 can win; among those, the most money wins; eligible players tied for most money share the result; and with no eligible player nobody wins.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a card to auction | asked: the seat equal to auctioneer | options: each distinct artist currently in that seat's hand; other seats are not asked
  - Talk message | asked: all seats | options: any short text
  - Sealed bid | asked: all seats, including the auctioneer | options: a whole number from 0 to that seat's current money
  - Season-end nomination (after auction 4 of each season) | asked: all seats | options: Red, Blue, Green, Yellow

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: auctions_done == 16
  - each player's standing: (you.paintings_bought >= 3) * (you.money + 1) (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - min_to_win: 1 (a player whose standing is below it cannot win; if none reaches it, the match ends with no winner)
  - how the result is decided: Only players who bought at least 3 paintings are eligible. Among them the most money wins, and eligible players tied for most money share the result. If nobody is eligible, nobody wins.
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

- each player: `money` (number, visible: ally, starts 100): The player's money, seen only by its owner until it is revealed at game end; this is the score
- each player: `paintings_bought` (number, visible: public, starts 0): Paintings bought during the whole game; at least 3 are needed to be eligible to win
- the table: `value_red` (number, visible: public, starts 0): Red's cumulative value
- the table: `value_blue` (number, visible: public, starts 0): Blue's cumulative value
- the table: `value_green` (number, visible: public, starts 0): Green's cumulative value
- the table: `value_yellow` (number, visible: public, starts 0): Yellow's cumulative value
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, cards_per_artist = 6, hand_size = 5, set_aside_cards = 4, starting_money = 100, seasons = 4, auctions_per_season = 4, total_auctions = 16, value_first = 30, value_second = 20, value_third = 10, value_fourth = 0, auctioneer_share_divisor = 2, min_paintings_to_be_eligible = 3, min_bid = 0
- the game ends with ONE ending whose `rank_by` is `(you.paintings_bought >= 3) * (you.money + 1)`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- that ending's `min_to_win` is `1`: a player below it cannot win, and if nobody reaches it the match ends with no winner
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
{
  "schema": 1,
  "meta": {
    "id": "modern_art_four_seasons",
    "name": "Modern Art: Four Seasons",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four dealers auction paintings by four artists over four seasons with sealed bids. The richest player who bought at least 3 paintings wins."
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
        "key": "money",
        "visible": "ally",
        "type": "number",
        "initial": 100
      },
      {
        "key": "paintings_bought",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "collection",
        "visible": "public",
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
        "key": "nomination",
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
        "key": "payout_last",
        "visible": "ally",
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Red",
          "Red",
          "Red",
          "Red",
          "Red",
          "Blue",
          "Blue",
          "Blue",
          "Blue",
          "Blue",
          "Blue",
          "Green",
          "Green",
          "Green",
          "Green",
          "Green",
          "Green",
          "Yellow",
          "Yellow",
          "Yellow",
          "Yellow",
          "Yellow",
          "Yellow"
        ]
      },
      {
        "key": "set_aside",
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
        "key": "season",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "auction_in_season",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "auctions_done",
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
        "key": "current_card",
        "visible": "public",
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
        "key": "buyer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_yellow",
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
        "key": "value_yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "place_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "place_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "place_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "place_yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "key_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "key_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "key_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "key_yellow",
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
        "key": "cards_per_artist",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "set_aside_cards",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_money",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "seasons",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "auctions_per_season",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "total_auctions",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "value_first",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "value_second",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "value_third",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "value_fourth",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "auctioneer_share_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "min_paintings_to_be_eligible",
        "visible": "public",
        "type": "number",
        "initial": 3
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
      "label": "the deal",
      "do": [
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
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "label": "set aside and starting values",
      "do": [
        {"set": {"key": "set_aside", "value": {"calc": "deck"}}},
        {"set": {"key": "deck", "value": []}},
        {"set": {"key": "pick", "value": ""}},
        {"set": {"players": "all", "key": "money", "value": {"calc": "starting_money"}}},
        {"set": {"players": "all", "key": "paintings_bought", "value": 0}},
        {"set": {"key": "value_red", "value": 0}},
        {"set": {"key": "value_blue", "value": 0}},
        {"set": {"key": "value_green", "value": 0}},
        {"set": {"key": "value_yellow", "value": 0}},
        {"set": {"key": "count_red", "value": 0}},
        {"set": {"key": "count_blue", "value": 0}},
        {"set": {"key": "count_green", "value": 0}},
        {"set": {"key": "count_yellow", "value": 0}},
        {"set": {"key": "season", "value": 1}},
        {"set": {"key": "auction_in_season", "value": 1}},
        {"set": {"key": "auctions_done", "value": 0}}
      ]
    },
    {
      "use": "sync",
      "label": "your hand",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "money"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "auction",
      "label": "prepare the auction",
      "do": [
        {"set": {"key": "auctioneer", "value": {"calc": "((season + auction_in_season - 2) % len(players)) + 1"}}},
        {"set": {"players": "all", "key": "bid", "value": 0}},
        {"set": {"players": "all", "key": "message", "value": ""}},
        {"set": {"players": "all", "key": "nomination", "value": ""}},
        {"set": {"key": "buyer", "value": 0}},
        {"set": {"key": "high_bid", "value": 0}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[a for a in ['Red', 'Blue', 'Green', 'Yellow'] if a in you.hand]"}}}
      ]
    },
    {
      "use": "ask",
      "phase": "auction",
      "label": "choose a card",
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
        "bind": "card"
      },
      "each": {
        "do": [
          {"set": {"key": "current_card", "value": "$answer"}},
          {"remove": {"player": "$seat", "key": "hand", "value": "$answer"}}
        ]
      },
      "text": "You are the auctioneer. Choose one card from your hand to auction; it leaves your hand and its artist is announced to all."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "the artist is counted",
      "do": [
        {"adjust": {"key": "count_red", "value": 1, "if": {"calc": "current_card == 'Red'"}}},
        {"adjust": {"key": "count_blue", "value": 1, "if": {"calc": "current_card == 'Blue'"}}},
        {"adjust": {"key": "count_green", "value": 1, "if": {"calc": "current_card == 'Green'"}}},
        {"adjust": {"key": "count_yellow", "value": 1, "if": {"calc": "current_card == 'Yellow'"}}}
      ],
      "text": "Seat {auctioneer} auctions a {current_card} painting."
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
      "text": "Say one short thing to the table about the {current_card} painting. Messages are not binding."
    },
    {
      "use": "poll",
      "phase": "auction",
      "label": "sealed bid",
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
      "text": "Submit a sealed bid for the {current_card} painting: a whole number from {min_bid} to your current money. No bid is shown to anyone."
    },
    {
      "use": "update",
      "phase": "auction",
      "label": "resolve the auction",
      "do": [
        {"set": {"key": "high_bid", "value": {"calc": "max([p.bid for p in players])"}}},
        {"set": {"key": "buyer", "value": {"calc": "0 if high_bid == 0 else max([(p.bid * 4 + 3 - ((p.seat - auctioneer + 3) % 4)) * 10 + p.seat for p in players]) % 10"}}},
        {"adjust": {"player": {"calc": "buyer"}, "key": "money", "value": {"calc": "-high_bid"}, "if": {"calc": "buyer > 0"}}},
        {"adjust": {"player": {"calc": "auctioneer"}, "key": "money", "value": {"calc": "int(high_bid / auctioneer_share_divisor)"}, "if": {"calc": "buyer > 0 and buyer != auctioneer"}}},
        {"append": {"player": {"calc": "buyer"}, "key": "collection", "value": {"calc": "current_card"}, "if": {"calc": "buyer > 0"}}},
        {"adjust": {"player": {"calc": "buyer"}, "key": "paintings_bought", "value": 1, "if": {"calc": "buyer > 0"}}}
      ]
    },
    {
      "use": "tell",
      "phase": "auction",
      "label": "sold",
      "when": {
        "calc": "buyer > 0"
      },
      "to": "all",
      "text": "Seat {buyer} bought the {current_card} painting."
    },
    {
      "use": "tell",
      "phase": "auction",
      "label": "unsold",
      "when": {
        "calc": "buyer == 0"
      },
      "to": "all",
      "text": "The {current_card} painting went unsold."
    },
    {
      "use": "tell",
      "phase": "auction",
      "label": "the price",
      "when": {
        "calc": "buyer > 0"
      },
      "to": {
        "where": "you.seat == buyer or you.seat == auctioneer"
      },
      "text": "The price was {high_bid}."
    },
    {
      "use": "poll",
      "phase": "season end",
      "label": "nomination",
      "when": {
        "calc": "auction_in_season == auctions_per_season"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Red",
          "Blue",
          "Green",
          "Yellow"
        ]
      },
      "store": "nomination",
      "text": "Season {season} is ending. Secretly name one artist; your nomination adds 1 to that artist's season count. All nominations are revealed afterwards."
    },
    {
      "use": "update",
      "phase": "season end",
      "label": "rank the artists",
      "when": {
        "calc": "auction_in_season == auctions_per_season"
      },
      "do": [
        {"adjust": {"key": "count_red", "value": {"calc": "count(p.nomination == 'Red' for p in players)"}}},
        {"adjust": {"key": "count_blue", "value": {"calc": "count(p.nomination == 'Blue' for p in players)"}}},
        {"adjust": {"key": "count_green", "value": {"calc": "count(p.nomination == 'Green' for p in players)"}}},
        {"adjust": {"key": "count_yellow", "value": {"calc": "count(p.nomination == 'Yellow' for p in players)"}}},
        {"set": {"key": "key_red", "value": {"calc": "count_red * 10000 + value_red * 10 + 3 - ((5 - season) % 4)"}}},
        {"set": {"key": "key_blue", "value": {"calc": "count_blue * 10000 + value_blue * 10 + 3 - ((6 - season) % 4)"}}},
        {"set": {"key": "key_green", "value": {"calc": "count_green * 10000 + value_green * 10 + 3 - ((7 - season) % 4)"}}},
        {"set": {"key": "key_yellow", "value": {"calc": "count_yellow * 10000 + value_yellow * 10 + 3 - ((8 - season) % 4)"}}},
        {"set": {"key": "place_red", "value": {"calc": "0 if count_red == 0 or count(k > key_red for k in [key_blue, key_green, key_yellow]) >= 3 else 1 + count(k > key_red for k in [key_blue, key_green, key_yellow])"}}},
        {"set": {"key": "place_blue", "value": {"calc": "0 if count_blue == 0 or count(k > key_blue for k in [key_red, key_green, key_yellow]) >= 3 else 1 + count(k > key_blue for k in [key_red, key_green, key_yellow])"}}},
        {"set": {"key": "place_green", "value": {"calc": "0 if count_green == 0 or count(k > key_green for k in [key_red, key_blue, key_yellow]) >= 3 else 1 + count(k > key_green for k in [key_red, key_blue, key_yellow])"}}},
        {"set": {"key": "place_yellow", "value": {"calc": "0 if count_yellow == 0 or count(k > key_yellow for k in [key_red, key_blue, key_green]) >= 3 else 1 + count(k > key_yellow for k in [key_red, key_blue, key_green])"}}},
        {"adjust": {"key": "value_red", "value": {"calc": "value_first if place_red == 1 else (value_second if place_red == 2 else (value_third if place_red == 3 else value_fourth))"}}},
        {"adjust": {"key": "value_blue", "value": {"calc": "value_first if place_blue == 1 else (value_second if place_blue == 2 else (value_third if place_blue == 3 else value_fourth))"}}},
        {"adjust": {"key": "value_green", "value": {"calc": "value_first if place_green == 1 else (value_second if place_green == 2 else (value_third if place_green == 3 else value_fourth))"}}},
        {"adjust": {"key": "value_yellow", "value": {"calc": "value_first if place_yellow == 1 else (value_second if place_yellow == 2 else (value_third if place_yellow == 3 else value_fourth))"}}}
      ],
      "text": "Nominations: Seat 1 {players[0].nomination}, Seat 2 {players[1].nomination}, Seat 3 {players[2].nomination}, Seat 4 {players[3].nomination}. Season counts: Red {count_red}, Blue {count_blue}, Green {count_green}, Yellow {count_yellow}. Places (0 = did not place): Red {place_red}, Blue {place_blue}, Green {place_green}, Yellow {place_yellow}. Cumulative values: Red {value_red}, Blue {value_blue}, Green {value_green}, Yellow {value_yellow}."
    },
    {
      "use": "update",
      "phase": "season end",
      "label": "the payout",
      "when": {
        "calc": "auction_in_season == auctions_per_season"
      },
      "do": [
        {"set": {"players": "all", "key": "payout_last", "value": {"calc": "sum([(value_red if place_red > 0 else 0) if c == 'Red' else ((value_blue if place_blue > 0 else 0) if c == 'Blue' else ((value_green if place_green > 0 else 0) if c == 'Green' else (value_yellow if place_yellow > 0 else 0))) for c in you.collection])"}}},
        {"adjust": {"players": "all", "key": "money", "value": {"calc": "you.payout_last"}}}
      ],
      "text": "The bank pays out on paintings of placed artists. Cumulative values: Red {value_red}, Blue {value_blue}, Green {value_green}, Yellow {value_yellow}."
    },
    {
      "use": "tell",
      "phase": "season end",
      "label": "your payout",
      "when": {
        "calc": "auction_in_season == auctions_per_season"
      },
      "to": "acting",
      "text": "Your payout this season is {payout_last}."
    },
    {
      "use": "update",
      "phase": "season end",
      "label": "clear the season",
      "when": {
        "calc": "auction_in_season == auctions_per_season"
      },
      "do": [
        {"set": {"players": "all", "key": "collection", "value": []}},
        {"set": {"key": "count_red", "value": 0}},
        {"set": {"key": "count_blue", "value": 0}},
        {"set": {"key": "count_green", "value": 0}},
        {"set": {"key": "count_yellow", "value": 0}},
        {"set": {"key": "place_red", "value": 0}},
        {"set": {"key": "place_blue", "value": 0}},
        {"set": {"key": "place_green", "value": 0}},
        {"set": {"key": "place_yellow", "value": 0}}
      ],
      "text": "All paintings are discarded and season counts reset to 0."
    },
    {
      "use": "update",
      "phase": "advance",
      "label": "next auction",
      "do": [
        {"adjust": {"key": "auctions_done", "value": 1}},
        {"adjust": {"key": "season", "value": 1, "if": {"calc": "auction_in_season == auctions_per_season"}}},
        {"set": {"key": "auction_in_season", "value": {"calc": "1 if auction_in_season == auctions_per_season else auction_in_season + 1"}}}
      ]
    },
    {
      "use": "check",
      "phase": "advance",
      "label": "after the last auction",
      "when": {
        "calc": "auctions_done >= total_auctions"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "auctions_done >= total_auctions"
      },
      "rank_by": "(you.paintings_bought >= 3) * (you.money + 1)",
      "min_to_win": 1,
      "reveal": [
        "money"
      ],
      "text": "Winner: {result}. Final money (paintings bought): Seat 1 {players[0].money} ({players[0].paintings_bought}), Seat 2 {players[1].money} ({players[1].paintings_bought}), Seat 3 {players[2].money} ({players[2].paintings_bought}), Seat 4 {players[3].money} ({players[3].paintings_bought}); {min_paintings_to_be_eligible} paintings needed to be eligible."
    }
  },
  "limits": {
    "rounds": 16,
    "rounds_max": 16,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Four players sit in seats 1-4. The deck has {deck_size} cards: {cards_per_artist} each of Red, Blue, Green and Yellow. It is shuffled and each player is dealt {hand_size} cards as a hidden hand; the remaining {set_aside_cards} cards are set aside unseen. Each player starts with {starting_money} money. Money is hidden; each player sees only their own. Every artist starts with cumulative value 0 and season count 0.\n\nThere are {total_auctions} auctions in {seasons} seasons of {auctions_per_season}. In auction k of season s the auctioneer is seat ((s + k - 2) mod 4) + 1: Season 1: 1,2,3,4. Season 2: 2,3,4,1. Season 3: 3,4,1,2. Season 4: 4,1,2,3. Each player is auctioneer once per season and ends with 1 unused card.\n\nEACH AUCTION. (1) The auctioneer privately chooses one card from their hand and removes it from the hand. Its artist is announced to all. (2) That artist's season count rises by 1, whether or not the painting sells. (3) Talk: every player writes one short message at the same time, without seeing the others'. All messages are then shown to everyone. Messages are not binding. (4) Every player, including the auctioneer, submits a sealed bid at the same time: a whole number from {min_bid} to the bidder's current money. (5) Resolution: if the highest bid is 0, the painting is unsold and discarded and no money changes hands. Otherwise the highest bidder buys it. If several players tie for highest, the buyer is the first of them in the order seat (A mod 4)+1, seat ((A+1) mod 4)+1, seat ((A+2) mod 4)+1, then the auctioneer, where A is the auctioneer's seat (for example, with auctioneer 2 and seats 1 and 4 tied, seat 4 buys). The buyer pays the bid. If the buyer is not the auctioneer, the auctioneer receives the bid divided by {auctioneer_share_divisor}, rounded down, and the rest goes to the bank. If the auctioneer buys, the whole bid goes to the bank and the auctioneer receives nothing. The painting joins the buyer's collection, and the buyer's paintings-bought count rises by 1. (6) Everyone is told the artist and the buyer, or that the painting went unsold. The price is told privately to the buyer and to the auctioneer only. Losing bids are never revealed.\n\nSEASON END (after the 4th auction of each season). (a) Nomination: every player at the same time secretly names one of the four artists. Each nomination adds 1 to that artist's season count. All nominations are then revealed. (b) Ranking: artists are ranked by season count, higher first. Ties are broken first by higher cumulative value, then by this season's priority: Season 1 R>B>G>Y; Season 2 B>G>Y>R; Season 3 G>Y>R>B; Season 4 Y>R>B>G. An artist with season count 0 cannot place. (c) Values: add {value_first} to the cumulative value of the 1st artist, {value_second} to the 2nd and {value_third} to the 3rd. The 4th artist gains {value_fourth}. (d) Payout: for each painting a player owns of an artist that placed in the top three this season, the bank pays that player the artist's cumulative value (after step c). Paintings of an artist that did not place pay 0. Each player is told their own payout privately. The artists' cumulative values are public. (e) All owned paintings are discarded, and all season counts reset to 0.\n\nGAME END. The game ends after the Season 4 payout, and final money totals are revealed. Only players who bought at least {min_paintings_to_be_eligible} paintings during the game are eligible to win. Among eligible players, the one with the most money wins; eligible players tied for most money share the result. If no player is eligible, nobody wins."
}
````
