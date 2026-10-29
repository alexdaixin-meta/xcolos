# Task: write the XColos game file for "Pocket Smear"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

PLAYERS: exactly 3, seated as Player 1, Player 2 and Player 3. Seat order is 1, 2, 3, then back to 1.

DECK: 24 cards in three suits (Red, Blue, Green). Each suit has ranks 1 to 8. Card points, used only for Game: rank 8 = 4, rank 7 = 3, rank 6 = 2, rank 5 = 1, all other ranks = 0.

STRUCTURE: The game is 9 deals. Each deal is 4 rounds with one trick per round, so the game is 36 rounds. The dealer rotates: Player 1 deals deals 1, 4 and 7; Player 2 deals deals 2, 5 and 8; Player 3 deals deals 3, 6 and 9. For each deal, PRIORITY ORDER is: the player after the dealer in seat order, then the next player, then the dealer. All scores start at 0.

DEAL (first round of each deal): Shuffle all 24 cards and deal 4 cards privately to each player. The other 12 cards are set aside face down, unseen by anyone, for the whole deal. Each player sees only their own hand.

BID (first round of each deal, one simultaneous poll): Every player at the same moment submits ONE answer made of two parts: (a) either PASS or a whole number from 2 to 6, and (b) one suit that appears in their own hand. A suit must be named even when passing. Examples: '4 Blue', 'PASS Red'. When all answers are in, the engine reveals every player's bid amount (or PASS).
- The highest number wins. A tie goes to the tied player who comes first in priority order.
- The winner becomes the PITCHER, their number becomes the CONTRACT, and their named suit becomes TRUMP.
- If all three pass, the dealer becomes the pitcher with a contract of 2, and trump is the suit the dealer named.
- The engine announces the pitcher, the contract and trump. The suits named by the other two players are NEVER revealed.

TRICKS (each round of a deal): Three cards are played one at a time, starting with the LEADER and continuing in seat order.
- Leader: in the first trick of a deal, the leader is the pitcher, who must lead a trump card. The pitcher always holds one, because they named a suit from their hand. In later tricks of the deal, the leader is the winner of the previous trick, who may lead any card.
- Following: each later player must play a card of the led suit if they hold one, but may instead play a trump even if they hold the led suit. A player holding no card of the led suit may play any card.
- Winning: the trick goes to the highest-ranked trump played. If no trump was played, it goes to the highest-ranked card of the led suit.
- All played cards are visible to everyone. The three cards go into the trick winner's captured pile.

DEAL SCORING (after the 4th trick of each deal; only cards played this deal count; every dealt card is played):
- HIGH, 1 point: to the player who captured the highest-ranked trump played.
- LOW, 1 point: to the player who captured the lowest-ranked trump played. This may be the same card as High. At least one trump is always played, because the first lead is trump.
- GAME, 1 point: to the player whose captured pile has the most card points. If two or more players tie for most, nobody scores Game.
- THREE, 3 points: to the player who captured the trump of rank 3, if it was dealt. If it was not dealt, nobody scores it.
- Each player's deal points are the sum of the categories they won, from 0 to 6.
- Each of the two non-pitchers adds their deal points to their score.
- If the pitcher's deal points are at least the contract, the pitcher adds their deal points to their score.
- Otherwise the pitcher is SET: the pitcher subtracts the contract from their score and does not add their deal points.
- Scores may go negative. Captured piles are then cleared and the next deal begins.

COMMUNICATION: There is no table talk. Players communicate only through bids and played cards.

END: After the 9th deal is scored, the game ends.

How the winner is decided: After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Pocket Smear (3 to 3 players, best with 3)

