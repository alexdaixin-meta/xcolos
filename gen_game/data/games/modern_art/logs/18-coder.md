# 18 coder

- time: 2026-10-27T18:34:42+00:00 (99.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 6f841731425c08de, reply sha256 a3c6c3cf14fb9703

## Sent

````
# Task: write the XColos game file for "Modern Art: Private Collections"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
- There are exactly 4 players, in seats 1 to 4.
- There are five artists: A, B, C, D and E. The deck has 20 cards, 4 of each artist.
- Shuffle the deck and deal 5 cards to each player. Each hand is private: only its owner sees it.
- Each player starts with 100 money. Money is public.
- Each artist has a MARKET COUNT, starting at 0. Market counts are public.
- Each player has a COLLECTION, starting empty. Collections are public.
- Draw one seat at random to be the auctioneer in round 1.

EACH ROUND (12 rounds)
1. OFFER. The auctioneer chooses one card from their own hand. It is removed from the hand and revealed as the painting for sale. That artist's market count rises by 1, whether or not the painting sells.
2. TALK. Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages bind nobody, and players may lie.
3. BID. All 4 players, including the auctioneer, secretly and simultaneously choose a bid. A bid is any whole number from 0 up to the player's current money. A bid above the player's money counts as all of their money.
4. RESOLVE.
   a. If every bid is 0, the auctioneer keeps the painting for free.
   b. Otherwise the highest bid wins.
   c. The auctioneer wins only if their bid is strictly higher than every other bid. If the auctioneer wins, they pay their bid to the bank.
   d. If one non-auctioneer has the highest bid, that player wins and pays their bid to the auctioneer.
   e. If two or more non-auctioneers tie for the highest bid (and the auctioneer did not bid more), the tied player with the least current money wins and pays their bid to the auctioneer.
   f. If the tied players also have equal money, the painting is discarded unsold and nobody pays. The market count still keeps its +1.
   g. A won painting goes into the winner's collection and stays there to the end.
5. REVEAL. All four bids, the winner (if any) and the price paid are announced.
6. ROTATE. The auctioneer role passes clockwise to the next seat, so each seat is auctioneer in exactly 3 rounds.
- Each player auctions 3 of their 5 cards. Their remaining 2 cards are never played and never count.

END OF GAME (after round 12)
1. Rank the five artists by market count, highest first. Ties are broken alphabetically: A above B above C above D above E.
2. Each painting in a collection is worth: 60 if its artist ranks 1st, 40 if 2nd, 20 if 3rd, and 0 if 4th or 5th.
3. Each player's SCORE is their money plus the total value of their collection.

How the winner is decided: After round 12, the player with the highest score (money plus collection value) wins. If two or more players tie for the highest score, the game is a draw between them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Modern Art: Private Collections (4 to 4 players, best with 4)

Four players take turns auctioning paintings from five artists in sealed simultaneous bids over 12 rounds. At the end, paintings by the three most-offered artists pay out, and money plus collection value decides the winner.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Cards held, each one of A, B, C, D or E. Only the owner sees them.
  - each player: money (number, starts 100); everyone sees it. Current money.
  - each player: collection (list, starts []); everyone sees it. Paintings won, listed by artist letter. They stay to the end.
  - each player: coll_a (number, starts 0); everyone sees it. Number of A paintings in the collection (mirror of collection, used for arithmetic).
  - each player: coll_b (number, starts 0); everyone sees it. Number of B paintings in the collection.
  - each player: coll_c (number, starts 0); everyone sees it. Number of C paintings in the collection.
  - each player: coll_d (number, starts 0); everyone sees it. Number of D paintings in the collection.
  - each player: coll_e (number, starts 0); everyone sees it. Number of E paintings in the collection.
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid. All bids are announced at REVEAL.
  - each player: score (number, starts 0); everyone sees it. Money plus collection value, computed at game end.
  - the table: deck (list, starts ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E']); hidden from all players. Undealt cards.
  - the table: market_a (number, starts 0); everyone sees it. Market count of artist A.
  - the table: market_b (number, starts 0); everyone sees it. Market count of artist B.
  - the table: market_c (number, starts 0); everyone sees it. Market count of artist C.
  - the table: market_d (number, starts 0); everyone sees it. Market count of artist D.
  - the table: market_e (number, starts 0); everyone sees it. Market count of artist E.
  - the table: auctioneer (number, starts 1); everyone sees it. Seat of this round's auctioneer.
  - the table: round_no (number, starts 1); everyone sees it. Current round, 1 to 12. It becomes 13 after the last round.
  - the table: painting (text, starts ''); everyone sees it. Artist letter of the painting for sale this round.
  - the table: winner_seat (number, starts 0); everyone sees it. Seat that won this round's painting, or 0 if it was discarded.
  - the table: price (number, starts 0); everyone sees it. Price paid this round.
  - the table: value_a (number, starts 0); everyone sees it. End-of-game value of an A painting (60/40/20/0).
  - the table: value_b (number, starts 0); everyone sees it. End-of-game value of a B painting.
  - the table: value_c (number, starts 0); everyone sees it. End-of-game value of a C painting.
  - the table: value_d (number, starts 0); everyone sees it. End-of-game value of a D painting.
  - the table: value_e (number, starts 0); everyone sees it. End-of-game value of an E painting.
  - parameters, each kept as a table attribute: players = 4, artists = 5, cards_per_artist = 4, deck_size = 20, hand_size = 5, starting_money = 100, rounds = 12, auctions_per_seat = 3, unplayed_cards_per_seat = 2, value_rank_1 = 60, value_rank_2 = 40, value_rank_3 = 20, value_rank_4_5 = 0, min_bid = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 4 players in seats 1 to 4.
  2. The deck holds 20 cards: 4 each of artists A, B, C, D and E.
  3. Deal 5 cards to each player by drawing at random from deck into the player's hand; the deck ends empty. Hands are visible only to their owners.
  4. Each player starts with money 100, an empty collection, all coll_* counts 0 and score 0.
  5. All five market counts start at 0.
  6. Draw one seat at random and set auctioneer to it; set round_no to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [ask] the seat equal to auctioneer answers: one card from their own hand (A, B, C, D or E, as held). What happens: Remove one copy of the chosen card from the auctioneer's hand; set painting to its artist; add 1 to market_<artist>, whether or not it later sells.
  2. [tell] all players. What happens: Announce: 'Round {round_no}: Seat {auctioneer} offers a painting by {painting}. Market counts A {market_a}, B {market_b}, C {market_c}, D {market_d}, E {market_e}.'
  3. [poll] all players answers: one short free-text message. What happens: Once all messages are in, broadcast them to all: 'Seat {seat} says: {value}'. Messages bind nobody.
  4. [poll] all players answers: a whole number from 0 to the player's current money. What happens: Set each player's bid. Bids stay hidden until REVEAL.
  5. [update] all players. What happens: Let H be the maximum bid. (a) If H = 0: winner_seat = auctioneer, price = 0, and nobody pays. (c) Else, if the auctioneer's bid = H and no other bid equals H: winner_seat = auctioneer, price = H, and the auctioneer's money decreases by H (paid to the bank). (d) Else, if exactly one non-auctioneer bid H: that seat wins, price = H, its money decreases by H and the auctioneer's money increases by H. (e) Else, among the non-auctioneers who bid H, let M be the least money: if exactly one of them has money M, that seat wins and pays H to the auctioneer as in (d); (f) otherwise winner_seat = 0, price = 0, nobody pays and the painting is discarded, while the market count keeps its +1. (g) If winner_seat > 0, append painting to that seat's collection and add 1 to its coll_<painting>.
  6. [tell] all players. What happens: Announce all four bids (Seat 1..4: bid), the winner_seat (or 'discarded unsold' if 0) and the price.
  7. [update] all players. What happens: auctioneer = (auctioneer mod 4) + 1; round_no increases by 1.
  8. [update] all players. What happens: When round_no = 13: for each artist X with alphabet index i (A=0 .. E=4), let key_X = market_X * 10 + (4 - i) and rank_X = 1 + the number of artists whose key is greater than key_X; set value_X = 60 if rank_X = 1, 40 if rank_X = 2, 20 if rank_X = 3, else 0. Then for each player, score = money + coll_a*value_a + coll_b*value_b + coll_c*value_c + coll_d*value_d + coll_e*value_e.
  9. [check] all players. What happens: End the game if round_no > 12; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the 4 players is dealt 5 cards from a 20-card deck (4 each of A-E), leaving the deck empty, and each hand is visible only to its owner.
  R2. At setup, each player has money 100 and an empty collection, and every market count is 0.
  R3. At setup, the round-1 auctioneer is one seat drawn at random.
  R4. When the auctioneer offers a card, one copy of it is removed from their hand, painting is set to its artist, and that artist's market count rises by 1.
  R5. When a painting is discarded unsold, its artist's market count still keeps the +1 from being offered.
  R6. Each round every player sends one talk message simultaneously, and all four messages are then shown to everyone.
  R7. Each round every player, including the auctioneer, submits a sealed bid from 0 to their current money, simultaneously.
  R8. When every bid is 0, the auctioneer gets the painting into their collection and nobody's money changes.
  R9. When the auctioneer's bid is strictly higher than every other bid (e.g. 30 vs 20, 10, 0), the auctioneer gets the painting and their money falls by 30, paid to the bank.
  R10. When the auctioneer ties the highest non-auctioneer bid (e.g. both bid 30), the auctioneer does not win and the non-auctioneer resolution applies.
  R11. When a single non-auctioneer has the highest bid (e.g. 40), that player gets the painting, their money falls by 40, and the auctioneer's money rises by 40.
  R12. When two or more non-auctioneers tie for the highest bid and one of them has strictly the least money, that player wins and pays their bid to the auctioneer.
  R13. When the tied non-auctioneers with the least money are two or more with equal money, the painting is discarded, winner_seat is 0, and nobody pays.
  R14. A won painting is appended to the winner's collection and stays there until the end of the game.
  R15. After each auction, all four bids, the winner (or 'discarded') and the price paid are announced to everyone.
  R16. After each round, the auctioneer becomes (auctioneer mod 4) + 1, so each seat auctions in exactly 3 of the 12 rounds.
  R17. The game ends after round 12, and the 2 cards each player never offered count for nothing.
  R18. At game end, artists are ranked by market count, highest first, with ties broken alphabetically (A above B above C above D above E).
  R19. At game end, a painting is worth 60 if its artist ranks 1st, 40 if 2nd, 20 if 3rd, and 0 if 4th or 5th.
  R20. At game end, each player's score is their money plus the total value of their collection, and the highest score wins, with tied top scores sharing the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - OFFER: which card to auction | asked: the seat equal to auctioneer | options: each artist letter currently in that seat's hand (one option per distinct letter held); other seats are not asked
  - TALK: one short message | asked: every seat | options: free text
  - BID: sealed bid | asked: every seat, including the auctioneer | options: a whole number from 0 to that seat's current money

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_no > 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After round 12, each player's score is their money plus the value of their collection. The highest score wins, and players tied at the top share the win (a draw between them).
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

- each player: `money` (number, visible: public, starts 100): Current money.
- each player: `collection` (list, visible: public, starts []): Paintings won, listed by artist letter. They stay to the end.
- each player: `score` (number, visible: public, starts 0): Money plus collection value, computed at game end.
- the table: `market_a` (number, visible: public, starts 0): Market count of artist A.
- the table: `market_b` (number, visible: public, starts 0): Market count of artist B.
- the table: `market_c` (number, visible: public, starts 0): Market count of artist C.
- the table: `market_d` (number, visible: public, starts 0): Market count of artist D.
- the table: `market_e` (number, visible: public, starts 0): Market count of artist E.
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 4, artists = 5, cards_per_artist = 4, deck_size = 20, hand_size = 5, starting_money = 100, rounds = 12, auctions_per_seat = 3, unplayed_cards_per_seat = 2, value_rank_1 = 60, value_rank_2 = 40, value_rank_3 = 20, value_rank_4_5 = 0, min_bid = 0
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
    "id": "modern_art_private_collections",
    "name": "Modern Art: Private Collections",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four collectors auction paintings by five artists in sealed simultaneous bids over 12 rounds; money plus collection value wins."
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
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "collection",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "coll_a",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "coll_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "coll_c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "coll_d",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "coll_e",
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
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": ["A", "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C", "D", "D", "D", "D", "E", "E", "E", "E"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "market_a",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "market_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "market_c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "market_d",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "market_e",
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
        "key": "round_no",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "painting",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "winner_seat",
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
        "key": "last_bids",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "value_a",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_c",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_d",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_e",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "others_high",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "auc_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "least",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "cands",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "keys",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "artists",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_artist",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "starting_money",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "auctions_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "unplayed_cards_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_rank_1",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "value_rank_2",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "value_rank_3",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "value_rank_4_5",
        "visible": "public",
        "type": "number",
        "initial": 0
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
      "label": "deal the hands",
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
      "label": "starting state",
      "do": [
        {"set": {"players": "all", "key": "money", "value": {"calc": "starting_money"}}},
        {"set": {"players": "all", "key": "collection", "value": []}},
        {"set": {"players": "all", "key": "coll_a", "value": 0}},
        {"set": {"players": "all", "key": "coll_b", "value": 0}},
        {"set": {"players": "all", "key": "coll_c", "value": 0}},
        {"set": {"players": "all", "key": "coll_d", "value": 0}},
        {"set": {"players": "all", "key": "coll_e", "value": 0}},
        {"set": {"players": "all", "key": "score", "value": 0}},
        {"set": {"key": "market_a", "value": 0}},
        {"set": {"key": "market_b", "value": 0}},
        {"set": {"key": "market_c", "value": 0}},
        {"set": {"key": "market_d", "value": 0}},
        {"set": {"key": "market_e", "value": 0}},
        {"set": {"key": "auctioneer", "value": {"calc": "min(players, 1 + int(uniform(0, players)))"}}},
        {"set": {"key": "round_no", "value": 1}}
      ],
      "text": "Seat {auctioneer} is drawn at random to be the first auctioneer."
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
      "phase": "offer",
      "label": "prepare the round",
      "do": [
        {"set": {"players": "all", "key": "offer", "value": {"calc": "[x for x in ['A', 'B', 'C', 'D', 'E'] if x in you.hand]"}}},
        {"set": {"players": "all", "key": "bid", "value": 0}}
      ]
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "the offer",
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
      "text": "Round {round_no}: you are the auctioneer. Choose one card from your hand to put up for auction. Its artist's market count rises by 1 whether or not it sells."
    },
    {
      "use": "update",
      "phase": "offer",
      "label": "the painting is revealed",
      "do": [
        {"remove": {"player": {"calc": "auctioneer"}, "key": "hand", "value": "$card"}},
        {"set": {"key": "painting", "value": "$card"}},
        {"adjust": {"key": "market_a", "value": 1, "if": {"calc": "painting == 'A'"}}},
        {"adjust": {"key": "market_b", "value": 1, "if": {"calc": "painting == 'B'"}}},
        {"adjust": {"key": "market_c", "value": 1, "if": {"calc": "painting == 'C'"}}},
        {"adjust": {"key": "market_d", "value": 1, "if": {"calc": "painting == 'D'"}}},
        {"adjust": {"key": "market_e", "value": 1, "if": {"calc": "painting == 'E'"}}}
      ]
    },
    {
      "use": "tell",
      "phase": "offer",
      "label": "the painting for sale",
      "to": "all",
      "text": "Round {round_no}: Seat {auctioneer} offers a painting by {painting}. Market counts A {market_a}, B {market_b}, C {market_c}, D {market_d}, E {market_e}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table about the {painting} painting. Everyone writes at the same time; messages bind nobody and may be lies."
    },
    {
      "use": "poll",
      "phase": "bid",
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
      "text": "Round {round_no}: Seat {auctioneer} is selling a {painting} painting. Enter your sealed bid, a whole number from {min_bid} to your current money. All bids are revealed after everyone has bid."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the auction",
      "do": [
        {"set": {"players": "all", "key": "bid", "value": {"calc": "min(you.bid, you.money)"}}},
        {"set": {"key": "last_bids", "value": {"calc": "[p.bid for p in players]"}}},
        {"set": {"key": "high", "value": {"calc": "max([p.bid for p in players])"}}},
        {"set": {"key": "others_high", "value": {"calc": "max([p.bid for p in players if p.seat != auctioneer])"}}},
        {"set": {"key": "auc_bid", "value": {"calc": "sum([p.bid for p in players if p.seat == auctioneer])"}}},
        {"set": {"key": "tied", "value": {"calc": "[p.seat for p in players if p.seat != auctioneer and p.bid == high]"}}},
        {"set": {"key": "least", "value": {"calc": "min([p.money for p in players if p.seat in tied] + [starting_money * players])"}}},
        {"set": {"key": "cands", "value": {"calc": "[p.seat for p in players if p.seat in tied and p.money == least]"}}},
        {"set": {"key": "winner_seat", "value": {"calc": "auctioneer if high == 0 else (auctioneer if auc_bid > others_high else (sum(cands) if len(cands) == 1 else 0))"}}},
        {"set": {"key": "price", "value": {"calc": "0 if (winner_seat == 0 or high == 0) else high"}}},
        {"adjust": {"player": {"calc": "winner_seat"}, "key": "money", "value": {"calc": "-price"}, "if": {"calc": "winner_seat > 0 and price > 0"}}},
        {"adjust": {"player": {"calc": "auctioneer"}, "key": "money", "value": {"calc": "price"}, "if": {"calc": "winner_seat > 0 and winner_seat != auctioneer and price > 0"}}},
        {"append": {"player": {"calc": "winner_seat"}, "key": "collection", "value": {"calc": "painting"}, "if": {"calc": "winner_seat > 0"}}},
        {"adjust": {"player": {"calc": "winner_seat"}, "key": "coll_a", "value": 1, "if": {"calc": "winner_seat > 0 and painting == 'A'"}}},
        {"adjust": {"player": {"calc": "winner_seat"}, "key": "coll_b", "value": 1, "if": {"calc": "winner_seat > 0 and painting == 'B'"}}},
        {"adjust": {"player": {"calc": "winner_seat"}, "key": "coll_c", "value": 1, "if": {"calc": "winner_seat > 0 and painting == 'C'"}}},
        {"adjust": {"player": {"calc": "winner_seat"}, "key": "coll_d", "value": 1, "if": {"calc": "winner_seat > 0 and painting == 'D'"}}},
        {"adjust": {"player": {"calc": "winner_seat"}, "key": "coll_e", "value": 1, "if": {"calc": "winner_seat > 0 and painting == 'E'"}}}
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the sale",
      "when": {
        "calc": "winner_seat > 0"
      },
      "to": "all",
      "text": "Round {round_no} bids, seats 1 to 4: {last_bids}. Seat {winner_seat} wins the {painting} painting for a price of {price}."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "discarded unsold",
      "when": {
        "calc": "winner_seat == 0"
      },
      "to": "all",
      "text": "Round {round_no} bids, seats 1 to 4: {last_bids}. The highest non-auctioneer bidders tied with equal money: the {painting} painting is discarded unsold, price {price}, nobody pays. Its market count keeps its +1."
    },
    {
      "use": "update",
      "phase": "rotate",
      "label": "rotate the auctioneer",
      "do": [
        {"set": {"key": "auctioneer", "value": {"calc": "auctioneer % players + 1"}}},
        {"adjust": {"key": "round_no", "value": 1}}
      ]
    },
    {
      "use": "update",
      "phase": "rotate",
      "label": "final valuation",
      "when": {
        "calc": "round_no > rounds"
      },
      "do": [
        {"set": {"key": "keys", "value": {"calc": "[market_a * 10 + 4, market_b * 10 + 3, market_c * 10 + 2, market_d * 10 + 1, market_e * 10]"}}},
        {"set": {"key": "value_a", "value": {"calc": "[value_rank_1, value_rank_2, value_rank_3, value_rank_4_5, value_rank_4_5][count(k > keys[0] for k in keys)]"}}},
        {"set": {"key": "value_b", "value": {"calc": "[value_rank_1, value_rank_2, value_rank_3, value_rank_4_5, value_rank_4_5][count(k > keys[1] for k in keys)]"}}},
        {"set": {"key": "value_c", "value": {"calc": "[value_rank_1, value_rank_2, value_rank_3, value_rank_4_5, value_rank_4_5][count(k > keys[2] for k in keys)]"}}},
        {"set": {"key": "value_d", "value": {"calc": "[value_rank_1, value_rank_2, value_rank_3, value_rank_4_5, value_rank_4_5][count(k > keys[3] for k in keys)]"}}},
        {"set": {"key": "value_e", "value": {"calc": "[value_rank_1, value_rank_2, value_rank_3, value_rank_4_5, value_rank_4_5][count(k > keys[4] for k in keys)]"}}},
        {"set": {"players": "all", "key": "score", "value": {"calc": "you.money + you.coll_a * value_a + you.coll_b * value_b + you.coll_c * value_c + you.coll_d * value_d + you.coll_e * value_e"}}}
      ],
      "text": "Final painting values: A {value_a}, B {value_b}, C {value_c}, D {value_d}, E {value_e}."
    },
    {
      "use": "check",
      "phase": "rotate",
      "label": "after round 12",
      "when": {
        "calc": "round_no > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_no > rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}, Seat 4 {players[3].score}; painting values A {value_a}, B {value_b}, C {value_c}, D {value_d}, E {value_e}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "SETUP. {players} players, seats 1 to 4. There are {artists} artists: A, B, C, D and E. The deck has {deck_size} cards, {cards_per_artist} of each artist. The deck is shuffled and {hand_size} cards are dealt to each player; each hand is private, only its owner sees it. Each player starts with {starting_money} money; money is public. Each artist has a public market count, starting at 0. Each player has a public collection, starting empty. One seat is drawn at random to be the auctioneer in round 1.\n\nEACH ROUND ({rounds} rounds).\n1. OFFER. The auctioneer chooses one card from their own hand. It is removed from the hand and revealed as the painting for sale. That artist's market count rises by 1, whether or not the painting sells.\n2. TALK. Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages bind nobody, and players may lie.\n3. BID. All 4 players, including the auctioneer, secretly and simultaneously choose a bid: any whole number from {min_bid} up to the player's current money. A bid above the player's money counts as all of their money.\n4. RESOLVE.\n a. If every bid is 0, the auctioneer keeps the painting for free.\n b. Otherwise the highest bid wins.\n c. The auctioneer wins only if their bid is strictly higher than every other bid. If the auctioneer wins, they pay their bid to the bank. If the auctioneer only ties the highest other bid, the auctioneer does not win and the rules below apply.\n d. If one non-auctioneer has the highest bid, that player wins and pays their bid to the auctioneer.\n e. If two or more non-auctioneers tie for the highest bid (and the auctioneer did not bid more), the tied player with the least current money wins and pays their bid to the auctioneer.\n f. If the tied players also have equal money, the painting is discarded unsold and nobody pays. The market count still keeps its +1.\n g. A won painting goes into the winner's collection and stays there to the end.\n5. REVEAL. All four bids, the winner (if any) and the price paid are announced.\n6. ROTATE. The auctioneer role passes clockwise to the next seat (seat 4 passes to seat 1), so each seat is auctioneer in exactly {auctions_per_seat} rounds. Each player auctions {auctions_per_seat} of their {hand_size} cards; their remaining {unplayed_cards_per_seat} cards are never played and never count.\n\nEND OF GAME (after round {rounds}).\n1. Rank the five artists by market count, highest first. Ties are broken alphabetically: A above B above C above D above E.\n2. Each painting in a collection is worth {value_rank_1} if its artist ranks 1st, {value_rank_2} if 2nd, {value_rank_3} if 3rd, and {value_rank_4_5} if 4th or 5th.\n3. Each player's score is their money plus the total value of their collection. The highest score wins; players tied for the highest score share the win (a draw between them)."
}
```
````
