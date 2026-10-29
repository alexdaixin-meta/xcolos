# 25 coder

- time: 2026-10-28T03:20:43+00:00 (208.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 94ecd7e6c5b47793, reply sha256 9657d0636e603cef

## Sent

````
# Task: write the XColos game file for "Malý Mariáš (Little Mariáš)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. There are 12 cards: four suits, Hearts (H), Bells (B), Leaves (L) and Acorns (A), each with three ranks, Ace (A), Ten (10) and King (K). A card is written rank then suit, for example AH, 10L, KB. Internally, card code = 3 x suit index + rank index, with suits H=0, B=1, L=2, A=3 and ranks K=0, 10=1, A=2. Rank order within a suit is A > 10 > K. Card points: each Ace 10, each Ten 10, each King 0. Whoever wins the 4th (last) trick of a deal gets 10 more. The total per deal is 90.

STRUCTURE. The match is 9 deals of 4 tricks each, which is 36 rounds. Each round is one trick. The eldest hand of deal d is seat ((d-1) mod 3)+1, so seats 1, 2, 3, 1, 2, 3, 1, 2, 3. Every player starts with score 0.

WHAT PLAYERS SEE. Each player sees their own hand (private), all scores, the current deal and trick number, the declarer, contract and trump once set, the stake multiplier, the cards played so far in the current trick with who played them, the card points taken so far by the declarer and by the defenders, and every public announcement. Internal working values are not shown.

ROUND STEPS (steps marked [trick 1] or [trick 2] happen only in that trick of a deal):
1. [trick 1] Deal. Build the list of the 12 codes 0-11, shuffle it once, and give positions 1-4 to seat 1, positions 5-8 to seat 2 and positions 9-12 to seat 3. Reset the declarer points, defender points and multiplier to 1.
2. [trick 1] Bid (simultaneous, secret). Each player answers 'PASS' or 'N S', where N is 50, 60, 70, 80 or 90 and S is H, B, L or A. The eldest may not pass: PASS or any invalid answer from the eldest counts as '50 A'. An invalid answer from anyone else counts as PASS.
3. [trick 1] Resolve the bid. The highest N becomes the declarer, with contract N and trump S. On a tie, the tied player first in seat order starting from the eldest wins. The other two are defenders. Set base stake = N/10 - 4 (so 50→1, 60→2, 70→3, 80→4, 90→5). The declarer leads trick 1. Announce all bids, the declarer, the contract and the trump.
4. [trick 2] Flek poll (simultaneous). Each defender answers FLEK or NO, and the declarer answers RE or NO. Invalid answers count as NO.
5. [trick 2] Resolve. If at least one defender said FLEK, the multiplier is doubled. If, in addition, the declarer said RE, it is doubled again. Announce all answers and the multiplier.
6. First card. The leader names a card from their hand.
7. Resolve the first card. If the card is not in the leader's hand, the lowest-code card in their hand is played instead. Remove it from the hand and add it to the trick. Set led suit to its suit. Set best_key = rank index + (10 if its suit is trump) + 5, and set best_seat = the leader. Announce the card.
8. Second card. The next seat clockwise, (leader mod 3)+1, names a card.
9. Resolve the second card. The card is legal if: it is of the led suit; or the hand has no led-suit card and the card is trump; or the hand has neither led-suit cards nor trumps. If the named card is not held or not legal, play instead the lowest-code held card of the led suit, else the lowest-code held trump, else the lowest-code held card. Remove the card from the hand and add it to the trick. Its key = rank index + (10 if trump) + (5 if of the led suit). If its key is greater than best_key, set best_key to it and best_seat to this seat. Announce the card.
10. Third card. The next seat names a card.
11. Resolve the third card exactly as in step 9.
12. Award the trick. Add the trick's card points, plus 10 if this is trick 4, to the declarer's points if best_seat is the declarer, otherwise to the defenders' points. Set leader = best_seat. Announce the winner and the running points.
13. [trick 4] Settle the deal. Stake = base stake x multiplier x (2 if trump is Hearts, else 1). If the declarer's points are at least the contract N, the declarer gains 2 x stake and each defender loses stake. Otherwise the declarer loses 2 x stake and each defender gains stake. Announce the result and the scores.
14. Advance. Add 1 to the trick number. After trick 4, reset it to 1, add 1 to the deal number and rotate the eldest. After deal 9, the match ends.

There is no discussion phase. Hands are always non-empty when their owner must play, because each player plays exactly one card per trick and holds 4 cards for 4 tricks.

How the winner is decided: After 9 deals, the player with the highest score wins. If two or three players tie for highest, those players draw. Scores are the sum of the zero-sum deal settlements in step 13.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Malý Mariáš (Little Mariáš) (3 to 3 players, best with 3)

Three-player trick-taking game with 12 cards: a secret bid picks a declarer, contract and trump, defenders may double (flek) and the declarer redouble (re), and 9 deals of 4 tricks are settled zero-sum.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Running match score, the sum of the deal settlements.
  - each player: hand (list, starts []); only its owner sees it. Card codes held (code = 3 x suit + rank; suits H=0, B=1, L=2, A=3; ranks K=0, 10=1, A=2).
  - each player: bid (text, starts ''); only its owner sees it. This deal's secret bid, 'PASS' or 'N S'. It is announced after resolution.
  - each player: bid_value (number, starts 0); only its owner sees it. N of the bid (0 for PASS), after the eldest default is applied.
  - each player: flek_answer (text, starts 'NO'); only its owner sees it. Answer in the flek poll: FLEK, RE or NO. It is announced after resolution.
  - the table: deck (list, starts [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]); hidden from all players. The 12 card codes, shuffled and dealt at trick 1 of each deal.
  - the table: deal (number, starts 1); everyone sees it. Current deal, 1 to 9 (10 means the match is over).
  - the table: trick (number, starts 1); everyone sees it. Current trick within the deal, 1 to 4.
  - the table: eldest (number, starts 1); everyone sees it. Eldest seat of this deal, equal to ((deal-1) mod 3)+1.
  - the table: declarer (number, starts 0); everyone sees it. Seat of the declarer for this deal.
  - the table: contract (number, starts 0); everyone sees it. Contract N (50 to 90).
  - the table: trump (number, starts -1); everyone sees it. Trump suit index (H=0, B=1, L=2, A=3).
  - the table: base_stake (number, starts 0); everyone sees it. Base stake, contract/10 - 4.
  - the table: multiplier (number, starts 1); everyone sees it. Stake multiplier from flek and re.
  - the table: declarer_points (number, starts 0); everyone sees it. Card points taken by the declarer this deal.
  - the table: defender_points (number, starts 0); everyone sees it. Card points taken by the defenders this deal.
  - the table: leader (number, starts 1); everyone sees it. Seat that leads the current trick.
  - the table: trick_cards (list, starts []); everyone sees it. Card codes played to the current trick, in order.
  - the table: trick_seats (list, starts []); everyone sees it. Seats that played each card of the current trick, in order.
  - the table: led_suit (number, starts -1); everyone sees it. Suit index of the first card of the current trick.
  - the table: best_key (number, starts 0); hidden from all players. Internal strength of the best card so far in the trick.
  - the table: best_seat (number, starts 0); hidden from all players. Internal: seat currently winning the trick.
  - parameters, each kept as a table attribute: num_cards = 12, num_suits = 4, num_ranks = 3, cards_per_hand = 4, ace_points = 10, ten_points = 10, king_points = 0, last_trick_bonus = 10, points_per_deal = 90, deals = 9, tricks_per_deal = 4, total_rounds = 36, bid_min = 50, bid_max = 90, bid_step = 10, eldest_default_bid = 50, stake_divisor = 10, stake_offset = 4, initial_multiplier = 1, flek_factor = 2, re_factor = 2, hearts_factor = 2, declarer_win_factor = 2, declarer_loss_factor = 2, trump_key_bonus = 10, led_suit_key_bonus = 5, initial_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's score is set to 0.
  2. Set deal = 1, trick = 1, eldest = 1, multiplier = 1.
  3. The 12 card codes 0-11 are placed in the table list deck.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: [when trick = 1] Shuffle deck once. Give positions 1-4 to seat 1's hand, 5-8 to seat 2's hand and 9-12 to seat 3's hand. Set declarer_points = 0, defender_points = 0, multiplier = 1, trick_cards = [], trick_seats = [].
  2. [sync] all players. What happens: [when trick = 1] Each player is sent their own hand and the public state.
  3. [poll] all players answers: eldest: one of the 20 bids 'N S' (N in 50,60,70,80,90; S in H,B,L,A); others: 'PASS' or one of the 20 bids. What happens: [when trick = 1] Set each player's bid. If the eldest answers PASS or an invalid bid, it becomes '50 A'. An invalid answer from any other player becomes 'PASS'. Set bid_value = N, or 0 for PASS.
  4. [update] table. What happens: [when trick = 1] The declarer is the seat with the highest value of bid_value*10 + (3 - ((seat - eldest) mod 3)), so ties go to the seat first in order from the eldest. Set contract = that seat's N, trump = that seat's suit index, base_stake = contract/10 - 4, leader = declarer. Announce all bids, the declarer, the contract and the trump.
  5. [poll] all players answers: defenders: FLEK or NO; declarer: RE or NO. What happens: [when trick = 2] Set each player's flek_answer. An invalid answer counts as NO.
  6. [update] table. What happens: [when trick = 2] If at least one defender has flek_answer = FLEK, multiplier = multiplier x 2. If, in addition, the declarer's flek_answer = RE, multiplier = multiplier x 2 again. Announce all answers and the multiplier.
  7. [ask] the seat equal to leader answers: a card from their hand. What happens: The named card is recorded.
  8. [update] table. What happens: If the named card is not in the leader's hand, use the lowest code in that hand instead. Remove the card from the hand. Append it to trick_cards and append leader to trick_seats. Set led_suit = floor(card/3), best_key = (card mod 3) + (10 if floor(card/3) = trump) + 5, best_seat = leader. Announce the card.
  9. [ask] the seat (leader mod 3)+1 answers: a card from their hand. What happens: The named card is recorded.
  10. [update] table. What happens: The card is legal if its suit = led_suit; or the hand has no led_suit card and its suit = trump; or the hand has neither led_suit cards nor trumps. If it is not held or not legal, use the lowest-code held led_suit card, else the lowest-code held trump, else the lowest-code held card. Remove it from the hand and append it to trick_cards and the seat to trick_seats. key = (card mod 3) + (10 if suit = trump) + (5 if suit = led_suit). If key > best_key, set best_key = key and best_seat = this seat. Announce the card.
  11. [ask] the seat ((leader mod 3)+1) mod 3 + 1 answers: a card from their hand. What happens: The named card is recorded.
  12. [update] table. What happens: Same as the second-card resolution, for this seat.
  13. [update] table. What happens: Trick points = sum over trick_cards of (10 if card mod 3 >= 1 else 0), plus 10 if trick = 4. If best_seat = declarer, add them to declarer_points, otherwise to defender_points. Set leader = best_seat, then clear trick_cards and trick_seats. Announce the trick winner, declarer_points and defender_points.
  14. [update] all players. What happens: [when trick = 4] stake = base_stake x multiplier x (2 if trump = 0 else 1). If declarer_points >= contract: the declarer's score += 2 x stake and each defender's score -= stake. Otherwise: the declarer's score -= 2 x stake and each defender's score += stake. Announce the result and the scores.
  15. [update] table. What happens: trick += 1. If trick > 4: trick = 1, deal += 1, eldest = ((deal-1) mod 3)+1, and every player's bid is reset to '', bid_value to 0 and flek_answer to 'NO'.
  16. [check] table. What happens: End the match if deal > 9, otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. There are 12 cards, codes 0-11, with suit = floor(code/3) (H=0, B=1, L=2, A=3) and rank = code mod 3 (K=0, 10=1, A=2), and the rank order within a suit is A > 10 > K.
  R2. When a trick is awarded, each Ace and each Ten in it is worth 10 points and each King 0.
  R3. When trick 4 of a deal is awarded, its winner's side gets 10 extra points, so a deal totals 90 points.
  R4. The match is 9 deals of 4 tricks (36 rounds), and the eldest of deal d is seat ((d-1) mod 3)+1.
  R5. When trick 1 of a deal begins, the 12 codes are shuffled and positions 1-4 go to seat 1, 5-8 to seat 2 and 9-12 to seat 3, and declarer_points, defender_points and multiplier are reset to 0, 0 and 1.
  R6. When bidding at trick 1, every player answers secretly and at the same time with PASS or 'N S', where N is in {50,60,70,80,90} and S is in {H,B,L,A}.
  R7. When the eldest answers PASS or an invalid bid, it counts as '50 A'.
  R8. When a non-eldest player gives an invalid bid, it counts as PASS.
  R9. When bids are resolved, the highest N becomes the declarer with contract N and trump S, and on a tie the tied seat first in seat order starting from the eldest wins.
  R10. When the declarer is set, base_stake = N/10 - 4 (50→1, 60→2, 70→3, 80→4, 90→5), and the declarer leads trick 1.
  R11. When bids are resolved, all bids, the declarer, the contract and the trump are announced.
  R12. When the flek poll runs at trick 2, defenders answer FLEK or NO and the declarer answers RE or NO, all at the same time, and invalid answers count as NO.
  R13. When at least one defender says FLEK, the multiplier doubles to 2.
  R14. When at least one defender says FLEK and the declarer says RE, the multiplier becomes 4.
  R15. When no defender says FLEK, the multiplier stays 1, even if the declarer says RE.
  R16. When the leader names a card not in their hand, their lowest-code card is played instead.
  R17. When the first card is played, led_suit = its suit, best_key = rank + (10 if trump) + 5, and best_seat = the leader.
  R18. When a following player plays, the card must be of the led suit; failing that a trump; failing both, any card.
  R19. When a following player names an illegal or unheld card, the lowest-code held led-suit card is played, else the lowest-code held trump, else the lowest-code held card.
  R20. When a following card's key = rank + (10 if trump) + (5 if led suit) exceeds best_key, that seat becomes best_seat.
  R21. When a trick is awarded, its points go to declarer_points if best_seat is the declarer, otherwise to defender_points, and best_seat leads the next trick.
  R22. When a deal is settled, stake = base_stake x multiplier x (2 if trump is Hearts, else 1).
  R23. When declarer_points >= contract at settlement, the declarer gains 2 x stake and each defender loses stake.
  R24. When declarer_points < contract at settlement, the declarer loses 2 x stake and each defender gains stake.
  R25. When deal 9's trick 4 has been settled, the match ends and the highest score wins, with players tied at the top drawing.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid (trick 1) | asked: all players at once | options: the eldest: the 20 bids '50 H' … '90 A' (no PASS); any other seat: PASS plus the 20 bids
  - Flek poll (trick 2) | asked: all players at once | options: the declarer: RE, NO; each defender: FLEK, NO
  - First card | asked: the leader | options: every card in the leader's hand
  - Second card / third card | asked: the next seat clockwise, then the one after | options: the cards in that hand of the led suit; if none, the trumps held; if neither, every card held

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deal > 9
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their score, the sum of the zero-sum deal settlements over 9 deals. The highest score wins, and players tied at the top draw by sharing the win.
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

- each player: `score` (number, visible: public, starts 0): Running match score, the sum of the deal settlements.
- the table: `deal` (number, visible: public, starts 1): Current deal, 1 to 9 (10 means the match is over).
- the table: `declarer` (number, visible: public, starts 0): Seat of the declarer for this deal.
- the table: `contract` (number, visible: public, starts 0): Contract N (50 to 90).
- the table: `trump` (number, visible: public, starts -1): Trump suit index (H=0, B=1, L=2, A=3).
- the table: `multiplier` (number, visible: public, starts 1): Stake multiplier from flek and re.
- parameters (each must be an attribute holding this value, never a number buried in a step): num_cards = 12, num_suits = 4, num_ranks = 3, cards_per_hand = 4, ace_points = 10, ten_points = 10, king_points = 0, last_trick_bonus = 10, points_per_deal = 90, deals = 9, tricks_per_deal = 4, total_rounds = 36, bid_min = 50, bid_max = 90, bid_step = 10, eldest_default_bid = 50, stake_divisor = 10, stake_offset = 4, initial_multiplier = 1, flek_factor = 2, re_factor = 2, hearts_factor = 2, declarer_win_factor = 2, declarer_loss_factor = 2, trump_key_bonus = 10, led_suit_key_bonus = 5, initial_score = 0
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
{
  "schema": 1,
  "meta": {
    "id": "maly_marias",
    "name": "Malý Mariáš (Little Mariáš)",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, 12 cards, 9 deals of 4 tricks: a secret bid picks declarer, contract and trump, defenders may flek, the declarer may re, and every deal is settled zero-sum."
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
        "key": "bid",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "flek_answer",
        "visible": "ally",
        "type": "text",
        "initial": "NO"
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_offer",
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
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
      },
      {
        "key": "deal",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "eldest",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "declarer",
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
        "initial": -1
      },
      {
        "key": "trump_name",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "base_stake",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "declarer_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defender_points",
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
        "key": "turn_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "trick_seats",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "last_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_trick_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_summary",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "flek_summary",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "stake",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deal_result",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "best_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "best_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cur_hand",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "led_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "trump_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "top_bid",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "decl_bid",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "all_codes",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": ["KH", "10H", "AH", "KB", "10B", "AB", "KL", "10L", "AL", "KA", "10A", "AA"]
      },
      {
        "key": "suit_names",
        "visible": "none",
        "type": "list",
        "initial": ["Hearts", "Bells", "Leaves", "Acorns"]
      },
      {
        "key": "bid_options",
        "visible": "none",
        "type": "list",
        "initial": ["50 H", "50 B", "50 L", "50 A", "60 H", "60 B", "60 L", "60 A", "70 H", "70 B", "70 L", "70 A", "80 H", "80 B", "80 L", "80 A", "90 H", "90 B", "90 L", "90 A"]
      },
      {
        "key": "bid_idx",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
      },
      {
        "key": "num_cards",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "num_suits",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "num_ranks",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "ace_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "ten_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "king_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 90
      },
      {
        "key": "deals",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "bid_min",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "bid_max",
        "visible": "public",
        "type": "number",
        "initial": 90
      },
      {
        "key": "bid_step",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "eldest_default_bid",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "stake_divisor",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "stake_offset",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "initial_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "flek_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "re_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hearts_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "declarer_win_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "declarer_loss_factor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "trump_key_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "led_suit_key_bonus",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "initial_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "initial_score"
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
            "key": "trick",
            "value": 1
          }
        },
        {
          "set": {
            "key": "eldest",
            "value": 1
          }
        },
        {
          "set": {
            "key": "multiplier",
            "value": {
              "calc": "initial_multiplier"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_codes"
            }
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
      "phase": "deal",
      "label": "the deal",
      "when": {
        "calc": "trick == 1"
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
            "key": "pick",
            "value": {
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
              "calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"
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
            "key": "declarer_points",
            "value": 0
          }
        },
        {
          "set": {
            "key": "defender_points",
            "value": 0
          }
        },
        {
          "set": {
            "key": "multiplier",
            "value": {
              "calc": "initial_multiplier"
            }
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "trick_seats",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_offer",
            "value": {
              "calc": "[card_names[c] for c in you.hand]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(['PASS'] if you.seat != eldest else []) + bid_options"
            }
          }
        }
      ],
      "text": "Deal {deal} of {deals}: the cards are shuffled and dealt, {cards_per_hand} to each seat. Seat {eldest} is eldest."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "trick == 1"
      },
      "mode": "self",
      "to": "all",
      "text": "Your hand and standing:"
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "the bid",
      "when": {
        "calc": "trick == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "bid",
      "text": "Deal {deal}: bid in secret. Answer 'N S' where N is 50, 60, 70 or 80 or 90 (the card points you promise to take as declarer) and S is the trump suit H, B, L or A; or PASS. The eldest (seat {eldest}) may not pass. The highest N becomes declarer; a tie goes to the tied seat first in order from the eldest."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the bid resolves",
      "when": {
        "calc": "trick == 1"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == eldest and not (you.bid in bid_options)"
            },
            "key": "bid",
            "value": {
              "calc": "bid_options[(eldest_default_bid - bid_min) // bid_step * num_suits + num_suits - 1]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != eldest and not (you.bid in bid_options)"
            },
            "key": "bid",
            "value": "PASS"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_value",
            "value": {
              "calc": "max([bid_min + bid_step * (i // num_suits) for i in bid_idx if bid_options[i] == you.bid] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "top_bid",
            "value": {
              "calc": "max([p.bid_value + len(players) - ((p.seat - eldest) % len(players)) for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "declarer",
            "value": {
              "calc": "min([p.seat for p in players if p.bid_value + len(players) - ((p.seat - eldest) % len(players)) == top_bid])"
            }
          }
        },
        {
          "set": {
            "key": "decl_bid",
            "value": {
              "calc": "[p.bid for p in players if p.seat == declarer][0]"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "sum([p.bid_value for p in players if p.seat == declarer])"
            }
          }
        },
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "sum([i % num_suits for i in bid_idx if bid_options[i] == decl_bid])"
            }
          }
        },
        {
          "set": {
            "key": "base_stake",
            "value": {
              "calc": "contract // stake_divisor - stake_offset"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "declarer"
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
        },
        {
          "set": {
            "key": "bid_summary",
            "value": {
              "calc": "'seat 1 ' + players[0].bid + ', seat 2 ' + players[1].bid + ', seat 3 ' + players[2].bid"
            }
          }
        }
      ],
      "text": "Bids: {bid_summary}. Declarer: seat {declarer}, contract {contract}, trump {trump_name}. Base stake {base_stake}. Seat {declarer} leads."
    },
    {
      "use": "poll",
      "phase": "flek",
      "label": "flek and re",
      "when": {
        "calc": "trick == 2"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "flek_answer",
      "text": "Flek poll for deal {deal} (declarer seat {declarer}, contract {contract}, trump {trump_name}). A defender answers FLEK or NO; the declarer answers RE or NO. If at least one defender says FLEK the multiplier doubles; if the declarer also says RE it doubles again. RE without a FLEK changes nothing."
    },
    {
      "use": "update",
      "phase": "flek",
      "label": "flek resolves",
      "when": {
        "calc": "trick == 2"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "not (you.flek_answer in ['FLEK', 'RE'])"
            },
            "key": "flek_answer",
            "value": "NO"
          }
        },
        {
          "set": {
            "key": "multiplier",
            "value": {
              "calc": "multiplier * flek_factor"
            },
            "if": {
              "calc": "count(p.flek_answer == 'FLEK' and p.seat != declarer for p in players) >= 1"
            }
          }
        },
        {
          "set": {
            "key": "multiplier",
            "value": {
              "calc": "multiplier * re_factor"
            },
            "if": {
              "calc": "count(p.flek_answer == 'FLEK' and p.seat != declarer for p in players) >= 1 and count(p.flek_answer == 'RE' and p.seat == declarer for p in players) >= 1"
            }
          }
        },
        {
          "set": {
            "key": "flek_summary",
            "value": {
              "calc": "'seat 1 ' + players[0].flek_answer + ', seat 2 ' + players[1].flek_answer + ', seat 3 ' + players[2].flek_answer"
            }
          }
        }
      ],
      "text": "Flek answers: {flek_summary}. The multiplier is now {multiplier}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "first card",
      "to": {
        "where": "you.seat == leader"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "card_offer"
        }
      },
      "verify": {
        "bind": "c1"
      },
      "text": "Deal {deal}, trick {trick}: you lead. Trump is {trump_name}. Name a card from your hand."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "first card resolves",
      "do": [
        {
          "set": {
            "key": "cur_hand",
            "value": {
              "calc": "[p.hand for p in players if p.seat == leader][0]"
            }
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "sum([c for c in all_codes if card_names[c] == $c1])"
            }
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "card if card in cur_hand else min(cur_hand)"
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
              "calc": "card"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "card"
            }
          }
        },
        {
          "append": {
            "key": "trick_seats",
            "value": {
              "calc": "leader"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "card // num_ranks"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "card % num_ranks + (trump_key_bonus if card // num_ranks == trump else 0) + led_suit_key_bonus"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "leader"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[card]"
            }
          }
        },
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "leader % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == turn_seat"
            },
            "key": "card_offer",
            "value": {
              "calc": "[card_names[c] for c in you.hand if c // num_ranks == led_suit] if len([c for c in you.hand if c // num_ranks == led_suit]) > 0 else ([card_names[c] for c in you.hand if c // num_ranks == trump] if len([c for c in you.hand if c // num_ranks == trump]) > 0 else [card_names[c] for c in you.hand])"
            }
          }
        }
      ],
      "text": "Seat {leader} leads {last_card}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "second card",
      "to": {
        "where": "you.seat == turn_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "card_offer"
        }
      },
      "verify": {
        "bind": "c2"
      },
      "text": "Deal {deal}, trick {trick}: cards so far {trick_cards} by seats {trick_seats}; trump is {trump_name}. Play a card: of the led suit if you can, else a trump, else any card."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "second card resolves",
      "do": [
        {
          "set": {
            "key": "cur_hand",
            "value": {
              "calc": "[p.hand for p in players if p.seat == turn_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "sum([c for c in all_codes if card_names[c] == $c2])"
            }
          }
        },
        {
          "set": {
            "key": "led_cards",
            "value": {
              "calc": "[c for c in cur_hand if c // num_ranks == led_suit]"
            }
          }
        },
        {
          "set": {
            "key": "trump_cards",
            "value": {
              "calc": "[c for c in cur_hand if c // num_ranks == trump]"
            }
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "card if (card in cur_hand and (card in led_cards or (len(led_cards) == 0 and card in trump_cards) or (len(led_cards) == 0 and len(trump_cards) == 0))) else (min(led_cards) if len(led_cards) > 0 else (min(trump_cards) if len(trump_cards) > 0 else min(cur_hand)))"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "turn_seat"
            },
            "key": "hand",
            "value": {
              "calc": "card"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "card"
            }
          }
        },
        {
          "append": {
            "key": "trick_seats",
            "value": {
              "calc": "turn_seat"
            }
          }
        },
        {
          "set": {
            "key": "card_key",
            "value": {
              "calc": "card % num_ranks + (trump_key_bonus if card // num_ranks == trump else 0) + (led_suit_key_bonus if card // num_ranks == led_suit else 0)"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "turn_seat"
            },
            "if": {
              "calc": "card_key > best_key"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max(best_key, card_key)"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[card]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == turn_seat % len(players) + 1"
            },
            "key": "card_offer",
            "value": {
              "calc": "[card_names[c] for c in you.hand if c // num_ranks == led_suit] if len([c for c in you.hand if c // num_ranks == led_suit]) > 0 else ([card_names[c] for c in you.hand if c // num_ranks == trump] if len([c for c in you.hand if c // num_ranks == trump]) > 0 else [card_names[c] for c in you.hand])"
            }
          }
        }
      ],
      "text": "Seat {turn_seat} plays {last_card}."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "third card",
      "to": {
        "where": "you.seat == turn_seat % len(players) + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "card_offer"
        }
      },
      "verify": {
        "bind": "c3"
      },
      "text": "Deal {deal}, trick {trick}: cards so far {trick_cards} by seats {trick_seats}; trump is {trump_name}. Play a card: of the led suit if you can, else a trump, else any card."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "third card resolves",
      "do": [
        {
          "set": {
            "key": "turn_seat",
            "value": {
              "calc": "turn_seat % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "cur_hand",
            "value": {
              "calc": "[p.hand for p in players if p.seat == turn_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "sum([c for c in all_codes if card_names[c] == $c3])"
            }
          }
        },
        {
          "set": {
            "key": "led_cards",
            "value": {
              "calc": "[c for c in cur_hand if c // num_ranks == led_suit]"
            }
          }
        },
        {
          "set": {
            "key": "trump_cards",
            "value": {
              "calc": "[c for c in cur_hand if c // num_ranks == trump]"
            }
          }
        },
        {
          "set": {
            "key": "card",
            "value": {
              "calc": "card if (card in cur_hand and (card in led_cards or (len(led_cards) == 0 and card in trump_cards) or (len(led_cards) == 0 and len(trump_cards) == 0))) else (min(led_cards) if len(led_cards) > 0 else (min(trump_cards) if len(trump_cards) > 0 else min(cur_hand)))"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "turn_seat"
            },
            "key": "hand",
            "value": {
              "calc": "card"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "card"
            }
          }
        },
        {
          "append": {
            "key": "trick_seats",
            "value": {
              "calc": "turn_seat"
            }
          }
        },
        {
          "set": {
            "key": "card_key",
            "value": {
              "calc": "card % num_ranks + (trump_key_bonus if card // num_ranks == trump else 0) + (led_suit_key_bonus if card // num_ranks == led_suit else 0)"
            }
          }
        },
        {
          "set": {
            "key": "best_seat",
            "value": {
              "calc": "turn_seat"
            },
            "if": {
              "calc": "card_key > best_key"
            }
          }
        },
        {
          "set": {
            "key": "best_key",
            "value": {
              "calc": "max(best_key, card_key)"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[card]"
            }
          }
        }
      ],
      "text": "Seat {turn_seat} plays {last_card}."
    },
    {
      "use": "update",
      "phase": "award",
      "label": "the trick is awarded",
      "do": [
        {
          "set": {
            "key": "last_trick_points",
            "value": {
              "calc": "sum([(ace_points if c % num_ranks == 2 else (ten_points if c % num_ranks == 1 else king_points)) for c in trick_cards]) + (last_trick_bonus if trick == tricks_per_deal else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "declarer_points",
            "value": {
              "calc": "last_trick_points"
            },
            "if": {
              "calc": "best_seat == declarer"
            }
          }
        },
        {
          "adjust": {
            "key": "defender_points",
            "value": {
              "calc": "last_trick_points"
            },
            "if": {
              "calc": "best_seat != declarer"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "best_seat"
            }
          }
        },
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "trick_seats",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "card_offer",
            "value": {
              "calc": "[card_names[c] for c in you.hand]"
            }
          }
        }
      ],
      "text": "Seat {leader} wins trick {trick} worth {last_trick_points} points. Declarer {declarer_points}, defenders {defender_points}."
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "the deal is settled",
      "when": {
        "calc": "trick == tricks_per_deal"
      },
      "do": [
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "base_stake * multiplier * (hearts_factor if trump == 0 else 1)"
            }
          }
        },
        {
          "set": {
            "key": "deal_result",
            "value": {
              "calc": "'made' if declarer_points >= contract else 'failed'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "declarer"
            },
            "key": "score",
            "value": {
              "calc": "declarer_win_factor * stake"
            },
            "if": {
              "calc": "declarer_points >= contract"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != declarer"
            },
            "key": "score",
            "value": {
              "calc": "-stake"
            },
            "if": {
              "calc": "declarer_points >= contract"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "declarer"
            },
            "key": "score",
            "value": {
              "calc": "-declarer_loss_factor * stake"
            },
            "if": {
              "calc": "declarer_points < contract"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != declarer"
            },
            "key": "score",
            "value": {
              "calc": "stake"
            },
            "if": {
              "calc": "declarer_points < contract"
            }
          }
        }
      ],
      "text": "Deal {deal} settled: declarer seat {declarer} took {declarer_points} against a contract of {contract}, so the contract is {deal_result}. Stake {stake}. Scores: seat 1 {players[0].score}, seat 2 {players[1].score}, seat 3 {players[2].score}."
    },
    {
      "use": "update",
      "phase": "advance",
      "label": "advance",
      "do": [
        {
          "adjust": {
            "key": "trick",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "deal",
            "value": 1,
            "if": {
              "calc": "trick > tricks_per_deal"
            }
          }
        },
        {
          "set": {
            "key": "eldest",
            "value": {
              "calc": "(deal - 1) % len(players) + 1"
            },
            "if": {
              "calc": "trick > tricks_per_deal"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": "",
            "if": {
              "calc": "trick > tricks_per_deal"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_value",
            "value": 0,
            "if": {
              "calc": "trick > tricks_per_deal"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "flek_answer",
            "value": "NO",
            "if": {
              "calc": "trick > tricks_per_deal"
            }
          }
        },
        {
          "set": {
            "key": "trick",
            "value": 1,
            "if": {
              "calc": "trick > tricks_per_deal"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['RE', 'NO'] if you.seat == declarer else ['FLEK', 'NO']"
            },
            "if": {
              "calc": "trick == 2"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "advance",
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
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {num_cards} cards: four suits, Hearts (H), Bells (B), Leaves (L) and Acorns (A), each with three ranks, Ace (A), Ten (10) and King (K). A card is written rank then suit, for example AH, 10L, KB. Your hand is shown as card codes: code = 3 x suit index + rank index, with suits H=0, B=1, L=2, A=3 and ranks K=0, 10=1, A=2 (so 0=KH, 1=10H, 2=AH, 3=KB, 4=10B, 5=AB, 6=KL, 7=10L, 8=AL, 9=KA, 10=10A, 11=AA). Rank order within a suit is A > 10 > K. Card points: each Ace {ace_points}, each Ten {ten_points}, each King {king_points}. Whoever wins the 4th (last) trick of a deal gets {last_trick_bonus} more. The total per deal is {points_per_deal}.\n\nSTRUCTURE. The match is {deals} deals of {tricks_per_deal} tricks each, {total_rounds} rounds; each round is one trick. The eldest hand of deal d is seat ((d-1) mod 3)+1, so seats 1, 2, 3, 1, 2, 3, 1, 2, 3. Every player starts with score {initial_score}. There is no discussion.\n\nDEAL (trick 1). The 12 cards are shuffled and {cards_per_hand} go to each seat. Declarer points, defender points and the multiplier are reset to 0, 0 and {initial_multiplier}.\n\nBID (trick 1, simultaneous and secret). Each player answers PASS or 'N S', where N is 50, 60, 70, 80 or 90 ({bid_min} to {bid_max} in steps of {bid_step}) and S is H, B, L or A. The eldest may not pass: PASS or any invalid answer from the eldest counts as '{eldest_default_bid} A'. An invalid answer from anyone else counts as PASS. The highest N becomes the declarer, with contract N and trump S. On a tie, the tied player first in seat order starting from the eldest wins. The other two are defenders. Base stake = N/{stake_divisor} - {stake_offset} (50 gives 1, 60 gives 2, 70 gives 3, 80 gives 4, 90 gives 5). The declarer leads trick 1. All bids, the declarer, the contract and the trump are announced.\n\nFLEK (trick 2, simultaneous). Each defender answers FLEK or NO, and the declarer answers RE or NO. Invalid answers count as NO. If at least one defender said FLEK, the multiplier is multiplied by {flek_factor}; if not, it stays as it is, even if the declarer said RE. If at least one defender said FLEK and the declarer also said RE, it is multiplied by {re_factor} again (so 4). All answers and the multiplier are announced.\n\nPLAY. The leader names a card from their hand; if it is not in their hand, their lowest-code card is played instead. Its suit is the led suit. Then the next seat clockwise, and then the one after, each play a card: it must be of the led suit; if they have none, a trump; if they have neither, any card. You are only offered legal cards; if a named card is not held or not legal, the lowest-code held led-suit card is played instead, else the lowest-code held trump, else the lowest-code held card. Each card's strength is rank index + {trump_key_bonus} if it is a trump + {led_suit_key_bonus} if it is of the led suit; the leader's card counts as led suit. A later card takes the trick only if its strength is greater than the best so far. The trick's card points (plus {last_trick_bonus} on trick 4) go to the declarer's points if the declarer won it, otherwise to the defenders' points, and the trick's winner leads the next trick.\n\nSETTLEMENT (after trick 4). Stake = base stake x multiplier x ({hearts_factor} if trump is Hearts, else 1). If the declarer's points are at least the contract N, the declarer gains {declarer_win_factor} x stake and each defender loses stake. Otherwise the declarer loses {declarer_loss_factor} x stake and each defender gains stake. Scores may go below zero.\n\nEND. After deal {deals}, the player with the highest score wins. If two or three players tie for highest, they share the win."
}
````
