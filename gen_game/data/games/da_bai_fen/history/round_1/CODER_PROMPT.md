# Task: write the XColos game file for "Da Bai Fen Lite"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SEATS AND TEAMS. Seats 1, 2, 3 and 4 sit in anticlockwise order. Seats 1 and 3 are Team North-South (NS). Seats 2 and 4 are Team East-West (EW). Partners cannot see each other's cards. There is no talk; the only communication is the cards played.

DECK. The deck has 30 cards. Each of four suits (Spades, Hearts, Clubs, Diamonds) has seven cards: 5, 8, 10, J, Q, K, A, with rank values 5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7. There are also two jokers: the Big Joker and the Small Joker. Point cards: each K is worth 10 points, each 10 is worth 10 points, each 5 is worth 5 points. All other cards and both jokers are worth 0. The deck holds 100 points in total.

MATCH STRUCTURE. The match has 4 hands of 8 rounds each, 32 rounds in total. The declarer is seat 1 in hand 1, seat 2 in hand 2, seat 3 in hand 3 and seat 4 in hand 4. The declarer's team is the Declaring Team for that hand; the other team is the Defending Team.

ROUND 1 OF EACH HAND (DEAL AND TRUMPS). The 30 cards are shuffled (the only random draw of the round). Each player privately receives 7 cards. The remaining 2 cards form the face-down kitty, which no one sees. The declarer then names one suit as the trump suit, and it is announced to all. Trumps are the Big Joker, the Small Joker and the 7 cards of the trump suit, 9 cards in all. For following purposes all trumps form one suit, the Trump suit. The declarer will lead the first trick.

ROUNDS 2 TO 8 OF EACH HAND (ONE TRICK EACH).
(a) The leader plays any one card face up. The suit of that card is the led suit; if the card is a trump, the led suit is Trump.
(b) The other three players then each play one card face up, one after another, in anticlockwise order from the leader. Each sees the cards already played. A player holding a card of the led suit must play one. A player holding none may play any card. An illegal play is rejected and the player must choose again.
(c) Strength of each played card. Big Joker = 40. Small Joker = 39. A trump-suit card = 20 + its rank value. A non-trump card of the led suit = 10 + its rank value. Any other card = its rank value.
(d) The card with the highest strength wins the trick. Ties cannot occur. The winner's team adds the point values of the four cards to its hand points, and the winner leads the next trick.
(e) In round 8 (the 7th and last trick), the kitty is also revealed after the trick, and its points are added to the hand points of the team that won that trick.

END OF HAND SCORING. Let P be the Defending Team's hand points, always a multiple of 5 from 0 to 100.
- P from 0 to 15: Declaring Team +3 match points.
- P from 20 to 35: Declaring Team +2.
- P from 40 to 55: Defending Team +1.
- P from 60 to 75: Defending Team +2.
- P from 80 to 100: Defending Team +3.
In addition, each team adds its hand points to its running card-point total. Hand points then reset to 0 for the next hand.

How the winner is decided: After hand 4, the team with more match points wins, and both its players win. If match points are equal, the team with the higher card-point total over all four hands wins. If that is also equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Da Bai Fen Lite (4 to 4 players, best with 4)

A four-player partnership trick-taking game (NS v EW) over 4 hands of 7 tricks with a 30-card deck and jokers. Teams win match points by how many card points the defenders capture.