A three-player trick-taking game of 9 four-trick deals: bid blind, the highest bidder names trump, then everyone fights for High, Low, Game and Three while the pitcher tries to make the contract.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Running total score. It may go negative.
  - each player: hand (list, starts []); only its owner sees it. Cards held this deal, as codes suit*10+rank (Red=1, Blue=2, Green=3), so 18 is Red 8 and 23 is Blue 3.
  - each player: bid (number, starts 0); everyone sees it. Bid amount this deal: 2 to 6, or 0 for PASS. It is revealed after the bid poll.
  - each player: bid_suit (text, starts ''); only its owner sees it. Suit named with the bid. It must be in the player's hand and is never revealed, except that the pitcher's suit becomes trump.
  - each player: played_card (number, starts 0); everyone sees it. Card code played in the current trick, or 0 if none yet.
  - each player: captured (list, starts []); everyone sees it. Cards captured in tricks this deal.
  - each player: captured_points (number, starts 0); everyone sees it. Sum of card points in the captured pile this deal: rank 8 = 4, 7 = 3, 6 = 2, 5 = 1, others 0.
  - each player: deal_points (number, starts 0); everyone sees it. Category points won in this deal, from 0 to 6.
  - the table: deck (list, starts [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38]); hidden from all players. Undealt cards. It is rebuilt to all 24 cards at the start of each deal.
  - the table: set_aside (list, starts []); hidden from all players. The 12 cards set aside face down and unseen for the deal.
  - the table: rounds_played (number, starts 0); everyone sees it. Tricks completed so far, from 0 to 36.
  - the table: deal_number (number, starts 1); everyone sees it. Current deal, from 1 to 9.
  - the table: trick_in_deal (number, starts 1); everyone sees it. Current trick within the deal, from 1 to 4.
  - the table: dealer (number, starts 1); everyone sees it. Dealer seat: ((deal_number - 1) mod 3) + 1.
  - the table: pitcher (number, starts 0); everyone sees it. Seat of the bid winner this deal.
  - the table: contract (number, starts 0); everyone sees it. The pitcher's winning bid, or 2 if all passed.
  - the table: trump (number, starts 0); everyone sees it. Trump suit code (1 Red, 2 Blue, 3 Green): the pitcher's named suit.
  - the table: leader (number, starts 0); everyone sees it. Seat that leads the current trick.
  - the table: led_suit (number, starts 0); everyone sees it. Suit code of the card led in the current trick.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the last trick.
  - the table: high_trump_rank (number, starts 0); hidden from all players. Highest trump rank played this deal (0 = none yet).
  - the table: high_trump_seat (number, starts 0); hidden from all players. Seat that captured the highest trump played.
  - the table: low_trump_rank (number, starts 9); hidden from all players. Lowest trump rank played this deal (9 = none yet).
  - the table: low_trump_seat (number, starts 0); hidden from all players. Seat that captured the lowest trump played.
  - the table: three_seat (number, starts 0); hidden from all players. Seat that captured the trump 3 this deal (0 = not played or not dealt).
  - parameters, each kept as a table attribute: players = 3, deals = 9, tricks_per_deal = 4, total_rounds = 36, suits = 3, ranks_per_suit = 8, deck_size = 24, hand_size = 4, set_aside_cards = 12, bid_min = 2, bid_max = 6, pass_value = 0, all_pass_contract = 2, card_points_rank_8 = 4, card_points_rank_7 = 3, card_points_rank_6 = 2, card_points_rank_5 = 1, card_points_other_ranks = 0, high_points = 1, low_points = 1, game_points = 1, three_points = 3, three_rank = 3, max_deal_points = 6, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the 3 players as Player 1, Player 2 and Player 3; seat order is 1, 2, 3, then back to 1.
  2. Set every score to 0, deal_number to 1, trick_in_deal to 1 and rounds_played to 0.
  3. Encode the 24 cards as suit*10+rank, with Red=1, Blue=2, Green=3 and ranks 1 to 8; they are shown to players as names such as 'Red 8'.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When trick_in_deal == 1: dealer = ((deal_number - 1) mod 3) + 1; deck = all 24 card codes; for each player, clear hand, captured and played_card, and set captured_points = 0, deal_points = 0, bid = 0, bid_suit = ''; draw 4 cards at random from deck into each player's hand; move the remaining 12 deck cards into set_aside; reset high_trump_rank = 0, high_trump_seat = 0, low_trump_rank = 9, low_trump_seat = 0, three_seat = 0.
  2. [sync] all players. What happens: When trick_in_deal == 1: each player sees their own hand, the dealer and every score.
  3. [poll] all players answers: One choice from: 'PASS <suit>' or '<n> <suit>' for n in 2..6, where <suit> is any suit present in the player's own hand. What happens: When trick_in_deal == 1: bid = n (0 for PASS); bid_suit = the named suit. The bid amounts are broadcast: 'Seat {seat} bids {bid or PASS}'. The suits are not shown.
  4. [update] all players. What happens: When trick_in_deal == 1: if max(bid) > 0, pitcher = the seat with the highest bid, ties going to the earliest seat in priority order (dealer+1, dealer+2, dealer, mod 3), and contract = that bid; otherwise pitcher = dealer and contract = 2. trump = pitcher's bid_suit; leader = pitcher.
  5. [tell] all players. What happens: When trick_in_deal == 1: announce 'Pitcher: Seat {pitcher}, contract {contract}, trump {trump}'.
  6. [ask] seat leader answers: A card from own hand; on trick_in_deal == 1 only trump cards are offered. What happens: played_card = chosen card; remove it from hand; led_suit = floor(card/10); broadcast the card to all.
  7. [ask] seat (leader mod 3) + 1 answers: A legal card from own hand: if the hand holds the led suit, cards of the led suit plus any trumps; otherwise any card. What happens: played_card = chosen card; remove it from hand; broadcast the card to all.
  8. [ask] seat ((leader + 1) mod 3) + 1 answers: A legal card from own hand, by the same following rule. What happens: played_card = chosen card; remove it from hand; broadcast the card to all.
  9. [update] all players. What happens: trick_winner = the seat whose played_card has suit == trump and the highest rank, or if no trump was played, the seat with the highest rank of led_suit. Append all three played cards to trick_winner's captured; add their card points to trick_winner's captured_points. For each played trump of rank r: if r > high_trump_rank, set high_trump_rank = r and high_trump_seat = trick_winner; if r < low_trump_rank, set low_trump_rank = r and low_trump_seat = trick_winner; if r == 3, set three_seat = trick_winner. Then leader = trick_winner, clear every played_card and announce the winner.
  10. [update] all players. What happens: When trick_in_deal == 4: deal_points = (seat == high_trump_seat ? 1 : 0) + (seat == low_trump_seat ? 1 : 0) + (captured_points strictly greater than both other players' captured_points ? 1 : 0) + (seat == three_seat ? 3 : 0). For each non-pitcher, score += deal_points. For the pitcher: if deal_points >= contract, score += deal_points; else score -= contract. Announce every deal_points value and score. Clear every captured pile.
  11. [update] all players. What happens: rounds_played += 1; if trick_in_deal == 4, then trick_in_deal = 1 and deal_number += 1; otherwise trick_in_deal += 1.
  12. [check] all players. What happens: End the game if rounds_played == 36 (9 deals scored); otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When deal d begins, then the dealer is seat ((d-1) mod 3)+1: seat 1 deals deals 1, 4 and 7, seat 2 deals 2, 5 and 8, and seat 3 deals 3, 6 and 9.
  R2. When a deal begins, then all 24 cards are shuffled, each player receives exactly 4 private cards, and the other 12 are set aside unseen for the whole deal.
  R3. When bidding, then every player answers at once with PASS or a number from 2 to 6, plus one suit present in their own hand; a suit is named even when passing.
  R4. When the bids are in, then every player's amount or PASS is revealed, and the suits of the two non-pitchers are never revealed.
  R5. When bids differ, then the highest number wins: that player becomes pitcher, the number becomes the contract and the named suit becomes trump.
  R6. When the highest bid is tied, then the tied player earliest in priority order (dealer+1, then dealer+2, then dealer) wins the bid.
  R7. When all three players pass, then the dealer becomes pitcher with contract 2, and trump is the dealer's named suit.
  R8. When the first trick of a deal is played, then the pitcher leads and must lead a trump card.
  R9. When a later trick of a deal is played, then the winner of the previous trick leads any card.
  R10. When a trick is played, then the cards go one at a time from the leader in seat order.
  R11. When a following player holds the led suit, then they must play the led suit or a trump.
  R12. When a following player holds no card of the led suit, then they may play any card.
  R13. When at least one trump is in a trick, then the highest-ranked trump wins it; otherwise the highest-ranked card of the led suit wins it.
  R14. When a trick is won, then all three cards are visible to everyone and go into the winner's captured pile.
  R15. When a deal is scored, then 1 point (High) goes to the player who captured the highest-ranked trump played.
  R16. When a deal is scored, then 1 point (Low) goes to the player who captured the lowest-ranked trump played, which may be the same card as High.
  R17. When a deal is scored, then 1 point (Game) goes to the player with the most captured card points (rank 8 = 4, 7 = 3, 6 = 2, 5 = 1, others 0), and nobody scores Game if two or more players tie for most.
  R18. When the trump 3 was dealt and played, then 3 points (Three) go to the player who captured it; if it was not dealt, nobody scores Three.
  R19. When a deal is scored, then each non-pitcher adds their deal points (0 to 6) to their score.
  R20. When the pitcher's deal points are at least the contract, then the pitcher adds their deal points to their score.
  R21. When the pitcher's deal points are below the contract, then the pitcher is set: they subtract the contract from their score and add nothing; scores may go negative.
  R22. When the 9th deal (36th trick) has been scored, then the game ends and the highest total score wins; players tied for highest share it, which the source calls a draw.
  R23. When playing, then there is no table talk: players communicate only through bids and played cards.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid poll | asked: all seats | options: For each suit S present in the seat's own hand: 'PASS S', '2 S', '3 S', '4 S', '5 S', '6 S'. Suits not in the hand are never offered.
  - Lead card | asked: the leader | options: First trick of a deal (the pitcher leading): only the trump cards in their hand. Later tricks: every card in their hand.
  - Follow card (second and third player) | asked: the two seats after the leader, in seat order | options: If the hand holds the led suit: every card of the led suit plus every trump in the hand. If the hand holds no card of the led suit: every card in the hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: rounds_played == 36
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after 9 deals; the highest score wins, and players tied for highest share the result (the source calls this a draw).
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

- each player: `score` (number, visible: public, starts 0): Running total score. It may go negative.
- each player: `bid` (number, visible: public, starts 0): Bid amount this deal: 2 to 6, or 0 for PASS. It is revealed after the bid poll.
- the table: `deal_number` (number, visible: public, starts 1): Current deal, from 1 to 9.
- the table: `pitcher` (number, visible: public, starts 0): Seat of the bid winner this deal.
- the table: `contract` (number, visible: public, starts 0): The pitcher's winning bid, or 2 if all passed.
- the table: `trump` (number, visible: public, starts 0): Trump suit code (1 Red, 2 Blue, 3 Green): the pitcher's named suit.
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 3, deals = 9, tricks_per_deal = 4, total_rounds = 36, suits = 3, ranks_per_suit = 8, deck_size = 24, hand_size = 4, set_aside_cards = 12, bid_min = 2, bid_max = 6, pass_value = 0, all_pass_contract = 2, card_points_rank_8 = 4, card_points_rank_7 = 3, card_points_rank_6 = 2, card_points_rank_5 = 1, card_points_other_ranks = 0, high_points = 1, low_points = 1, game_points = 1, three_points = 3, three_rank = 3, max_deal_points = 6, starting_score = 0
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
