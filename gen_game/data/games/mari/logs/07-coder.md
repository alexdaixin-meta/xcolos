# 07 coder

- time: 2026-10-28T02:32:32+00:00 (267.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 16e105a7102734ff, reply sha256 6f59c123a568b5c7

## Sent

````
# Task: write the XColos game file for "Little Bidding Mariáš"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

CARDS. There are 20 cards in four suits, Hearts, Bells, Leaves and Acorns, each with ranks A, 10, K, O (Ober) and U (Unter). Within a suit the ranks run from highest to lowest A, 10, K, O, U. Each Ace and each Ten is worth 10 card points; all other cards are worth 0. Winning the 6th (last) trick of a deal is worth 10 more points, so the deal has 90 card points in total. Internally each card has the code suit*5 + rank, with suits Hearts=0, Bells=1, Leaves=2, Acorns=3 and ranks U=0, O=1, K=2, 10=3, A=4. Players see and name cards by their names, for example 'Ten of Leaves'. Suit order for tie-breaks is Hearts, Bells, Leaves, Acorns.

MATCH. The match has 6 deals of 6 tricks each, 36 rounds in total. Each round is one trick. Players are seated P1, P2, P3, and seat order is cyclic (P1, P2, P3, P1, ...). The eldest is P1 in deals 1 and 4, P2 in deals 2 and 5, and P3 in deals 3 and 6. Every score starts at 0. Players may not exchange messages at any time; defenders cooperate only through their card play.

DEAL (first round of each deal). The engine shuffles all 20 cards and deals 6 to each player privately. The remaining 2 cards are the talon: face down, seen by no one, and out of play for the whole deal.

BIDDING (first round of each deal, one simultaneous poll). Every player privately submits one answer containing a bid and a suit. A bid is PASS or one of 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150. A suit is Hearts, Bells, Leaves or Acorns.
- Any bid not in this list counts as PASS.
- The eldest may not pass: an eldest PASS or invalid bid counts as 50.
- A missing or invalid suit becomes the suit in which that player holds the most cards, ties broken by the suit order.
All bids and suits are then revealed together. The highest bid wins. If bids are equal, the eldest wins the tie first, then the next player in seat order after the eldest. The winner is the declarer, their bid is the contract T, and their suit is trump. The other two players are the defenders and form a team for this deal.

MARRIAGES (announced right after bidding). Every player who holds both the K and the O of one suit has a marriage in that suit. A marriage is worth 40 in the trump suit and 20 in any other suit, and it belongs to its holder's side (declarer or defenders). The engine publicly announces every marriage, its holder and its value. At the end of the deal a side's marriages count only if that side won at least one trick.

PLAYING A TRICK. The declarer leads the first trick of the deal. After that, the winner of the previous trick leads. Starting with the leader, each player in seat order plays one card, and each card is announced to all. The leader may play any card. For the other players:
(a) If you hold a card of the led suit, you must play that suit. You must also play one that beats the highest card of the led suit already in the trick, if you can. This beating duty is lifted only when the led suit is not trump and a trump has already been played to this trick.
(b) If you hold no card of the led suit but hold a trump, you must play a trump. It must beat the highest trump already in the trick, if you can.
(c) Otherwise you may play any card.
If a player names a card that is illegal or not in their hand, the engine plays for them the legal card of lowest rank; among equal ranks, the first in the suit order.
The trick is won by the highest trump in it, or by the highest card of the led suit if it holds no trump. Equivalently, each card gets the key rank + 10 if it is trump + 5 if it is of the led suit, and the highest key wins. The card points of the trick, plus 10 if it is the 6th trick, go to the winner's side: the declarer alone, or the defenders together. The engine announces the trick winner and both sides' running points.

END OF DEAL (after the 6th trick).
1. The declarer's tally is the declarer's points (including any last-trick 10), plus the declarer's marriages if the declarer won at least 1 trick, minus the defenders' marriages if the defenders won at least 1 trick.
2. Let S = (T − 40) / 10, so a contract of 50 gives S = 1 and 150 gives S = 11.
3. If the tally is at least T, the contract is made and S is unchanged. Otherwise S becomes −(S + 1).
4. If trump is Hearts, S is doubled.
5. The declarer's score changes by 2×S, and each defender's score changes by −S.
6. The engine announces the tally, whether the contract was made, and all scores.

ENGINE STEP LIST (per round; steps marked [trick 1] run only in the first round of a deal, and steps marked [trick 6] only in the last).
1. [trick 1] Shuffle and deal 6 hidden cards to each player and 2 to the talon.
2. [trick 1] Reset the declarer's points, the defenders' points and the declarer's tricks to 0.
3. [trick 1] Simultaneous poll: bid and suit.
4. [trick 1] Calc: apply the invalid-input rules; set declarer, T, trump, and leader = declarer.
5. [trick 1] Calc: the marriage values of the declarer's side and of the defenders' side.
6. [trick 1] Announce the bids, declarer, contract, trump and marriages.
7. Clear the list of cards in the current trick.
8. The leader chooses a card.
9. Validate or apply the fallback; remove the card from the hand, add it to the trick list, announce it.
10. The next player chooses a card.
11. Validate, remove, add and announce as in step 9.
12. The third player chooses a card.
13. Validate, remove, add and announce as in step 9.
14. Calc the trick winner by maximum key. Add the trick points (+10 on trick 6) to the winner's side, add 1 to the declarer's tricks if the declarer won, set the leader to the winner, and announce.
15. [trick 6] Calc the tally, S, the fail transform, Hearts doubling and all score changes.
16. [trick 6] Announce the tally, the result and the scores.
17. Advance the round counter.
18. [round 36] End the match and decide the winner.

ATTRIBUTES (16). Per player (4): score, hand, bid, bid suit. Table (12): round number, talon, declarer, contract T, trump, leader, cards in the current trick, declarer's points, defenders' points, declarer's tricks, declarer-side marriage value, defender-side marriage value. The deal number, trick number and eldest are derived from the round number. The defenders' trick count is (tricks completed − declarer's tricks).

How the winner is decided: After round 36 (6 deals), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw. Every deal is zero-sum (the declarer gains 2×S, and each defender loses S), so the totals always sum to 0.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Little Bidding Mariáš (3 to 3 players, best with 3)

Three-player trick-taking game over 6 deals of 6 tricks: one simultaneous bid picks a declarer and trump, marriages are announced, and the declarer plays alone against two defenders to reach the contract.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Match score, the sum of the deal settlements so far.
  - each player: hand (list, starts []); only its owner sees it. Card codes (suit*5+rank) held privately. 6 are dealt each deal and one is removed per trick.
  - each player: bid (text, starts 'PASS'); everyone sees it. This deal's bid: PASS or 50..150 in steps of 10. Submitted in a simultaneous poll and revealed together.
  - each player: bid_suit (text, starts ''); everyone sees it. Suit named with the bid: Hearts, Bells, Leaves or Acorns.
  - the table: round (number, starts 1); everyone sees it. Round (trick) counter, 1..36. deal = floor((round-1)/6)+1, trick = (round-1)%6+1, eldest seat = ((deal-1)%3)+1.
  - the table: deck (list, starts 'codes 0..19'); hidden from all players. The full 20-card pack that each deal is shuffled and dealt from.
  - the table: talon (list, starts []); hidden from all players. The 2 undealt cards, face down and out of play for the deal.
  - the table: declarer (number, starts 0); everyone sees it. Seat of this deal's declarer.
  - the table: contract (number, starts 0); everyone sees it. Contract T, the declarer's winning bid.
  - the table: trump (text, starts ''); everyone sees it. Trump suit, the declarer's bid suit.
  - the table: leader (number, starts 0); everyone sees it. Seat that leads the current trick.
  - the table: trick_cards (list, starts []); everyone sees it. Cards played to the current trick, in play order starting with the leader.
  - the table: declarer_points (number, starts 0); everyone sees it. Card points won by the declarer this deal, including the last-trick 10.
  - the table: defender_points (number, starts 0); everyone sees it. Card points won by the defenders together this deal.
  - the table: declarer_tricks (number, starts 0); everyone sees it. Tricks won by the declarer this deal. Defender tricks = tricks completed - declarer_tricks.
  - the table: declarer_marriages (number, starts 0); everyone sees it. Total marriage value held by the declarer.
  - the table: defender_marriages (number, starts 0); everyone sees it. Total marriage value held by the two defenders.
  - parameters, each kept as a table attribute: card_count = 20, suit_count = 4, ranks_per_suit = 5, suit_code_multiplier = 5, hand_size = 6, talon_size = 2, tricks_per_deal = 6, deals = 6, total_rounds = 36, ace_points = 10, ten_points = 10, last_trick_bonus = 10, deal_card_points_total = 90, min_bid = 50, max_bid = 150, bid_step = 10, eldest_forced_bid = 50, trump_marriage_value = 40, plain_marriage_value = 20, contract_offset = 40, contract_divisor = 10, hearts_multiplier = 2, declarer_score_multiplier = 2, defender_score_multiplier = 1, trump_key_bonus = 10, led_suit_key_bonus = 5, starting_score = 0, min_tricks_for_marriages = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the players as P1, P2 and P3. Seat order is cyclic.
  2. Set every score to 0 and round to 1.
  3. Fill the deck with the 20 card codes 0..19 (suit*5+rank; Hearts=0, Bells=1, Leaves=2, Acorns=3; U=0, O=1, K=2, 10=3, A=4).
  4. Players may not exchange messages at any time, so the game has no talk step.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: [when (round-1)%6==0] Return all cards to the deck. Draw 6 cards at random from the deck into each player's hand and the remaining 2 into talon (hidden). Set declarer_points=0, defender_points=0, declarer_tricks=0, trick_cards=[].
  2. [sync] all players. What happens: [when (round-1)%6==0] Each player privately sees their own hand, named by card names (e.g. 'Ten of Leaves').
  3. [poll] all players answers: One choice of 'BID SUIT', where BID is PASS or 50,60,...,150 and SUIT is Hearts, Bells, Leaves or Acorns. The eldest is not offered PASS.. What happens: [when (round-1)%6==0] Sets bid and bid_suit for every player. No answer is seen until all are in.
  4. [update] table. What happens: [when (round-1)%6==0] A bid not in the list becomes PASS. An eldest PASS or invalid bid becomes 50. A missing or invalid suit becomes the suit with the most cards in that player's hand, ties broken by Hearts, Bells, Leaves, Acorns. declarer = the seat with the maximum of bidvalue*10 + (3 - ((seat - eldest) mod 3)), with PASS = 0. Set contract = declarer's bid, trump = declarer's bid_suit, leader = declarer.
  5. [update] table. What happens: [when (round-1)%6==0] For each player and each suit s where both codes s*5+2 (K) and s*5+1 (O) are in hand, the marriage is worth 40 if s is trump, else 20. declarer_marriages = the sum for the declarer. defender_marriages = the sum for the two other seats.
  6. [tell] all players. What happens: [when (round-1)%6==0] Announce all bids and suits, the declarer, the contract, the trump, and every marriage with its holder and value.
  7. [update] table. What happens: Set trick_cards = [].
  8. [ask] seat leader answers: One card from own hand, chosen by name.. What happens: The chosen card is the lead.
  9. [update] seat leader. What happens: If the card is not in hand, use the lowest-rank card in hand, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it to all.
  10. [ask] seat leader%3+1 answers: One card from own hand, chosen by name (offered the legal cards).. What happens: The chosen card is this seat's play.
  11. [update] seat leader%3+1. What happens: If the card is illegal or not in hand, play the legal card of lowest rank, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it. JUDGED: a referee rules true or false on "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."; write this step's `when` as {"prose": that sentence, verbatim}.
  12. [ask] seat (leader+1)%3+1 answers: One card from own hand, chosen by name (offered the legal cards).. What happens: The chosen card is this seat's play.
  13. [update] seat (leader+1)%3+1. What happens: Validate as in the second player's step, using the fallback if needed. Remove the card from hand, append it to trick_cards, and announce it. JUDGED: a referee rules true or false on "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."; write this step's `when` as {"prose": that sentence, verbatim}.
  14. [update] table. What happens: Each card's key = rank + 10*(suit==trump) + 5*(suit==led suit). The winner is the seat that played the maximum key, the i-th card belonging to seat ((leader-1+i)%3)+1. points = 10 per Ace or Ten in trick_cards, +10 if (round-1)%6==5. If winner==declarer, add points to declarer_points and 1 to declarer_tricks; otherwise add points to defender_points. Set leader = winner. Announce the winner, declarer_points and defender_points.
  15. [update] all players. What happens: [when (round-1)%6==5] tally = declarer_points + (declarer_tricks>=1 ? declarer_marriages : 0) - ((6-declarer_tricks)>=1 ? defender_marriages : 0). S = (contract-40)/10. If tally < contract, S = -(S+1). If trump == Hearts, S = 2*S. The declarer's score += 2*S; each defender's score -= S.
  16. [tell] all players. What happens: [when (round-1)%6==5] Announce the tally, whether the contract was made, and all scores.
  17. [update] table. What happens: round += 1.
  18. [check] table. What happens: End the match if round > 36; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a deal starts (round 1, 7, 13, 19, 25, 31), then each player receives 6 hidden cards and 2 cards go to the talon, which is out of play.
  R2. When a deal starts, then declarer_points, defender_points and declarer_tricks are reset to 0.
  R3. When the deal is d, then the eldest is seat ((d-1)%3)+1: P1 in deals 1 and 4, P2 in deals 2 and 5, P3 in deals 3 and 6.
  R4. When bidding, then all players submit a bid and suit simultaneously and all are revealed together.
  R5. When a bid is not one of PASS, 50, 60, ..., 150, then it counts as PASS.
  R6. When the eldest passes or bids invalidly, then the eldest's bid counts as 50.
  R7. When a suit is missing or invalid, then it becomes the suit in which that player holds the most cards, ties broken by Hearts, Bells, Leaves, Acorns.
  R8. When bids are compared, then the highest bid wins; on a tie the eldest wins, then the next seat after the eldest.
  R9. When the declarer is set, then contract equals the declarer's bid, trump equals the declarer's suit, and the declarer leads trick 1.
  R10. When a player holds the K and O of one suit, then that is a marriage worth 40 in trump and 20 otherwise, credited to the holder's side and publicly announced.
  R11. When a later player holds a card of the led suit, then they must play that suit and beat the highest led-suit card in the trick if they can, unless the led suit is not trump and a trump is already in the trick.
  R12. When a later player has no card of the led suit but holds a trump, then they must play a trump that beats the highest trump in the trick if they can.
  R13. When a later player has neither the led suit nor a trump, then they may play any card.
  R14. When a player names an illegal card or one not in their hand, then the engine plays their legal card of lowest rank, ties broken by suit order.
  R15. When a trick is complete, then the card with the highest key (rank + 10 if trump + 5 if of the led suit) wins.
  R16. When a trick is won, then its Aces and Tens score 10 each to the winner's side, plus 10 if it is the 6th trick of the deal.
  R17. When a trick is won, then the winner leads the next trick.
  R18. When a deal ends, then tally = declarer_points + declarer_marriages (if the declarer won at least 1 trick) - defender_marriages (if the defenders won at least 1 trick).
  R19. When a deal ends with tally >= contract, then S = (contract-40)/10. For example, a 50 contract that is made gives S = 1.
  R20. When a deal ends with tally < contract, then S = -((contract-40)/10 + 1). For example, a failed 50 contract gives S = -2.
  R21. When trump is Hearts, then S is doubled.
  R22. When a deal is settled, then the declarer's score changes by 2*S and each defender's score changes by -S.
  R23. When round 36 is complete, then the match ends and the highest score wins; a tie at the top is shared.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Bid and suit poll | asked: all players | options: The eldest: each of 50,60,...,150 combined with each of Hearts, Bells, Leaves, Acorns (44 options). Any other seat: those 44 plus PASS with each suit (48 options).
  - Leader's card | asked: seat leader | options: Every card in the leader's hand.
  - Second and third player's card | asked: the two non-leading seats | options: Only the cards in hand that are legal under the follow/beat/trump rules. With no led suit and no trump in hand, every card in hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 36
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 6 deals (36 tricks), the player with the highest total score wins. Players tied at the top share the result.
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

- each player: `score` (number, visible: public, starts 0): Match score, the sum of the deal settlements so far.
- the table: `round` (number, visible: public, starts 1): Round (trick) counter, 1..36. deal = floor((round-1)/6)+1, trick = (round-1)%6+1, eldest seat = ((deal-1)%3)+1.
- the table: `declarer` (number, visible: public, starts 0): Seat of this deal's declarer.
- the table: `contract` (number, visible: public, starts 0): Contract T, the declarer's winning bid.
- the table: `trump` (text, visible: public, starts ''): Trump suit, the declarer's bid suit.
- the table: `declarer_points` (number, visible: public, starts 0): Card points won by the declarer this deal, including the last-trick 10.
- the table: `defender_points` (number, visible: public, starts 0): Card points won by the defenders together this deal.
- parameters (each must be an attribute holding this value, never a number buried in a step): card_count = 20, suit_count = 4, ranks_per_suit = 5, suit_code_multiplier = 5, hand_size = 6, talon_size = 2, tricks_per_deal = 6, deals = 6, total_rounds = 36, ace_points = 10, ten_points = 10, last_trick_bonus = 10, deal_card_points_total = 90, min_bid = 50, max_bid = 150, bid_step = 10, eldest_forced_bid = 50, trump_marriage_value = 40, plain_marriage_value = 20, contract_offset = 40, contract_divisor = 10, hearts_multiplier = 2, declarer_score_multiplier = 2, defender_score_multiplier = 1, trump_key_bonus = 10, led_suit_key_bonus = 5, starting_score = 0, min_tricks_for_marriages = 1
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
    "id": "little_bidding_marias",
    "name": "Little Bidding Mariáš",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players, six deals of six tricks: one secret bid picks a declarer and trump, and the declarer plays alone against two defenders to make the contract."
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
        "visible": "public",
        "type": "text",
        "initial": "PASS"
      },
      {
        "key": "bid_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "legal",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "bid_answer",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
      },
      {
        "key": "talon",
        "visible": "none",
        "type": "list",
        "initial": []
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
        "type": "text",
        "initial": ""
      },
      {
        "key": "leader",
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
        "key": "declarer_tricks",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "declarer_marriages",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "defender_marriages",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "marriage_list",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trick_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tally",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "made",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
      },
      {
        "key": "card_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Unter of Hearts",
          "Ober of Hearts",
          "King of Hearts",
          "Ten of Hearts",
          "Ace of Hearts",
          "Unter of Bells",
          "Ober of Bells",
          "King of Bells",
          "Ten of Bells",
          "Ace of Bells",
          "Unter of Leaves",
          "Ober of Leaves",
          "King of Leaves",
          "Ten of Leaves",
          "Ace of Leaves",
          "Unter of Acorns",
          "Ober of Acorns",
          "King of Acorns",
          "Ten of Acorns",
          "Ace of Acorns"
        ]
      },
      {
        "key": "suit_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Hearts",
          "Bells",
          "Leaves",
          "Acorns"
        ]
      },
      {
        "key": "suit_indices",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3]
      },
      {
        "key": "bid_texts",
        "visible": "none",
        "type": "list",
        "initial": ["50", "60", "70", "80", "90", "100", "110", "120", "130", "140", "150"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "played",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "led_suit",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "trump_in_trick",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "high_led",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_trump",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "trump_idx",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stake",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_count",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "suit_count",
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
        "key": "suit_code_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "talon_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "tricks_per_deal",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deals",
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
        "key": "last_trick_bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "deal_card_points_total",
        "visible": "public",
        "type": "number",
        "initial": 90
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "max_bid",
        "visible": "public",
        "type": "number",
        "initial": 150
      },
      {
        "key": "bid_step",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "eldest_forced_bid",
        "visible": "public",
        "type": "number",
        "initial": 50
      },
      {
        "key": "trump_marriage_value",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "plain_marriage_value",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "contract_offset",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "contract_divisor",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "hearts_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "declarer_score_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "defender_score_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_tricks_for_marriages",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "prepare the match",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in full_deck]"
            }
          }
        }
      ],
      "text": "The match begins: {deals} deals of {tricks_per_deal} tricks. Every score starts at {starting_score}."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "shuffle and deal",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "key": "talon",
            "value": []
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in full_deck]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
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
            "key": "talon",
            "value": {
              "calc": "[c for c in deck]"
            }
          }
        },
        {
          "set": {
            "key": "deck",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "cards",
            "value": {
              "calc": "[card_names[c] for c in sorted(you.hand)]"
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
            "key": "declarer_tricks",
            "value": 0
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
            "players": "all",
            "key": "bid_answer",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_offer",
            "value": {
              "calc": "[b + ' ' + s for b in bid_texts for s in suit_names] + ([] if you.seat == ((round - 1) // tricks_per_deal) % 3 + 1 else ['PASS ' + s for s in suit_names])"
            }
          }
        }
      ],
      "text": "A new deal begins. Each player receives {hand_size} hidden cards; {talon_size} cards go face down to the talon and are out of play."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "your hand",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == 0"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "cards"
      ],
      "text": "Your hand for this deal:"
    },
    {
      "use": "poll",
      "phase": "bidding",
      "label": "bid and suit",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == 0"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "bid_offer"
        }
      },
      "store": "bid_answer",
      "text": "Bidding (round {round}). Choose one bid and one suit in a single answer, such as '70 Leaves' or 'PASS Hearts'. Bids run from {min_bid} to {max_bid} in steps of {bid_step}. The eldest may not pass. All bids are revealed together; the highest bid becomes declarer with the named suit as trump (ties go to the eldest, then the next seat after the eldest)."
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "settle the bidding",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "([b for b in bid_texts for s in suit_names if b + ' ' + s == you.bid_answer] + ['PASS'])[0]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == ((round - 1) // tricks_per_deal) % 3 + 1 and you.bid == 'PASS'"
            },
            "key": "bid",
            "value": {
              "calc": "[b for b in bid_texts if int(b) == eldest_forced_bid][0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid_suit",
            "value": {
              "calc": "([s for b in bid_texts + ['PASS'] for s in suit_names if b + ' ' + s == you.bid_answer] + [[s for s in suit_names if count(suit_names[c // suit_code_multiplier] == s for c in you.hand) == max([count(suit_names[c // suit_code_multiplier] == t for c in you.hand) for t in suit_names])][0]])[0]"
            }
          }
        },
        {
          "set": {
            "key": "declarer",
            "value": {
              "calc": "max([[(0 if p.bid == 'PASS' else int(p.bid)) * 10 + 3 - ((p.seat - (((round - 1) // tricks_per_deal) % 3 + 1)) % 3), p.seat] for p in players])[1]"
            }
          }
        },
        {
          "set": {
            "key": "contract",
            "value": {
              "calc": "int(players[declarer - 1].bid)"
            }
          }
        },
        {
          "set": {
            "key": "trump",
            "value": {
              "calc": "players[declarer - 1].bid_suit"
            }
          }
        },
        {
          "set": {
            "key": "trump_idx",
            "value": {
              "calc": "[k for k in suit_indices if suit_names[k] == trump][0]"
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
        }
      ]
    },
    {
      "use": "update",
      "phase": "bidding",
      "label": "find the marriages",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == 0"
      },
      "do": [
        {
          "set": {
            "key": "marriage_list",
            "value": {
              "calc": "[[p.seat, suit_names[k], (trump_marriage_value if k == trump_idx else plain_marriage_value)] for p in players for k in suit_indices if (k * suit_code_multiplier + 2) in p.hand and (k * suit_code_multiplier + 1) in p.hand]"
            }
          }
        },
        {
          "set": {
            "key": "declarer_marriages",
            "value": {
              "calc": "sum([x[2] for x in marriage_list if x[0] == declarer])"
            }
          }
        },
        {
          "set": {
            "key": "defender_marriages",
            "value": {
              "calc": "sum([x[2] for x in marriage_list if x[0] != declarer])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bidding",
      "label": "announce the contract",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == 0"
      },
      "to": "all",
      "text": "Bids [seat, bid, suit]: {[[p.seat, p.bid, p.bid_suit] for p in players]}. Declarer: seat {declarer}. Contract: {contract}. Trump: {trump}. Marriages [holder seat, suit, value] (empty list means none): {marriage_list}. Declarer-side marriages {declarer_marriages}, defender-side marriages {defender_marriages}. Seat {declarer} leads the first trick."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "clear the trick",
      "do": [
        {
          "set": {
            "key": "trick_cards",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[card_names[c] for c in sorted(you.hand)]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "trick",
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
        "bind": "lead_card"
      },
      "text": "You lead this trick. Trump is {trump}; declarer is seat {declarer} (contract {contract}). Play any card from your hand."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "play the lead",
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "([c for c in players[leader - 1].hand if card_names[c] == $lead_card] + [min([[c % suit_code_multiplier, c] for c in players[leader - 1].hand])[1]])[0]"
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
              "calc": "played"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader"
            },
            "key": "cards",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "set": {
            "key": "last_seat",
            "value": {
              "calc": "leader"
            }
          }
        },
        {
          "set": {
            "key": "led_suit",
            "value": {
              "calc": "trick_cards[0] // suit_code_multiplier"
            }
          }
        },
        {
          "set": {
            "key": "trump_in_trick",
            "value": {
              "calc": "any(t // suit_code_multiplier == trump_idx for t in trick_cards)"
            }
          }
        },
        {
          "set": {
            "key": "high_led",
            "value": {
              "calc": "max([t % suit_code_multiplier for t in trick_cards if t // suit_code_multiplier == led_suit])"
            }
          }
        },
        {
          "set": {
            "key": "high_trump",
            "value": {
              "calc": "max([t % suit_code_multiplier for t in trick_cards if t // suit_code_multiplier == trump_idx] + [-1])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "legal",
            "value": {
              "calc": "(([c for c in you.hand if c // suit_code_multiplier == led_suit and c % suit_code_multiplier > high_led] if any(c // suit_code_multiplier == led_suit and c % suit_code_multiplier > high_led for c in you.hand) and not (led_suit != trump_idx and trump_in_trick) else [c for c in you.hand if c // suit_code_multiplier == led_suit]) if any(c // suit_code_multiplier == led_suit for c in you.hand) else (([c for c in you.hand if c // suit_code_multiplier == trump_idx and c % suit_code_multiplier > high_trump] if any(c // suit_code_multiplier == trump_idx and c % suit_code_multiplier > high_trump for c in you.hand) else [c for c in you.hand if c // suit_code_multiplier == trump_idx]) if any(c // suit_code_multiplier == trump_idx for c in you.hand) else you.hand))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[card_names[c] for c in sorted(you.legal)]"
            }
          }
        }
      ],
      "text": "Seat {last_seat} leads the {last_card}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "second card",
      "to": {
        "where": "you.seat == leader % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "card2"
      },
      "text": "Seat {last_seat} led the {last_card}. Trump is {trump}; declarer is seat {declarer}. You are offered only your legal cards: follow suit and beat if you can (no need to beat if the led suit is not trump and a trump is already in), otherwise trump and overtrump if you can, otherwise any card."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "play the second card",
      "when": {
        "prose": "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "([c for c in players[leader % 3].legal if card_names[c] == $card2] + [min([[c % suit_code_multiplier, c] for c in players[leader % 3].legal])[1]])[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader % 3 + 1"
            },
            "key": "hand",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader % 3 + 1"
            },
            "key": "cards",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "set": {
            "key": "last_seat",
            "value": {
              "calc": "leader % 3 + 1"
            }
          }
        },
        {
          "set": {
            "key": "trump_in_trick",
            "value": {
              "calc": "any(t // suit_code_multiplier == trump_idx for t in trick_cards)"
            }
          }
        },
        {
          "set": {
            "key": "high_led",
            "value": {
              "calc": "max([t % suit_code_multiplier for t in trick_cards if t // suit_code_multiplier == led_suit])"
            }
          }
        },
        {
          "set": {
            "key": "high_trump",
            "value": {
              "calc": "max([t % suit_code_multiplier for t in trick_cards if t // suit_code_multiplier == trump_idx] + [-1])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "legal",
            "value": {
              "calc": "(([c for c in you.hand if c // suit_code_multiplier == led_suit and c % suit_code_multiplier > high_led] if any(c // suit_code_multiplier == led_suit and c % suit_code_multiplier > high_led for c in you.hand) and not (led_suit != trump_idx and trump_in_trick) else [c for c in you.hand if c // suit_code_multiplier == led_suit]) if any(c // suit_code_multiplier == led_suit for c in you.hand) else (([c for c in you.hand if c // suit_code_multiplier == trump_idx and c % suit_code_multiplier > high_trump] if any(c // suit_code_multiplier == trump_idx and c % suit_code_multiplier > high_trump for c in you.hand) else [c for c in you.hand if c // suit_code_multiplier == trump_idx]) if any(c // suit_code_multiplier == trump_idx for c in you.hand) else you.hand))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[card_names[c] for c in sorted(you.legal)]"
            }
          }
        }
      ],
      "text": "Seat {last_seat} plays the {last_card}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "second card fallback",
      "when": {
        "calc": "len(trick_cards) < 2"
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "min([[c % suit_code_multiplier, c] for c in players[leader % 3].legal])[1]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader % 3 + 1"
            },
            "key": "hand",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "leader % 3 + 1"
            },
            "key": "cards",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "set": {
            "key": "last_seat",
            "value": {
              "calc": "leader % 3 + 1"
            }
          }
        },
        {
          "set": {
            "key": "trump_in_trick",
            "value": {
              "calc": "any(t // suit_code_multiplier == trump_idx for t in trick_cards)"
            }
          }
        },
        {
          "set": {
            "key": "high_led",
            "value": {
              "calc": "max([t % suit_code_multiplier for t in trick_cards if t // suit_code_multiplier == led_suit])"
            }
          }
        },
        {
          "set": {
            "key": "high_trump",
            "value": {
              "calc": "max([t % suit_code_multiplier for t in trick_cards if t // suit_code_multiplier == trump_idx] + [-1])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "legal",
            "value": {
              "calc": "(([c for c in you.hand if c // suit_code_multiplier == led_suit and c % suit_code_multiplier > high_led] if any(c // suit_code_multiplier == led_suit and c % suit_code_multiplier > high_led for c in you.hand) and not (led_suit != trump_idx and trump_in_trick) else [c for c in you.hand if c // suit_code_multiplier == led_suit]) if any(c // suit_code_multiplier == led_suit for c in you.hand) else (([c for c in you.hand if c // suit_code_multiplier == trump_idx and c % suit_code_multiplier > high_trump] if any(c // suit_code_multiplier == trump_idx and c % suit_code_multiplier > high_trump for c in you.hand) else [c for c in you.hand if c // suit_code_multiplier == trump_idx]) if any(c // suit_code_multiplier == trump_idx for c in you.hand) else you.hand))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[card_names[c] for c in sorted(you.legal)]"
            }
          }
        }
      ],
      "text": "The named card was not legal, so the engine plays the lowest legal card for seat {last_seat}: the {last_card}."
    },
    {
      "use": "ask",
      "phase": "trick",
      "label": "third card",
      "to": {
        "where": "you.seat == (leader + 1) % 3 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "card3"
      },
      "text": "Seat {last_seat} just played the {last_card}; cards in this trick so far are announced above. Trump is {trump}; declarer is seat {declarer}. You are offered only your legal cards: follow suit and beat the highest led-suit card if you can (no need to beat if the led suit is not trump and a trump is already in), otherwise trump and overtrump if you can, otherwise any card."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "play the third card",
      "when": {
        "prose": "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "([c for c in players[(leader + 1) % 3].legal if card_names[c] == $card3] + [min([[c % suit_code_multiplier, c] for c in players[(leader + 1) % 3].legal])[1]])[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "(leader + 1) % 3 + 1"
            },
            "key": "hand",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "(leader + 1) % 3 + 1"
            },
            "key": "cards",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "set": {
            "key": "last_seat",
            "value": {
              "calc": "(leader + 1) % 3 + 1"
            }
          }
        }
      ],
      "text": "Seat {last_seat} plays the {last_card}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "third card fallback",
      "when": {
        "calc": "len(trick_cards) < 3"
      },
      "do": [
        {
          "set": {
            "key": "played",
            "value": {
              "calc": "min([[c % suit_code_multiplier, c] for c in players[(leader + 1) % 3].legal])[1]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "(leader + 1) % 3 + 1"
            },
            "key": "hand",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "(leader + 1) % 3 + 1"
            },
            "key": "cards",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "append": {
            "key": "trick_cards",
            "value": {
              "calc": "played"
            }
          }
        },
        {
          "set": {
            "key": "last_card",
            "value": {
              "calc": "card_names[played]"
            }
          }
        },
        {
          "set": {
            "key": "last_seat",
            "value": {
              "calc": "(leader + 1) % 3 + 1"
            }
          }
        }
      ],
      "text": "The named card was not legal, so the engine plays the lowest legal card for seat {last_seat}: the {last_card}."
    },
    {
      "use": "update",
      "phase": "trick",
      "label": "take the trick",
      "do": [
        {
          "set": {
            "key": "trick_winner",
            "value": {
              "calc": "((leader - 1 + max([[trick_cards[i] % suit_code_multiplier + (trump_key_bonus if trick_cards[i] // suit_code_multiplier == trump_idx else 0) + (led_suit_key_bonus if trick_cards[i] // suit_code_multiplier == led_suit else 0), i] for i in [0, 1, 2]])[1]) % 3) + 1"
            }
          }
        },
        {
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "sum([(ace_points if t % suit_code_multiplier == 4 else (ten_points if t % suit_code_multiplier == 3 else 0)) for t in trick_cards]) + (last_trick_bonus if (round - 1) % tricks_per_deal == tricks_per_deal - 1 else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "declarer_points",
            "value": {
              "calc": "trick_points"
            },
            "if": {
              "calc": "trick_winner == declarer"
            }
          }
        },
        {
          "adjust": {
            "key": "declarer_tricks",
            "value": 1,
            "if": {
              "calc": "trick_winner == declarer"
            }
          }
        },
        {
          "adjust": {
            "key": "defender_points",
            "value": {
              "calc": "trick_points"
            },
            "if": {
              "calc": "trick_winner != declarer"
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
      "text": "Seat {trick_winner} wins the trick, worth {trick_points}. Declarer points {declarer_points}, defender points {defender_points}. Seat {trick_winner} leads next."
    },
    {
      "use": "update",
      "phase": "settlement",
      "label": "settle the deal",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == tricks_per_deal - 1"
      },
      "do": [
        {
          "set": {
            "key": "tally",
            "value": {
              "calc": "declarer_points + (declarer_marriages if declarer_tricks >= min_tricks_for_marriages else 0) - (defender_marriages if tricks_per_deal - declarer_tricks >= min_tricks_for_marriages else 0)"
            }
          }
        },
        {
          "set": {
            "key": "made",
            "value": {
              "calc": "'made' if tally >= contract else 'failed'"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "(contract - contract_offset) // contract_divisor"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake if tally >= contract else -(stake + 1)"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "stake * hearts_multiplier if trump == 'Hearts' else stake"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == declarer"
            },
            "key": "score",
            "value": {
              "calc": "declarer_score_multiplier * stake"
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
              "calc": "-(defender_score_multiplier * stake)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "settlement",
      "label": "announce the settlement",
      "when": {
        "calc": "(round - 1) % tricks_per_deal == tricks_per_deal - 1"
      },
      "to": "all",
      "text": "Deal over. Declarer seat {declarer} tallied {tally} against a contract of {contract}: the contract is {made}. Scores: P1 {players[0].score}, P2 {players[1].score}, P3 {players[2].score}."
    },
    {
      "use": "update",
      "phase": "settlement",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "settlement",
      "label": "after the last deal",
      "when": {
        "calc": "round > total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > total_rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: P1 {players[0].score}, P2 {players[1].score}, P3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "CARDS. {card_count} cards in {suit_count} suits (Hearts, Bells, Leaves, Acorns), each with ranks A, 10, K, O (Ober), U (Unter), highest to lowest. Each Ace is worth {ace_points} and each Ten {ten_points} card points; other cards are worth 0. Winning the last (6th) trick of a deal is worth {last_trick_bonus} more, so a deal holds {deal_card_points_total} card points. Suit order for tie-breaks is Hearts, Bells, Leaves, Acorns.\n\nMATCH. {deals} deals of {tricks_per_deal} tricks, {total_rounds} rounds; each round is one trick. Seats P1, P2, P3 in cyclic order. The eldest is P1 in deals 1 and 4, P2 in deals 2 and 5, P3 in deals 3 and 6. Scores start at {starting_score}. Players may not exchange messages at any time; defenders cooperate only through their card play.\n\nDEAL. At the start of each deal all cards are shuffled and each player gets {hand_size} private cards. The other {talon_size} form the talon: face down, seen by no one, out of play for the whole deal.\n\nBIDDING. Every player privately submits one answer with a bid and a suit. A bid is PASS or {min_bid} to {max_bid} in steps of {bid_step}; a suit is Hearts, Bells, Leaves or Acorns. Any bid not in this list counts as PASS. The eldest may not pass: an eldest PASS or invalid bid counts as {eldest_forced_bid}. A missing or invalid suit becomes the suit in which that player holds the most cards, ties broken by the suit order. All bids and suits are revealed together. The highest bid wins; if bids are equal, the eldest wins the tie first, then the next player in seat order after the eldest. The winner is the declarer, their bid is the contract T, and their suit is trump. The other two are the defenders and form a team for this deal.\n\nMARRIAGES. Right after bidding, every player holding both the K and the O of one suit has a marriage in that suit, worth {trump_marriage_value} in trump and {plain_marriage_value} in any other suit, belonging to its holder's side. Every marriage, its holder and value are announced publicly. At the end of the deal a side's marriages count only if that side won at least {min_tricks_for_marriages} trick; if it won no trick they do not count.\n\nPLAYING A TRICK. The declarer leads the first trick; after that the winner of the previous trick leads. Starting with the leader, each player in seat order plays one card, announced to all. The leader may play any card. For the others: (a) If you hold a card of the led suit, you must play that suit, and you must play one that beats the highest card of the led suit already in the trick, if you can. This beating duty is lifted only when the led suit is not trump and a trump has already been played to this trick. (b) If you hold no card of the led suit but hold a trump, you must play a trump, and it must beat the highest trump already in the trick, if you can. (c) Otherwise you may play any card. You are offered only your legal cards. If a player names a card that is illegal or not in their hand, the engine plays for them the legal card of lowest rank; among equal ranks, the first in the suit order. A legal named card is played as named.\nThe trick is won by the highest trump in it, or by the highest card of the led suit if it holds no trump (each card's key is its rank, +{trump_key_bonus} if trump, +{led_suit_key_bonus} if of the led suit; the highest key wins). The trick's card points, plus {last_trick_bonus} if it is the 6th trick, go to the winner's side: the declarer alone, or the defenders together. The trick winner and both sides' running points are announced.\n\nEND OF DEAL. 1. The declarer's tally is the declarer's points (including any last-trick bonus), plus the declarer's marriages if the declarer won at least 1 trick, minus the defenders' marriages if the defenders won at least 1 trick. 2. S = (T - {contract_offset}) / {contract_divisor}, so 50 gives S = 1 and 150 gives S = 11. 3. If the tally is at least T, the contract is made and S is unchanged; otherwise the contract fails and S becomes -(S + 1) (a failed 50 gives -2). 4. If trump is Hearts, S is multiplied by {hearts_multiplier}. 5. The declarer's score changes by {declarer_score_multiplier} x S and each defender's score changes by -S. 6. The tally, whether the contract was made, and all scores are announced.\n\nWINNING. After round {total_rounds} (6 deals), the player with the highest total score wins. Players tied at the top share the win. Every deal is zero-sum, so the totals always sum to 0."
}
```
````
