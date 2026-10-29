# 17 coder

- time: 2026-10-27T18:21:07+00:00 (190.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 b1d244e67423104e, reply sha256 4d9f8047e8de3bea

## Sent

````
# Task: write the XColos game file for "Nyet! Trio (Widow edition, compact)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- There are exactly 3 players: P1, P2, P3. Clockwise order is P1 -> P2 -> P3 -> P1.
- The deck has 24 unique cards: four colours (Red, Yellow, Green, Blue), each numbered 1 to 6.
- Each player has score, lone_tricks and last_win, all starting at 0.
- The game lasts 36 rounds: 6 deals of 6 rounds each. Round 1 of each deal (rounds 1, 7, 13, 19, 25, 31) is the VETO round. Rounds 2 to 6 of each deal are TRICK rounds.

VETO ORDER (First, Second, Third)
- Deals 1 and 4: P1, P2, P3.
- Deals 2 and 5: P2, P3, P1.
- Deals 3 and 6: P3, P1, P2.

TRUMP LINE ORDER (rotates each deal)
- Deal 1: Red, Yellow, Green, Blue.
- Deal 2: Yellow, Green, Blue, Red.
- Deal 3: Green, Blue, Red, Yellow.
- Deal 4: Blue, Red, Yellow, Green.
- Deal 5: Red, Yellow, Green, Blue.
- Deal 6: Yellow, Green, Blue, Red.

VETO ROUND
(1) Shuffle all 24 cards. Deal 5 to each player as a private hand. Turn one of the remaining 9 face up: this is the Widow, which everyone sees. The other 8 are set aside face down and are never revealed. Any cards left in hands from the previous deal are discarded unseen before the shuffle.
(2) The Nyet board is cleared. It has two lines: the TRUMP line (4 colour boxes, in this deal's order) and the LONE line (3 boxes: First, Second, Third). Announce the Widow and the board.
(3) Talk: all three players write one short message at the same time, without seeing the others' messages. All messages are then shown to everyone. Talk is not binding.
(4) First, then Second, then Third each places one Nyet token on one empty box. Each sees the tokens already placed. A token may go on any empty TRUMP box. A token may go on a LONE box only if no token is yet on the LONE line: at most one LONE token per deal. A player may not token the last empty box of a line. There is always at least one legal box.
(5) Trump is the first untokened box on the TRUMP line, in this deal's order. The Lone is the first untokened box on the LONE line (First, then Second, then Third). The other two players are the Pair.
(6) The Lone adds the Widow to their hand and holds 6 cards. Announce trump, the Lone and the Pair. The Lone leads the first trick.

TRICK ROUND
(7) The leader plays one card face up. Then the next player clockwise plays one, then the third player plays one. Each sees the cards already played. The led colour is the colour of the leader's card. A player holding a card of the led colour must play one. A player with none may play any card.
(8) Winner: if any trump was played, the highest trump wins. Otherwise the highest card of the led colour wins. Cards are unique, so there is always one winner.
(9) Scoring: if the Lone won, the Lone gains 2 points and 1 lone_trick. If a Pair member won, each Pair member gains 1 point. The winner's last_win is set to the current round number.
(10) The winner leads the next trick of this deal.
(11) Announce the cards played, the winner and all scores.
- After the 5th trick of a deal, the Lone still holds 1 card. It is never played or revealed and is discarded at the next shuffle. Choosing which card to keep back is the Lone's discard.

END
After round 36, the winner is decided as in the objective.

How the winner is decided: The highest score wins. If players tie, the tied player with the most lone_tricks wins. If still tied, the tied player with the highest last_win wins (the one who won a trick most recently; this is unique unless no tied player has won a trick). If still tied, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Nyet! Trio (Widow edition, compact) (3 to 3 players, best with 3)

Three players veto trump and choose who goes Lone, then play 5 tricks per deal over 6 deals. The Lone takes the face-up Widow and scores 2 per trick won; the other two, the Pair, each score 1 per trick their side wins.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. points scored
  - each player: lone_tricks (number, starts 0); everyone sees it. tricks won while Lone (first tie-break)
  - each player: last_win (number, starts 0); everyone sees it. round number of this player's most recent trick win, 0 if none (second tie-break)
  - each player: hand (list, starts []); only its owner sees it. private hand of cards such as 'Red 3'
  - each player: role (text, starts ''); everyone sees it. 'lone' or 'pair' for the current deal
  - each player: played_colour (text, starts ''); everyone sees it. colour of the card played to the current trick
  - each player: played_rank (number, starts 0); everyone sees it. rank (1 to 6) of the card played to the current trick
  - each player: strength (number, starts 0); everyone sees it. scratch value: strength of the card this player played to the current trick, worked out from the face-up card, so it reveals nothing hidden
  - the table: round (number, starts 0); everyone sees it. current round, 1 to 36
  - the table: deal (number, starts 0); everyone sees it. current deal, 1 to 6
  - the table: round_in_deal (number, starts 0); everyone sees it. 1 is the veto round; 2 to 6 are trick rounds
  - the table: deck (list, starts []); hidden from all players. undealt cards; after a deal it holds the 8 set-aside cards, which are never revealed
  - the table: widow (text, starts ''); everyone sees it. the face-up Widow card for this deal
  - the table: trump_order (list, starts []); everyone sees it. this deal's trump line, in order
  - the table: veto_order (list, starts []); everyone sees it. this deal's First, Second and Third seats
  - the table: trump_tokens (list, starts []); everyone sees it. trump boxes holding a Nyet token
  - the table: lone_tokens (list, starts []); everyone sees it. lone boxes (First, Second, Third) holding a Nyet token
  - the table: trump (text, starts ''); everyone sees it. this deal's trump colour
  - the table: lone_seat (number, starts 0); everyone sees it. seat of this deal's Lone
  - the table: leader (number, starts 0); everyone sees it. seat that leads the current trick
  - the table: led_colour (text, starts ''); everyone sees it. colour of the leader's card in the current trick
  - the table: trick_winner (number, starts 0); everyone sees it. seat that won the last trick
  - parameters, each kept as a table attribute: players = 3, colours = 4, ranks_per_colour = 6, deck_size = 24, hand_size = 5, widow_cards = 1, set_aside_cards = 8, lone_hand_size = 6, total_rounds = 36, deals = 6, rounds_per_deal = 6, veto_rounds_per_deal = 1, tricks_per_deal = 5, trump_boxes = 4, lone_boxes = 3, tokens_per_deal = 3, max_lone_tokens_per_deal = 1, lone_trick_points = 2, lone_trick_count_gain = 1, pair_trick_points_each = 1, lone_cards_kept_back = 1, trump_strength_bonus = 200, led_strength_bonus = 100, rank_weight_score = 10000, rank_weight_lone_tricks = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 are P1, P2 and P3; clockwise order is 1 -> 2 -> 3 -> 1.
  2. Every player's score, lone_tricks and last_win are set to 0.
  3. The full card set is 24 unique cards: Red, Yellow, Green and Blue, each numbered 1 to 6.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; deal = floor((round - 1) / 6) + 1; round_in_deal = ((round - 1) mod 6) + 1
  2. [update] all players. What happens: when round_in_deal == 1: empty every hand (cards are discarded unseen); deck = all 24 cards; draw 5 cards at random from deck into each player's hand; draw 1 card at random from deck into widow (the remaining 8 stay in deck, hidden, as the set-aside cards); clear trump_tokens and lone_tokens; set trump_order (deals 1 and 5: Red, Yellow, Green, Blue; deals 2 and 6: Yellow, Green, Blue, Red; deal 3: Green, Blue, Red, Yellow; deal 4: Blue, Red, Yellow, Green); set veto_order (deals 1 and 4: 1, 2, 3; deals 2 and 5: 2, 3, 1; deals 3 and 6: 3, 1, 2); clear trump, lone_seat and roles
  3. [sync] all players. What happens: when round_in_deal == 1: each player sees their own 5-card hand
  4. [tell] all players. What happens: when round_in_deal == 1: announce deal, widow, trump_order (the TRUMP line), the LONE line boxes First/Second/Third with their seats from veto_order, and that the board is empty
  5. [poll] all players answers: short text (non-binding talk). What happens: when round_in_deal == 1: all messages are collected at once and then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}
  6. [ask] seat veto_order[1] (First) answers: one empty box: a TRUMP colour not in trump_tokens, or a LONE box (First/Second/Third) if lone_tokens is empty; never the last empty box of a line. What happens: when round_in_deal == 1: append the chosen colour to trump_tokens, or the chosen lone box to lone_tokens; announce the placement
  7. [ask] seat veto_order[2] (Second) answers: one empty box, under the same restrictions, seeing the tokens already placed. What happens: when round_in_deal == 1: append to trump_tokens or lone_tokens; announce the placement
  8. [ask] seat veto_order[3] (Third) answers: one empty box, under the same restrictions, seeing the tokens already placed. What happens: when round_in_deal == 1: append to trump_tokens or lone_tokens; announce the placement
  9. [update] all players. What happens: when round_in_deal == 1: trump = first colour in trump_order not in trump_tokens; lone_seat = the veto_order seat at the first of the First, Second, Third positions not in lone_tokens; role = 'lone' for lone_seat and 'pair' for the other two; append widow to the Lone's hand (6 cards); leader = lone_seat
  10. [tell] all players. What happens: when round_in_deal == 1: announce trump, the Lone (lone_seat) and the Pair seats, and that the Lone leads the first trick
  11. [sync] all players. What happens: when round_in_deal == 1: each player sees their own hand (the Lone now sees 6 cards)
  12. [ask] seat leader answers: one card from own hand. What happens: when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; led_colour = played_colour; announce the card
  13. [ask] seat clockwise after leader answers: one card from own hand of colour led_colour if holding any, otherwise any card in hand. What happens: when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; announce the card
  14. [ask] seat two clockwise after leader answers: one card from own hand of colour led_colour if holding any, otherwise any card in hand. What happens: when round_in_deal >= 2: remove the card from hand; set played_colour and played_rank; announce the card
  15. [update] all players. What happens: when round_in_deal >= 2: for each player, strength = (played_colour == trump) * 200 + (played_colour == led_colour) * 100 + played_rank; trick_winner = the seat with the highest strength; if trick_winner == lone_seat then that player's score += 2 and lone_tricks += 1, otherwise each player with role 'pair' gets score += 1; trick_winner's last_win = round; leader = trick_winner
  16. [tell] all players. What happens: when round_in_deal >= 2: announce the three cards played, trick_winner, and every score, lone_tricks and last_win
  17. [sync] all players. What happens: when round_in_deal >= 2: each player sees their own remaining hand
  18. [check] all players. What happens: end the game if round >= 36, otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each of the 3 players has score 0, lone_tricks 0 and last_win 0.
  R2. When round is 1, 7, 13, 19, 25 or 31, then it is a veto round; every other round is a trick round.
  R3. When a veto round starts, then all hands are emptied, the 24-card deck is rebuilt, each player receives 5 private cards, 1 card becomes the public widow, and 8 cards remain hidden in deck.
  R4. When a veto round starts, then trump_tokens and lone_tokens are empty.
  R5. When deal is 1 or 4, then the veto order is seats 1, 2, 3; when deal is 2 or 5, it is 2, 3, 1; when deal is 3 or 6, it is 3, 1, 2.
  R6. When deal is 1 or 5, then trump_order is Red, Yellow, Green, Blue; when deal is 2 or 6, it is Yellow, Green, Blue, Red; when deal is 3, it is Green, Blue, Red, Yellow; when deal is 4, it is Blue, Red, Yellow, Green.
  R7. When the veto round talk happens, then all 3 players submit one short message at once, and all messages are shown to everyone only after all are in.
  R8. When a player places a Nyet token, then it goes on exactly one empty box, and the player sees all tokens already placed.
  R9. When lone_tokens already holds a token, then no further token may be placed on the LONE line this deal.
  R10. When a box is the last empty box of its line, then no token may be placed on it.
  R11. When all 3 tokens are placed, then trump is the first colour in trump_order without a token.
  R12. When all 3 tokens are placed, then the Lone is the seat of the first of First, Second, Third without a token, and the other two seats are the Pair.
  R13. When the Lone is chosen, then the widow is added to the Lone's hand, giving 6 cards, and the Lone leads the first trick.
  R14. When a trick is played, then the leader plays first, then the next seat clockwise, then the third seat, each seeing the cards already played.
  R15. When a player holds a card of led_colour, then they must play a card of led_colour; otherwise they may play any card in hand.
  R16. When any trump is played in a trick, then the highest trump wins; otherwise the highest card of led_colour wins.
  R17. When the Lone wins a trick, then the Lone's score rises by 2 and lone_tricks by 1.
  R18. When a Pair member wins a trick, then the score of each of the two Pair members rises by 1.
  R19. When a player wins a trick, then their last_win is set to the current round number and they lead the next trick of the deal.
  R20. When the 5th trick of a deal ends, then the Lone's 1 remaining card is never played or revealed and is discarded at the next shuffle.
  R21. When round 36 ends, then the game ends.
  R22. When the game ends, then the highest score wins; ties go to most lone_tricks, then highest last_win; players still tied share the win as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Veto talk | asked: all three seats at once | options: a short free-text message
  - Nyet token placement (First, Second, Third in turn) | asked: the seat at that position of veto_order | options: if lone_tokens is empty: each TRUMP colour not in trump_tokens plus each LONE box (First, Second, Third) not in lone_tokens, excluding any box that is the last empty one of its line; if lone_tokens has a token: only the TRUMP colours not in trump_tokens, excluding the last empty one
  - Lead a card | asked: the leader | options: every card in the leader's hand
  - Follow to the trick | asked: the second and third seats clockwise from the leader | options: if the seat holds a card of led_colour: only its cards of led_colour; otherwise every card in its hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 36
  - each player's standing: you.score * 10000 + you.lone_tricks * 100 + you.last_win (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The highest score wins. A tie goes to the tied player with the most lone_tricks, then to the one with the highest last_win (who won a trick most recently). Players still level share the win, which is the draw.
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

- each player: `score` (number, visible: public, starts 0): points scored
- each player: `lone_tricks` (number, visible: public, starts 0): tricks won while Lone (first tie-break)
- each player: `last_win` (number, visible: public, starts 0): round number of this player's most recent trick win, 0 if none (second tie-break)
- the table: `round` (number, visible: public, starts 0): current round, 1 to 36
- the table: `widow` (text, visible: public, starts ''): the face-up Widow card for this deal
- the table: `trump` (text, visible: public, starts ''): this deal's trump colour
- the table: `lone_seat` (number, visible: public, starts 0): seat of this deal's Lone
- the table: `trick_winner` (number, visible: public, starts 0): seat that won the last trick
- parameters (each must be an attribute holding this value, never a number buried in a step): players = 3, colours = 4, ranks_per_colour = 6, deck_size = 24, hand_size = 5, widow_cards = 1, set_aside_cards = 8, lone_hand_size = 6, total_rounds = 36, deals = 6, rounds_per_deal = 6, veto_rounds_per_deal = 1, tricks_per_deal = 5, trump_boxes = 4, lone_boxes = 3, tokens_per_deal = 3, max_lone_tokens_per_deal = 1, lone_trick_points = 2, lone_trick_count_gain = 1, pair_trick_points_each = 1, lone_cards_kept_back = 1, trump_strength_bonus = 200, led_strength_bonus = 100, rank_weight_score = 10000, rank_weight_lone_tricks = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 10000 + you.lone_tricks * 100 + you.last_win`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) In every calc, make sure `players` means the numeric parameter (value 3), not the engine's built-in list of players. Reference it unambiguously, for example as a table attribute (`table.players`) or whatever form the engine uses for table attributes, and check every modulo expression (veto order, trump line rotation, next leader) for the same clash. Keep all parameters as attributes holding their values, never as literal numbers in steps. 2) Mark pure bookkeeping attributes as hidden (`none` on the table, `ally` on a player): led_colour, played_colour, role, token boxes and similar scratch values. 3) The public interface fields `trump` and `widow` must stay public. Order the steps so that no state print happens while they are blank: shuffle, deal and turn up the Widow before the first announcement, and set trump before any state is shown after the veto, or show only fields that are already filled at that point. 4) Run a full 36-round random-seat match to confirm there is no CalcError and no blank-field warning.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "nyet_trio_widow_compact",
    "name": "Nyet! Trio (Widow edition, compact)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players veto trump and who goes Lone, then play 5 tricks per deal over 6 deals; the Lone takes the face-up Widow and scores 2 per trick, the Pair 1 each."
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
        "key": "lone_tricks",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_win",
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
        "key": "role",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_colour",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "played_rank",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "strength",
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
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_in_deal",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "widow",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trump_order",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "veto_order",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trump_tokens",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "lone_tokens",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "lone_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clockwise",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "all_cards",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red 1",
          "Red 2",
          "Red 3",
          "Red 4",
          "Red 5",
          "Red 6",
          "Yellow 1",
          "Yellow 2",
          "Yellow 3",
          "Yellow 4",
          "Yellow 5",
          "Yellow 6",
          "Green 1",
          "Green 2",
          "Green 3",
          "Green 4",
          "Green 5",
          "Green 6",
          "Blue 1",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Blue 5",
          "Blue 6"
        ]
      },
      {
        "key": "colour_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Yellow",
          "Green",
          "Blue"
        ]
      },
      {
        "key": "lone_line",
        "visible": "none",
        "type": "list",
        "initial": [
          "First",
          "Second",
          "Third"
        ]
      },
      {
        "key": "trump_lines",
        "visible": "none",
        "type": "list",
        "initial": [
          [
            "Red",
            "Yellow",
            "Green",
            "Blue"
          ],
          [
            "Yellow",
            "Green",
            "Blue",
            "Red"
          ],
          [
            "Green",
            "Blue",
            "Red",
            "Yellow"
          ],
          [
            "Blue",
            "Red",
            "Yellow",
            "Green"
          ]
        ]
      },
      {
        "key": "veto_orders",
        "visible": "none",
        "type": "list",
        "initial": [
          [
            1,
            2,
            3
          ],
          [
            2,
            3,
            1
          ],
          [
            3,
            1,
            2
          ]
        ]
      },
      {
        "key": "players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "widow_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside_cards",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "lone_hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
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
        "key": "veto_rounds_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "trump_boxes",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "lone_boxes",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "tokens_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_lone_tokens_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lone_trick_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "lone_trick_count_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pair_trick_points_each",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "lone_cards_kept_back",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trump_strength_bonus",
        "visible": "public",
        "type": "number",
        "initial": 200
      },
      {
        "key": "led_strength_bonus",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "rank_weight_score",
        "visible": "public",
        "type": "number",
        "initial": 10000
      },
      {
        "key": "rank_weight_lone_tricks",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seats and clockwise order",
      "do": [
        {
          "set": {
            "key": "clockwise",
            "value": {
              "calc": "[p.seat for p in acting]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "scores start at zero",
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
            "players": "all",
            "key": "lone_tricks",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_win",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the full card set",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_cards"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "round",
      "label": "advance the round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "deal",
            "value": {
              "calc": "int((round - 1) / rounds_per_deal) + 1"
            }
          }
        },
        {
          "set": {
            "key": "round_in_deal",
            "value": {
              "calc": "(round - 1) % rounds_per_deal + 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "veto",
      "label": "shuffle and deal",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[]"
            }
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
            "key": "widow",
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
            "key": "trump_tokens",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "lone_tokens",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "trump_order",
            "value": {
              "calc": "trump_lines[(deal - 1) % len(trump_lines)]"
            }
          }
        },
        {
          "set": {
            "key": "veto_order",
            "value": {
              "calc": "veto_orders[(deal - 1) % len(veto_orders)]"
            }
          }
        },
        {
          "set": {
            "key": "trump",
            "value": ""
          }
        },
        {
          "set": {
            "key": "lone_seat",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "role",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "([c for c in trump_order if c not in trump_tokens] if len(trump_order) - len(trump_tokens) > 1 else []) + ([b for b in lone_line if b not in lone_tokens] if len(lone_tokens) < max_lone_tokens_per_deal and len(lone_line) - len(lone_tokens) > 1 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "veto",
      "label": "your new hand",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your hand for this deal:"
    },
    {
      "use": "tell",
      "phase": "veto",
      "label": "the widow and the board",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": "all",
      "text": "Deal {deal} of {deals}. The Widow, face up for everyone, is {widow}. The Nyet board is empty. TRUMP line, in order: {trump_order}. LONE line: First = seat {veto_order[0]}, Second = seat {veto_order[1]}, Third = seat {veto_order[2]}."
    },
    {
      "use": "poll",
      "phase": "veto",
      "label": "veto talk",
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
      "text": "Before the Nyet tokens go down, write one short message to the table. Everyone writes at the same time and all messages are shown together. Talk is not binding."
    },
    {
      "use": "ask",
      "phase": "veto",
      "label": "first nyet",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "you.seat == veto_order[0]"
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
            "append": {
              "key": "trump_tokens",
              "value": "$answer",
              "if": {
                "calc": "$answer in trump_order"
              }
            }
          },
          {
            "append": {
              "key": "lone_tokens",
              "value": "$answer",
              "if": {
                "calc": "$answer in lone_line"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "([c for c in trump_order if c not in trump_tokens] if len(trump_order) - len(trump_tokens) > 1 else []) + ([b for b in lone_line if b not in lone_tokens] if len(lone_tokens) < max_lone_tokens_per_deal and len(lone_line) - len(lone_tokens) > 1 else [])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (First) places a Nyet token on {value}."
      },
      "text": "You are First. Place one Nyet token on an empty box. A colour box vetoes that colour as trump; a LONE box (First, Second, Third) vetoes that position as the Lone. Tokens already placed: TRUMP {trump_tokens}, LONE {lone_tokens}."
    },
    {
      "use": "ask",
      "phase": "veto",
      "label": "second nyet",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "you.seat == veto_order[1]"
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
            "append": {
              "key": "trump_tokens",
              "value": "$answer",
              "if": {
                "calc": "$answer in trump_order"
              }
            }
          },
          {
            "append": {
              "key": "lone_tokens",
              "value": "$answer",
              "if": {
                "calc": "$answer in lone_line"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "([c for c in trump_order if c not in trump_tokens] if len(trump_order) - len(trump_tokens) > 1 else []) + ([b for b in lone_line if b not in lone_tokens] if len(lone_tokens) < max_lone_tokens_per_deal and len(lone_line) - len(lone_tokens) > 1 else [])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (Second) places a Nyet token on {value}."
      },
      "text": "You are Second. Place one Nyet token on an empty box. Tokens already placed: TRUMP {trump_tokens}, LONE {lone_tokens}."
    },
    {
      "use": "ask",
      "phase": "veto",
      "label": "third nyet",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": {
        "where": "you.seat == veto_order[2]"
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
            "append": {
              "key": "trump_tokens",
              "value": "$answer",
              "if": {
                "calc": "$answer in trump_order"
              }
            }
          },
          {
            "append": {
              "key": "lone_tokens",
              "value": "$answer",
              "if": {
                "calc": "$answer in lone_line"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (Third) places a Nyet token on {value}."
      },
      "text": "You are Third. Place one Nyet token on an empty box. Tokens already placed: TRUMP {trump_tokens}, LONE {lone_tokens}."
    },
    {
      "use": "update",
      "phase": "veto",
      "label": "trump and the lone",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "do": [
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "[c for c in trump_order if c not in trump_tokens][0]"
            }
          }
        },
        {
          "set": {
            "key": "lone_seat",
            "value": {
              "calc": "veto_order[0] if lone_line[0] not in lone_tokens else (veto_order[1] if lone_line[1] not in lone_tokens else veto_order[2])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "role",
            "value": {
              "calc": "'lone' if you.seat == lone_seat else 'pair'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "lone_seat"
            },
            "key": "hand",
            "value": {
              "calc": "widow"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "lone_seat"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "veto",
      "label": "the deal is set",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "to": "all",
      "text": "Trump is {trump}. Seat {lone_seat} is the Lone and takes the Widow ({widow}) into hand; seats {[p.seat for p in acting if p.seat != lone_seat]} are the Pair. Seat {lone_seat} leads the first trick."
    },
    {
      "use": "sync",
      "phase": "veto",
      "label": "your hand for the tricks",
      "when": {
        "calc": "round_in_deal == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand",
        "role"
      ],
      "text": "Your hand and role for this deal:"
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "lead",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "lead_card"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_colour",
              "value": {
                "calc": "[c for c in colour_names if c in $answer][0]"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_rank",
              "value": {
                "calc": "int($answer[-1])"
              }
            }
          },
          {
            "set": {
              "key": "led_colour",
              "value": {
                "calc": "[c for c in colour_names if c in $answer][0]"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "[c for c in you.hand if led_colour in c] if any(led_colour in c for c in you.hand) else you.hand"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
      },
      "text": "You lead this trick. Play any card from your hand, face up. Trump is {trump}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second card",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == leader % len(clockwise) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "second_card"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_colour",
              "value": {
                "calc": "[c for c in colour_names if c in $answer][0]"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_rank",
              "value": {
                "calc": "int($answer[-1])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play a card to the trick. If you hold a card of the led colour you must play one (only those are offered); otherwise you may play any card. Trump is {trump}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third card",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": {
        "where": "you.seat == (leader + 1) % len(clockwise) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "third_card"
      },
      "each": {
        "do": [
          {
            "remove": {
              "player": "$seat",
              "key": "hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_colour",
              "value": {
                "calc": "[c for c in colour_names if c in $answer][0]"
              }
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_rank",
              "value": {
                "calc": "int($answer[-1])"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
      },
      "text": "Play the last card to the trick. If you hold a card of the led colour you must play one (only those are offered); otherwise you may play any card. Trump is {trump}."
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
            "key": "strength",
            "value": {
              "calc": "(trump_strength_bonus if you.played_colour == trump else 0) + (led_strength_bonus if you.played_colour == led_colour else 0) + you.played_rank"
            }
          }
        },
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "[p.seat for p in acting if p.strength == max([q.strength for q in acting])][0]"
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
              "calc": "lone_trick_points"
            },
            "if": {
              "calc": "trick_winner == lone_seat"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "lone_tricks",
            "value": {
              "calc": "lone_trick_count_gain"
            },
            "if": {
              "calc": "trick_winner == lone_seat"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.role == 'pair'"
            },
            "key": "score",
            "value": {
              "calc": "pair_trick_points_each"
            },
            "if": {
              "calc": "trick_winner != lone_seat"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "trick_winner"
            },
            "key": "last_win",
            "value": {
              "calc": "round"
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
      ]
    },
    {
      "use": "tell",
      "phase": "trick",
      "label": "trick result",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "to": "all",
      "text": "Cards played: {lead_card}, {second_card}, {third_card} (trump {trump}). Seat {trick_winner} wins the trick and leads next. Standings [seat, score, lone_tricks, last_win]: {[[p.seat, p.score, p.lone_tricks, p.last_win] for p in acting]}."
    },
    {
      "use": "sync",
      "phase": "trick",
      "label": "your remaining hand",
      "when": {
        "calc": "round_in_deal >= 2"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your remaining hand:"
    },
    {
      "use": "check",
      "phase": "trick",
      "label": "after round 36",
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
      "rank_by": "you.score * rank_weight_score + you.lone_tricks * rank_weight_lone_tricks + you.last_win",
      "text": "Winner: {result}. Final [seat, score, lone_tricks, last_win]: {[[p.seat, p.score, p.lone_tricks, p.last_win] for p in acting]}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "Nyet! Trio is for exactly {players} players: seats 1, 2 and 3. Clockwise order is 1 -> 2 -> 3 -> 1. The deck has {deck_size} unique cards: {colours} colours (Red, Yellow, Green, Blue), each numbered 1 to {ranks_per_colour}. Everyone's score, lone_tricks and last_win start at 0.\n\nThe game lasts {total_rounds} rounds: {deals} deals of {rounds_per_deal} rounds each. Round 1 of each deal (rounds 1, 7, 13, 19, 25, 31) is the VETO round; rounds 2 to 6 of each deal are TRICK rounds, one trick each, so {tricks_per_deal} tricks per deal.\n\nVETO ORDER (First, Second, Third): deals 1 and 4: seats 1, 2, 3; deals 2 and 5: seats 2, 3, 1; deals 3 and 6: seats 3, 1, 2.\nTRUMP LINE ORDER: deal 1: Red, Yellow, Green, Blue; deal 2: Yellow, Green, Blue, Red; deal 3: Green, Blue, Red, Yellow; deal 4: Blue, Red, Yellow, Green; deal 5: Red, Yellow, Green, Blue; deal 6: Yellow, Green, Blue, Red.\n\nVETO ROUND. (1) All {deck_size} cards are shuffled. Each player is dealt {hand_size} cards as a private hand. One of the remaining 9 is turned face up: this is the Widow, which everyone sees. The other {set_aside_cards} are set aside face down and are never revealed. Cards left in hands from the previous deal are discarded unseen before the shuffle. (2) The Nyet board is cleared. It has two lines: the TRUMP line ({trump_boxes} colour boxes, in this deal's order) and the LONE line ({lone_boxes} boxes: First, Second, Third). (3) Talk: all three players write one short message at the same time, without seeing the others' messages; then all messages are shown to everyone. Talk is not binding. (4) First, then Second, then Third each places one Nyet token on one empty box ({tokens_per_deal} tokens per deal), seeing the tokens already placed. A token may go on any empty TRUMP box. A token may go on a LONE box only if no token is yet on the LONE line: at most {max_lone_tokens_per_deal} LONE token per deal. A player may not token the last empty box of a line. You are only offered the boxes you may legally choose, and there is always at least one. (5) Trump is the first untokened box on the TRUMP line, in this deal's order. The Lone is the seat at the first untokened box on the LONE line (First, then Second, then Third). The other two players are the Pair. (6) The Lone adds the Widow to their hand and holds {lone_hand_size} cards. The Lone leads the first trick.\n\nTRICK ROUND. (7) The leader plays one card face up. Then the next player clockwise plays one, then the third player plays one. Each sees the cards already played. The led colour is the colour of the leader's card. A player holding a card of the led colour must play one (only those cards are offered); a player with none may play any card. (8) Winner: if any trump was played, the highest trump wins. Otherwise the highest card of the led colour wins. Cards are unique, so there is always one winner. (9) Scoring: if the Lone won, the Lone gains {lone_trick_points} points and {lone_trick_count_gain} lone_trick. If a Pair member won, each Pair member gains {pair_trick_points_each} point. The winner's last_win is set to the current round number. (10) The winner leads the next trick of this deal. (11) The cards played, the winner and all scores are announced.\nAfter the 5th trick of a deal, the Lone still holds {lone_cards_kept_back} card. It is never played or revealed and is discarded at the next shuffle. Choosing which card to keep back is the Lone's discard.\n\nEND. After round {total_rounds} the game ends. The highest score wins. If players tie, the tied player with the most lone_tricks wins. If still tied, the tied player with the highest last_win wins (the one who won a trick most recently). If still tied, the game is a draw and those players share the win."
}
```
````
