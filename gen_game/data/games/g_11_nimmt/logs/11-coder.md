# 11 coder

- time: 2026-10-27T21:31:39+00:00 (126.9s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 30dd2f1129480d32, reply sha256 af33aee660042a79

## Sent

````
# Task: write the XColos game file for "Eleven Takes: Three Piles"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
1. Use a deck of cards numbered 1 to 40.
2. Ox-heads per card: 3 if the number is a multiple of 10; 2 if it is a multiple of 5 but not of 10; 1 otherwise. The whole deck holds 52 ox-heads.
3. Shuffle once. This is the only random event in the game. Deal 6 cards face down to each player as a private hand. Turn 3 cards face up to start Pile A, Pile B and Pile C, one card each. The remaining cards (13 with 4 players, 19 with 3) are set aside unseen for the rest of the game.
4. Place a supply of bull tokens equal to the number of players minus 1 (3 with 4 players, 2 with 3 players).
5. Seats are numbered 1 to N. Seat 1 moves first, and play proceeds in seat order.

WHAT IS PUBLIC
- The full ordered contents of every pile.
- Each player's hand size and bull count.
- Every action taken.
Only the contents of hands and the set-aside cards are hidden.

LEGAL PLAY
6. A card c may be played on a pile whose top card is t if (c - t) mod 40 is between 1 and 6. Examples: on 12 you may play 13 to 18; on 37 you may play 38, 39, 40, 1, 2 or 3.

A TURN (one engine round)
7. The active player privately chooses one action:
   (a) PLAY card X onto pile P, where X is in their hand and legal on P; or
   (b) TAKE pile P.
   A player may take even when a legal play exists. If the chosen action is illegal, or the player has no legal play and chose PLAY, they instead TAKE the smallest pile (ties: A before B before C).
8. If the player PLAYED: card X goes on top of pile P. If they hold at least 1 bull, they may then add one more card legal on the new top of the same pile. If they hold 2 or more bulls, they may add a second extra card the same way. They may stop at any point. An illegal extra card is ignored and ends the run. Bulls are not spent by using them.
9. If the player TOOK pile P:
   - All cards of P go into their hand.
   - They must then choose any one card from their hand to place face up as the single card of the restarted pile P.
   - If P held 3 or more cards before it was taken, the player gains a bull from the supply. If the supply is empty, they instead take one bull from the opponent holding the most bulls; ties go to the first such player in seat order after the taker. If no opponent has a bull, nothing happens.
10. If the active player's hand is now empty, the game will end at the end of the current cycle, that is, after the player in seat N has finished their turn. Every player therefore gets the same number of turns.
11. Pass the turn to the next seat.

END OF GAME
12. The game ends at the end of the cycle in which any player emptied their hand. It also ends after 10 full cycles (40 turns with 4 players) or 12 full cycles (36 turns with 3 players), whichever comes first.
13. Each player's penalty is the total ox-heads of the cards in their hand. A player with an empty hand scores 0.

How the winner is decided: The player with the lowest penalty wins. If two or more players tie for lowest, the game is a draw among them (an engine draw).

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Eleven Takes: Three Piles (3 to 4 players, best with 4)

Players play cards from hidden hands onto three shared piles in a clockwise number range, or take a pile into their hand and earn bulls that allow extra plays; the lowest ox-head penalty in hand wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The cards (numbers 1-40) in this player's private hand.
  - each player: hand_size (number, starts 6); everyone sees it. The number of cards in hand. It is public by the rules and kept equal to the length of hand.
  - each player: bulls (number, starts 0); everyone sees it. Bull tokens held. Each one allows one extra card after a play, up to 2 extras. Bulls are never spent.
  - each player: penalty (number, starts 0); everyone sees it. Total ox-heads of the cards in hand. It is computed when the game ends, and 0 for an empty hand.
  - the table: set_aside (list, starts []); hidden from all players. The cards left over after the deal, set aside unseen for the whole game: 13 with 4 players, 19 with 3.
  - the table: pile_a (list, starts []); everyone sees it. Ordered contents of Pile A. The last element is the top card.
  - the table: pile_b (list, starts []); everyone sees it. Ordered contents of Pile B. The last element is the top card.
  - the table: pile_c (list, starts []); everyone sees it. Ordered contents of Pile C. The last element is the top card.
  - the table: bull_supply (number, starts 0); everyone sees it. Bull tokens left in the supply. It starts at the number of players minus 1.
  - the table: active_seat (number, starts 1); everyone sees it. The seat whose turn it is.
  - the table: cycle (number, starts 0); everyone sees it. The number of full cycles completed, where one cycle is a turn for every seat.
  - the table: max_cycles (number, starts 10); everyone sees it. The cycle limit, 18 - 2*N: 10 with 4 players, 12 with 3.
  - the table: ending_triggered (bool, starts False); everyone sees it. True once any player has emptied their hand. The game then ends after seat N's turn.
  - the table: last_action (text, starts ''); everyone sees it. A public record of the active player's action this turn: the card played and the pile, or the pile taken and the restart card.
  - the table: chosen_pile (text, starts ''); everyone sees it. The pile (A, B or C) named in this turn's action.
  - the table: action_kind (text, starts ''); everyone sees it. Either 'play' or 'take' for the current turn.
  - the table: taken_size (number, starts 0); everyone sees it. How many cards the taken pile held before it was taken.
  - the table: extra_stopped (bool, starts False); everyone sees it. True once the active player stops adding extra cards this turn, or an extra card ends the run.
  - parameters, each kept as a table attribute: deck_low = 1, deck_high = 40, deck_size = 40, oxheads_multiple_of_10 = 3, oxheads_multiple_of_5_not_10 = 2, oxheads_other = 1, deck_total_oxheads = 52, hand_size_start = 6, pile_count = 3, start_cards_per_pile = 1, set_aside_with_4 = 13, set_aside_with_3 = 19, bull_supply_offset = 1, legal_step_min = 1, legal_step_max = 6, legal_modulus = 40, take_bull_threshold = 3, bulls_for_first_extra = 1, bulls_for_second_extra = 2, max_cycles_with_4 = 10, max_cycles_with_3 = 12, max_turns_with_4 = 40, max_turns_with_3 = 36, empty_hand_penalty = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the deck as the numbers 1 to 40. A card's ox-heads are 3 if it is a multiple of 10, 2 if it is a multiple of 5 but not of 10, and 1 otherwise, for 52 ox-heads in total.
  2. Shuffle once, using the seeded random draw. This is the only random event in the game.
  3. Deal 6 cards to each player's hand by drawing at random from the deck. Set each hand_size to 6.
  4. Draw one card each to form pile_a, pile_b and pile_c, face up, so each pile is a public one-card list.
  5. Put the remaining cards in set_aside, hidden from everyone (13 with 4 players, 19 with 3). They are never used again.
  6. Set bull_supply to N - 1 and max_cycles to 18 - 2*N. Set active_seat to 1, cycle to 0 and ending_triggered to false.
  7. Seats are numbered 1 to N. Seat 1 moves first and play proceeds in seat order.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [sync] all players. What happens: Each player sees their own hand, and everyone sees the piles, every hand_size, bulls, bull_supply, cycle and last_action.
  2. [ask] the seat equal to active_seat answers: One choice from: 'play X on P' for every card X in hand that is legal on pile P (that is, (X - top(P)) mod 40 is between 1 and 6), plus 'take A', 'take B' and 'take C'.. What happens: Sets action_kind to 'play' or 'take' and sets chosen_pile. A missing or invalid answer is replaced by taking the smallest pile, with ties broken A before B before C. Clears extra_stopped.
  3. [update] the seat equal to active_seat. What happens: When action_kind is 'play': remove X from hand, append X to the chosen pile, subtract 1 from hand_size, and set last_action to 'Seat s plays X on P'.
  4. [ask] the seat equal to active_seat, when action_kind is 'play' and bulls >= 1 answers: Either 'stop', or one card in hand that is legal on the new top of the chosen pile.. What happens: If 'stop', set extra_stopped to true. Otherwise remove the card from hand, append it to the chosen pile, subtract 1 from hand_size, and add it to last_action.
  5. [ask] the seat equal to active_seat, when action_kind is 'play', bulls >= 2 and extra_stopped is false answers: Either 'stop', or one card in hand that is legal on the new top of the chosen pile.. What happens: If a card is given, remove it from hand, append it to the chosen pile, subtract 1 from hand_size, and add it to last_action.
  6. [update] the seat equal to active_seat. What happens: When action_kind is 'take': set taken_size to the length of the chosen pile, append all of its cards to hand, set the pile to empty, and add taken_size to hand_size.
  7. [ask] the seat equal to active_seat, when action_kind is 'take' answers: One card from the player's hand.. What happens: Remove that card from hand, set the chosen pile to a list holding only that card, subtract 1 from hand_size, and set last_action to 'Seat s takes P (k cards) and restarts it with Y'.
  8. [update] the seat equal to active_seat. What happens: When action_kind is 'take' and taken_size >= 3: if bull_supply > 0, subtract 1 from bull_supply and add 1 to the taker's bulls. Otherwise, if any opponent has bulls > 0, take 1 bull from the opponent with the most bulls, breaking ties by the smallest (seat - active_seat) mod N, and add it to the taker's bulls. If no opponent has a bull, nothing happens.
  9. [update] the seat equal to active_seat. What happens: If the active player's hand_size = 0, set ending_triggered to true.
  10. [update] all players. What happens: If active_seat = N, add 1 to cycle and set active_seat to 1. Otherwise add 1 to active_seat.
  11. [update] all players. What happens: When active_seat = 1 and (ending_triggered is true or cycle >= max_cycles): set every player's penalty to the sum, over the cards in their hand, of 3 for a multiple of 10, 2 for a multiple of 5 that is not a multiple of 10, and 1 otherwise. An empty hand gives 0.
  12. [check] all players. What happens: End the game if active_seat = 1 and (ending_triggered is true or cycle >= max_cycles). Otherwise continue with the next turn.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck is the numbers 1 to 40, each player's hand holds 6 cards, pile_a, pile_b and pile_c hold 1 card each, and set_aside holds the remaining 13 cards with 4 players or 19 with 3.
  R2. When ox-heads are counted, a multiple of 10 is worth 3, a multiple of 5 that is not a multiple of 10 is worth 2, and any other card is worth 1, so the deck totals 52.
  R3. When the game starts, bull_supply is N - 1: 3 with 4 players and 2 with 3.
  R4. When a card c is played on a pile with top card t, the play is legal only if (c - t) mod 40 is between 1 and 6. For example, on 12 the cards 13 to 18 are legal, and on 37 the cards 38, 39, 40, 1, 2 and 3 are legal.
  R5. When the active player chooses 'play X on P', X is removed from their hand, appended to the top of pile P, and their hand_size drops by 1.
  R6. When the active player has played and holds at least 1 bull, they may add one more card legal on the new top of the same pile, or stop.
  R7. When the active player has played, holds 2 or more bulls and did not stop after the first extra card, they may add a second extra card legal on the new top of the same pile, or stop.
  R8. When a player uses bulls to add extra cards, their bulls count is unchanged.
  R9. When the active player chooses 'take P', every card of pile P is added to their hand and hand_size rises by the pile's size.
  R10. When a player has taken pile P, they must choose one card from their hand to become the only card of pile P, and hand_size drops by 1.
  R11. When the taken pile held 3 or more cards and bull_supply > 0, bull_supply drops by 1 and the taker's bulls rise by 1.
  R12. When the taken pile held 3 or more cards and bull_supply = 0, the taker takes 1 bull from the opponent with the most bulls, ties going to the first such opponent in seat order after the taker. If no opponent has a bull, nothing changes.
  R13. When the taken pile held 2 or fewer cards, no bull changes hands.
  R14. When the active player gives no valid answer to the action question, they take the smallest pile, with ties broken A before B before C.
  R15. When a player may take, they may do so even if a legal play exists.
  R16. When a player's hand_size reaches 0 on their turn, ending_triggered becomes true and the game ends after seat N's turn in that cycle, so every player has the same number of turns.
  R17. When 10 full cycles have been played with 4 players (40 turns), or 12 with 3 players (36 turns), the game ends.
  R18. When the game ends, each player's penalty is the total ox-heads in their hand, and a player with an empty hand has penalty 0.
  R19. When the game ends, the player with the lowest penalty wins, and players tied for the lowest share a draw.
  R20. When any action is taken, last_action records it publicly, and pile contents, hand_size and bulls are always public, while hands and set_aside stay hidden.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Main action on your turn | asked: the seat equal to active_seat | options: Every 'play X on P' where X is in that seat's hand and (X - top of P) mod 40 is between 1 and 6, for P in A, B and C, plus 'take A', 'take B' and 'take C' always. A seat with no legal play is offered only the three take options.
  - First extra card after a play | asked: the active seat, only if it played and holds 1 or more bulls | options: 'stop', plus every card in hand that is legal on the new top of the pile just played on. If no card is legal, only 'stop' is offered.
  - Second extra card after a play | asked: the active seat, only if it played, holds 2 or more bulls and did not stop at the first extra | options: 'stop', plus every card in hand that is legal on the new top of the same pile. If no card is legal, only 'stop' is offered.
  - Restart card for the taken pile | asked: the active seat, only after a take | options: Every card currently in that seat's hand, including the cards just taken.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: active_seat = 1 and (ending_triggered = true or cycle >= max_cycles)
  - each player's standing: 0 - you.penalty (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is minus their penalty, the total ox-heads in their hand at the end. The lowest penalty wins, and players tied for the lowest share the win as a draw.
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

- each player: `hand_size` (number, visible: public, starts 6): The number of cards in hand. It is public by the rules and kept equal to the length of hand.
- each player: `bulls` (number, visible: public, starts 0): Bull tokens held. Each one allows one extra card after a play, up to 2 extras. Bulls are never spent.
- each player: `penalty` (number, visible: public, starts 0): Total ox-heads of the cards in hand. It is computed when the game ends, and 0 for an empty hand.
- the table: `pile_a` (list, visible: public, starts []): Ordered contents of Pile A. The last element is the top card.
- the table: `pile_b` (list, visible: public, starts []): Ordered contents of Pile B. The last element is the top card.
- the table: `pile_c` (list, visible: public, starts []): Ordered contents of Pile C. The last element is the top card.
- the table: `bull_supply` (number, visible: public, starts 0): Bull tokens left in the supply. It starts at the number of players minus 1.
- the table: `cycle` (number, visible: public, starts 0): The number of full cycles completed, where one cycle is a turn for every seat.
- the table: `ending_triggered` (bool, visible: public, starts False): True once any player has emptied their hand. The game then ends after seat N's turn.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_low = 1, deck_high = 40, deck_size = 40, oxheads_multiple_of_10 = 3, oxheads_multiple_of_5_not_10 = 2, oxheads_other = 1, deck_total_oxheads = 52, hand_size_start = 6, pile_count = 3, start_cards_per_pile = 1, set_aside_with_4 = 13, set_aside_with_3 = 19, bull_supply_offset = 1, legal_step_min = 1, legal_step_max = 6, legal_modulus = 40, take_bull_threshold = 3, bulls_for_first_extra = 1, bulls_for_second_extra = 2, max_cycles_with_4 = 10, max_cycles_with_3 = 12, max_turns_with_4 = 40, max_turns_with_3 = 36, empty_hand_penalty = 0
- the game ends with ONE ending whose `rank_by` is `0 - you.penalty`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Set `ending_triggered` to true only in the step that runs after an action leaves the active player's hand empty (hand_size == 0). Do not set it when the cycle limit is reached. Handle the 10/12-cycle limit through a separate end condition: compare `cycle` with `max_cycles`, which is derived from max_cycles_with_4 / max_cycles_with_3, either in the ending's own condition or in a separate internal flag such as `cycle_limit_reached`. The game should end when `ending_triggered` is true at the end of seat N's turn, or when `cycle` >= `max_cycles`. Check that `cycle` increments exactly once after seat N's turn. Keep the final penalty computation as it is, with empty_hand_penalty for an empty hand and the ox-head sum otherwise.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "eleven_takes_three_piles",
    "name": "Eleven Takes: Three Piles",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Play cards from a hidden hand onto three shared piles, or take a pile and earn bulls; the lowest ox-head penalty in hand wins."
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
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bulls",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "penalty",
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
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_a",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_b",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_c",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "bull_supply",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cycle",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_cycles",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "ending_triggered",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "chosen_pile",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "action_kind",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "taken_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "extra_stopped",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_low",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_high",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "oxheads_multiple_of_10",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "oxheads_multiple_of_5_not_10",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "oxheads_other",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_total_oxheads",
        "visible": "public",
        "type": "number",
        "initial": 52
      },
      {
        "key": "hand_size_start",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "pile_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "start_cards_per_pile",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside_with_4",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "set_aside_with_3",
        "visible": "public",
        "type": "number",
        "initial": 19
      },
      {
        "key": "bull_supply_offset",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "legal_step_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "legal_step_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "legal_modulus",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "take_bull_threshold",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bulls_for_first_extra",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "bulls_for_second_extra",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_cycles_with_4",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_cycles_with_3",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "max_turns_with_4",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "max_turns_with_3",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "empty_hand_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
      },
      {
        "key": "card_labels",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_oxheads",
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
        "key": "chosen_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "extra_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "restart_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bull_from",
        "visible": "none",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in cards if c >= deck_low and c <= deck_high]"
            }
          }
        },
        {
          "set": {
            "key": "deck_oxheads",
            "value": {
              "calc": "sum([oxheads_multiple_of_10 if c % 10 == 0 else (oxheads_multiple_of_5_not_10 if c % 5 == 0 else oxheads_other) for c in deck])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle and deal the hands",
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
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "start the three piles",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pile_a", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pile_b", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pile_c", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "The piles start: A {pile_a}, B {pile_b}, C {pile_c}."
    },
    {
      "use": "update",
      "label": "set aside the rest",
      "do": [
        {
          "set": {
            "key": "set_aside",
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
        }
      ]
    },
    {
      "use": "update",
      "label": "the supply and the turn order",
      "do": [
        {
          "set": {
            "key": "bull_supply",
            "value": {
              "calc": "len(players) - bull_supply_offset"
            }
          }
        },
        {
          "set": {
            "key": "max_cycles",
            "value": {
              "calc": "max_cycles_with_4 if len(players) >= 4 else max_cycles_with_3"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        },
        {
          "set": {
            "key": "cycle",
            "value": 0
          }
        },
        {
          "set": {
            "key": "ending_triggered",
            "value": false
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
      "use": "sync",
      "phase": "turn",
      "label": "the state",
      "mode": "self",
      "to": "all",
      "text": "Seat {active_seat} is to move. Where things stand:"
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "build the action offer",
      "do": [
        {"set": {"key": "extra_stopped", "value": false}},
        {"set": {"key": "action_kind", "value": ""}},
        {"set": {"key": "chosen_pile", "value": ""}},
        {"set": {"key": "taken_size", "value": 0}},
        {"set": {"key": "chosen_card", "value": 0}},
        {"set": {"key": "extra_card", "value": 0}},
        {"set": {"key": "restart_card", "value": 0}},
        {"set": {"key": "bull_from", "value": 0}},
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['play ' + card_labels[c - 1] + ' on A' for c in you.hand if (c - pile_a[len(pile_a) - 1]) % legal_modulus >= legal_step_min and (c - pile_a[len(pile_a) - 1]) % legal_modulus <= legal_step_max] + ['play ' + card_labels[c - 1] + ' on B' for c in you.hand if (c - pile_b[len(pile_b) - 1]) % legal_modulus >= legal_step_min and (c - pile_b[len(pile_b) - 1]) % legal_modulus <= legal_step_max] + ['play ' + card_labels[c - 1] + ' on C' for c in you.hand if (c - pile_c[len(pile_c) - 1]) % legal_modulus >= legal_step_min and (c - pile_c[len(pile_c) - 1]) % legal_modulus <= legal_step_max] + ['take A', 'take B', 'take C']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "main action",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "main"
      },
      "text": "Your turn. Piles: A {pile_a}, B {pile_b}, C {pile_c} (last card is the top). Your hand: {hand}. Play a legal card onto a pile, or take a pile."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "read the action",
      "do": [
        {
          "set": {
            "key": "chosen_card",
            "value": {
              "calc": "max([c for c in cards if $main == 'play ' + card_labels[c - 1] + ' on A' or $main == 'play ' + card_labels[c - 1] + ' on B' or $main == 'play ' + card_labels[c - 1] + ' on C'] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "chosen_pile",
            "value": {
              "calc": "'A' if ($main == 'take A' or any([$main == 'play ' + card_labels[c - 1] + ' on A' for c in cards])) else ('B' if ($main == 'take B' or any([$main == 'play ' + card_labels[c - 1] + ' on B' for c in cards])) else ('C' if ($main == 'take C' or any([$main == 'play ' + card_labels[c - 1] + ' on C' for c in cards])) else ('A' if len(pile_a) <= len(pile_b) and len(pile_a) <= len(pile_c) else ('B' if len(pile_b) <= len(pile_c) else 'C'))))"
            }
          }
        },
        {
          "set": {
            "key": "action_kind",
            "value": {
              "calc": "'play' if chosen_card > 0 else 'take'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the play",
      "when": {
        "calc": "action_kind == 'play'"
      },
      "do": [
        {
          "remove": {
            "players": {"where": "you.seat == active_seat"},
            "key": "hand",
            "value": {"calc": "chosen_card"}
          }
        },
        {
          "adjust": {
            "players": {"where": "you.seat == active_seat"},
            "key": "hand_size",
            "value": -1
          }
        },
        {"append": {"key": "pile_a", "value": {"calc": "chosen_card"}, "if": {"calc": "chosen_pile == 'A'"}}},
        {"append": {"key": "pile_b", "value": {"calc": "chosen_card"}, "if": {"calc": "chosen_pile == 'B'"}}},
        {"append": {"key": "pile_c", "value": {"calc": "chosen_card"}, "if": {"calc": "chosen_pile == 'C'"}}},
        {
          "set": {
            "key": "last_action",
            "value": {
              "calc": "'Seat ' + card_labels[active_seat - 1] + ' plays ' + card_labels[chosen_card - 1] + ' on ' + chosen_pile"
            }
          }
        },
        {
          "set": {
            "players": {"where": "you.seat == active_seat"},
            "key": "offer",
            "value": {
              "calc": "['stop'] + [card_labels[c - 1] for c in you.hand if (c - (pile_a[len(pile_a) - 1] if chosen_pile == 'A' else (pile_b[len(pile_b) - 1] if chosen_pile == 'B' else pile_c[len(pile_c) - 1]))) % legal_modulus >= legal_step_min and (c - (pile_a[len(pile_a) - 1] if chosen_pile == 'A' else (pile_b[len(pile_b) - 1] if chosen_pile == 'B' else pile_c[len(pile_c) - 1]))) % legal_modulus <= legal_step_max]"
            }
          }
        }
      ],
      "text": "{last_action}."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "first extra card",
      "when": {
        "calc": "action_kind == 'play' and max([p.bulls for p in players if p.seat == active_seat] + [0]) >= bulls_for_first_extra"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "x1"
      },
      "text": "Your bull lets you add one more card legal on the new top of pile {chosen_pile}, or stop. Piles: A {pile_a}, B {pile_b}, C {pile_c}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "apply the first extra card",
      "when": {
        "calc": "action_kind == 'play' and max([p.bulls for p in players if p.seat == active_seat] + [0]) >= bulls_for_first_extra"
      },
      "do": [
        {
          "set": {
            "key": "extra_card",
            "value": {
              "calc": "max([c for c in cards if card_labels[c - 1] == $x1] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "extra_stopped",
            "value": {
              "calc": "extra_card == 0"
            }
          }
        },
        {
          "remove": {
            "players": {"where": "you.seat == active_seat"},
            "key": "hand",
            "value": {"calc": "extra_card"},
            "if": {"calc": "extra_card > 0"}
          }
        },
        {
          "adjust": {
            "players": {"where": "you.seat == active_seat"},
            "key": "hand_size",
            "value": -1,
            "if": {"calc": "extra_card > 0"}
          }
        },
        {"append": {"key": "pile_a", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'A'"}}},
        {"append": {"key": "pile_b", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'B'"}}},
        {"append": {"key": "pile_c", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'C'"}}},
        {
          "set": {
            "key": "last_action",
            "value": {"calc": "last_action + ', then ' + card_labels[extra_card - 1]"},
            "if": {"calc": "extra_card > 0"}
          }
        },
        {
          "set": 
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Your turn. Piles: A [20], B [16], C [27] (last card is the top). Your hand: {hand}. Play a'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Your turn. Piles: A [20], B [16], C [27, 33] (last card is the top). Your hand: {hand}. Pl'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'You took pile B. Your hand: {hand}. Choose one card from your hand to place face up as the'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "eleven_takes_three_piles",
    "name": "Eleven Takes: Three Piles",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Play cards from a hidden hand onto three shared piles, or take a pile and earn bulls; the lowest ox-head penalty in hand wins."
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
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bulls",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "penalty",
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
        "key": "set_aside",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_a",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_b",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "pile_c",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "bull_supply",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cycle",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_cycles",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "ending_triggered",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "chosen_pile",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "action_kind",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "taken_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "extra_stopped",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "deck_low",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_high",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "oxheads_multiple_of_10",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "oxheads_multiple_of_5_not_10",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "oxheads_other",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_total_oxheads",
        "visible": "public",
        "type": "number",
        "initial": 52
      },
      {
        "key": "hand_size_start",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "pile_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "start_cards_per_pile",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "set_aside_with_4",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "set_aside_with_3",
        "visible": "public",
        "type": "number",
        "initial": 19
      },
      {
        "key": "bull_supply_offset",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "legal_step_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "legal_step_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "legal_modulus",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "take_bull_threshold",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bulls_for_first_extra",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "bulls_for_second_extra",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_cycles_with_4",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_cycles_with_3",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "max_turns_with_4",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "max_turns_with_3",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "empty_hand_penalty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
      },
      {
        "key": "card_labels",
        "visible": "none",
        "type": "list",
        "initial": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]
      },
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_oxheads",
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
        "key": "chosen_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "extra_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "restart_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bull_from",
        "visible": "none",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[c for c in cards if c >= deck_low and c <= deck_high]"
            }
          }
        },
        {
          "set": {
            "key": "deck_oxheads",
            "value": {
              "calc": "sum([oxheads_multiple_of_10 if c % 10 == 0 else (oxheads_multiple_of_5_not_10 if c % 5 == 0 else oxheads_other) for c in deck])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle and deal the hands",
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
        {"append": {"player": 3, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"players": {"where": "you.seat == 4"}, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "start the three piles",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pile_a", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pile_b", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "pile_c", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}}
      ],
      "text": "The piles start: A {pile_a}, B {pile_b}, C {pile_c}."
    },
    {
      "use": "update",
      "label": "set aside the rest",
      "do": [
        {
          "set": {
            "key": "set_aside",
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
        }
      ]
    },
    {
      "use": "update",
      "label": "the supply and the turn order",
      "do": [
        {
          "set": {
            "key": "bull_supply",
            "value": {
              "calc": "len(players) - bull_supply_offset"
            }
          }
        },
        {
          "set": {
            "key": "max_cycles",
            "value": {
              "calc": "max_cycles_with_4 if len(players) >= 4 else max_cycles_with_3"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        },
        {
          "set": {
            "key": "cycle",
            "value": 0
          }
        },
        {
          "set": {
            "key": "ending_triggered",
            "value": false
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
      "use": "sync",
      "phase": "turn",
      "label": "the state",
      "mode": "self",
      "to": "all",
      "text": "Seat {active_seat} is to move. Where things stand:"
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "build the action offer",
      "do": [
        {"set": {"key": "extra_stopped", "value": false}},
        {"set": {"key": "action_kind", "value": ""}},
        {"set": {"key": "chosen_pile", "value": ""}},
        {"set": {"key": "taken_size", "value": 0}},
        {"set": {"key": "chosen_card", "value": 0}},
        {"set": {"key": "extra_card", "value": 0}},
        {"set": {"key": "restart_card", "value": 0}},
        {"set": {"key": "bull_from", "value": 0}},
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['play ' + card_labels[c - 1] + ' on A' for c in you.hand if (c - pile_a[len(pile_a) - 1]) % legal_modulus >= legal_step_min and (c - pile_a[len(pile_a) - 1]) % legal_modulus <= legal_step_max] + ['play ' + card_labels[c - 1] + ' on B' for c in you.hand if (c - pile_b[len(pile_b) - 1]) % legal_modulus >= legal_step_min and (c - pile_b[len(pile_b) - 1]) % legal_modulus <= legal_step_max] + ['play ' + card_labels[c - 1] + ' on C' for c in you.hand if (c - pile_c[len(pile_c) - 1]) % legal_modulus >= legal_step_min and (c - pile_c[len(pile_c) - 1]) % legal_modulus <= legal_step_max] + ['take A', 'take B', 'take C']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "main action",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "main"
      },
      "text": "Your turn. Piles: A {pile_a}, B {pile_b}, C {pile_c} (the last card is the top). Your hand is shown in your state. Play a legal card onto a pile, or take a pile."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "read the action",
      "do": [
        {
          "set": {
            "key": "chosen_card",
            "value": {
              "calc": "max([c for c in cards if $main == 'play ' + card_labels[c - 1] + ' on A' or $main == 'play ' + card_labels[c - 1] + ' on B' or $main == 'play ' + card_labels[c - 1] + ' on C'] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "chosen_pile",
            "value": {
              "calc": "'A' if ($main == 'take A' or any([$main == 'play ' + card_labels[c - 1] + ' on A' for c in cards])) else ('B' if ($main == 'take B' or any([$main == 'play ' + card_labels[c - 1] + ' on B' for c in cards])) else ('C' if ($main == 'take C' or any([$main == 'play ' + card_labels[c - 1] + ' on C' for c in cards])) else ('A' if len(pile_a) <= len(pile_b) and len(pile_a) <= len(pile_c) else ('B' if len(pile_b) <= len(pile_c) else 'C'))))"
            }
          }
        },
        {
          "set": {
            "key": "action_kind",
            "value": {
              "calc": "'play' if chosen_card > 0 else 'take'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the play",
      "when": {
        "calc": "action_kind == 'play'"
      },
      "do": [
        {
          "remove": {
            "player": {"calc": "active_seat"},
            "key": "hand",
            "value": {"calc": "chosen_card"}
          }
        },
        {
          "adjust": {
            "player": {"calc": "active_seat"},
            "key": "hand_size",
            "value": -1
          }
        },
        {"append": {"key": "pile_a", "value": {"calc": "chosen_card"}, "if": {"calc": "chosen_pile == 'A'"}}},
        {"append": {"key": "pile_b", "value": {"calc": "chosen_card"}, "if": {"calc": "chosen_pile == 'B'"}}},
        {"append": {"key": "pile_c", "value": {"calc": "chosen_card"}, "if": {"calc": "chosen_pile == 'C'"}}},
        {
          "set": {
            "key": "last_action",
            "value": {
              "calc": "'Seat ' + card_labels[active_seat - 1] + ' plays ' + card_labels[chosen_card - 1] + ' on ' + chosen_pile"
            }
          }
        },
        {
          "set": {
            "players": {"where": "you.seat == active_seat"},
            "key": "offer",
            "value": {
              "calc": "['stop'] + [card_labels[c - 1] for c in you.hand if (c - (pile_a[len(pile_a) - 1] if chosen_pile == 'A' else (pile_b[len(pile_b) - 1] if chosen_pile == 'B' else pile_c[len(pile_c) - 1]))) % legal_modulus >= legal_step_min and (c - (pile_a[len(pile_a) - 1] if chosen_pile == 'A' else (pile_b[len(pile_b) - 1] if chosen_pile == 'B' else pile_c[len(pile_c) - 1]))) % legal_modulus <= legal_step_max]"
            }
          }
        }
      ],
      "text": "{last_action}."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "first extra card",
      "when": {
        "calc": "action_kind == 'play' and max([p.bulls for p in players if p.seat == active_seat] + [0]) >= bulls_for_first_extra"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "x1"
      },
      "text": "Your bull lets you add one more card legal on the new top of pile {chosen_pile}, or stop. Piles: A {pile_a}, B {pile_b}, C {pile_c}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "apply the first extra card",
      "when": {
        "calc": "action_kind == 'play' and max([p.bulls for p in players if p.seat == active_seat] + [0]) >= bulls_for_first_extra"
      },
      "do": [
        {
          "set": {
            "key": "extra_card",
            "value": {
              "calc": "max([c for c in cards if card_labels[c - 1] == $x1] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "extra_stopped",
            "value": {
              "calc": "extra_card == 0"
            }
          }
        },
        {
          "remove": {
            "player": {"calc": "active_seat"},
            "key": "hand",
            "value": {"calc": "extra_card"},
            "if": {"calc": "extra_card > 0"}
          }
        },
        {
          "adjust": {
            "player": {"calc": "active_seat"},
            "key": "hand_size",
            "value": -1,
            "if": {"calc": "extra_card > 0"}
          }
        },
        {"append": {"key": "pile_a", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'A'"}}},
        {"append": {"key": "pile_b", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'B'"}}},
        {"append": {"key": "pile_c", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'C'"}}},
        {
          "set": {
            "key": "last_action",
            "value": {"calc": "last_action + ', then ' + card_labels[extra_card - 1]"},
            "if": {"calc": "extra_card > 0"}
          }
        },
        {
          "set": {
            "players": {"where": "you.seat == active_seat"},
            "key": "offer",
            "value": {
              "calc": "['stop'] + [card_labels[c - 1] for c in you.hand if (c - (pile_a[len(pile_a) - 1] if chosen_pile == 'A' else (pile_b[len(pile_b) - 1] if chosen_pile == 'B' else pile_c[len(pile_c) - 1]))) % legal_modulus >= legal_step_min and (c - (pile_a[len(pile_a) - 1] if chosen_pile == 'A' else (pile_b[len(pile_b) - 1] if chosen_pile == 'B' else pile_c[len(pile_c) - 1]))) % legal_modulus <= legal_step_max]"
            }
          }
        }
      ],
      "text": "{last_action}."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "second extra card",
      "when": {
        "calc": "action_kind == 'play' and not extra_stopped and max([p.bulls for p in players if p.seat == active_seat] + [0]) >= bulls_for_second_extra"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "x2"
      },
      "text": "Your second bull lets you add one more card legal on the new top of pile {chosen_pile}, or stop. Piles: A {pile_a}, B {pile_b}, C {pile_c}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "apply the second extra card",
      "when": {
        "calc": "action_kind == 'play' and not extra_stopped and max([p.bulls for p in players if p.seat == active_seat] + [0]) >= bulls_for_second_extra"
      },
      "do": [
        {
          "set": {
            "key": "extra_card",
            "value": {
              "calc": "max([c for c in cards if card_labels[c - 1] == $x2] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "extra_stopped",
            "value": true
          }
        },
        {
          "remove": {
            "player": {"calc": "active_seat"},
            "key": "hand",
            "value": {"calc": "extra_card"},
            "if": {"calc": "extra_card > 0"}
          }
        },
        {
          "adjust": {
            "player": {"calc": "active_seat"},
            "key": "hand_size",
            "value": -1,
            "if": {"calc": "extra_card > 0"}
          }
        },
        {"append": {"key": "pile_a", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'A'"}}},
        {"append": {"key": "pile_b", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'B'"}}},
        {"append": {"key": "pile_c", "value": {"calc": "extra_card"}, "if": {"calc": "extra_card > 0 and chosen_pile == 'C'"}}},
        {
          "set": {
            "key": "last_action",
            "value": {"calc": "last_action + ', then ' + card_labels[extra_card - 1]"},
            "if": {"calc": "extra_card > 0"}
          }
        }
      ],
      "text": "{last_action}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the take",
      "when": {
        "calc": "action_kind == 'take'"
      },
      "do": [
        {
          "set": {
            "key": "taken_size",
            "value": {
              "calc": "len(pile_a) if chosen_pile == 'A' else (len(pile_b) if chosen_pile == 'B' else len(pile_c))"
            }
          }
        },
        {
          "set": {
            "players": {"where": "you.seat == active_seat"},
            "key": "hand",
            "value": {
              "calc": "you.hand + (pile_a if chosen_pile == 'A' else (pile_b if chosen_pile == 'B' else pile_c))"
            }
          }
        },
        {
          "adjust": {
            "player": {"calc": "active_seat"},
            "key": "hand_size",
            "value": {"calc": "taken_size"}
          }
        },
        {"set": {"key": "pile_a", "value": [], "if": {"calc": "chosen_pile == 'A'"}}},
        {"set": {"key": "pile_b", "value": [], "if": {"calc": "chosen_pile == 'B'"}}},
        {"set": {"key": "pile_c", "value": [], "if": {"calc": "chosen_pile == 'C'"}}},
        {
          "set": {
            "players": {"where": "you.seat == active_seat"},
            "key": "offer",
            "value": {
              "calc": "[card_labels[c - 1] for c in you.hand]"
            }
          }
        }
      ],
      "text": "Seat {active_seat} takes pile {chosen_pile} ({taken_size} cards)."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "restart card",
      "when": {
        "calc": "action_kind == 'take'"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "rc"
      },
      "text": "You took pile {chosen_pile}; its cards are now in your hand. Choose one card from your hand to place face up as the only card of the restarted pile {chosen_pile}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "restart the pile",
      "when": {
        "calc": "action_kind == 'take'"
      },
      "do": [
        {
          "set": {
            "key": "restart_card",
            "value": {
              "calc": "max([c for c in cards if card_labels[c - 1] == $rc] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "restart_card",
            "value": {
              "calc": "[p.hand for p in players if p.seat == active_seat][0][0]"
            },
            "if": {"calc": "restart_card == 0"}
          }
        },
        {
          "remove": {
            "player": {"calc": "active_seat"},
            "key": "hand",
            "value": {"calc": "restart_card"}
          }
        },
        {
          "adjust": {
            "player": {"calc": "active_seat"},
            "key": "hand_size",
            "value": -1
          }
        },
        {"set": {"key": "pile_a", "value": {"calc": "[restart_card]"}, "if": {"calc": "chosen_pile == 'A'"}}},
        {"set": {"key": "pile_b", "value": {"calc": "[restart_card]"}, "if": {"calc": "chosen_pile == 'B'"}}},
        {"set": {"key": "pile_c", "value": {"calc": "[restart_card]"}, "if": {"calc": "chosen_pile == 'C'"}}},
        {
          "set": {
            "key": "last_action",
            "value": {
              "calc": "'Seat ' + card_labels[active_seat - 1] + ' takes ' + chosen_pile + ' (' + card_labels[taken_size - 1] + ' cards) and restarts it with ' + card_labels[restart_card - 1]"
            }
          }
        }
      ],
      "text": "{last_action}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the bull",
      "when": {
        "calc": "action_kind == 'take' and taken_size >= take_bull_threshold"
      },
      "do": [
        {
          "set": {
            "key": "bull_from",
            "value": {
              "calc": "sum([p.seat for p in players if p.seat != active_seat and p.bulls > 0 and p.bulls * (len(players) + 1) - ((p.seat - active_seat) % len(players)) == max([q.bulls * (len(players) + 1) - ((q.seat - active_seat) % len(players)) for q in players if q.seat != active_seat and q.bulls > 0] + [-1000])])"
            },
            "if": {"calc": "bull_supply == 0"}
          }
        },
        {
          "adjust": {
            "player": {"calc": "active_seat"},
            "key": "bulls",
            "value": 1,
            "if": {"calc": "bull_supply > 0 or bull_from > 0"},
            "text": "Seat {player} gains a bull."
          }
        },
        {
          "adjust": {
            "player": {"calc": "bull_from"},
            "key": "bulls",
            "value": -1,
            "if": {"calc": "bull_from > 0"},
            "text": "The bull is taken from seat {player}."
          }
        },
        {
          "adjust": {
            "key": "bull_supply",
            "value": -1,
            "if": {"calc": "bull_supply > 0"}
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "empty hand",
      "when": {
        "calc": "any([p.hand_size == 0 for p in players if p.seat == active_seat])"
      },
      "do": [
        {
          "set": {
            "key": "ending_triggered",
            "value": true
          }
        }
      ],
      "text": "Seat {active_seat} has emptied their hand. The game ends after the last seat's turn in this cycle."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "pass the turn",
      "do": [
        {
          "adjust": {
            "key": "cycle",
            "value": 1,
            "if": {"calc": "active_seat == len(players)"}
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "1 if active_seat == len(players) else active_seat + 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "count the penalties",
      "when": {
        "calc": "active_seat == 1 and (ending_triggered or cycle >= max_cycles)"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "penalty",
            "value": {
              "calc": "sum([oxheads_multiple_of_10 if c % 10 == 0 else (oxheads_multiple_of_5_not_10 if c % 5 == 0 else oxheads_other) for c in you.hand]) if len(you.hand) > 0 else empty_hand_penalty"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "turn",
      "label": "end of the cycle",
      "when": {
        "calc": "active_seat == 1 and (ending_triggered or cycle >= max_cycles)"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "active_seat == 1 and (ending_triggered or cycle >= max_cycles)"
      },
      "rank_by": "0 - you.penalty",
      "text": "Winner: {result}. Final penalties [seat, ox-heads]: {[[p.seat, p.penalty] for p in players]}."
    }
  },
  "limits": {
    "rounds": 48,
    "rounds_max": 48,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "The deck holds the cards {deck_low} to {deck_high} ({deck_size} cards). Ox-heads per card: {oxheads_multiple_of_10} if the number is a multiple of 10; {oxheads_multiple_of_5_not_10} if it is a multiple of 5 but not of 10; {oxheads_other} otherwise. The whole deck holds {deck_total_oxheads} ox-heads.\n\nSETUP: The deck is shuffled once; this is the only random event in the game. Each player is dealt {hand_size_start} cards face down as a private hand. {pile_count} cards are turned face up to start Pile A, Pile B and Pile C, {start_cards_per_pile} card each. The remaining cards ({set_aside_with_4} with 4 players, {set_aside_with_3} with 3) are set aside unseen for the rest of the game. The bull supply holds the number of players minus {bull_supply_offset} tokens (3 with 4 players, 2 with 3). Seat 1 moves first and play proceeds in seat order.\n\nPUBLIC: the full ordered contents of every pile (the last card listed is the top), each player's hand size and bull count, and every action taken. Only the contents of hands and the set-aside cards are hidden.\n\nLEGAL PLAY: A card c may be played on a pile whose top card is t if (c - t) mod {legal_modulus} is between {legal_step_min} and {legal_step_max}. On 12 you may play 13 to 18; on 37 you may play 38, 39, 40, 1, 2 or 3.\n\nA TURN: The active player privately chooses one action: (a) PLAY card X onto pile P, where X is in their hand and legal on P; or (b) TAKE pile P. A player may take even when a legal play exists. You are only offered legal plays; if no valid answer is given, the player instead takes the smallest pile (ties: A before B before C).\n\nIf the player PLAYED: card X goes on top of pile P. If they hold at least {bulls_for_first_extra} bull, they may then add one more card legal on the new top of the same pile, or stop. If they hold {bulls_for_second_extra} or more bulls and did not stop, they may add a second extra card the same way, or stop. They may stop at any point. Bulls are not spent by using them.\n\nIf the player TOOK pile P: all cards of P go into their hand. They must then choose any one card from their hand to place face up as the single card of the restarted pile P. If P held {take_bull_threshold} or more cards before it was taken, the player gains a bull from the supply. If the supply is empty, they instead take one bull from the opponent holding the most bulls; ties go to the first such player in seat order after the taker. If no opponent has a bull, nothing happens. If P held fewer than {take_bull_threshold} cards, no bull changes hands.\n\nIf the active player's hand is now empty, the game will end at the end of the current cycle, after the last seat has finished their turn, so every player gets the same number of turns. Then the turn passes to the next seat.\n\nEND OF GAME: The game ends at the end of the cycle in which any player emptied their hand. It also ends after {max_cycles_with_4} full cycles ({max_turns_with_4} turns with 4 players) or {max_cycles_with_3} full cycles ({max_turns_with_3} turns with 3 players), whichever comes first. Each player's penalty is the total ox-heads of the cards in their hand; a player with an empty hand scores {empty_hand_penalty}. The player with the lowest penalty wins; players tied for the lowest share the win."
}
```
````