STATE (every item below must exist in the file):
  - each player: team (text, starts 'NS for seats 1 and 3, EW for seats 2 and 4'); everyone sees it. the player's team
  - each player: hand (list, starts []); only its owner sees it. the cards the player holds, as codes such as 'S-K', 'H-10', 'BJ' (Big Joker), 'SJ' (Small Joker)
  - each player: played_card (text, starts ''); everyone sees it. the card the player played to the current trick, face up
  - each player: card_strength (number, starts 0); everyone sees it. the strength of played_card in the current trick
  - each player: match_points (number, starts 0); everyone sees it. the team's match points, mirrored on both partners
  - each player: card_points (number, starts 0); everyone sees it. the team's running card-point total over completed hands, mirrored on both partners
  - the table: deck (list, starts 'all 30 cards'); hidden from all players. the undealt cards: 4 suits x {5,8,10,J,Q,K,A} plus BJ and SJ
  - the table: kitty (list, starts []); hidden from all players. the 2 face-down cards left after the deal
  - the table: hand_number (number, starts 1); everyone sees it. the current hand, 1 to 4
  - the table: round_in_hand (number, starts 1); everyone sees it. the round within the hand, 1 to 8 (1 = deal and trumps, 2 to 8 = tricks)
  - the table: declarer (number, starts 1); everyone sees it. the declarer's seat, equal to hand_number
  - the table: declaring_team (text, starts 'NS'); everyone sees it. the declarer's team: NS when declarer is 1 or 3, EW when declarer is 2 or 4
  - the table: trump_suit (text, starts ''); everyone sees it. the trump suit named by the declarer
  - the table: leader (number, starts 1); everyone sees it. the seat that leads the current trick
  - the table: led_suit (text, starts ''); everyone sees it. the suit of the led card, or 'Trump' if the led card is a trump
  - the table: trick_winner (number, starts 0); everyone sees it. the seat whose card has the highest card_strength in the trick
  - the table: trick_points (number, starts 0); everyone sees it. the sum of point values of the 4 cards in the trick
  - the table: ns_hand_points (number, starts 0); everyone sees it. card points NS has won this hand
  - the table: ew_hand_points (number, starts 0); everyone sees it. card points EW has won this hand
  - the table: defender_points (number, starts 0); everyone sees it. P, the Defending Team's hand points at the end of the hand
  - the table: ns_match_points (number, starts 0); everyone sees it. NS match points
  - the table: ew_match_points (number, starts 0); everyone sees it. EW match points
  - the table: ns_card_points (number, starts 0); everyone sees it. NS running card-point total
  - the table: ew_card_points (number, starts 0); everyone sees it. EW running card-point total
  - parameters, each kept as a table attribute: seats = 4, deck_size = 30, suits = 4, cards_per_suit = 7, jokers = 2, rank_5 = 1, rank_8 = 2, rank_10 = 3, rank_j = 4, rank_q = 5, rank_k = 6, rank_a = 7, points_k = 10, points_10 = 10, points_5 = 5, points_other = 0, total_points = 100, hands = 4, rounds_per_hand = 8, total_rounds = 32, tricks_per_hand = 7, cards_dealt_each = 7, kitty_size = 2, trump_count = 9, big_joker_strength = 40, small_joker_strength = 39, trump_base = 20, led_suit_base = 10, off_suit_base = 0, band_declarer_3_max = 15, band_declarer_2_min = 20, band_declarer_2_max = 35, band_defender_1_min = 40, band_defender_1_max = 55, band_defender_2_min = 60, band_defender_2_max = 75, band_defender_3_min = 80, award_3 = 3, award_2 = 2, award_1 = 1, rank_weight_match_points = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 and 3 get team NS; seats 2 and 4 get team EW.
  2. All match_points, card_points and team totals start at 0.
  3. Set hand_number = 1, round_in_hand = 1, declarer = 1, declaring_team = NS.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: when round_in_hand == 1: deck is reset to all 30 cards; every hand, kitty and trump_suit are cleared; ns_hand_points = ew_hand_points = 0; declarer = hand_number; declaring_team = NS if declarer is odd, else EW; leader = declarer
  2. [update] all players. What happens: when round_in_hand == 1: draw 7 random cards from deck into each player's hand (removed from deck), then move the 2 remaining cards of deck into kitty
  3. [sync] all players. What happens: when round_in_hand == 1: each player sees their own hand only
  4. [ask] the declarer (seat = declarer) answers: one of: Spades, Hearts, Clubs, Diamonds. What happens: when round_in_hand == 1: trump_suit = the answer; announce to all 'Trump suit is {trump_suit}; seat {declarer} leads.'
  5. [update] all players. What happens: when round_in_hand >= 2: every played_card = '' and card_strength = 0; led_suit = ''
  6. [ask] each player in turn, starting from seat = leader and going anticlockwise (leader, leader+1, leader+2, leader+3, wrapping 4 to 1) answers: one card from own hand: the leader may choose any card; a follower must choose a card of led_suit if holding one (jokers and trump_suit cards count as suit 'Trump'), otherwise any card. What happens: when round_in_hand >= 2: the card moves from hand to played_card, face up to all; if the player is the leader, led_suit = 'Trump' when the card is a joker or of trump_suit, else the card's suit; card_strength = 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump card of led_suit, otherwise rank (5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7) JUDGED: a referee rules true or false on "The card this player chose is legal: either the player is the leader, or the card is of the led suit (jokers and trump-suit cards counting as Trump), or the player held no card of the led suit."; write this step's `when` as {"prose": that sentence, verbatim}.
  7. [update] all players. What happens: when round_in_hand >= 2: trick_winner = the seat with the highest card_strength; trick_points = sum over the 4 played cards of (10 for K, 10 for 10, 5 for 5, 0 otherwise); if trick_winner's team is NS then ns_hand_points += trick_points, else ew_hand_points += trick_points; leader = trick_winner; announce 'Seat {trick_winner} wins the trick for {trick_points} points.'
  8. [update] all players. What happens: when round_in_hand == 8: reveal kitty to all; add the kitty's point values to the hand points of trick_winner's team
  9. [update] all players. What happens: when round_in_hand == 8: defender_points = ew_hand_points if declaring_team is NS, else ns_hand_points; if defender_points <= 15, the declaring team's match points += 3; if 20..35, the declaring team += 2; if 40..55, the defending team += 1; if 60..75, the defending team += 2; if >= 80, the defending team += 3; ns_card_points += ns_hand_points; ew_card_points += ew_hand_points; copy the team match points and card points onto each player's match_points and card_points; announce the hand result
  10. [update] all players. What happens: if round_in_hand == 8 then hand_number += 1 and round_in_hand = 1, else round_in_hand += 1
  11. [check] all players. What happens: end the game when hand_number > 4; otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Seats 1 and 3 are team NS and seats 2 and 4 are team EW, and no talk step exists.
  R2. When round_in_hand is 1, each player is dealt 7 cards from the 30-card deck and the other 2 cards go to the hidden kitty.
  R3. The declarer is seat 1 in hand 1, seat 2 in hand 2, seat 3 in hand 3 and seat 4 in hand 4.
  R4. When round_in_hand is 1, the declarer names one of Spades, Hearts, Clubs or Diamonds as trump_suit, it is announced to all, and the declarer leads the first trick.
  R5. Trumps are BJ, SJ and the 7 cards of trump_suit, 9 cards in all, and they count as the single suit 'Trump' for following.
  R6. When the leader plays a card, led_suit becomes that card's suit, or 'Trump' if the card is a joker or of trump_suit.
  R7. When a follower holds a card of led_suit, then only led_suit cards are offered; when they hold none, then every card in their hand is offered.
  R8. Players play to a trick in anticlockwise order starting from the leader, and each sees the cards already played.
  R9. Card strength is 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump led_suit card, and rank otherwise, with 5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7.
  R10. The highest-strength card wins the trick; its team adds the trick's points (K=10, 10=10, 5=5, others 0) to its hand points, and its player leads next.
  R11. When round_in_hand is 8, after the trick the kitty is revealed and its points go to the team that won that trick.
  R12. At the end of a hand, if defender_points is 0 to 15, the Declaring Team gains 3 match points.
  R13. At the end of a hand, if defender_points is 20 to 35, the Declaring Team gains 2 match points.
  R14. At the end of a hand, if defender_points is 40 to 55, the Defending Team gains 1 match point.
  R15. At the end of a hand, if defender_points is 60 to 75, the Defending Team gains 2 match points.
  R16. At the end of a hand, if defender_points is 80 to 100, the Defending Team gains 3 match points.
  R17. At the end of each hand, each team adds its hand points to its card-point total, and hand points reset to 0 for the next hand.
  R18. After 4 hands (32 rounds), the team with more match points wins; if level, the team with more card points wins; if both are level, the match is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Name the trump suit (round 1 of each hand) | asked: the declarer only | options: Spades, Hearts, Clubs, Diamonds
  - Play a card to the trick (rounds 2 to 8) | asked: each seat in turn from the leader | options: the leader: every card in own hand; a follower holding at least one card of led_suit (for led_suit Trump: jokers and trump_suit cards; for any other suit: cards of that suit that are not trumps): only those cards; a follower holding no led_suit card: every card in own hand

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number > 4 (after 32 rounds)
  - each player's standing: you.match_points * 1000 + you.card_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The team with more match points wins, and both its partners win. If match points are equal, the team with the higher card-point total wins. If both are equal, all four players share the top value, which is a draw.
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

