# 14 coder

- time: 2026-10-28T03:26:50+00:00 (126.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 726a2acb1a80a223, reply sha256 ab998ec945881079

## Sent

````
# Task: write the XColos game file for "Concealed Quadrille"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

PACK AND CARD CODES: 20 cards. Each suit has A, 2, J, Q, K. Suits are numbered Spades 1, Clubs 2, Hearts 3, Diamonds 4. Ranks are numbered A 1, 2 2, J 3, Q 4, K 5. A card's code is 10 x suit + rank: for example K of Hearts = 35, A of Spades = 11 (Spadille), A of Clubs = 21 (Baste). Cards are always shown to players by name and code.

SEATS AND PUBLIC RECORDS: Seats 1-4 sit clockwise. Each player has a public score (starts 0), a public 'tricks won' total for the game (starts 0) and a public 'hand tricks' count (reset to 0 at the start of each hand).

STRUCTURE: 8 hands of 5 tricks, 40 rounds. One round is one trick. Hand h covers rounds 5h-4 to 5h. The priority seat of hand h is seat ((h-1) mod 4)+1, so the order is 1, 2, 3, 4, 1, 2, 3, 4.

START OF EACH HAND (first trick of the hand only):
1. DEAL: Shuffle the 20 cards and deal 5 privately to each player. Set every player's hand tricks to 0.
2. BID: All players at the same moment choose Pass, 3, 4 or 5: the number of tricks out of 5 their side promises to win. All bids are announced.
3. TAKER: The highest bid wins. Ties go to the tied player who comes first clockwise starting from the priority seat (that seat itself first). If all four pass, the priority seat is Taker with contract 3. The winning bid is the contract B.
4. DECLARATION: The Taker privately chooses a trump suit (Spades, Clubs, Hearts or Diamonds) and a partner seat (any of seats 1-4, including their own): 16 options. The trump suit is announced to all. If the partner seat is another player, the hand is a CALL and that player alone is privately told 'you are the Taker's partner'. If the Taker names their own seat, the hand is a SOLO and nobody is told anything beyond the trump suit. Nobody else learns the partner seat until the hand ends.

TRUMPS: The trumps are every card of the trump suit plus Spadille (code 11) and Baste (code 21), whatever the trump suit. Spadille and Baste count as trump-suit cards and as no other suit. Manille is the 2 of the trump suit. With red trump there are 7 trumps, and Spades and Clubs each have 4 non-trump cards. With black trump there are 6 trumps.

PLAY OF A TRICK:
- On the first trick of a hand the Taker leads. Afterwards the winner of the previous trick leads.
- The leader chooses any card from their hand. It is removed from the hand and shown to all.
- The led suit L is the trump suit if the led card is Spadille, Baste or any trump-suit card. Otherwise it is the led card's suit.
- The other three players then each choose a card from their hand at the same moment. A player holding any card of suit L (counting Spadille and Baste as trump suit) must play one. A player holding none may play any card. Illegal choices are not accepted.

CARD POWER: For each of the four played cards, with t the trump suit number:
- Spadille (11): 30.
- Manille (code 10t+2): 29.
- Baste (21): 28.
- Other card of the trump suit: 20 + rank (K 25, Q 24, J 23, red A 21).
- Non-trump card of the led suit: its rank (K 5, Q 4, J 3, 2 2, red A 1).
- Any other card: 0.
The highest power wins the trick. Ties cannot occur. All four cards and the winner are announced, and the winner adds 1 to their tricks won and their hand tricks.

HAND SCORING (after the fifth trick of a hand):
- T = the Taker's hand tricks, plus the partner's hand tricks if the hand is a call.
- d = B-1 if T >= B (made). d = -(B-1) if T = B-1 (remise). d = -B if T <= B-2 (codille).
- CALL: the Taker and the partner each gain d; the other two each lose d.
- SOLO: the Taker gains 3d; each of the other three loses d.
- Every hand sums to zero. The partner seat (or the fact that it was a solo), T, d and all scores are then announced.

NO TALK: There is no discussion phase. All communication is through bids and cards.

END: After round 40 the game ends and the winner is decided as in the objective.

STEP LIST PER ROUND (for building):
(1) [first trick of hand] deal 5 cards to each player.
(2) [first trick] reset hand tricks to 0.
(3) [first trick] simultaneous bid poll.
(4) [first trick] announce bids, compute Taker and B with key = bid x 10 + (4 - ((seat - priority) mod 4)), Pass = 0; all pass gives the priority seat and B = 3.
(5) [first trick] Taker's declaration choice.
(6) [first trick] store t and the hidden partner, announce trump.
(7) [first trick, when call] privately notify the partner.
(8) set leader = Taker on the first trick, else the last winner.
(9) leader's lead choice, remove the card, announce.
(10) compute L.
(11) simultaneous follow poll of the other three, with the legality check.
(12) compute power for all four played cards with the one formula.
(13) argmax: set last winner.
(14) announce the cards and winner, add 1 to the winner's tricks won and hand tricks.
(15) [fifth trick of hand] compute T and d.
(16) [fifth trick] update all scores with call/solo conditions.
(17) [fifth trick] announce partner or solo, T, d and scores.
(18) [round 40] decide the winner.

How the winner is decided: After round 40, the player with the highest score wins. If several tie for the highest score, the one among them with the most tricks won over the whole game wins. If that also ties, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Concealed Quadrille (4 to 4 players, best with 4)

Four-player trick-taking game over 8 hands of 5 tricks. Players bid for the contract, the Taker names trumps and secretly calls a partner (or plays solo), and the hand is scored to zero sum.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. running game score
  - each player: tricks_won (number, starts 0); everyone sees it. tricks won over the whole game, used as the tie-break
  - each player: hand_tricks (number, starts 0); everyone sees it. tricks won in the current hand, reset each hand
  - each player: hand (list, starts []); only its owner sees it. card codes held, shown by name and code
  - each player: bid (number, starts 0); everyone sees it. this hand's bid (0 = Pass, else 3, 4 or 5)
  - each player: is_partner (bool, starts False); only its owner sees it. privately told: you are the Taker's partner in this hand (call only)
  - each player: played_card (number, starts 0); everyone sees it. code of the card played to the current trick
  - each player: power (number, starts 0); everyone sees it. card power of played_card in the current trick
  - the table: deck (list, starts [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45]); hidden from all players. undealt cards
  - the table: round_no (number, starts 0); everyone sees it. current round (trick) number, 1 to 40
  - the table: hand_no (number, starts 0); everyone sees it. current hand h = ceil(round_no / 5)
  - the table: trick_in_hand (number, starts 0); everyone sees it. round_no - 5*(hand_no - 1), 1 to 5
  - the table: priority_seat (number, starts 1); everyone sees it. ((hand_no - 1) mod 4) + 1
  - the table: taker (number, starts 0); everyone sees it. Taker's seat this hand
  - the table: contract (number, starts 0); everyone sees it. contract B
  - the table: trump (number, starts 0); everyone sees it. trump suit number t (1 Spades, 2 Clubs, 3 Hearts, 4 Diamonds)
  - the table: partner_seat (number, starts 0); hidden from all players. seat named by the Taker; equal to taker means solo; announced at hand end
  - the table: is_solo (bool, starts False); hidden from all players. partner_seat == taker; announced at hand end
  - the table: leader (number, starts 0); everyone sees it. seat leading the current trick
  - the table: led_suit (number, starts 0); everyone sees it. led suit L: trump if the led card is 11, 21 or of suit trump, else floor(code/10)
  - the table: last_winner (number, starts 0); everyone sees it. winner of the most recent trick
  - the table: hand_total (number, starts 0); everyone sees it. T: Taker's hand_tricks plus partner's if call (announced at hand end)
  - the table: hand_delta (number, starts 0); everyone sees it. d for the hand (announced at hand end)
  - parameters, each kept as a table attribute: deck_size = 20, suits = 4, ranks_per_suit = 5, hand_size = 5, hands = 8, tricks_per_hand = 5, rounds = 40, bid_pass_value = 0, bid_min = 3, bid_max = 5, all_pass_contract = 3, declaration_options = 16, spadille_code = 11, baste_code = 21, power_spadille = 30, power_manille = 29, power_baste = 28, power_trump_base = 20, power_off_suit = 0, solo_multiplier = 3, trumps_red = 7, trumps_black = 6, tiebreak_key_bid_multiplier = 10, rank_score_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 to 4 sit clockwise.
  2. Every player's score, tricks_won and hand_tricks are 0.
  3. The deck holds the 20 codes 11-15, 21-25, 31-35, 41-45 (code = 10 x suit + rank; suits Spades 1, Clubs 2, Hearts 3, Diamonds 4; ranks A 1, 2 2, J 3, Q 4, K 5).
  4. Cards are always shown to players by name and code (e.g. 11 = Ace of Spades, Spadille; 21 = Ace of Clubs, Baste).
  5. round_no is 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_no += 1; hand_no = ceil(round_no/5); trick_in_hand = round_no - 5*(hand_no-1); priority_seat = ((hand_no-1) mod 4)+1; every played_card = 0 and power = 0
  2. [update] all players. What happens: when trick_in_hand == 1: return all cards to deck (deck = all 20 codes, every hand = []), then deal 5 random cards from deck to each player's hand (remove from deck, append to hand); every hand_tricks = 0, bid = 0, is_partner = false
  3. [sync] all players. What happens: when trick_in_hand == 1: each player is sent their own hand by name and code
  4. [poll] all players answers: one of: Pass, 3, 4, 5. What happens: when trick_in_hand == 1: bid = 0 for Pass, else the number; all bids announced together
  5. [update] all players. What happens: when trick_in_hand == 1: key(seat) = bid*10 + (4 - ((seat - priority_seat) mod 4)); if every bid == 0 then taker = priority_seat and contract = 3, else taker = seat with max key and contract = that seat's bid; announce taker and contract
  6. [ask] seat taker answers: one of 16 options: trump suit (Spades, Clubs, Hearts, Diamonds) x partner seat (1, 2, 3, 4; own seat = solo). What happens: when trick_in_hand == 1: trump = chosen suit number; partner_seat = chosen seat; is_solo = (partner_seat == taker); announce trump only
  7. [update] seat partner_seat. What happens: when trick_in_hand == 1 and is_solo == false: is_partner of partner_seat = true; that player alone is privately told 'you are the Taker's partner'
  8. [update] all players. What happens: leader = taker if trick_in_hand == 1, else last_winner
  9. [ask] seat leader answers: any card code in the leader's hand. What happens: leader's played_card = chosen code; remove it from hand; announce the card by name and code
  10. [update] all players. What happens: suit(c) = trump if c in {11,21}, else floor(c/10); led_suit = suit(leader's played_card)
  11. [poll] every seat except leader answers: a card code from own hand: if the hand holds any card with suit(c) == led_suit, only those cards are offered, else any card. What happens: each responder's played_card = chosen code; remove it from hand
  12. [update] all players. What happens: for each player with c = played_card, r = c mod 10: power = 30 if c == 11; 29 if c == 10*trump+2; 28 if c == 21; 20 + r if floor(c/10) == trump; r if suit(c) == led_suit; else 0
  13. [update] all players. What happens: last_winner = seat with the highest power (ties impossible); last_winner's tricks_won += 1 and hand_tricks += 1; announce all four cards and the winner
  14. [update] all players. What happens: when trick_in_hand == 5: hand_total = taker.hand_tricks + (is_solo ? 0 : partner_seat.hand_tricks); hand_delta = contract-1 if hand_total >= contract; -(contract-1) if hand_total == contract-1; -contract if hand_total <= contract-2
  15. [update] all players. What happens: when trick_in_hand == 5: if is_solo then taker.score += 3*hand_delta and each other seat score -= hand_delta; else taker and partner_seat score += hand_delta and the other two score -= hand_delta
  16. [tell] all players. What happens: when trick_in_hand == 5: announce partner_seat (or that it was a solo), hand_total, hand_delta and all scores
  17. [check] all players. What happens: end the game if round_no == 40, else continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The pack has 20 cards with codes 10 x suit + rank, suits Spades 1, Clubs 2, Hearts 3, Diamonds 4 and ranks A 1, 2 2, J 3, Q 4, K 5; 11 is Spadille and 21 is Baste.
  R2. The game has 40 rounds; each round is one trick; hand h covers rounds 5h-4 to 5h, so there are 8 hands of 5 tricks.
  R3. The priority seat of hand h is ((h-1) mod 4)+1, giving 1, 2, 3, 4, 1, 2, 3, 4.
  R4. On the first trick of each hand, all 20 cards are shuffled, each player is dealt 5 private cards, and every hand_tricks is set to 0.
  R5. On the first trick of each hand, all players bid at once, each choosing Pass, 3, 4 or 5, and all bids are announced.
  R6. The highest bid becomes Taker with contract B equal to that bid; ties go to the tied seat first clockwise from the priority seat (key = bid*10 + 4 - ((seat - priority) mod 4)).
  R7. When all four players pass, the priority seat is Taker with contract 3.
  R8. The Taker privately chooses a trump suit and a partner seat from 16 options, and the trump suit is announced to all.
  R9. When the Taker names another seat, the hand is a call and only that seat is privately told it is the partner.
  R10. When the Taker names their own seat, the hand is a solo and nobody is told anything beyond the trump suit.
  R11. The partner seat stays hidden until the hand ends.
  R12. The trumps are every card of the trump suit plus 11 and 21; 11 and 21 count only as the trump suit, and Manille is code 10*trump+2.
  R13. The Taker leads the first trick of a hand, and the previous trick's winner leads every later trick.
  R14. The led card leaves the leader's hand and is shown to all; the led suit is trump if the card is 11, 21 or of the trump suit, else the card's suit.
  R15. The other three players play at once, and a player holding any card of the led suit (11 and 21 count as trump) must play one.
  R16. A player holding no card of the led suit may play any card, and illegal cards are never accepted.
  R17. Card power is 30 for 11, 29 for Manille, 28 for 21, 20 + rank for other trump-suit cards, the rank for non-trump cards of the led suit, and 0 for any other card.
  R18. The highest power wins the trick; all four cards and the winner are announced, and the winner gains 1 tricks_won and 1 hand_tricks.
  R19. After the fifth trick of a hand, T is the Taker's hand_tricks plus the partner's hand_tricks if the hand is a call.
  R20. When T >= B, d = B-1 (made); when T = B-1, d = -(B-1) (remise); when T <= B-2, d = -B (codille).
  R21. In a call, the Taker and the partner each gain d and the other two each lose d.
  R22. In a solo, the Taker gains 3d and each of the other three loses d.
  R23. After each hand, the partner seat (or solo), T, d and all scores are announced.
  R24. There is no talk phase; players communicate only through bids and cards.
  R25. After round 40 the game ends: highest score wins, ties on score are broken by most tricks_won, and a further tie is a shared win (draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid (first trick of each hand) | asked: all seats | options: Pass, 3, 4, 5
  - Declaration (first trick of each hand) | asked: the Taker only | options: 16 combinations of trump suit (Spades, Clubs, Hearts, Diamonds) and partner seat (1, 2, 3, 4, own seat meaning solo)
  - Lead | asked: the leader only | options: every card in the leader's hand
  - Follow | asked: the three seats other than the leader | options: a seat holding any card of the led suit (11 and 21 counted as trump suit): only those cards; a seat holding none: every card in its hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_no == 40
  - each player's standing: you.score * 100 + you.tricks_won (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest score wins; among players tied on score, the one with the most tricks won over the game wins; players still level share the win (a draw).
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

- each player: `score` (number, visible: public, starts 0): running game score
- each player: `tricks_won` (number, visible: public, starts 0): tricks won over the whole game, used as the tie-break
- each player: `hand_tricks` (number, visible: public, starts 0): tricks won in the current hand, reset each hand
- the table: `taker` (number, visible: public, starts 0): Taker's seat this hand
- the table: `contract` (number, visible: public, starts 0): contract B
- the table: `trump` (number, visible: public, starts 0): trump suit number t (1 Spades, 2 Clubs, 3 Hearts, 4 Diamonds)
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 20, suits = 4, ranks_per_suit = 5, hand_size = 5, hands = 8, tricks_per_hand = 5, rounds = 40, bid_pass_value = 0, bid_min = 3, bid_max = 5, all_pass_contract = 3, declaration_options = 16, spadille_code = 11, baste_code = 21, power_spadille = 30, power_manille = 29, power_baste = 28, power_trump_base = 20, power_off_suit = 0, solo_multiplier = 3, trumps_red = 7, trumps_black = 6, tiebreak_key_bid_multiplier = 10, rank_score_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.tricks_won`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "concealed_quadrille",
    "name": "Concealed Quadrille",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four players, 8 hands of 5 tricks: bid for the contract, name trumps, secretly call a partner or go solo, and score to zero sum."
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
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_tricks",
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
        "key": "hand_names",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "is_partner",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "follow_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45]
      },
      {
        "key": "all_codes",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_name",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "suit_names",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "seat_labels",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead_code",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "taker",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_name",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "partner_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "is_solo",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit_name",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_report",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hand_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_delta",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_report",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
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
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "bid_pass_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "all_pass_contract",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "declaration_options",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "spadille_code",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "baste_code",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "power_spadille",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "power_manille",
        "visible": "public",
        "type": "number",
        "initial": 29
      },
      {
        "key": "power_baste",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "power_trump_base",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "power_off_suit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "solo_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "trumps_red",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "trumps_black",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tiebreak_key_bid_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "rank_score_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
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
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_tricks",
            "value": 0
          }
        },
        {
          "set": {
            "key": "all_codes",
            "value": [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45]
          }
        },
        {
          "set": {
            "key": "card_name",
            "value": [
              "", "", "", "", "", "", "", "", "", "", "",
              "Ace of Spades (11, Spadille)",
              "2 of Spades (12)",
              "Jack of Spades (13)",
              "Queen of Spades (14)",
              "King of Spades (15)",
              "", "", "", "", "",
              "Ace of Clubs (21, Baste)",
              "2 of Clubs (22)",
              "Jack of Clubs (23)",
              "Queen of Clubs (24)",
              "King of Clubs (25)",
              "", "", "", "", "",
              "Ace of Hearts (31)",
              "2 of Hearts (32)",
              "Jack of Hearts (33)",
              "Queen of Hearts (34)",
              "King of Hearts (35)",
              "", "", "", "", "",
              "Ace of Diamonds (41)",
              "2 of Diamonds (42)",
              "Jack of Diamonds (43)",
              "Queen of Diamonds (44)",
              "King of Diamonds (45)"
            ]
          }
        },
        {
          "set": {
            "key": "suit_names",
            "value": ["", "Spades", "Clubs", "Hearts", "Diamonds"]
          }
        },
        {
          "set": {
            "key": "seat_labels",
            "value": ["", "seat 1", "seat 2", "seat 3", "seat 4"]
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_codes"
            }
          }
        },
        {
          "set": {
            "key": "round_no",
            "value": 0
          }
        }
      ],
      "text": "Seats 1 to 4 sit clockwise. Scores and tricks start at 0. The pack holds 20 cards, always shown by name and code."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "trick",
      "label": "the next trick",
      "do": [
        {
          "adjust": {
            "key": "round_no",
            "value": 1
          }
        },
        {
          "set": {
            "key": "hand_no",
            "value": {
              "calc": "int((round_no - 1) / tricks_per_hand) + 1"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "round_no - tricks_per_hand * (hand_no - 1)"
            }
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": {
              "calc": "((hand_no - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "power",
            "value": 0
          }
        }
      ],
      "text": "Round {round_no}: trick {trick_in_hand} of hand {hand_no}. Priority seat this hand: {priority_seat}."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_codes"
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
            "key": "hand_tricks",
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
            "key": "bid_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_partner",
            "value": false
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "sorted(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_names",
            "value": {
              "calc": "[card_name[c] for c in you.hand]"
            }
          }
        }
      ],
      "text": "Hand {hand_no}: the 20 cards are shuffled and 5 are dealt privately to each player."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand_names",
        "hand"
      ],
      "text": "Your cards for hand {hand_no} (name and code):"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bid",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Pass",
          "3",
          "4",
          "5"
        ]
      },
      "store": "bid_said",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Hand {hand_no}, priority seat {priority_seat}. Bid Pass, 3, 4 or 5: the number of tricks out of 5 your side promises to win. The highest bid becomes Taker; ties go to the tied seat first clockwise from the priority seat. If all pass, the priority seat is Taker with contract {all_pass_contract}."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the taker",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "bid_pass_value if you.bid_said == 'Pass' else int(you.bid_said)"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_key_bid_multiplier + (len(players) - ((p.seat - priority_seat) % len(players))) for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "taker",
            "value": {
              "calc": "priority_seat if all(p.bid == bid_pass_value for p in players) else [p.seat for p in players if p.bid * tiebreak_key_bid_multiplier + (len(players) - ((p.seat - priority_seat) % len(players))) == best_key][0]"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "all_pass_contract if all(p.bid == bid_pass_value for p in players) else max([p.bid for p in players])"
            }
          }
        }
      ],
      "text": "Seat {taker} is the Taker with contract {contract}."
    },
    {
      "use": "ask",
      "phase": "declare",
      "label": "the declaration",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": {
        "where": "you.seat == taker"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Spades, partner seat 1",
          "Spades, partner seat 2",
          "Spades, partner seat 3",
          "Spades, partner seat 4",
          "Clubs, partner seat 1",
          "Clubs, partner seat 2",
          "Clubs, partner seat 3",
          "Clubs, partner seat 4",
          "Hearts, partner seat 1",
          "Hearts, partner seat 2",
          "Hearts, partner seat 3",
          "Hearts, partner seat 4",
          "Diamonds, partner seat 1",
          "Diamonds, partner seat 2",
          "Diamonds, partner seat 3",
          "Diamonds, partner seat 4"
        ]
      },
      "verify": {
        "bind": "decl"
      },
      "text": "You are the Taker with contract {contract}. Choose a trump suit and a partner seat. Naming your own seat plays a solo. Only the trump suit is announced; the partner (if another seat) is told privately; nobody else learns the partner seat until the hand ends."
    },
    {
      "use": "update",
      "phase": "declare",
      "label": "trumps declared",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "1 if 'Spades' in $decl else (2 if 'Clubs' in $decl else (3 if 'Hearts' in $decl else 4))"
            }
          }
        },
        {
          "set": {
            "key": "partner_seat",
            "value": {
              "calc": "1 if 'seat 1' in $decl else (2 if 'seat 2' in $decl else (3 if 'seat 3' in $decl else 4))"
            }
          }
        },
        {
          "set": {
            "key": "is_solo",
            "value": {
              "calc": "partner_seat == taker"
            }
          }
        },
        {
          "set": {
            "key": "trump_name",
            "value": {
              "calc": "suit_names[trump]"
            }
          }
        }
      ],
      "text": "Seat {taker} names {trump_name} as trumps (suit {trump}). Contract {contract}."
    },
    {
      "use": "update",
      "phase": "declare",
      "label": "the partner is told",
      "when": {
        "calc": "trick_in_hand == 1 and not is_solo"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "partner_seat"
            },
            "key": "is_partner",
            "value": true,
            "announce_to": {
              "where": "you.seat == partner_seat"
            },
            "text": "You are the Taker's partner in this hand."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the leader",
      "do": [
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "taker if trick_in_hand == 1 else last_winner"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == leader"
            },
            "key": "offer",
            "value": {
              "calc": "[card_name[c] for c in you.hand]"
            }
          }
        }
      ],
      "text": "S
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (led_suit_name, trump_name) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "concealed_quadrille",
    "name": "Concealed Quadrille",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four players, 8 hands of 5 tricks: bid for the contract, name trumps, secretly call a partner or go solo, and score to zero sum."
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
        "key": "tricks_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_tricks",
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
        "key": "hand_names",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "is_partner",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "played_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "power",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "follow_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45]
      },
      {
        "key": "all_codes",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_name",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "suit_names",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "seat_labels",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead_code",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_in_hand",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "taker",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "contract",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "partner_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "is_solo",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "leader",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_report",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "hand_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_delta",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_report",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ranks_per_suit",
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
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "bid_pass_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "all_pass_contract",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "declaration_options",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "spadille_code",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "baste_code",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "power_spadille",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "power_manille",
        "visible": "public",
        "type": "number",
        "initial": 29
      },
      {
        "key": "power_baste",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "power_trump_base",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "power_off_suit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "solo_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "trumps_red",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "trumps_black",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "tiebreak_key_bid_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "rank_score_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
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
            "key": "tricks_won",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_tricks",
            "value": 0
          }
        },
        {
          "set": {
            "key": "all_codes",
            "value": [11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45]
          }
        },
        {
          "set": {
            "key": "card_name",
            "value": [
              "", "", "", "", "", "", "", "", "", "", "",
              "Ace of Spades (11, Spadille)",
              "2 of Spades (12)",
              "Jack of Spades (13)",
              "Queen of Spades (14)",
              "King of Spades (15)",
              "", "", "", "", "",
              "Ace of Clubs (21, Baste)",
              "2 of Clubs (22)",
              "Jack of Clubs (23)",
              "Queen of Clubs (24)",
              "King of Clubs (25)",
              "", "", "", "", "",
              "Ace of Hearts (31)",
              "2 of Hearts (32)",
              "Jack of Hearts (33)",
              "Queen of Hearts (34)",
              "King of Hearts (35)",
              "", "", "", "", "",
              "Ace of Diamonds (41)",
              "2 of Diamonds (42)",
              "Jack of Diamonds (43)",
              "Queen of Diamonds (44)",
              "King of Diamonds (45)"
            ]
          }
        },
        {
          "set": {
            "key": "suit_names",
            "value": ["", "Spades", "Clubs", "Hearts", "Diamonds"]
          }
        },
        {
          "set": {
            "key": "seat_labels",
            "value": ["", "Seat 1", "Seat 2", "Seat 3", "Seat 4"]
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_codes"
            }
          }
        },
        {
          "set": {
            "key": "round_no",
            "value": 0
          }
        }
      ],
      "text": "Seats 1 to 4 sit clockwise. Scores and tricks start at 0. The pack holds 20 cards, always shown by name and code."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "trick",
      "label": "the next trick",
      "do": [
        {
          "adjust": {
            "key": "round_no",
            "value": 1
          }
        },
        {
          "set": {
            "key": "hand_no",
            "value": {
              "calc": "int((round_no - 1) / tricks_per_hand) + 1"
            }
          }
        },
        {
          "set": {
            "key": "trick_in_hand",
            "value": {
              "calc": "round_no - tricks_per_hand * (hand_no - 1)"
            }
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": {
              "calc": "((hand_no - 1) % len(players)) + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "power",
            "value": 0
          }
        }
      ],
      "text": "Round {round_no}: trick {trick_in_hand} of hand {hand_no}. Priority seat this hand: {priority_seat}."
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_codes"
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
            "key": "hand_tricks",
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
            "key": "bid_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "is_partner",
            "value": false
          }
        },
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "sorted(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_names",
            "value": {
              "calc": "[card_name[c] for c in you.hand]"
            }
          }
        }
      ],
      "text": "Hand {hand_no}: the 20 cards are shuffled and 5 are dealt privately to each player."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand_names",
        "hand"
      ],
      "text": "Your cards for hand {hand_no} (name and code):"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bid",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Pass",
          "3",
          "4",
          "5"
        ]
      },
      "store": "bid_said",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} bids {value}."
      },
      "text": "Hand {hand_no}, priority seat {priority_seat}. Bid Pass, 3, 4 or 5: the number of tricks out of 5 your side promises to win. The highest bid becomes Taker; ties go to the tied seat first clockwise from the priority seat. If all pass, the priority seat is Taker with contract {all_pass_contract}."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the taker",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "bid_pass_value if you.bid_said == 'Pass' else int(you.bid_said)"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max([p.bid * tiebreak_key_bid_multiplier + (len(players) - ((p.seat - priority_seat) % len(players))) for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "taker",
            "value": {
              "calc": "priority_seat if all(p.bid == bid_pass_value for p in players) else [p.seat for p in players if p.bid * tiebreak_key_bid_multiplier + (len(players) - ((p.seat - priority_seat) % len(players))) == best_key][0]"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "all_pass_contract if all(p.bid == bid_pass_value for p in players) else max([p.bid for p in players])"
            }
          }
        }
      ],
      "text": "Seat {taker} is the Taker with contract {contract}."
    },
    {
      "use": "ask",
      "phase": "declare",
      "label": "the declaration",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "to": {
        "where": "you.seat == taker"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Spades, partner seat 1",
          "Spades, partner seat 2",
          "Spades, partner seat 3",
          "Spades, partner seat 4",
          "Clubs, partner seat 1",
          "Clubs, partner seat 2",
          "Clubs, partner seat 3",
          "Clubs, partner seat 4",
          "Hearts, partner seat 1",
          "Hearts, partner seat 2",
          "Hearts, partner seat 3",
          "Hearts, partner seat 4",
          "Diamonds, partner seat 1",
          "Diamonds, partner seat 2",
          "Diamonds, partner seat 3",
          "Diamonds, partner seat 4"
        ]
      },
      "verify": {
        "bind": "decl"
      },
      "text": "You are the Taker with contract {contract}. Choose a trump suit and a partner seat. Naming your own seat plays a solo. Only the trump suit is announced; the partner (if another seat) is told privately; nobody else learns the partner seat until the hand ends."
    },
    {
      "use": "update",
      "phase": "declare",
      "label": "trumps declared",
      "when": {
        "calc": "trick_in_hand == 1"
      },
      "do": [
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "1 if 'Spades' in $decl else (2 if 'Clubs' in $decl else (3 if 'Hearts' in $decl else 4))"
            }
          }
        },
        {
          "set": {
            "key": "partner_seat",
            "value": {
              "calc": "1 if 'seat 1' in $decl else (2 if 'seat 2' in $decl else (3 if 'seat 3' in $decl else 4))"
            }
          }
        },
        {
          "set": {
            "key": "is_solo",
            "value": {
              "calc": "partner_seat == taker"
            }
          }
        },
        {
          "set": {
            "key": "trump_name",
            "value": {
              "calc": "suit_names[trump]"
            }
          }
        }
      ],
      "text": "Seat {taker} names {trump_name} as trumps (suit {trump}). Contract {contract}."
    },
    {
      "use": "update",
      "phase": "declare",
      "label": "the partner is told",
      "when": {
        "calc": "trick_in_hand == 1 and not is_solo"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "partner_seat"
            },
            "key": "is_partner",
            "value": true,
            "announce_to": {
              "where": "you.seat == partner_seat"
            },
            "text": "You are the Taker's partner in this hand."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the leader",
      "do": [
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "taker if trick_in_hand == 1 else last_winner"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == leader"
            },
            "key": "offer",
            "value": {
              "calc": "[card_name[c] for c in you.hand]"
            }
          }
        }
      ],
      "text": "Seat {leader} leads trick {trick_in_hand} of hand {hand_no}."
    },
    {
      "use": "ask",
      "phase": "lead",
      "label": "the lead",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "lead"
      },
      "text": "You lead trick {trick_in_hand}. Trumps: {trump_name} (suit {trump}), plus Spadille (11) and Baste (21). Choose any card from your hand; it is shown to all."
    },
    {
      "use": "update",
      "phase": "lead",
      "label": "the led card",
      "do": [
        {
          "set": {
            "key": "lead_code",
            "value": {
              "calc": "[c for c in all_codes if card_name[c] == $lead][0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "leader"
            },
            "key": "played_card",
            "value": {
              "calc": "lead_code"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "hand",
            "value": {
              "calc": "lead_code"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "leader"
            },
            "key": "hand_names",
            "value": {
              "calc": "[card_name[c] for c in you.hand]"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "trump if (lead_code == spadille_code or lead_code == baste_code) else int(lead_code / 10)"
            }
          }
        },
        {
          "set": {
            "key": "led_suit_name",
            "value": {
              "calc": "suit_names[led_suit]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "follow_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "offer",
            "value": {
              "calc": "[card_name[c] for c in you.hand if (trump if (c == spadille_code or c == baste_code) else int(c / 10)) == led_suit] if len([c for c in you.hand if (trump if (c == spadille_code or c == baste_code) else int(c / 10)) == led_suit]) > 0 else [card_name[c] for c in you.hand]"
            }
          }
        }
      ],
      "text": "Seat {leader} leads {lead}. Led suit: {led_suit_name} (suit {led_suit})."
    },
    {
      "use": "poll",
      "phase": "follow",
      "label": "the follow",
      "to": {
        "where": "you.seat != leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "follow_said",
      "text": "Seat {leader} led {lead}; the led suit is {led_suit_name}. Trumps: {trump_name}. Play a card: if you hold any card of the led suit (Spadille and Baste count as trumps) you must play one, and only those are offered; otherwise any card is offered."
    },
    {
      "use": "update",
      "phase": "follow",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "played_card",
            "value": {
              "calc": "[c for c in all_codes if card_name[c] == you.follow_said][0]"
            }
          }
        },
        {
          "remove": {
            "players": {
              "where": "you.seat != leader"
            },
            "key": "hand",
            "value": {
              "calc": "you.played_card"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_names",
            "value": {
              "calc": "[card_name[c] for c in you.hand]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "power",
            "value": {
              "calc": "power_spadille if you.played_card == spadille_code else (power_manille if you.played_card == 10 * trump + 2 else (power_baste if you.played_card == baste_code else (power_trump_base + you.played_card % 10 if int(you.played_card / 10) == trump else (you.played_card % 10 if int(you.played_card / 10) == led_suit else power_off_suit))))"
            }
          }
        },
        {
          "set": {
            "key": "last_winner",
            "value": {
              "calc": "[p.seat for p in players if p.power == max([q.power for q in players])][0]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "last_winner"
            },
            "key": "tricks_won",
            "value": 1
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "last_winner"
            },
            "key": "hand_tricks",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_report",
            "value": {
              "calc": "seat_labels[1] + ': ' + card_name[players[0].played_card] + '; ' + seat_labels[2] + ': ' + card_name[players[1].played_card] + '; ' + seat_labels[3] + ': ' + card_name[players[2].played_card] + '; ' + seat_labels[4] + ': ' + card_name[players[3].played_card] + '. Winner: ' + seat_labels[last_winner]"
            }
          }
        }
      ],
      "text": "Trick {trick_in_hand} of hand {hand_no}: {trick_report}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the hand result",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "set": {
            "key": "hand_total",
            "value": {
              "calc": "sum([p.hand_tricks for p in players if p.seat == taker or (p.seat == partner_seat and not is_solo)])"
            }
          }
        },
        {
          "set": {
            "key": "hand_delta",
            "value": {
              "calc": "(contract - 1) if hand_total >= contract else ((1 - contract) if hand_total == contract - 1 else (0 - contract))"
            }
          }
        },
        {
          "set": {
            "key": "hand_report",
            "value": {
              "calc": "('It was a solo by ' + seat_labels[taker]) if is_solo else (seat_labels[taker] + ' called ' + seat_labels[partner_seat] + ' as partner')"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the scores",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == taker"
            },
            "key": "score",
            "value": {
              "calc": "solo_multiplier * hand_delta if is_solo else hand_delta"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == partner_seat and you.seat != taker"
            },
            "key": "score",
            "value": {
              "calc": "hand_delta"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != taker and you.seat != partner_seat"
            },
            "key": "score",
            "value": {
              "calc": "0 - hand_delta"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "the hand is scored",
      "when": {
        "calc": "trick_in_hand == tricks_per_hand"
      },
      "to": "all",
      "text": "Hand {hand_no} is over. {hand_report}. Contract {contract}, tricks T = {hand_total}, d = {hand_delta}. Scores: seat 1 {players[0].score}, seat 2 {players[1].score}, seat 3 {players[2].score}, seat 4 {players[3].score}."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after round 40",
      "when": {
        "calc": "round_no >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_no >= rounds"
      },
      "rank_by": "you.score * 100 + you.tricks_won",
      "text": "Winner: {result}. Final scores (tricks won): Seat 1 {players[0].score} ({players[0].tricks_won}), Seat 2 {players[1].score} ({players[1].tricks_won}), Seat 3 {players[2].score} ({players[2].tricks_won}), Seat 4 {players[3].score} ({players[3].tricks_won})."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "PACK: {deck_size} cards, {ranks_per_suit} in each of {suits} suits: A, 2, J, Q, K. Suits are numbered Spades 1, Clubs 2, Hearts 3, Diamonds 4; ranks A 1, 2 2, J 3, Q 4, K 5. A card's code is 10 x suit + rank (K of Hearts = 35). {spadille_code} (Ace of Spades) is Spadille and {baste_code} (Ace of Clubs) is Baste. Cards are always shown by name and code.\n\nSEATS: Seats 1-4 sit clockwise. Each player has a public score (starts 0), a public tricks won total for the game (starts 0) and a public hand tricks count (reset to 0 each hand).\n\nSTRUCTURE: {hands} hands of {tricks_per_hand} tricks, {rounds} rounds; one round is one trick. Hand h covers rounds 5h-4 to 5h. The priority seat of hand h is seat ((h-1) mod 4)+1: 1, 2, 3, 4, 1, 2, 3, 4.\n\nSTART OF EACH HAND (first trick only):\n1. DEAL: the 20 cards are shuffled and 5 are dealt privately to each player ({hand_size} each). Every hand tricks count is set to 0.\n2. BID: all players at the same moment choose Pass, 3, 4 or 5 (bids from {bid_min} to {bid_max}): the number of tricks out of 5 their side promises to win. All bids are announced.\n3. TAKER: the highest bid wins and becomes the contract B. Ties go to the tied player who comes first clockwise starting from the priority seat (that seat itself first). If all four pass, the priority seat is Taker with contract {all_pass_contract}.\n4. DECLARATION: the Taker privately chooses a trump suit (Spades, Clubs, Hearts or Diamonds) and a partner seat (any of seats 1-4, including their own): {declaration_options} options. The trump suit is announced to all. If the partner seat is another player, the hand is a CALL and that player alone is privately told 'you are the Taker's partner'. If the Taker names their own seat, the hand is a SOLO and nobody is told anything beyond the trump suit. Nobody else learns the partner seat until the hand ends.\n\nTRUMPS: every card of the trump suit plus Spadille and Baste, whatever the trump suit. Spadille and Baste count as trump-suit cards and as no other suit. Manille is the 2 of the trump suit. With red trump there are {trumps_red} trumps; with black trump there are {trumps_black}.\n\nPLAY OF A TRICK: on the first trick of a hand the Taker leads; afterwards the winner of the previous trick leads. The leader chooses any card from their hand; it is removed from the hand and shown to all. The led suit is the trump suit if the led card is Spadille, Baste or any trump-suit card; otherwise it is the led card's suit. The other three players then each choose a card at the same moment. A player holding any card of the led suit (counting Spadille and Baste as trump suit) must play one, and only those cards are offered. A player holding none may play any card. Illegal cards are never offered or accepted.\n\nCARD POWER (t = trump suit): Spadille {power_spadille}; Manille (code 10t+2) {power_manille}; Baste {power_baste}; other trump-suit card {power_trump_base} + rank; non-trump card of the led suit: its rank; any other card {power_off_suit}. The highest power wins the trick (ties cannot occur). All four cards and the winner are announced, and the winner adds 1 to their tricks won and hand tricks.\n\nHAND SCORING (after the fifth trick): T = the Taker's hand tricks, plus the partner's hand tricks if the hand is a call. If T >= B (made), d = B-1. If T = B-1 (remise), d = -(B-1). If T <= B-2 (codille), d = -B. CALL: the Taker and the partner each gain d; the other two each lose d. SOLO: the Taker gains {solo_multiplier}d; each of the other three loses d. Every hand sums to zero. The partner seat (or the fact that it was a solo), T, d and all scores are then announced.\n\nNO TALK: there is no discussion phase. All communication is through bids and cards.\n\nEND: after round {rounds} the game ends. The highest score wins. Among players tied on score, the one with the most tricks won over the whole game wins. Players still level share the win (a draw)."
}
```
````
