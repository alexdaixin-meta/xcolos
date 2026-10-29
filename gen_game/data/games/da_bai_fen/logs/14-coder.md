# 14 coder

- time: 2026-10-28T03:16:57+00:00 (152.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 6c313b8f3df2ece7, reply sha256 24ab4d8a14065b78

## Sent

````
# Task: write the XColos game file for "Da Bai Fen Duplicate"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SEATS AND TEAMS: Seats are numbered 1, 2, 3, 4 in anticlockwise order. Team A is seats 1 and 3; Team B is seats 2 and 4. Play always proceeds anticlockwise: after seat 1 comes 2, then 3, then 4, then 1.

CARDS: The deck has 26 cards: the Big Joker, the Small Joker, and four suits (Spades, Hearts, Clubs, Diamonds) each containing A, K, Q, J, 10, 5. Point values are 5 = 5 points, 10 = 10 points, K = 10 points, and all other cards 0. Each suit holds 25 points, so the deck holds 100.

TRUMPS: Hands 1 and 3 have Spades as trump; hands 2 and 4 have Hearts as trump. The trumps are, from high to low: Big Joker, Small Joker, then A, K, Q, J, 10, 5 of the trump suit. Both jokers belong to the trump suit for following purposes. In every non-trump suit the order is A, K, Q, J, 10, 5.

THE MATCH has 4 hands of 6 tricks each, 24 rounds in total. Each round is one trick.

DEALING: At the start of hand 1 the 26 cards are shuffled at random. Each seat receives 6 cards, which are private to that seat, and the remaining 2 cards form the kitty, face down and seen by no one. Hand 2 is a new random shuffle, dealt the same way. Hand 3 replays hand 1: every seat receives the exact 6 cards held in hand 1 by the seat before it in seat order (seat 2 gets seat 1's hand 1 cards, seat 3 gets seat 2's, seat 4 gets seat 3's, seat 1 gets seat 4's), and the kitty is the same 2 cards. Hand 4 replays hand 2 in the same rotated way. Players are told when a hand is a replay.

FIRST LEADER of each hand: seat 1 in hand 1, seat 2 in hand 2, seat 2 in hand 3, seat 3 in hand 4. In each replay, the first leader holds the same cards as the first leader of the original hand.

A TRICK (one round): The leader plays any one card from their hand face up. Then the other three seats, in anticlockwise order, each play one card. Each player sees all cards already played to the trick.
- Following: If the led card is a trump (a joker or a trump-suit card), each player must play a trump if they hold one. Otherwise each player must play a card of the led suit if they hold one. A player with no card of the required suit may play any card.
- The engine lists only the legal cards as options.
- Winning: If any trump was played, the highest trump wins the trick. Otherwise the highest card of the led suit wins. Off-suit non-trump cards never win.

AFTER EACH TRICK: All four cards are announced along with the winner. The winner's team adds the point value of the four cards to its match total. The winner leads the next trick of the same hand.

END OF HAND: After the 6th trick the kitty is revealed. Its point value multiplied by 2 is added to the match total of the team that won the 6th trick. The next hand begins with its own deal and first leader.

INFORMATION: Each player always sees their own cards, all cards played so far in the hand, both teams' match totals, the trump suit, the trick number and the hand number. Other players' hands and the kitty stay hidden until the kitty is revealed at the end of the hand. There is no table talk.

How the winner is decided: After hand 4, the team with the higher match total (captured card points plus doubled kitty points) wins. If the totals are equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Da Bai Fen Duplicate (4 to 4 players, best with 4)

Four players in two fixed partnerships play 4 hands of 6 trick-taking rounds with a 26-card deck. Hands 3 and 4 replay the deals of hands 1 and 2, rotated one seat, and the team that captures more card points wins.

STATE (every item below must exist in the file):
  - each player: team (text, starts 'A for seats 1 and 3, B for seats 2 and 4'); everyone sees it. The seat's partnership.
  - each player: hand (list, starts []); only its owner sees it. The cards the seat currently holds. Each card is a code: suit letter S, H, C or D plus rank A, K, Q, 10, J or 5, or JOKER_BIG or JOKER_SMALL.
  - each player: hand1_cards (list, starts []); only its owner sees it. The 6 cards this seat was dealt in hand 1, kept for the replay in hand 3.
  - each player: hand2_cards (list, starts []); only its owner sees it. The 6 cards this seat was dealt in hand 2, kept for the replay in hand 4.
  - each player: played_card (text, starts ''); everyone sees it. The card this seat played to the current trick.
  - each player: card_strength (number, starts 0); everyone sees it. Strength of the played card in this trick: 200 + rank if it is a trump, 100 + rank if it is of the led non-trump suit, otherwise 0.
  - each player: score (number, starts 0); everyone sees it. The match total of this seat's team, mirrored onto both partners.
  - the table: deck (list, starts 'all 26 cards'); hidden from all players. Undealt cards for a fresh shuffle.
  - the table: kitty (list, starts []); hidden from all players. The 2 face-down cards of the current hand.
  - the table: kitty_hand1 (list, starts []); hidden from all players. The kitty of hand 1, kept for hand 3.
  - the table: kitty_hand2 (list, starts []); hidden from all players. The kitty of hand 2, kept for hand 4.
  - the table: kitty_revealed (list, starts []); everyone sees it. The kitty, shown after the 6th trick of a hand.
  - the table: hand_number (number, starts 1); everyone sees it. The current hand, from 1 to 4.
  - the table: trick_number (number, starts 1); everyone sees it. The current trick within the hand, from 1 to 6.
  - the table: trump_suit (text, starts 'S'); everyone sees it. The trump suit: S in hands 1 and 3, H in hands 2 and 4.
  - the table: is_replay (bool, starts False); everyone sees it. True in hands 3 and 4.
  - the table: leader (number, starts 1); everyone sees it. The seat that leads the current trick.
  - the table: led_card (text, starts ''); everyone sees it. The first card played to the current trick.
  - the table: led_is_trump (bool, starts False); everyone sees it. Whether the led card is a joker or a trump-suit card.
  - the table: led_suit (text, starts ''); everyone sees it. The suit of the led card. TRUMP if the led card is trump.
  - the table: trick_cards (list, starts []); everyone sees it. The cards played to the current trick, in order.
  - the table: played_this_hand (list, starts []); everyone sees it. All cards played so far in the current hand.
  - the table: trick_winner (number, starts 0); everyone sees it. The seat that won the last trick.
  - the table: trick_points (number, starts 0); everyone sees it. The point value of the 4 cards in the last trick.
  - the table: team_a_total (number, starts 0); everyone sees it. Match total of Team A (seats 1 and 3).
  - the table: team_b_total (number, starts 0); everyone sees it. Match total of Team B (seats 2 and 4).
  - parameters, each kept as a table attribute: deck_size = 26, cards_per_seat = 6, kitty_size = 2, hands = 4, tricks_per_hand = 6, total_rounds = 24, points_five = 5, points_ten = 10, points_king = 10, points_other = 0, points_per_suit = 25, points_in_deck = 100, kitty_multiplier = 2, first_leader_hand_1 = 1, first_leader_hand_2 = 2, first_leader_hand_3 = 2, first_leader_hand_4 = 3, rank_big_joker = 8, rank_small_joker = 7, rank_ace = 6, rank_king = 5, rank_queen = 4, rank_jack = 3, rank_ten = 2, rank_five = 1, trump_strength_base = 200, led_suit_strength_base = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1 and 3 are given team A, and seats 2 and 4 are given team B.
  2. The table deck is filled with the 26 cards: JOKER_BIG, JOKER_SMALL, and A, K, Q, J, 10, 5 of each of S, H, C, D.
  3. hand_number = 1, trick_number = 1, trump_suit = S, leader = 1, and team_a_total = team_b_total = 0. Every score is 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Runs only when trick_number == 1. Clears played_this_hand and kitty_revealed. If hand_number is 1 or 2, the deck is refilled with all 26 cards; each seat then draws 6 cards at random from the deck into its hand, and the 2 cards left move to the kitty. When hand_number == 1, each hand is copied to hand1_cards and the kitty to kitty_hand1. When hand_number == 2, each hand is copied to hand2_cards and the kitty to kitty_hand2. If hand_number == 3, each seat s gets hand = hand1_cards of seat s-1 (seat 1 gets seat 4's), and kitty = kitty_hand1. If hand_number == 4, each seat s gets hand = hand2_cards of seat s-1, and kitty = kitty_hand2. trump_suit is S if hand_number is 1 or 3, otherwise H. leader is 1, 2, 2 or 3 for hands 1 to 4. is_replay = (hand_number >= 3).
  2. [tell] all players. What happens: Runs only when trick_number == 1. Announces 'Hand {hand_number} begins. Trump is {trump_suit}. Seat {leader} leads.' When is_replay is true, it adds 'This hand is a replay: each seat holds the cards the previous seat held in hand {hand_number - 2}.'
  3. [sync] all players. What happens: Each seat is sent its own hand, plus played_this_hand, team_a_total, team_b_total, trump_suit, trick_number and hand_number.
  4. [ask] each player in turn, starting with the seat in leader and going anticlockwise (leader, leader+1, ... wrapping 4 to 1) answers: One card from the seat's own hand, chosen from the legal options only (see offers).. What happens: The card is removed from the player's hand and appended to trick_cards and played_this_hand, and played_card is set. For the first player, led_card is set to the card. led_is_trump = (the card is a joker or of trump_suit). led_suit = TRUMP if led_is_trump, otherwise the card's suit.
  5. [update] all players. What happens: Each seat gets card_strength = 200 + rank if played_card is a joker or of trump_suit; otherwise 100 + rank if led_is_trump is false and played_card's suit == led_suit; otherwise 0. Ranks are Big Joker 8, Small Joker 7, A 6, K 5, Q 4, J 3, 10 2, 5 1. trick_winner = the seat with the highest card_strength. trick_points = the sum of the points of the 4 trick_cards, where 5 = 5, 10 = 10, K = 10 and all others = 0. If trick_winner is 1 or 3, team_a_total += trick_points; otherwise team_b_total += trick_points. Seats 1 and 3 get score = team_a_total, and seats 2 and 4 get score = team_b_total. leader = trick_winner.
  6. [tell] all players. What happens: Announces 'Trick {trick_number} of hand {hand_number}: cards {trick_cards}. Seat {trick_winner} wins {trick_points} points. Team A {team_a_total}, Team B {team_b_total}.'
  7. [update] all players. What happens: Runs only when trick_number == 6. kitty_revealed = kitty. If trick_winner is 1 or 3, team_a_total += 2 * (points of kitty); otherwise team_b_total += 2 * (points of kitty). Both teams' scores are mirrored to the seats again.
  8. [tell] all players. What happens: Runs only when trick_number == 6. Announces 'End of hand {hand_number}. Kitty: {kitty_revealed}, doubled for the team of seat {trick_winner}. Team A {team_a_total}, Team B {team_b_total}.'
  9. [update] all players. What happens: trick_cards is cleared, led_card is set to empty, and each played_card is set to empty. trick_number += 1. If trick_number > 6, then trick_number = 1 and hand_number += 1.
  10. [check] all players. What happens: The game ends if hand_number > 4. Otherwise it continues with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Team A is seats 1 and 3, and Team B is seats 2 and 4. Play goes 1, 2, 3, 4, 1.
  R2. The deck has 26 cards: Big Joker, Small Joker, and A, K, Q, J, 10, 5 of Spades, Hearts, Clubs and Diamonds.
  R3. A 5 is worth 5 points, a 10 is worth 10, a K is worth 10, and every other card is worth 0, so the deck holds 100 points.
  R4. In hands 1 and 3 the trump suit is Spades, and in hands 2 and 4 it is Hearts.
  R5. Trumps rank from high to low as Big Joker, Small Joker, A, K, Q, J, 10, 5 of the trump suit, and both jokers count as trump for following.
  R6. In a non-trump suit the cards rank A, K, Q, J, 10, 5.
  R7. At the start of hands 1 and 2, the 26 cards are shuffled, each seat gets 6 private cards, and the remaining 2 cards form a hidden kitty.
  R8. In hand 3, seat s holds exactly the 6 cards seat s-1 held in hand 1 (seat 1 gets seat 4's), and the kitty equals hand 1's kitty.
  R9. In hand 4, seat s holds exactly the 6 cards seat s-1 held in hand 2 (seat 1 gets seat 4's), and the kitty equals hand 2's kitty.
  R10. Players are told at the start of hands 3 and 4 that the hand is a replay.
  R11. The first leader is seat 1 in hand 1, seat 2 in hand 2, seat 2 in hand 3 and seat 3 in hand 4.
  R12. The leader may play any card in their hand.
  R13. When the led card is a trump, a player holding a trump is offered only their trumps.
  R14. When the led card is a non-trump suit, a player holding that suit is offered only cards of that suit.
  R15. A player with no card of the required suit is offered every card in their hand.
  R16. When any trump is played to a trick, the highest trump wins the trick.
  R17. When no trump is played, the highest card of the led suit wins, and off-suit non-trump cards never win.
  R18. After each trick, the winner's team adds the point value of the 4 cards to its match total.
  R19. The winner of a trick leads the next trick of the same hand.
  R20. After the 6th trick of a hand, the kitty is revealed and 2 times its point value is added to the team that won the 6th trick.
  R21. Other players' hands and the kitty stay hidden until the kitty is revealed at the end of the hand.
  R22. The match ends after hand 4 (24 tricks), and the team with the higher match total wins.
  R23. When the two match totals are equal, the match is a draw.
  R24. There is no table talk.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Play a card to the trick | asked: the leader (first to play) | options: Every card in the leader's hand.
  - Play a card to the trick | asked: a following seat, when led_is_trump is true | options: If the seat holds any joker or trump_suit card, only those cards. Otherwise every card in its hand.
  - Play a card to the trick | asked: a following seat, when led_is_trump is false | options: If the seat holds any card of led_suit, counting only non-joker cards when led_suit is not the trump suit, only those cards. Otherwise every card in its hand.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number > 4 (after 24 tricks)
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each seat's standing is its team's match total: captured card points plus doubled kitty points. Both partners of the team with the higher total win. If the totals are equal, all four seats tie at the top, which is the draw.
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

- each player: `team` (text, visible: public, starts 'A for seats 1 and 3, B for seats 2 and 4'): The seat's partnership.
- each player: `score` (number, visible: public, starts 0): The match total of this seat's team, mirrored onto both partners.
- the table: `kitty_revealed` (list, visible: public, starts []): The kitty, shown after the 6th trick of a hand.
- the table: `hand_number` (number, visible: public, starts 1): The current hand, from 1 to 4.
- the table: `trick_number` (number, visible: public, starts 1): The current trick within the hand, from 1 to 6.
- the table: `trump_suit` (text, visible: public, starts 'S'): The trump suit: S in hands 1 and 3, H in hands 2 and 4.
- the table: `trick_winner` (number, visible: public, starts 0): The seat that won the last trick.
- the table: `team_a_total` (number, visible: public, starts 0): Match total of Team A (seats 1 and 3).
- the table: `team_b_total` (number, visible: public, starts 0): Match total of Team B (seats 2 and 4).
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 26, cards_per_seat = 6, kitty_size = 2, hands = 4, tricks_per_hand = 6, total_rounds = 24, points_five = 5, points_ten = 10, points_king = 10, points_other = 0, points_per_suit = 25, points_in_deck = 100, kitty_multiplier = 2, first_leader_hand_1 = 1, first_leader_hand_2 = 2, first_leader_hand_3 = 2, first_leader_hand_4 = 3, rank_big_joker = 8, rank_small_joker = 7, rank_ace = 6, rank_king = 5, rank_queen = 4, rank_jack = 3, rank_ten = 2, rank_five = 1, trump_strength_base = 200, led_suit_strength_base = 100
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
    "id": "da_bai_fen_duplicate",
    "name": "Da Bai Fen Duplicate",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Two fixed partnerships play 4 hands of 6 tricks with a 26-card deck. Hands 3 and 4 replay hands 1 and 2, rotated one seat."
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
        "key": "team",
        "visible": "public",
        "type": "text",
        "initial": "",
        "values": [
          "",
          "A",
          "B"
        ]
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand1_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand2_cards",
        "visible": "ally",
        "type": "list",
        "initial": []
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
        "initial": [
          "JOKER_BIG",
          "JOKER_SMALL",
          "SA",
          "SK",
          "SQ",
          "SJ",
          "S10",
          "S5",
          "HA",
          "HK",
          "HQ",
          "HJ",
          "H10",
          "H5",
          "CA",
          "CK",
          "CQ",
          "CJ",
          "C10",
          "C5",
          "DA",
          "DK",
          "DQ",
          "DJ",
          "D10",
          "D5"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "kitty",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "kitty_hand1",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "kitty_hand2",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "kitty_revealed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trick_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trump_suit",
        "visible": "public",
        "type": "text",
        "initial": "S"
      },
      {
        "key": "is_replay",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "replay_source",
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
        "key": "led_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "led_is_trump",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "led_suit",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "trick_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "played_this_hand",
        "visible": "public",
        "type": "list",
        "initial": []
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
        "key": "team_a_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "team_b_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 26
      },
      {
        "key": "cards_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "kitty_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "tricks_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "points_five",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "points_ten",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_king",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_other",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_per_suit",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "points_in_deck",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "kitty_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_leader_hand_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_leader_hand_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_leader_hand_3",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_leader_hand_4",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_big_joker",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "rank_small_joker",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "rank_ace",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rank_king",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "rank_queen",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rank_jack",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rank_ten",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "rank_five",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "trump_strength_base",
        "visible": "public",
        "type": "number",
        "initial": 200
      },
      {
        "key": "led_suit_strength_base",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the teams",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "team",
            "value": {
              "calc": "'A' if you.seat % 2 == 1 else 'B'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "JOKER_BIG",
              "JOKER_SMALL",
              "SA",
              "SK",
              "SQ",
              "SJ",
              "S10",
              "S5",
              "HA",
              "HK",
              "HQ",
              "HJ",
              "H10",
              "H5",
              "CA",
              "CK",
              "CQ",
              "CJ",
              "C10",
              "C5",
              "DA",
              "DK",
              "DQ",
              "DJ",
              "D10",
              "D5"
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the starting values",
      "do": [
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "trump_suit",
            "value": "S"
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "first_leader_hand_1"
            }
          }
        },
        {
          "set": {
            "key": "team_a_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "team_b_total",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "the hand begins",
      "when": {
        "calc": "trick_number == 1"
      },
      "do": [
        {
          "set": {
            "key": "played_this_hand",
            "value": []
          }
        },
        {
          "set": {
            "key": "kitty_revealed",
            "value": []
          }
        },
        {
          "set": {
            "key": "trump_suit",
            "value": {
              "calc": "'S' if hand_number in [1, 3] else 'H'"
            }
          }
        },
        {
          "set": {
            "key": "leader",
            "value": {
              "calc": "first_leader_hand_1 if hand_number == 1 else (first_leader_hand_2 if hand_number == 2 else (first_leader_hand_3 if hand_number == 3 else first_leader_hand_4))"
            }
          }
        },
        {
          "set": {
            "key": "is_replay",
            "value": {
              "calc": "hand_number >= 3"
            }
          }
        },
        {
          "set": {
            "key": "replay_source",
            "value": {
              "calc": "hand_number - 2 if hand_number >= 3 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "a fresh deal",
      "when": {
        "calc": "trick_number == 1 and hand_number <= 2"
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
            "key": "deck",
            "value": [
              "JOKER_BIG",
              "JOKER_SMALL",
              "SA",
              "SK",
              "SQ",
              "SJ",
              "S10",
              "S5",
              "HA",
              "HK",
              "HQ",
              "HJ",
              "H10",
              "H5",
              "CA",
              "CK",
              "CQ",
              "CJ",
              "C10",
              "C5",
              "DA",
              "DK",
              "DQ",
              "DJ",
              "D10",
              "D5"
            ]
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
        {"set": {"key": "pick", "value": {"calc": "deck[min(int(uniform(0, len(deck))), len(deck) - 1)]"}}},
        {"append": {"player": 4, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {
          "set": {
            "key": "kitty",
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
        },
        {
          "set": {
            "players": "all",
            "key": "hand1_cards",
            "value": {
              "calc": "you.hand if hand_number == 1 else you.hand1_cards"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand2_cards",
            "value": {
              "calc": "you.hand if hand_number == 2 else you.hand2_cards"
            }
          }
        },
        {
          "set": {
            "key": "kitty_hand1",
            "value": {
              "calc": "kitty if hand_number == 1 else kitty_hand1"
            }
          }
        },
        {
          "set": {
            "key": "kitty_hand2",
            "value": {
              "calc": "kitty if hand_number == 2 else kitty_hand2"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "a replayed deal",
      "when": {
        "calc": "trick_number == 1 and hand_number >= 3"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "players[(you.seat - 2) % 4].hand1_cards if hand_number == 3 else players[(you.seat - 2) % 4].hand2_cards"
            }
          }
        },
        {
          "set": {
            "key": "kitty",
            "value": {
              "calc": "kitty_hand1 if hand_number == 3 else kitty_hand2"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "a new hand",
      "when": {
        "calc": "trick_number == 1 and not is_replay"
      },
      "to": "all",
      "text": "Hand {hand_number} begins. Trump is {trump_suit}. Seat {leader} leads."
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "a replayed hand",
      "when": {
        "calc": "trick_number == 1 and is_replay"
      },
      "to": "all",
      "text": "Hand {hand_number} begins. Trump is {trump_suit}. Seat {leader} leads. This hand is a replay: each seat holds the cards the previous seat held in hand {replay_source}."
    },
    {
      "use": "sync",
      "phase": "play",
      "label": "your cards",
      "mode": "self",
      "to": "all",
      "text": "Your cards and the table:"
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the lead",
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
        "bind": "lead"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} leads {value}."
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
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_this_hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_card",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "led_is_trump",
              "value": {
                "calc": "led_card in ['JOKER_BIG', 'JOKER_SMALL'] or led_card[0:1] == trump_suit"
              }
            }
          },
          {
            "set": {
              "key": "led_suit",
              "value": {
                "calc": "'TRUMP' if led_is_trump else led_card[0:1]"
              }
            }
          },
          {
            "set": {
              "players": "all",
              "key": "offer",
              "value": {
                "calc": "(([c for c in you.hand if c in ['JOKER_BIG', 'JOKER_SMALL'] or c[0:1] == trump_suit]) if len([c for c in you.hand if c in ['JOKER_BIG', 'JOKER_SMALL'] or c[0:1] == trump_suit]) > 0 else you.hand) if led_is_trump else (([c for c in you.hand if c not in ['JOKER_BIG', 'JOKER_SMALL'] and c[0:1] == led_suit]) if len([c for c in you.hand if c not in ['JOKER_BIG', 'JOKER_SMALL'] and c[0:1] == led_suit]) > 0 else you.hand)"
              }
            }
          }
        ]
      },
      "text": "Trick {trick_number} of hand {hand_number}. Trump is {trump_suit}. You lead: play any card from your hand."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the second card",
      "to": {
        "where": "you.seat == leader % 4 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "second"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
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
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_this_hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Trick {trick_number} of hand {hand_number}. Trump is {trump_suit}. Cards so far: {trick_cards}. Play a card; only your legal cards are offered."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the third card",
      "to": {
        "where": "you.seat == (leader + 1) % 4 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "third"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
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
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_this_hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Trick {trick_number} of hand {hand_number}. Trump is {trump_suit}. Cards so far: {trick_cards}. Play a card; only your legal cards are offered."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "the fourth card",
      "to": {
        "where": "you.seat == (leader + 2) % 4 + 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "fourth"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} plays {value}."
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
            "append": {
              "key": "trick_cards",
              "value": "$answer"
            }
          },
          {
            "append": {
              "key": "played_this_hand",
              "value": "$answer"
            }
          },
          {
            "set": {
              "player": "$seat",
              "key": "played_card",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "Trick {trick_number} of hand {hand_number}. Trump is {trump_suit}. Cards so far: {trick_cards}. Play a card; only your legal cards are offered."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the trick is won",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "card_strength",
            "value": {
              "calc": "(trump_strength_base + (rank_big_joker if you.played_card == 'JOKER_BIG' else (rank_small_joker if you.played_card == 'JOKER_SMALL' else (rank_ace if you.played_card[1:] == 'A' else (rank_king if you.played_card[1:] == 'K' else (rank_queen if you.played_card[1:] == 'Q' else (rank_jack if you.played_card[1:] == 'J' else (rank_ten if you.played_card[1:] == '10' else (rank_five if you.played_card[1:] == '5' else 0))))))))) if (you.played_card in ['JOKER_BIG', 'JOKER_SMALL'] or you.played_card[0:1] == trump_suit) else ((led_suit_strength_base + (rank_ace if you.played_card[1:] == 'A' else (rank_king if you.played_card[1:] == 'K' else (rank_queen if you.played_card[1:] == 'Q' else (rank_jack if you.played_card[1:] == 'J' else (rank_ten if you.played_card[1:] == '10' else (rank_five if you.played_card[1:] == '5' else 0))))))) if ((not led_is_trump) and you.played_card[0:1] == led_suit) else 0)"
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
          "set": {
            "key": "trick_points",
            "value": {
              "calc": "sum([points_five if c[1:] == '5' else (points_ten if c[1:] == '10' else (points_king if c[1:] == 'K' else points_other)) for c in trick_cards])"
            }
          }
        },
        {
          "adjust": {
            "key": "team_a_total",
            "value": {
              "calc": "trick_points"
            },
            "if": {
              "calc": "trick_winner in [1, 3]"
            }
          }
        },
        {
          "adjust": {
            "key": "team_b_total",
            "value": {
              "calc": "trick_points"
            },
            "if": {
              "calc": "trick_winner in [2, 4]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "team_a_total if you.team == 'A' else team_b_total"
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
      "phase": "score",
      "label": "the trick result",
      "to": "all",
      "text": "Trick {trick_number} of hand {hand_number}: cards {trick_cards}. Seat {trick_winner} wins {trick_points} points. Team A {team_a_total}, Team B {team_b_total}."
    },
    {
      "use": "update",
      "phase": "score",
      "label": "the kitty",
      "when": {
        "calc": "trick_number == tricks_per_hand"
      },
      "do": [
        {
          "set": {
            "key": "kitty_revealed",
            "value": {
              "calc": "kitty"
            }
          }
        },
        {
          "adjust": {
            "key": "team_a_total",
            "value": {
              "calc": "kitty_multiplier * sum([points_five if c[1:] == '5' else (points_ten if c[1:] == '10' else (points_king if c[1:] == 'K' else points_other)) for c in kitty])"
            },
            "if": {
              "calc": "trick_winner in [1, 3]"
            }
          }
        },
        {
          "adjust": {
            "key": "team_b_total",
            "value": {
              "calc": "kitty_multiplier * sum([points_five if c[1:] == '5' else (points_ten if c[1:] == '10' else (points_king if c[1:] == 'K' else points_other)) for c in kitty])"
            },
            "if": {
              "calc": "trick_winner in [2, 4]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "team_a_total if you.team == 'A' else team_b_total"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "the end of the hand",
      "when": {
        "calc": "trick_number == tricks_per_hand"
      },
      "to": "all",
      "text": "End of hand {hand_number}. Kitty: {kitty_revealed}, doubled for the team of seat {trick_winner}. Team A {team_a_total}, Team B {team_b_total}."
    },
    {
      "use": "update",
      "phase": "score",
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
            "key": "led_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "played_card",
            "value": ""
          }
        },
        {
          "adjust": {
            "key": "trick_number",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1,
            "if": {
              "calc": "trick_number > tricks_per_hand"
            }
          }
        },
        {
          "set": {
            "key": "trick_number",
            "value": 1,
            "if": {
              "calc": "trick_number > tricks_per_hand"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last hand",
      "when": {
        "calc": "hand_number > hands"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number > hands"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final totals: Team A (seats 1 and 3) {team_a_total}, Team B (seats 2 and 4) {team_b_total}."
    }
  },
  "limits": {
    "rounds": 24,
    "rounds_max": 24,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Four players in two fixed partnerships. Seats are numbered 1, 2, 3, 4 in anticlockwise order. Team A is seats 1 and 3; Team B is seats 2 and 4. Play always proceeds anticlockwise: after seat 1 comes 2, then 3, then 4, then 1.\n\nCARDS: The deck has {deck_size} cards: the Big Joker (JOKER_BIG), the Small Joker (JOKER_SMALL), and four suits (Spades S, Hearts H, Clubs C, Diamonds D) each containing A, K, Q, J, 10, 5 (a card is written suit then rank, e.g. S10, HK). A 5 is worth {points_five} points, a 10 is worth {points_ten}, a K is worth {points_king}, and all other cards {points_other}. Each suit holds {points_per_suit} points, so the deck holds {points_in_deck}.\n\nTRUMPS: Hands 1 and 3 have Spades as trump; hands 2 and 4 have Hearts as trump. The trumps are, from high to low: Big Joker, Small Joker, then A, K, Q, J, 10, 5 of the trump suit. Both jokers belong to the trump suit for following purposes. In every non-trump suit the order is A, K, Q, J, 10, 5.\n\nTHE MATCH has {hands} hands of {tricks_per_hand} tricks each, {total_rounds} rounds in total. Each round is one trick.\n\nDEALING: At the start of hand 1 the cards are shuffled at random. Each seat receives {cards_per_seat} cards, private to that seat, and the remaining {kitty_size} cards form the kitty, face down and seen by no one. Hand 2 is a new random shuffle, dealt the same way. Hand 3 replays hand 1: every seat receives the exact cards held in hand 1 by the seat before it in seat order (seat 2 gets seat 1's hand 1 cards, seat 3 gets seat 2's, seat 4 gets seat 3's, seat 1 gets seat 4's), and the kitty is the same 2 cards. Hand 4 replays hand 2 in the same rotated way. Players are told when a hand is a replay.\n\nFIRST LEADER of each hand: seat {first_leader_hand_1} in hand 1, seat {first_leader_hand_2} in hand 2, seat {first_leader_hand_3} in hand 3, seat {first_leader_hand_4} in hand 4. In each replay, the first leader holds the same cards as the first leader of the original hand.\n\nA TRICK: The leader plays any one card from their hand face up. Then the other three seats, in anticlockwise order, each play one card, seeing all cards already played to the trick. Following: if the led card is a trump (a joker or a trump-suit card), a player holding a trump must play a trump and is offered only their trumps; a player holding no trump may play any card. If the led card is a non-trump suit, a player holding that suit must play it and is offered only cards of that suit; a player holding none of it may play any card. You are only ever offered legal cards. Winning: if any trump was played, the highest trump wins the trick. Otherwise the highest card of the led suit wins. Off-suit non-trump cards never win.\n\nAFTER EACH TRICK: All four cards are announced along with the winner. The winner's team adds the point value of the four cards to its match total. The winner leads the next trick of the same hand.\n\nEND OF HAND: After the 6th trick the kitty is revealed. Its point value multiplied by {kitty_multiplier} is added to the match total of the team that won the 6th trick. The next hand begins with its own deal and first leader.\n\nINFORMATION: You always see your own cards, all cards played so far in the hand, both teams' match totals, the trump suit, the trick number and the hand number. Other players' hands and the kitty stay hidden until the kitty is revealed at the end of the hand. There is no table talk.\n\nWINNING: After hand 4, the team with the higher match total (captured card points plus doubled kitty points) wins; both partners win. If the totals are equal, the match is a draw and all four seats share it."
}
```
````