- each player: `team` (text, visible: public, starts 'NS for seats 1 and 3, EW for seats 2 and 4'): the player's team
- each player: `match_points` (number, visible: public, starts 0): the team's match points, mirrored on both partners
- each player: `card_points` (number, visible: public, starts 0): the team's running card-point total over completed hands, mirrored on both partners
- the table: `hand_number` (number, visible: public, starts 1): the current hand, 1 to 4
- the table: `declarer` (number, visible: public, starts 1): the declarer's seat, equal to hand_number
- the table: `trump_suit` (text, visible: public, starts ''): the trump suit named by the declarer
- the table: `ns_hand_points` (number, visible: public, starts 0): card points NS has won this hand
- the table: `ew_hand_points` (number, visible: public, starts 0): card points EW has won this hand
- the table: `ns_match_points` (number, visible: public, starts 0): NS match points
- the table: `ew_match_points` (number, visible: public, starts 0): EW match points
- the table: `ns_card_points` (number, visible: public, starts 0): NS running card-point total
- the table: `ew_card_points` (number, visible: public, starts 0): EW running card-point total
- parameters (each must be an attribute holding this value, never a number buried in a step): seats = 4, deck_size = 30, suits = 4, cards_per_suit = 7, jokers = 2, rank_5 = 1, rank_8 = 2, rank_10 = 3, rank_j = 4, rank_q = 5, rank_k = 6, rank_a = 7, points_k = 10, points_10 = 10, points_5 = 5, points_other = 0, total_points = 100, hands = 4, rounds_per_hand = 8, total_rounds = 32, tricks_per_hand = 7, cards_dealt_each = 7, kitty_size = 2, trump_count = 9, big_joker_strength = 40, small_joker_strength = 39, trump_base = 20, led_suit_base = 10, off_suit_base = 0, band_declarer_3_max = 15, band_declarer_2_min = 20, band_declarer_2_max = 35, band_defender_1_min = 40, band_defender_1_max = 55, band_defender_2_min = 60, band_defender_2_max = 75, band_defender_3_min = 80, award_3 = 3, award_2 = 2, award_1 = 1, rank_weight_match_points = 1000
- the game ends with ONE ending whose `rank_by` is `you.match_points * 1000 + you.card_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
