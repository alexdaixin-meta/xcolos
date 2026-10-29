# 31 coder

- time: 2026-10-27T18:41:58+00:00 (91.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 a8aed06eafe2baad, reply sha256 7e9abf16faf90c99

## Sent

````
# Task: write the XColos game file for "Nyet! Contract Veto"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. The deck has 20 cards in four colours (Red, Blue, Green, Yellow), each numbered 1 to 5. Seats are 1, 2 and 3. Clockwise means 1 to 2, 2 to 3, and 3 to 1. All scores start at 0. The game has 6 deals. Each deal is 6 rounds: one setup round, then 5 trick rounds. That makes 36 rounds in total.

SETUP ROUND (first round of each deal).
1. Shuffle the deck. Deal 5 cards to each player, each hand seen only by its owner. The remaining 5 cards form the Widow, face down, seen by nobody until the game ends.
2. The Lone is seat 1 in deals 1 and 4, seat 2 in deals 2 and 5, and seat 3 in deals 3 and 6. The other two players are the Pair. This is announced.
3. TALK. All three players write one short message at the same moment, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
4. VETO. The two Pair members at the same moment each name one colour to ban. Both bans are then announced. If both ban the same colour, three colours remain unbanned. Otherwise two remain.
5. CONTRACT. The Lone chooses three things in one decision and announces them:
   (a) trump, which must be one of the unbanned colours;
   (b) the first leader, which may be any of the three seats;
   (c) the bid, a whole number from 0 to 5: the exact number of tricks the Lone promises to win this deal.

TRICK ROUNDS (rounds 2 to 6 of each deal, one trick each).
6. The leader plays one card face up. On the first trick, the leader is the player the Lone named. On later tricks, the leader is the winner of the previous trick. The led card's colour is the led colour.
7. The next player clockwise plays one card, then the remaining player plays one card. A player holding a card of the led colour must play one. A player holding none may play any card.
8. The trick winner is the player of the highest-numbered trump, if any trump was played. Otherwise, it is the player of the highest-numbered card of the led colour. There are no ties.
9. The trick winner gains 1 point, whether they are the Lone or a Pair member. The number of tricks the Lone has won this deal is tracked. The winner, the scores and the Lone's trick count are announced.
10. CONTRACT SCORING (after the 5th trick of the deal). Compare the Lone's tricks T with the bid B:
   - If T equals B, the Lone gains 6.
   - If T and B differ by exactly 1, the Lone gains 2 and each Pair member gains 1.
   - If T and B differ by 2 or more, each Pair member gains 3.
   The result is announced.
11. After deal 6 is scored, the game ends.

How the winner is decided: After 36 rounds (6 deals), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Nyet! Contract Veto (3 to 3 players, best with 3)

Three players play 6 deals of 5 tricks: in each deal the Pair veto trump colours, the Lone names trump, the first leader and an exact trick bid, and every trick scores 1 point for whoever wins it.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points: 1 per trick won plus contract scoring.
  - each player: hand (list, starts []); only its owner sees it. Cards held this deal, written as colour letter plus number (for example R5, B1, G3, Y2). Only the owner sees it.
  - each player: is_lone (bool, starts False); everyone sees it. True for the seat that is the Lone this deal. The other two seats are the Pair.
  - each player: ban (text, starts ''); everyone sees it. The colour this Pair member banned this deal. It is announced after both bans are in.
  - each player: played_card (text, starts ''); everyone sees it. The card this seat played to the current trick, face up.
  - each player: card_strength (number, starts 0); everyone sees it. Strength of played_card in the current trick: 10 plus its number if it is trump, its number if it is the led colour, otherwise 0.
  - the table: deck (list, starts ['R1', 'R2', 'R3', 'R4', 'R5', 'B1', 'B2', 'B3', 'B4', 'B5', 'G1', 'G2', 'G3', 'G4', 'G5', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5']); hidden from all players. The 20-card deck: 4 colours numbered 1 to 5.
  - the table: widow (list, starts []); hidden from all players. The 5 undealt cards of the current deal, face down and seen by nobody.
  - the table: deal (number, starts 1); everyone sees it. Current deal number, 1 to 6. It becomes 7 when the game is over.
  - the table: round_in_deal (number, starts 1); everyone sees it. Round within the deal: 1 is the setup round, 2 to 6 are the 5 trick rounds.
  - the table: round_number (number, starts 1); everyone sees it. Overall round number, 1 to 36.
  - the table: lone_seat (number, starts 1); everyone sees it. Seat of the Lone this deal: ((deal - 1) mod 3) + 1.
  - the table: unbanned (list, starts ['Red', 'Blue', 'Green', 'Yellow']); everyone sees it. Colours not banned by either Pair member this deal.
  - the table: trump (text, starts ''); everyone sees it. The trump colour named by the Lone this deal.
  - the table: bid (number, starts 0); everyone sees it. The exact number of tricks the Lone promised to win this deal, 0 to 5.
  - the table: leader (number, starts 1); everyone sees it. Seat that leads the current trick.
  - the table: led_colour (text, starts ''); everyone sees it. Colour of the card led to the current trick.
  - the table: trick_winner (number, starts 0); everyone sees it. Seat that won the most recent trick.
  - the table: lone_tricks (number, starts 0); everyone sees it. Tricks the Lone has won this deal.
  - parameters, each kept as a table attribute: player_count = 3, deck_size = 20, colour_count = 4, rank_min = 1, rank_max = 5, hand_size = 5, widow_size = 5, deals = 6, rounds_per_deal = 6, tricks_per_deal = 5, total_rounds = 36, bans_per_pair_member = 1, unbanned_if_same_ban = 3, unbanned_if_different_bans = 2, bid_min = 0, bid_max = 5, trick_point = 1, exact_bid_lone_gain = 6, off_by_one_lone_gain = 2, off_by_one_pair_gain = 1, off_by_two_or_more_pair_gain = 3, off_by_one_difference = 1, off_by_two_threshold = 2, trump_strength_offset = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are 1, 2 and 3. Clockwise order is 1 to 2, 2 to 3, and 3 to 1.
  2. Every player's score starts at 0.
  3. The deck list holds the 20 cards R1 to R5, B1 to B5, G1 to G5 and Y1 to Y5.
  4. deal is set to 1, round_in_deal to 1 and round_number to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When round_in_deal == 1 (setup round): every card in widow and in any hand is returned to deck. lone_seat = ((deal - 1) mod 3) + 1. is_lone is set true for the seat equal to lone_seat and false for the others. Each player's ban is set to empty, unbanned is reset to all four colours, trump to empty, bid to 0 and lone_tricks to 0. The Lone and the Pair are announced to everyone.
  2. [update] all players. What happens: When round_in_deal == 1: shuffle by drawing at random. Each player gets 5 random cards, each moved from deck into that player's hand. The remaining 5 cards of deck are moved into widow, which stays hidden from everyone.
  3. [sync] all players. What happens: When round_in_deal == 1: each player is sent their own hand, plus lone_seat and the scores.
  4. [poll] all players answers: short text message. What happens: When round_in_deal == 1: all three write at the same time, and the messages are then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes and nothing is binding.
  5. [poll] each player with is_lone == false answers: one of: Red, Blue, Green, Yellow. What happens: When round_in_deal == 1: each Pair member's ban is set to the chosen colour, chosen at the same time. Both banned colours are removed from unbanned, leaving 3 colours if the two bans match and 2 if they differ. Both bans and unbanned are announced.
  6. [ask] the seat with is_lone == true answers: one combined choice of trump (a colour in unbanned), first leader (seat 1, 2 or 3) and bid (a whole number 0 to 5), offered as items such as 'trump Red, leader seat 2, bid 3'. What happens: When round_in_deal == 1: trump, leader and bid are set from the choice and announced.
  7. [update] all players. What happens: When round_in_deal >= 2 (trick round): each played_card is set to empty, each card_strength to 0, and led_colour to empty.
  8. [ask] each player in turn, clockwise starting at leader answers: one card from the player's own hand; after the lead, only cards of led_colour if the player holds any. What happens: When round_in_deal >= 2: the card is removed from that player's hand and set as their played_card, shown face up. For the leader, led_colour is set to the card's colour. Each player hears the earlier plays.
  9. [update] all players. What happens: When round_in_deal >= 2: card_strength = 10 + number if the card's colour == trump; = number if its colour == led_colour and is not trump; otherwise 0. trick_winner is the seat with the highest card_strength. That seat's score += 1. If trick_winner == lone_seat, lone_tricks += 1. leader = trick_winner. The winner, all scores and lone_tricks are announced.
  10. [update] all players. What happens: When round_in_deal == 6 (after the 5th trick), with T = lone_tricks and B = bid: if |T - B| == 0, the Lone's score += 6; if |T - B| == 1, the Lone's score += 2 and each Pair member's score += 1; if |T - B| >= 2, each Pair member's score += 3. The result is announced.
  11. [update] all players. What happens: round_number += 1. If round_in_deal == 6, then deal += 1 and round_in_deal = 1; otherwise round_in_deal += 1.
  12. [check] all players. What happens: The game ends if deal > 6 (all 36 rounds played); otherwise it continues.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player's score is 0 and the deck holds 20 cards: Red, Blue, Green and Yellow, each numbered 1 to 5.
  R2. When a deal begins (round_in_deal 1), each of the 3 players receives exactly 5 random cards from the deck into their hand, and the remaining 5 cards go into the widow, which nobody sees.
  R3. When a deal begins, all cards from the previous deal's hands and widow are first returned to the deck, so 20 cards are dealt.
  R4. When the deal is 1 or 4 the Lone is seat 1; when it is 2 or 5 the Lone is seat 2; when it is 3 or 6 the Lone is seat 3; the other two seats are the Pair, and this is announced.
  R5. When the setup round's talk step runs, all 3 players submit one short message simultaneously, and all messages are then shown to everyone; no state changes.
  R6. When the veto step runs, only the 2 Pair members are asked, simultaneously, and each names one of Red, Blue, Green or Yellow.
  R7. When both Pair members ban the same colour, 3 colours remain unbanned; when they ban different colours, 2 remain.
  R8. When the Lone makes the contract, trump must be an unbanned colour, the first leader may be seat 1, 2 or 3, and the bid is a whole number from 0 to 5.
  R9. When the first trick of a deal is played, the leader is the seat the Lone named; on each later trick, the leader is the previous trick's winner.
  R10. When a trick is played, the leader plays first, then the next seat clockwise (1 to 2, 2 to 3, 3 to 1), then the remaining seat.
  R11. When a player who is not leading holds a card of the led colour, they must play a card of the led colour; when they hold none, they may play any card in their hand.
  R12. When a card is played, it is removed from the player's hand and shown face up to everyone.
  R13. When at least one trump is played in a trick, the player of the highest-numbered trump wins it; otherwise the player of the highest-numbered card of the led colour wins it.
  R14. When a trick is won, the winner's score increases by 1, whether they are the Lone or a Pair member.
  R15. When the Lone wins a trick, lone_tricks increases by 1; the winner, the scores and lone_tricks are announced after every trick.
  R16. When the 5th trick of a deal ends and the Lone's tricks equal the bid, the Lone gains 6 and the Pair gain nothing.
  R17. When the 5th trick of a deal ends and the Lone's tricks differ from the bid by exactly 1, the Lone gains 2 and each Pair member gains 1.
  R18. When the 5th trick of a deal ends and the Lone's tricks differ from the bid by 2 or more, each Pair member gains 3 and the Lone gains nothing.
  R19. When deal 6 has been scored (after round 36), the game ends and the player with the highest score wins; players level at the top share it.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk (setup round) | asked: all 3 seats | options: Any seat: one short free-text message.
  - Veto (setup round) | asked: the 2 Pair seats (is_lone false) | options: Each Pair seat: Red, Blue, Green, Yellow. The Lone is not asked.
  - Contract (setup round) | asked: the Lone seat only | options: Every combination of trump (each colour in unbanned, 2 or 3 of them), leader (seat 1, seat 2, seat 3) and bid (0, 1, 2, 3, 4, 5): 36 options when 2 colours remain unbanned and 54 when 3 remain.
  - Play a card (trick round) | asked: each seat in turn, clockwise from leader | options: Leader: any card in their hand. A later seat holding at least one card of led_colour: only those cards. A later seat holding no card of led_colour: any card in their hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal > 6
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after 6 deals (36 rounds). The highest total wins, and players level at the top share the result.
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

- each player: `score` (number, visible: public, starts 0): Total points: 1 per trick won plus contract scoring.
- each player: `is_lone` (bool, visible: public, starts False): True for the seat that is the Lone this deal. The other two seats are the Pair.
- each player: `ban` (text, visible: public, starts ''): The colour this Pair member banned this deal. It is announced after both bans are in.
- each player: `played_card` (text, visible: public, starts ''): The card this seat played to the current trick, face up.
- the table: `deal` (number, visible: public, starts 1): Current deal number, 1 to 6. It becomes 7 when the game is over.
- the table: `round_number` (number, visible: public, starts 1): Overall round number, 1 to 36.
- the table: `lone_seat` (number, visible: public, starts 1): Seat of the Lone this deal: ((deal - 1) mod 3) + 1.
- the table: `unbanned` (list, visible: public, starts ['Red', 'Blue', 'Green', 'Yellow']): Colours not banned by either Pair member this deal.
- the table: `trump` (text, visible: public, starts ''): The trump colour named by the Lone this deal.
- the table: `bid` (number, visible: public, starts 0): The exact number of tricks the Lone promised to win this deal, 0 to 5.
- the table: `leader` (number, visible: public, starts 1): Seat that leads the current trick.
- the table: `trick_winner` (number, visible: public, starts 0): Seat that won the most recent trick.
- the table: `lone_tricks` (number, visible: public, starts 0): Tricks the Lone has won this deal.
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, deck_size = 20, colour_count = 4, rank_min = 1, rank_max = 5, hand_size = 5, widow_size = 5, deals = 6, rounds_per_deal = 6, tricks_per_deal = 5, total_rounds = 36, bans_per_pair_member = 1, unbanned_if_same_ban = 3, unbanned_if_different_bans = 2, bid_min = 0, bid_max = 5, trick_point = 1, exact_bid_lone_gain = 6, off_by_one_lone_gain = 2, off_by_one_pair_gain = 1, off_by_two_or_more_pair_gain = 3, off_by_one_difference = 1, off_by_two_threshold = 2, trump_strength_offset = 10
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
{
  "schema": 1,
  "meta": {
    "id": "nyet_contract_veto",
    "name": "Nyet! Contract Veto",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, six deals of five tricks: the Pair veto trump colours, the Lone names trump, the first leader and an exact trick bid."
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
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "is_lone",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "ban",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "veto_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
        "initial": ["R1", "R2", "R3", "R4", "R5", "B1", "B2", "B3", "B4", "B5", "G1", "G2", "G3", "G4", "G5", "Y1", "Y2", "Y3", "Y4", "Y5"]
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": ["R1", "R2", "R3", "R4", "R5", "B1", "B2", "B3", "B4", "B5", "G1", "G2", "G3", "G4", "G5", "Y1", "Y2", "Y3", "Y4", "Y5"]
      },
      {
        "key": "widow",
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
        "key": "colour_names",
        "visible": "none",
        "type": "list",
        "initial": ["Red", "Blue", "Green", "Yellow"]
      },
      {
        "key": "seat_labels",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3"]
      },
      {
        "key": "bid_labels",
        "visible": "none",
        "type": "list",
        "initial": ["0", "1", "2", "3", "4", "5"]
      },
      {
        "key": "contract_offers",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "diff",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lone_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "unbanned",
        "visible": "public",
        "type": "list",
        "initial": ["Red", "Blue", "Green", "Yellow"]
      },
      {
        "key": "trump",
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
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lone_tricks",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "colour_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "widow_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "bans_per_pair_member",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "unbanned_if_same_ban",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "unbanned_if_different_bans",
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
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "trick_point",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_bid_lone_gain",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "off_by_one_lone_gain",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "off_by_one_pair_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "off_by_two_or_more_pair_gain",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "off_by_one_difference",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "off_by_two_threshold",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "trump_strength_offset",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
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
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        },
        {
          "set": {
            "key": "deal",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 1
          }
        }
      ],
      "text": "Seats are 1, 2 and 3; clockwise is 1 to 2, 2 to 3, 3 to 1. All scores start at 0. The deck holds {deck_size} cards."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "setup",
      "label": "a new deal",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        },
        {
          "set": {
            "key": "widow",
            "value": []
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
            "key": "lone_seat",
            "value": {
              "calc": "(deal - 1) % player_count + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_lone",
            "value": {
              "calc": "you.seat == lone_seat"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ban",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "veto_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "unbanned",
            "value": {
              "calc": "colour_names"
            }
          }
        },
        {
          "set": {
            "key": "trump",
            "value": "not yet named"
          }
        },
        {
          "set": {
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lone_tricks",
            "value": 0
          }
        }
      ],
      "text": "Deal {deal} of {deals} begins. All cards are returned to the deck. The Lone is seat {lone_seat}; the other two seats are the Pair."
    },
    {
      "use": "update",
      "phase": "setup",
      "label": "the deal",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "widow",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        }
      ],
      "text": "The cards are dealt: {hand_size} to each player, and the remaining {widow_size} go face down to the Widow, seen by nobody."
    },
    {
      "use": "sync",
      "phase": "setup",
      "label": "your hand",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": ["hand", "score", "is_lone"],
      "text": "Deal {deal}. The Lone is seat {lone_seat}. Your hand and standing:"
    },
    {
      "use": "poll",
      "phase": "setup",
      "label": "talk",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same moment and all messages are then shown to everyone. Messages bind nobody."
    },
    {
      "use": "poll",
      "phase": "setup",
      "label": "veto",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "not you.is_lone"
      },
      "answer": {
        "type": "choice",
        "options": ["Red", "Blue", "Green", "Yellow"]
      },
      "store": "veto_answer",
      "text": "You are in the Pair. Name one colour to ban as trump this deal. The other Pair member chooses at the same moment; both bans are then announced. If you both ban the same colour, three colours remain unbanned; otherwise two remain."
    },
    {
      "use": "update",
      "phase": "setup",
      "label": "the bans",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "not you.is_lone"
            },
            "key": "ban",
            "value": {
              "calc": "you.veto_answer"
            },
            "text": "Seat {player} bans {value}."
          }
        },
        {
          "set": {
            "key": "unbanned",
            "value": {
              "calc": "[c for c in colour_names if all(p.ban != c for p in players)]"
            }
          }
        },
        {
          "set": {
            "key": "contract_offers",
            "value": {
              "calc": "['trump ' + c + ', leader seat ' + s + ', bid ' + b for c in unbanned for s in seat_labels for b in bid_labels]"
            }
          }
        }
      ],
      "text": "Unbanned colours this deal: {unbanned}."
    },
    {
      "use": "ask",
      "phase": "setup",
      "label": "contract",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "you.is_lone"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "contract_offers"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "trump",
              "value": {
                "calc": "[c for c in unbanned if ('trump ' + c + ',') in $answer][0]"
              }
            }
          },
          {
            "set": {
              "key": "leader",
              "value": {
                "calc": "[int(s) for s in seat_labels if ('leader seat ' + s + ',') in $answer][0]"
              }
            }
          },
          {
            "set": {
              "key": "bid",
              "value": {
                "calc": "[int(b) for b in bid_labels if ('bid ' + b) in $answer][0]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Lone, seat {seat}, declares the contract: {value}."
      },
      "text": "You are the Lone. Choose the contract in one decision: trump (one of the unbanned colours {unbanned}), the first leader (any seat) and your bid, the exact number of tricks you will win this deal ({bid_min} to {bid_max})."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_strength",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_colour",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ],
      "text": "A new trick of deal {deal} (trump {trump}): seat {leader} leads."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the lead",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_colour",
              "value": {
                "calc": "[n for n in colour_names if n[0] == $answer[0]][0]"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_colour[0]] if any(c[0] == led_colour[0] for c in you.hand) else you.hand"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand, face up; its colour becomes the led colour. Trump is {trump}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the second play",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == leader % player_count + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play one card face up. Trump is {trump}. If you hold a card of the colour that was led you must play one; otherwise you may play any card. You are offered only the cards you may play."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the third play",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == (leader + 1) % player_count + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play one card face up. Trump is {trump}. If you hold a card of the colour that was led you must play one; otherwise you may play any card. You are offered only the cards you may play."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card_strength",
            "value": {
              "calc": "(trump_strength_offset + int(you.played_card[1]) if you.played_card[0] == trump[0] else (int(you.played_card[1]) if you.played_card[0] == led_colour[0] else 0)) if len(you.played_card) >= 2 else 0"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "[p.seat for p in players if p.card_strength == max([q.card_strength for q in players])][0]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "score",
            "value": {
              "calc": "trick_point"
            }
          }
        },
        {
          "adjust": {
            "key": "lone_tricks",
            "value": 1,
            "if": {
              "calc": "trick_winner == lone_seat"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ],
      "text": "Seat {trick_winner} wins the trick and scores {trick_point}. Scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}. The Lone has won {lone_tricks} tricks this deal (bid {bid})."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "contract scoring",
      "when": {
        "calc": "round_in_dea
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `colour_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `seat_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bid_labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "nyet_contract_veto",
    "name": "Nyet! Contract Veto",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, six deals of five tricks: the Pair veto trump colours, the Lone names trump, the first leader and an exact trick bid."
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
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "is_lone",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "ban",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_strength",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "veto_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
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
          "R1",
          "R2",
          "R3",
          "R4",
          "R5",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "G1",
          "G2",
          "G3",
          "G4",
          "G5",
          "Y1",
          "Y2",
          "Y3",
          "Y4",
          "Y5"
        ]
      },
      {
        "key": "widow",
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
        "key": "contract_offers",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "diff",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_in_deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lone_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "unbanned",
        "visible": "public",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow"
        ]
      },
      {
        "key": "trump",
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
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "led_colour",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lone_tricks",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "colour_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "widow_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "bans_per_pair_member",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "unbanned_if_same_ban",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "unbanned_if_different_bans",
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
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "trick_point",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "exact_bid_lone_gain",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "off_by_one_lone_gain",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "off_by_one_pair_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "off_by_two_or_more_pair_gain",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "off_by_one_difference",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "off_by_two_threshold",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "trump_strength_offset",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting state",
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
            "key": "deck",
            "value": [
              "R1",
              "R2",
              "R3",
              "R4",
              "R5",
              "B1",
              "B2",
              "B3",
              "B4",
              "B5",
              "G1",
              "G2",
              "G3",
              "G4",
              "G5",
              "Y1",
              "Y2",
              "Y3",
              "Y4",
              "Y5"
            ]
          }
        },
        {
          "set": {
            "key": "deal",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 1
          }
        }
      ],
      "text": "Seats are 1, 2 and 3; clockwise is 1 to 2, 2 to 3, 3 to 1. All scores start at 0. The deck holds {deck_size} cards."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "setup",
      "label": "a new deal",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "R1",
              "R2",
              "R3",
              "R4",
              "R5",
              "B1",
              "B2",
              "B3",
              "B4",
              "B5",
              "G1",
              "G2",
              "G3",
              "G4",
              "G5",
              "Y1",
              "Y2",
              "Y3",
              "Y4",
              "Y5"
            ]
          }
        },
        {
          "set": {
            "key": "widow",
            "value": []
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
            "key": "lone_seat",
            "value": {
              "calc": "(deal - 1) % player_count + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_lone",
            "value": {
              "calc": "you.seat == lone_seat"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "ban",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "veto_answer",
            "value": ""
          }
        },
        {
          "set": {
            "key": "unbanned",
            "value": [
              "Red",
              "Blue",
              "Green",
              "Yellow"
            ]
          }
        },
        {
          "set": {
            "key": "trump",
            "value": "not yet named"
          }
        },
        {
          "set": {
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "lone_tricks",
            "value": 0
          }
        }
      ],
      "text": "Deal {deal} of {deals} begins. All cards are returned to the deck. The Lone is seat {lone_seat}; the other two seats are the Pair."
    },
    {
      "use": "update",
      "phase": "setup",
      "label": "the deal",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "widow",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        }
      ],
      "text": "The cards are dealt: {hand_size} to each player, and the remaining {widow_size} go face down to the Widow, seen by nobody."
    },
    {
      "use": "sync",
      "phase": "setup",
      "label": "your hand",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "score",
        "is_lone"
      ],
      "text": "Deal {deal}. The Lone is seat {lone_seat}. Your hand and standing:"
    },
    {
      "use": "poll",
      "phase": "setup",
      "label": "talk",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same moment and all messages are then shown to everyone. Messages bind nobody."
    },
    {
      "use": "poll",
      "phase": "setup",
      "label": "veto",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "not you.is_lone"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Red",
          "Blue",
          "Green",
          "Yellow"
        ]
      },
      "store": "veto_answer",
      "text": "You are in the Pair. Name one colour to ban as trump this deal. The other Pair member chooses at the same moment; both bans are then announced. If you both ban the same colour, three colours remain unbanned; otherwise two remain."
    },
    {
      "use": "update",
      "phase": "setup",
      "label": "the bans",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "not you.is_lone"
            },
            "key": "ban",
            "value": {
              "calc": "you.veto_answer"
            },
            "text": "Seat {player} bans {value}."
          }
        },
        {
          "set": {
            "key": "unbanned",
            "value": {
              "calc": "[c for c in ['Red', 'Blue', 'Green', 'Yellow'] if all(p.ban != c for p in players)]"
            }
          }
        },
        {
          "set": {
            "key": "contract_offers",
            "value": {
              "calc": "['trump ' + c + ', leader seat ' + s + ', bid ' + b for c in unbanned for s in ['1', '2', '3'] for b in ['0', '1', '2', '3', '4', '5']]"
            }
          }
        }
      ],
      "text": "Unbanned colours this deal: {unbanned}."
    },
    {
      "use": "ask",
      "phase": "setup",
      "label": "contract",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "you.is_lone"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "contract_offers"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "trump",
              "value": {
                "calc": "[c for c in unbanned if ('trump ' + c + ',') in $answer][0]"
              }
            }
          },
          {
            "set": {
              "key": "leader",
              "value": {
                "calc": "[int(s) for s in ['1', '2', '3'] if ('leader seat ' + s + ',') in $answer][0]"
              }
            }
          },
          {
            "set": {
              "key": "bid",
              "value": {
                "calc": "[int(b) for b in ['0', '1', '2', '3', '4', '5'] if ('bid ' + b) in $answer][0]"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "The Lone, seat {seat}, declares the contract: {value}."
      },
      "text": "You are the Lone. Choose the contract in one decision: trump (one of the unbanned colours {unbanned}), the first leader (any seat) and your bid, the exact number of tricks you will win this deal ({bid_min} to {bid_max})."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_strength",
            "value": 0
          }
        },
        {
          "set": {
            "key": "led_colour",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "you.hand"
            }
          }
        }
      ],
      "text": "A new trick of deal {deal} (trump {trump}): seat {leader} leads."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the lead",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_colour",
              "value": {
                "calc": "[n for n in ['Red', 'Blue', 'Green', 'Yellow'] if n[0] == $answer[0]][0]"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if c[0] == led_colour[0]] if any(c[0] == led_colour[0] for c in you.hand) else you.hand"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand, face up; its colour becomes the led colour. Trump is {trump}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the second play",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == leader % player_count + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play one card face up. Trump is {trump}; the led colour is {led_colour}. If you hold a card of the led colour you must play one; otherwise you may play any card. You are offered only the cards you may play."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "the third play",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == (leader + 1) % player_count + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play one card face up. Trump is {trump}; the led colour is {led_colour}. If you hold a card of the led colour you must play one; otherwise you may play any card. You are offered only the cards you may play."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "the trick is won",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card_strength",
            "value": {
              "calc": "(trump_strength_offset + int(you.played_card[1]) if you.played_card[0] == trump[0] else (int(you.played_card[1]) if you.played_card[0] == led_colour[0] else 0)) if len(you.played_card) >= 2 else 0"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "[p.seat for p in players if p.card_strength == max([q.card_strength for q in players])][0]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "score",
            "value": {
              "calc": "trick_point"
            }
          }
        },
        {
          "adjust": {
            "key": "lone_tricks",
            "value": {
              "calc": "trick_point"
            },
            "if": {
              "calc": "trick_winner == lone_seat"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "trick_winner"
            }
          }
        }
      ],
      "text": "Seat {trick_winner} wins the trick and scores {trick_point}. Scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}. The Lone has won {lone_tricks} tricks this deal (bid {bid})."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "contract scoring",
      "when": {
        "calc": "round_in_deal == rounds_per_deal"
      },
      "do": [
        {
          "set": {
            "key": "diff",
            "value": {
              "calc": "abs(lone_tricks - bid)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "lone_seat"
            },
            "key": "score",
            "value": {
              "calc": "exact_bid_lone_gain"
            },
            "if": {
              "calc": "diff == 0"
            },
            "text": "The Lone made the contract exactly and gains {exact_bid_lone_gain}."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "lone_seat"
            },
            "key": "score",
            "value": {
              "calc": "off_by_one_lone_gain"
            },
            "if": {
              "calc": "diff == off_by_one_difference"
            },
            "text": "The Lone missed the bid by one: the Lone gains {off_by_one_lone_gain} and each Pair member gains {off_by_one_pair_gain}."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.is_lone"
            },
            "key": "score",
            "value": {
              "calc": "off_by_one_pair_gain"
            },
            "if": {
              "calc": "diff == off_by_one_difference"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.is_lone"
            },
            "key": "score",
            "value": {
              "calc": "off_by_two_or_more_pair_gain"
            },
            "if": {
              "calc": "diff >= off_by_two_threshold"
            },
            "text": "Seat {player} of the Pair gains {off_by_two_or_more_pair_gain}: the Lone missed the bid by two or more."
          }
        }
      ],
      "text": "Deal {deal} contract: the Lone (seat {lone_seat}) won {lone_tricks} tricks against a bid of {bid}. Scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "deal",
            "value": 1,
            "if": {
              "calc": "round_in_deal == rounds_per_deal"
            }
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": {
              "calc": "1 if round_in_deal == rounds_per_deal else round_in_deal + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "trick",
      "label": "after the last deal",
      "when": {
        "calc": "deal > deals"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "deal > deals"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Three players, seats 1, 2 and 3. Clockwise means 1 to 2, 2 to 3, and 3 to 1. The deck has {deck_size} cards in {colour_count} colours (Red, Blue, Green, Yellow), each numbered {rank_min} to {rank_max}; a card is written as colour letter plus number (R5, B1, G3, Y2). All scores start at 0. The game has {deals} deals; each deal is {rounds_per_deal} rounds: one setup round, then {tricks_per_deal} trick rounds.\n\nSETUP ROUND. All cards are returned to the deck and shuffled. Each player is dealt {hand_size} cards, seen only by their owner; the remaining {widow_size} cards form the Widow, face down, seen by nobody. The Lone is seat 1 in deals 1 and 4, seat 2 in deals 2 and 5, and seat 3 in deals 3 and 6; the other two players are the Pair. This is announced.\nTALK: all three players write one short message at the same moment, without seeing the others; all messages are then shown to everyone. Messages bind nobody.\nVETO: the two Pair members, at the same moment, each name one colour to ban. Both bans are then announced. If both ban the same colour, {unbanned_if_same_ban} colours remain unbanned; otherwise {unbanned_if_different_bans} remain.\nCONTRACT: the Lone chooses three things in one decision and announces them: trump, which must be one of the unbanned colours; the first leader, any of the three seats; and the bid, a whole number from {bid_min} to {bid_max}: the exact number of tricks the Lone promises to win this deal.\n\nTRICK ROUNDS (one trick each). The leader plays one card face up; on the first trick the leader is the seat the Lone named, on later tricks the winner of the previous trick. The led card's colour is the led colour. The next player clockwise plays one card, then the remaining player. A player holding a card of the led colour must play one; a player holding none may play any card. A played card leaves the hand and is shown face up to everyone. The trick winner is the player of the highest-numbered trump if any trump was played; otherwise the player of the highest-numbered card of the led colour. There are no ties. The trick winner gains {trick_point} point, whether Lone or Pair. The Lone's tricks this deal are counted; the winner, the scores and the Lone's trick count are announced.\n\nCONTRACT SCORING (after the 5th trick). With T the Lone's tricks and B the bid: if T equals B, the Lone gains {exact_bid_lone_gain} and the Pair gain nothing; if T and B differ by exactly {off_by_one_difference}, the Lone gains {off_by_one_lone_gain} and each Pair member gains {off_by_one_pair_gain}; if they differ by {off_by_two_threshold} or more, each Pair member gains {off_by_two_or_more_pair_gain} and the Lone gains nothing. The result is announced.\n\nAfter deal 6 is scored ({total_rounds} rounds), the game ends. The highest total score wins; players level at the top share the win."
}
```
````
