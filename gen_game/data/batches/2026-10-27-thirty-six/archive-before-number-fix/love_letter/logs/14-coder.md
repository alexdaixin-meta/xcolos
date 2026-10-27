# 14 coder

- time: 2026-10-27T18:35:08+00:00 (194.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 88f98748d6d800c0, reply sha256 18a520d8ce32e859

## Sent

````
# Task: write the XColos game file for "Love Letter: One Raise"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess.

PLAYERS: Seat 1 and Seat 2. Each starts with 0 points and 0 hands won.

ROUNDS: Each round is one turn by one player, the active player. The match lasts at most 40 turns.

STARTING A HAND (done at the start of a turn whenever a new hand is due, including turn 1):
- Shuffle all 16 cards into a deck. This is the only random event of the turn.
- Remove the top 3 cards face up as out of play and announce them to both players.
- Deal the next card face down to the starting player and the next to the other player. Each player sees only their own card.
- The remaining 11 cards stay as the deck in shuffled order, unseen. The bottom card of the deck is the burned card: it is never drawn normally.
- Stake = 1, no raise has been made, nobody is protected, and every player's discard sum for the hand = 0.
- Seat 1 starts hand 1. Afterwards, the player who did not win the previous hand starts. If nobody scored in the previous hand, the seat that did not start it starts.
- The starting player takes the first turn of the hand, which is this turn.

A TURN:
(1) RAISE: if no raise has been made in this hand, the active player, holding their one card, chooses 'raise' or 'no raise'.
(2) RESPONSE: if they raised, the opponent chooses 'accept' or 'concede'.
(3) RESOLVE:
- On 'concede', the active player wins the hand and gains 1 point. The hand ends and the rest of the turn is skipped; go to step 11.
- On 'accept', the stake becomes 2. No further raise is possible this hand.
(4) DRAW: the active player loses any Handmaid protection and takes the top card of the deck. They now hold two cards, seen only by them.
(5) PLAY: the active player chooses one of their two cards to discard face up.
(6) BOOKKEEPING:
- If they hold the Countess together with the King or a Prince, the Countess is discarded instead, whatever they chose.
- Add the discarded card's rank to their discard sum.
- If the discard is the Handmaid, they are protected until the start of their next turn.
- If the discard is the Princess, they are eliminated.
(7) DETAIL:
- If the discard is a Guard, the active player names a number from 2 to 8.
- If it is a Prince, they choose a target, themselves or the opponent. If the opponent is protected, they must target themselves.
(8) EFFECTS. The Guard, Priest, Baron and King do nothing if the opponent is protected.
- Guard: if the opponent's card equals the named number, the opponent is eliminated.
- Priest: the opponent's card is shown privately to the active player.
- Baron: both players privately see each other's cards. The lower card's holder is eliminated; on equal cards nothing happens.
- Prince: the target discards their card face up without effect and adds its rank to their discard sum. If it was the Princess, they are eliminated. Otherwise they take the top card of the deck; this may be the burned card if it is the only card left.
- King: the two players swap their cards.
- Countess, Handmaid, Princess: no further effect.
(9) ANNOUNCE to both players: the card discarded, any Guard number or Prince target, any card discarded by a Prince, any elimination together with the eliminated player's revealed card, the stake, both scores, and the number of cards left in the deck.
(10) HAND END CHECK:
- If a player is eliminated, the other player wins the hand and gains points equal to the stake.
- Otherwise, if the deck now holds 1 card or fewer, both players reveal their cards. The higher card wins the hand and gains the stake. On equal cards, the higher discard sum for this hand wins and gains the stake. If both are equal, nobody scores.
- The winner of a hand adds 1 to their hands won.
(11) MATCH CHECK AND NEXT TURN:
- If a player has 5 or more points, they win the match immediately.
- Otherwise, if this was turn 40, the match ends (see objective).
- Otherwise, if the hand ended, the next turn starts a new hand. If it did not, the other player becomes active.

How the winner is decided: The first player to reach 5 points wins; only one player can score per hand, so two players never reach 5 at once. If 40 turns pass with neither at 5, the player with more points wins. If points are equal, the player with more hands won wins. If those are also equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Love Letter: One Raise (2 to 2 players, best with 2)

Two-player Love Letter with a 16-card deck in which, once per hand, the player about to draw may raise the stake from 1 to 2 and the opponent must accept or concede 1 point; first to 5 points wins, capped at 40 turns.

STATE (every item below must exist in the file):
  - each player: points (number, starts 0); everyone sees it. match points; the score
  - each player: hands_won (number, starts 0); everyone sees it. hands won, the tie-break at turn 40
  - each player: hand (list, starts []); only its owner sees it. card ranks held: 1 between turns, 2 after drawing
  - each player: discard_sum (number, starts 0); everyone sees it. sum of the ranks this player discarded this hand
  - each player: protected (bool, starts False); everyone sees it. has Handmaid protection
  - each player: eliminated (bool, starts False); everyone sees it. knocked out of the current hand
  - the table: turn (number, starts 0); everyone sees it. turns played so far
  - the table: deck (list, starts []); hidden from all players. drawable cards, in random order (excludes the burned card)
  - the table: burned (list, starts []); hidden from all players. the bottom card of the deck, drawn only by a Prince when the deck is otherwise empty
  - the table: removed (list, starts []); everyone sees it. the 3 cards removed face up this hand
  - the table: new_hand_due (bool, starts True); hidden from all players. a new hand starts this turn
  - the table: starter_seat (number, starts 1); everyone sees it. the seat that starts the current or next hand
  - the table: active_seat (number, starts 1); everyone sees it. the active player this turn
  - the table: stake (number, starts 1); everyone sees it. points the winner of this hand gains
  - the table: raised (bool, starts False); everyone sees it. a raise has been accepted this hand
  - the table: raise_choice (text, starts ''); everyone sees it. the active player's raise or no raise this turn
  - the table: response (text, starts ''); everyone sees it. the opponent's accept or concede
  - the table: last_discard (number, starts 0); everyone sees it. rank of the card the active player discarded this turn
  - the table: guard_guess (number, starts 0); everyone sees it. the number named with a Guard
  - the table: prince_target (number, starts 0); everyone sees it. seat targeted by a Prince
  - the table: prince_discard (number, starts 0); everyone sees it. card discarded by the Prince's target
  - the table: hand_over (bool, starts False); everyone sees it. the current hand ended this turn
  - the table: hand_winner (number, starts 0); everyone sees it. seat that won the hand that just ended (0 if nobody)
  - parameters, each kept as a table attribute: deck_size = 16, guard_rank = 1, guard_copies = 5, priest_rank = 2, priest_copies = 2, baron_rank = 3, baron_copies = 2, handmaid_rank = 4, handmaid_copies = 2, prince_rank = 5, prince_copies = 2, king_rank = 6, king_copies = 1, countess_rank = 7, countess_copies = 1, princess_rank = 8, princess_copies = 1, removed_face_up = 3, cards_dealt_per_player = 1, deck_after_deal = 11, burned_cards = 1, starting_points = 0, starting_hands_won = 0, starting_stake = 1, raised_stake = 2, concede_gain = 1, max_raises_per_hand = 1, guard_guess_min = 2, guard_guess_max = 8, hand_end_deck_threshold = 1, points_to_win = 5, max_turns = 40, first_starter_seat = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 and Seat 2 each start with 0 points and 0 hands won.
  2. turn = 0, starter_seat = 1 and new_hand_due = true, so turn 1 starts hand 1 with Seat 1 active.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: When new_hand_due: deck = [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8]. Move 3 random cards from deck to removed. Move 1 random card to the starter_seat player's hand, then 1 to the other player's hand. Move 1 random card from deck to burned, leaving 10 in deck. stake = 1, raised = false, hand_over = false, hand_winner = 0. Every player: protected = false, eliminated = false, discard_sum = 0. active_seat = starter_seat, new_hand_due = false.
  2. [tell] all players. What happens: When a new hand was just started: announce the 3 cards in removed and which seat starts.
  3. [sync] all players. What happens: Each player sees their own hand.
  4. [update] all players. What happens: turn += 1; raise_choice = '', response = '', last_discard = 0, guard_guess = 0, prince_target = 0, prince_discard = 0.
  5. [ask] the active player answers: raise | no raise. What happens: When raised == false: set raise_choice.
  6. [ask] the opponent of the active player answers: accept | concede. What happens: When raise_choice == 'raise': set response.
  7. [update] all players. What happens: If response == 'concede': the active player's points += 1 and hands_won += 1; hand_winner = active_seat; hand_over = true. If response == 'accept': stake = 2 and raised = true.
  8. [update] the active player. What happens: When hand_over == false: the active player's protected = false; move 1 random card from deck to their hand.
  9. [sync] the active player. What happens: When hand_over == false: the active player sees both of their cards.
  10. [ask] the active player answers: one of the two ranks in their hand (only 7 if the hand holds 7 together with 5 or 6). What happens: When hand_over == false: set last_discard to the chosen rank.
  11. [update] the active player. What happens: When hand_over == false: remove last_discard from the active player's hand; their discard_sum += last_discard. If last_discard == 4, they become protected = true. If last_discard == 8, they become eliminated = true.
  12. [ask] the active player answers: a whole number from 2 to 8. What happens: When hand_over == false and last_discard == 1: set guard_guess.
  13. [ask] the active player answers: self | opponent (only self if the opponent is protected). What happens: When hand_over == false and last_discard == 5: prince_target = the chosen seat.
  14. [update] all players. What happens: Guard: when hand_over == false, last_discard == 1, the opponent is not protected and the opponent's hand card == guard_guess, the opponent's eliminated = true.
  15. [tell] the active player. What happens: Priest: when hand_over == false, last_discard == 2 and the opponent is not protected, privately show the opponent's hand card to the active player.
  16. [tell] both players, each privately. What happens: Baron: when hand_over == false, last_discard == 3 and the opponent is not protected, show each player the other's hand card privately.
  17. [update] all players. What happens: Baron: when hand_over == false, last_discard == 3 and the opponent is not protected, the player whose hand card is lower gets eliminated = true; if the cards are equal, nothing happens.
  18. [update] the Prince target. What happens: Prince: when hand_over == false and last_discard == 5: prince_discard = the target's hand card; empty the target's hand; the target's discard_sum += prince_discard. If prince_discard == 8, the target's eliminated = true. Otherwise move 1 random card from deck to the target's hand, or the burned card if deck is empty.
  19. [update] both players. What happens: King: when hand_over == false, last_discard == 6 and the opponent is not protected, swap the two players' hand lists.
  20. [sync] all players. What happens: When hand_over == false: each player sees their own current hand.
  21. [tell] all players. What happens: Announce last_discard, guard_guess or prince_target if any, prince_discard if any, any elimination with the eliminated player's revealed hand card, stake, both players' points, and the deck count (len(deck) + len(burned)).
  22. [update] all players. What happens: When hand_over == false: if a player is eliminated, the other player's points += stake and hands_won += 1, hand_winner = that seat, hand_over = true. Otherwise, if len(deck) + len(burned) <= 1: the higher hand card wins, and on equal cards the higher discard_sum wins. The winner's points += stake and hands_won += 1, hand_winner = that seat; if both are equal, hand_winner = 0. hand_over = true.
  23. [tell] all players. What happens: When a showdown happened: reveal both hand cards, both discard_sum values and the hand winner (or that nobody scored).
  24. [update] all players. What happens: If hand_over: starter_seat = the seat that is not hand_winner if hand_winner != 0, else the seat that is not starter_seat; new_hand_due = true. If not hand_over: active_seat = the other seat.
  25. [check] all players. What happens: End the game if any player's points >= 5 or turn >= 40; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 16 cards: five 1s (Guard), two 2s (Priest), two 3s (Baron), two 4s (Handmaid), two 5s (Prince), one 6 (King), one 7 (Countess) and one 8 (Princess).
  R2. When a hand starts, 3 random cards go face up to removed and are announced, each player gets 1 card, 1 card is set aside as burned, and 10 drawable cards remain.
  R3. When a hand starts, stake = 1, raised = false, and every player's protected = false, eliminated = false and discard_sum = 0.
  R4. Seat 1 starts hand 1.
  R5. When a hand had a winner, the other seat starts the next hand; when nobody scored, the seat that did not start it starts the next.
  R6. When no raise has been accepted this hand, the active player is asked 'raise' or 'no raise' before drawing; when raised == true, they are not asked.
  R7. When the active player raises and the opponent concedes, the active player gains 1 point and 1 hand won, and the hand ends with no draw or play.
  R8. When the active player raises and the opponent accepts, stake becomes 2 and no further raise is possible this hand.
  R9. When a turn goes on, the active player loses protection and draws 1 card from deck, then discards one of their two cards.
  R10. When the active player holds 7 together with 5 or 6, they must discard the 7.
  R11. When a card is discarded, its rank is added to its owner's discard_sum.
  R12. When a 4 (Handmaid) is discarded, its owner is protected until the start of their next turn.
  R13. When a player discards an 8 (Princess), by choice or through a Prince, they are eliminated.
  R14. When a 1 (Guard) is discarded, the active player names 2 to 8, and the unprotected opponent is eliminated if their card equals that number.
  R15. When a 2 (Priest) is discarded and the opponent is not protected, the active player privately sees the opponent's card.
  R16. When a 3 (Baron) is discarded and the opponent is not protected, the players privately see each other's cards and the lower card is eliminated; on equal cards nothing happens.
  R17. When a 5 (Prince) is discarded, the target (self or opponent, only self if the opponent is protected) discards their card without effect, adds it to their discard_sum, and draws 1 card, the burned card if the deck is empty.
  R18. When a 6 (King) is discarded and the opponent is not protected, the two players swap their cards.
  R19. When a 1, 2, 3 or 6 is discarded while the opponent is protected, it has no effect.
  R20. When a player is eliminated, the other player gains points equal to stake (1 or 2) and 1 hand won.
  R21. When no one is eliminated and 1 card or fewer remains in the deck (burned included), the higher card gains the stake; on equal cards the higher discard_sum gains it; if both are equal, nobody scores.
  R22. When a player reaches 5 points, the match ends and they win.
  R23. When turn 40 ends with nobody at 5, more points wins, then more hands won, and otherwise the match is a draw.
  R24. When a hand has not ended, the other player becomes active next turn; when it has ended, the next turn starts a new hand.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - raise | asked: the active player, only when raised == false | options: raise, no raise
  - response to a raise | asked: the opponent of the active player, only after a raise | options: accept, concede
  - card to discard | asked: the active player | options: holding 7 with 5 or 6: only 7; otherwise either of the two cards in hand
  - Guard number | asked: the active player, after discarding a 1 | options: whole number from 2 to 8
  - Prince target | asked: the active player, after discarding a 5 | options: opponent protected: self only; otherwise self or opponent

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: any player's points >= 5 or turn >= 40
  - each player's standing: you.points * 1000 + you.hands_won (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the most points wins; the first to reach 5 ends the match at once, since only one player scores per hand. At the 40-turn limit, more points wins, then more hands won. Players level on both share the win, which is a draw.
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

- each player: `points` (number, visible: public, starts 0): match points; the score
- each player: `hands_won` (number, visible: public, starts 0): hands won, the tie-break at turn 40
- the table: `turn` (number, visible: public, starts 0): turns played so far
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 16, guard_rank = 1, guard_copies = 5, priest_rank = 2, priest_copies = 2, baron_rank = 3, baron_copies = 2, handmaid_rank = 4, handmaid_copies = 2, prince_rank = 5, prince_copies = 2, king_rank = 6, king_copies = 1, countess_rank = 7, countess_copies = 1, princess_rank = 8, princess_copies = 1, removed_face_up = 3, cards_dealt_per_player = 1, deck_after_deal = 11, burned_cards = 1, starting_points = 0, starting_hands_won = 0, starting_stake = 1, raised_stake = 2, concede_gain = 1, max_raises_per_hand = 1, guard_guess_min = 2, guard_guess_max = 8, hand_end_deck_threshold = 1, points_to_win = 5, max_turns = 40, first_starter_seat = 1
- the game ends with ONE ending whose `rank_by` is `you.points * 1000 + you.hands_won`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "love_letter_one_raise",
    "name": "Love Letter: One Raise",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Love Letter on 16 cards, where the player about to draw may raise the stake once per hand. First to 5 points wins."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands_won",
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
        "key": "discard_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "protected",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "raise_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "resp_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "disc_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guess_said",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "target_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "peek",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "turn",
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
        "key": "burned",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "removed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "new_hand_due",
        "visible": "none",
        "type": "bool",
        "initial": true
      },
      {
        "key": "fresh_hand",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raised",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "raise_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_discard",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guard_guess",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prince_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prince_discard",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hand_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "end_kind",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "scores",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0
        ]
      },
      {
        "key": "elim_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "elim_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "shown_cards",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0
        ]
      },
      {
        "key": "shown_sums",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0
        ]
      },
      {
        "key": "opp_protected",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "my_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "opp_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "guard_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_copies",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "priest_rank",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "priest_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "baron_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "handmaid_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "handmaid_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "prince_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "prince_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "king_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "king_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "countess_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "countess_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "princess_rank",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "princess_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "removed_face_up",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "burned_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hands_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raised_stake",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "concede_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_raises_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_guess_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "guard_guess_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hand_end_deck_threshold",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "points_to_win",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "first_starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hands_won",
            "value": {
              "calc": "starting_hands_won"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first hand is due",
      "do": [
        {
          "set": {
            "key": "turn",
            "value": 0
          }
        },
        {
          "set": {
            "key": "starter_seat",
            "value": {
              "calc": "first_starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "new_hand_due",
            "value": true
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "start a new hand",
      "when": {
        "calc": "new_hand_due"
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
              1,
              1,
              1,
              1,
              1,
              2,
              2,
              3,
              3,
              4,
              4,
              5,
              5,
              6,
              7,
              8
            ]
          }
        },
        {
          "set": {
            "key": "removed",
            "value": []
          }
        },
        {
          "set": {
            "key": "burned",
            "value": []
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
            "key": "removed",
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
            "key": "removed",
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
            "key": "removed",
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
            "player": {
              "calc": "starter_seat"
            },
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
            "player": {
              "calc": "3 - starter_seat"
            },
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
            "key": "burned",
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
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(burned)"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "starting_stake"
            }
          }
        },
        {
          "set": {
            "key": "raised",
            "value": false
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": false
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard_sum",
            "value": 0
          }
        },
        {
          "set_status": {
            "players": "all",
            "to": "playing"
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "new_hand_due",
            "value": false
          }
        },
        {
          "set": {
            "key": "fresh_hand",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the new hand",
      "when": {
        "calc": "fresh_hand"
      },
      "to": "all",
      "text": "A new hand begins. Removed face up and out of play: {removed}. Seat {starter_seat} starts. Stake {stake}. Cards left in the deck: {deck_count}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the turn begins",
      "do": [
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "fresh_hand",
            "value": false
          }
        },
        {
          "set": {
            "key": "raise_choice",
            "value": ""
          }
        },
        {
          "set": {
            "key": "response",
            "value": ""
          }
        },
        {
          "set": {
            "key": "last_discard",
            "value": 0
          }
        },
        {
          "set": {
            "key": "guard_guess",
            "value": 0
          }
        },
        {
          "set": {
            "key": "prince_target",
            "value": 0
          }
        },
        {
          "set": {
            "key": "prince_discard",
            "value": 0
          }
        },
        {
          "set": {
            "key": "elim_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "elim_card",
            "value": 0
          }
        },
        {
          "set": {
            "key": "end_kind",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "resp_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "disc_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guess_said",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "target_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "peek",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "your card",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your card:"
    },
    {
      "use": "ask",
      "phase": "raise",
      "label": "raise",
      "when": {
        "calc": "not raised"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "no raise"
        ]
      },
      "store": "raise_said",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses: {value}."
      },
      "text": "Turn {turn}. You are the active player and hold the card {hand}; the stake is {stake}. Choose 'raise' or 'no raise' (only one raise per hand). If you raise and your opponent concedes, you win the hand and {concede_gain} point at once, with no draw. If you raise and they accept, the stake becomes {raised_stake}, no further raise is possible this hand, and you go on to draw and play. With 'no raise' you simply draw and play."
    },
    {
      "use": "ask",
      "phase": "raise",
      "label": "response to a raise",
      "when": {
        "calc": "any(p.raise_said == 'raise' for p in players)"
      },
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "accept",
          "concede"
        ]
      },
      "store": "resp_said",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the raise: {value}."
      },
      "text": "Seat {active_seat} has raised. Your card: {hand}. 'accept': the stake becomes {raised_stake}, no further raise is possible this hand, and play goes on. 'concede': Seat {active_seat} wins the hand and {concede_gain} point now, the rest of the turn is skipped, and a new hand starts next turn."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "resolve the raise and draw",
      "do": [
        {
          "set": {
            "key": "raise_choice",
            "value": {
              "calc": "players[active_seat - 1].raise_said"
            }
          }
        },
        {
          "set": {
            "key": "response",
            "value": {
              "calc": "players[2 - active_seat].resp_said"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "points",
            "value": {
              "calc": "concede_gain"
            },
            "if": {
              "calc": "response == 'concede'"
            },
            "text": "The raise was conceded: Seat {player} wins the hand and {concede_gain} point."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "active_seat"
            },
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "end_kind",
            "value": "concede",
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": true,
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "raised_stake"
            },
            "if": {
              "calc": "response == 'accept'"
            },
            "text": "The raise is accepted: the stake is now {raised_stake} for the rest of this hand."
          }
        },
        {
          "set": {
            "key": "raised",
            "value": true,
            "if": {
              "calc": "response == 'accept'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": false,
            "if": {
              "calc": "not hand_over"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            },
            "if": {
              "calc": "not hand_over and len(deck) > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "not hand_over and len(deck) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
          
... (cut)

Why it was refused: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: "Turn 1. You are the active player and hold the card {hand}; the stake is 1. Choose 'raise'"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: "Seat 1 has raised. Your card: {hand}. 'accept': the stake becomes 2, no further raise is p"); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'You drew a card. Your hand: {hand}. Choose which card to discard face up; its effect then '); use only names the step can fill in (see the broadcast rule: {value} and {seat})
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "love_letter_one_raise",
    "name": "Love Letter: One Raise",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two-player Love Letter on 16 cards. Once per hand the player about to draw may raise the stake. First to 5 points wins."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hands_won",
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
        "key": "discard_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "protected",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "raise_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "resp_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "disc_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guess_said",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "target_said",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "turn",
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
        "key": "burned",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "removed",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "new_hand_due",
        "visible": "none",
        "type": "bool",
        "initial": true
      },
      {
        "key": "fresh_hand",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raised",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "raise_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_discard",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guard_guess",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prince_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prince_discard",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hand_winner",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "end_kind",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "scores",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0
        ]
      },
      {
        "key": "elim_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "elim_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "shown_cards",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0
        ]
      },
      {
        "key": "shown_sums",
        "visible": "public",
        "type": "list",
        "initial": [
          0,
          0
        ]
      },
      {
        "key": "opp_protected",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "my_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "opp_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "guard_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_copies",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "priest_rank",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "priest_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_rank",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "baron_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "handmaid_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "handmaid_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "prince_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "prince_copies",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "king_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "king_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "countess_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "countess_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "princess_rank",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "princess_copies",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "removed_face_up",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "burned_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_hands_won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_stake",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raised_stake",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "concede_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_raises_per_hand",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_guess_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "guard_guess_max",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "hand_end_deck_threshold",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "points_to_win",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "max_turns",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "first_starter_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "points",
            "value": {
              "calc": "starting_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hands_won",
            "value": {
              "calc": "starting_hands_won"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first hand is due",
      "do": [
        {
          "set": {
            "key": "turn",
            "value": 0
          }
        },
        {
          "set": {
            "key": "starter_seat",
            "value": {
              "calc": "first_starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "new_hand_due",
            "value": true
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "start a new hand",
      "when": {
        "calc": "new_hand_due"
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
              1,
              1,
              1,
              1,
              1,
              2,
              2,
              3,
              3,
              4,
              4,
              5,
              5,
              6,
              7,
              8
            ]
          }
        },
        {
          "set": {
            "key": "removed",
            "value": []
          }
        },
        {
          "set": {
            "key": "burned",
            "value": []
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
            "key": "removed",
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
            "key": "removed",
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
            "key": "removed",
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
            "player": {
              "calc": "starter_seat"
            },
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
            "player": {
              "calc": "3 - starter_seat"
            },
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
            "key": "burned",
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
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(burned)"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "starting_stake"
            }
          }
        },
        {
          "set": {
            "key": "raised",
            "value": false
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": false
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard_sum",
            "value": 0
          }
        },
        {
          "set_status": {
            "players": "all",
            "to": "playing"
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starter_seat"
            }
          }
        },
        {
          "set": {
            "key": "new_hand_due",
            "value": false
          }
        },
        {
          "set": {
            "key": "fresh_hand",
            "value": true
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the new hand",
      "when": {
        "calc": "fresh_hand"
      },
      "to": "all",
      "text": "A new hand begins. Removed face up and out of play: {removed}. Seat {starter_seat} starts. Stake {stake}. Cards left in the deck (burned card included): {deck_count}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the turn begins",
      "do": [
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "fresh_hand",
            "value": false
          }
        },
        {
          "set": {
            "key": "raise_choice",
            "value": ""
          }
        },
        {
          "set": {
            "key": "response",
            "value": ""
          }
        },
        {
          "set": {
            "key": "last_discard",
            "value": 0
          }
        },
        {
          "set": {
            "key": "guard_guess",
            "value": 0
          }
        },
        {
          "set": {
            "key": "prince_target",
            "value": 0
          }
        },
        {
          "set": {
            "key": "prince_discard",
            "value": 0
          }
        },
        {
          "set": {
            "key": "elim_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "elim_card",
            "value": 0
          }
        },
        {
          "set": {
            "key": "end_kind",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "resp_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "disc_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guess_said",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "target_said",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": []
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "your card",
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your card:"
    },
    {
      "use": "ask",
      "phase": "raise",
      "label": "raise",
      "when": {
        "calc": "not raised"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "no raise"
        ]
      },
      "store": "raise_said",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses: {value}."
      },
      "text": "Turn {turn}. You are the active player; your one card is shown in your hand. The stake is {stake}. Choose 'raise' or 'no raise' (only one raise per hand). If you raise and your opponent concedes, you win the hand and {concede_gain} point at once, with no draw. If you raise and they accept, the stake becomes {raised_stake}, no further raise is possible this hand, and you go on to draw and play. With 'no raise' you simply draw and play."
    },
    {
      "use": "ask",
      "phase": "raise",
      "label": "response to a raise",
      "when": {
        "calc": "any(p.raise_said == 'raise' for p in players)"
      },
      "to": {
        "where": "you.seat != active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "accept",
          "concede"
        ]
      },
      "store": "resp_said",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the raise: {value}."
      },
      "text": "Seat {active_seat} has raised. Your card is shown in your hand. 'accept': the stake becomes {raised_stake}, no further raise is possible this hand, and play goes on. 'concede': Seat {active_seat} wins the hand and {concede_gain} point now, the rest of the turn is skipped, and a new hand starts next turn."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "resolve the raise and draw",
      "do": [
        {
          "set": {
            "key": "raise_choice",
            "value": {
              "calc": "players[active_seat - 1].raise_said"
            }
          }
        },
        {
          "set": {
            "key": "response",
            "value": {
              "calc": "players[2 - active_seat].resp_said"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "points",
            "value": {
              "calc": "concede_gain"
            },
            "if": {
              "calc": "response == 'concede'"
            },
            "text": "The raise was conceded: Seat {player} wins the hand and {concede_gain} point."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "active_seat"
            },
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "end_kind",
            "value": "concede",
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": true,
            "if": {
              "calc": "response == 'concede'"
            }
          }
        },
        {
          "set": {
            "key": "stake",
            "value": {
              "calc": "raised_stake"
            },
            "if": {
              "calc": "response == 'accept'"
            },
            "text": "The raise is accepted: the stake is now {raised_stake} for the rest of this hand."
          }
        },
        {
          "set": {
            "key": "raised",
            "value": true,
            "if": {
              "calc": "response == 'accept'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": false,
            "if": {
              "calc": "not hand_over"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            },
            "if": {
              "calc": "not hand_over and len(deck) > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "not hand_over and len(deck) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "not hand_over and len(deck) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "offer",
            "value": {
              "calc": "[countess_rank] if (countess_rank in you.hand and (prince_rank in you.hand or king_rank in you.hand)) else ([you.hand[0]] if (len(you.hand) < 2 or you.hand[0] == you.hand[1]) else you.hand)"
            },
            "if": {
              "calc": "not hand_over"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "play",
      "label": "your two cards",
      "when": {
        "calc": "not hand_over"
      },
      "mode": "self",
      "to": {
        "where": "you.seat == active_seat"
      },
      "fields": [
        "hand"
      ],
      "text": "You drew. Your cards:"
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "card to discard",
      "when": {
        "calc": "not hand_over and len(players[active_seat - 1].offer) > 1"
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
      "store": "disc_said",
      "text": "You hold two cards (shown in your hand). Choose which card to discard face up; its effect then happens and you keep the other. 1 Guard: name 2-8, the unprotected opponent is out if they hold it. 2 Priest: see the unprotected opponent's card. 3 Baron: compare cards with the unprotected opponent, the lower is out, equal does nothing. 4 Handmaid: protected until your next turn. 5 Prince: you or the opponent (only you if they are protected) discards their card and draws. 6 King: swap cards with the unprotected opponent. 7 Countess: no effect. 8 Princess: discarding it puts you out."
    },
    {
      "use": "update",
      "phase": "play",
      "label": "the discard",
      "when": {
        "calc": "not hand_over"
      },
      "do": [
        {
          "set": {
            "key": "last_discard",
            "value": {
              "calc": "players[active_seat - 1].offer[0] if len(players[active_seat - 1].offer) == 1 else int(players[active_seat - 1].disc_said)"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "last_discard"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "discard_sum",
            "value": {
              "calc": "last_discard"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": true,
            "if": {
              "calc": "last_discard == handmaid_rank"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "eliminated",
            "value": true,
            "if": {
              "calc": "last_discard == princess_rank"
            }
          }
        },
        {
          "set": {
            "key": "elim_seat",
            "value": {
              "calc": "active_seat"
            },
            "if": {
              "calc": "last_discard == princess_rank"
            }
          }
        },
        {
          "set": {
            "key": "elim_card",
            "value": {
              "calc": "princess_rank"
            },
            "if": {
              "calc": "last_discard == princess_rank"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "active_seat"
            },
            "to": "out",
            "if": {
              "calc": "last_discard == princess_rank"
            },
            "text": "Seat {player} discarded the Princess (8) and is out of this hand."
          }
        },
        {
          "set": {
            "key": "opp_protected",
            "value": {
              "calc": "players[2 - active_seat].protected"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "Guard number",
      "when": {
        "calc": "not hand_over and last_discard == guard_rank"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "guard_guess_min"
        },
        "max": {
          "calc": "guard_guess_max"
        }
      },
      "store": "guess_said",
      "text": "You discarded a Guard. Name a whole number from {guard_guess_min} to {guard_guess_max}. If your opponent is not protected and holds that card, they are out of the hand; otherwise nothing happens."
    },
    {
      "use": "ask",
      "phase": "play",
      "label": "Prince target",
      "when": {
        "calc": "not hand_over and last_discard == prince_rank and not opp_protected"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "self",
          "opponent"
        ]
      },
      "store": "target_said",
      "text": "You discarded a Prince. Choose its target: 'self' or 'opponent'. The target discards their card face up without effect (adding it to their discard sum) and draws a new one; if the discarded card is the Princess, the target is out of the hand."
    },
    {
      "use": "update",
      "phase": "effects",
      "label": "card effects",
      "when": {
        "calc": "not hand_over"
      },
      "do": [
        {
          "set": {
            "key": "my_card",
            "value": {
              "calc": "players[active_seat - 1].hand[0] if len(players[active_seat - 1].hand) > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "opp_card",
            "value": {
              "calc": "players[2 - active_seat].hand[0] if len(players[2 - active_seat].hand) > 0 else 0"
            }
          }
        },
        {
          "set": {
            "key": "guard_guess",
            "value": {
              "calc": "players[active_seat - 1].guess_said"
            },
            "if": {
              "calc": "last_discard == guard_rank"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "eliminated",
            "value": true,
            "if": {
              "calc": "last_discard == guard_rank and not opp_protected and opp_card == guard_guess"
            }
          }
        },
        {
          "set": {
            "key": "elim_seat",
            "value": {
              "calc": "3 - active_seat"
            },
            "if": {
              "calc": "last_discard == guard_rank and not opp_protected and opp_card == guard_guess"
            }
          }
        },
        {
          "set": {
            "key": "elim_card",
            "value": {
              "calc": "opp_card"
            },
            "if": {
              "calc": "last_discard == guard_rank and not opp_protected and opp_card == guard_guess"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "3 - active_seat"
            },
            "to": "out",
            "if": {
              "calc": "last_discard == guard_rank and not opp_protected and opp_card == guard_guess"
            },
            "text": "The Guard's guess is right: Seat {player} is out of this hand."
          }
        },
        {
          "disclose": {
            "attribute": "hand",
            "of": {
              "calc": "3 - active_seat"
            },
            "to": {
              "where": "you.seat == active_seat"
            },
            "if": {
              "calc": "last_discard == priest_rank and not opp_protected"
            },
            "text": "Priest: Seat {subject}'s card is {value}."
          }
        },
        {
          "disclose": {
            "attribute": "hand",
            "of": {
              "calc": "3 - active_seat"
            },
            "to": {
              "where": "you.seat == active_seat"
            },
            "if": {
              "calc": "last_discard == baron_rank and not opp_protected"
            },
            "text": "Baron: Seat {subject}'s card is {value}."
          }
        },
        {
          "disclose": {
            "attribute": "hand",
            "of": {
              "calc": "active_seat"
            },
            "to": {
              "where": "you.seat != active_seat"
            },
            "if": {
              "calc": "last_discard == baron_rank and not opp_protected"
            },
            "text": "Baron: Seat {subject}'s card is {value}."
          }
        },
        {
          "set": {
            "key": "elim_seat",
            "value": {
              "calc": "active_seat if my_card < opp_card else 3 - active_seat"
            },
            "if": {
              "calc": "last_discard == baron_rank and not opp_protected and my_card != opp_card"
            }
          }
        },
        {
          "set": {
            "key": "elim_card",
            "value": {
              "calc": "min(my_card, opp_card)"
            },
            "if": {
              "calc": "last_discard == baron_rank and not opp_protected and my_card != opp_card"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "elim_seat"
            },
            "key": "eliminated",
            "value": true,
            "if": {
              "calc": "last_discard == baron_rank and not opp_protected and my_card != opp_card"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "elim_seat"
            },
            "to": "out",
            "if": {
              "calc": "last_discard == baron_rank and not opp_protected and my_card != opp_card"
            },
            "text": "Baron: Seat {player} holds the lower card and is out of this hand."
          }
        },
        {
          "set": {
            "key": "prince_target",
            "value": {
              "calc": "active_seat if (opp_protected or players[active_seat - 1].target_said != 'opponent') else 3 - active_seat"
            },
            "if": {
              "calc": "last_discard == prince_rank"
            }
          }
        },
        {
          "set": {
            "key": "prince_discard",
            "value": {
              "calc": "players[prince_target - 1].hand[0] if len(players[prince_target - 1].hand) > 0 else 0"
            },
            "if": {
              "calc": "last_discard == prince_rank"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "prince_target"
            },
            "key": "hand",
            "value": [],
            "if": {
              "calc": "last_discard == prince_rank"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "prince_target"
            },
            "key": "discard_sum",
            "value": {
              "calc": "prince_discard"
            },
            "if": {
              "calc": "last_discard == prince_rank"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "prince_target"
            },
            "key": "eliminated",
            "value": true,
            "if": {
              "calc": "last_discard == prince_rank and prince_discard == princess_rank"
            }
          }
        },
        {
          "set": {
            "key": "elim_seat",
            "value": {
              "calc": "prince_target"
            },
            "if": {
              "calc": "last_discard == prince_rank and prince_discard == princess_rank"
            }
          }
        },
        {
          "set": {
            "key": "elim_card",
            "value": {
              "calc": "princess_rank"
            },
            "if": {
              "calc": "last_discard == prince_rank and prince_discard == princess_rank"
            }
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "prince_target"
            },
            "to": "out",
            "if": {
              "calc": "last_discard == prince_rank and prince_discard == princess_rank"
            },
            "text": "The Prince forced Seat {player} to discard the Princess: they are out of this hand."
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))] if len(deck) > 0 else burned[0]"
            },
            "if": {
              "calc": "last_discard == prince_rank and prince_discard != princess_rank and len(deck) + len(burned) > 0"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "prince_target"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "last_discard == prince_rank and prince_discard != princess_rank and len(deck) + len(burned) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "burned",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "last_discard == prince_rank and prince_discard != princess_rank and len(deck) == 0 and len(burned) > 0"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "last_discard == prince_rank and prince_discard != princess_rank and len(deck) > 0"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[opp_card]"
            },
            "if": {
              "calc": "last_discard == king_rank and not opp_protected"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "3 - active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "[my_card]"
            },
            "if": {
              "calc": "last_discard == king_rank and not opp_protected"
            },
            "text": "King: the two players swap their cards."
          }
        },
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "len(deck) + len(burned)"
            }
          }
        },
        {
          "set": {
            "key": "scores",
            "value": {
              "calc": "[p.points for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "effects",
      "label": "your card now",
      "when": {
        "calc": "not hand_over"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "hand"
      ],
      "text": "Your card now:"
    },
    {
      "use": "tell",
      "phase": "effects",
      "label": "the turn announced",
      "when": {
        "calc": "end_kind != 'concede'"
      },
      "to": "all",
      "text": "Seat {active_seat} discarded {last_discard}. Guard number named: {guard_guess} (0 = none). Prince target: seat {prince_target}, who discarded {prince_discard} (0 = none). Eliminated: seat {elim_seat}, revealed card {elim_card} (0 = nobody). Stake {stake}. Scores [Seat 1, Seat 2]: {scores}. Cards left in the deck: {deck_count}."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "hand end check",
      "when": {
        "calc": "not hand_over"
      },
      "do": [
        {
          "set": {
            "key": "end_kind",
            "value": "elimination",
            "if": {
              "calc": "any(p.eliminated for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "end_kind",
            "value": "showdown",
            "if": {
              "calc": "end_kind == '' and len(deck) + len(burned) <= hand_end_deck_threshold"
            }
          }
        },
        {
          "set": {
            "key": "shown_cards",
            "value": {
              "calc": "[(p.hand[0] if len(p.hand) > 0 else 0) for p in players]"
            },
            "if": {
              "calc": "end_kind == 'showdown'"
            }
          }
        },
        {
          "set": {
            "key": "shown_sums",
            "value": {
              "calc": "[p.discard_sum for p in players]"
            },
            "if": {
              "calc": "end_kind == 'showdown'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "[p.seat for p in players if not p.eliminated][0]"
            },
            "if": {
              "calc": "end_kind == 'elimination'"
            }
          }
        },
        {
          "set": {
            "key": "hand_winner",
            "value": {
              "calc": "1 if shown_cards[0] > shown_cards[1] else (2 if shown_cards[1] > shown_cards[0] else (1 if shown_sums[0] > shown_sums[1] else (2 if shown_sums[1] > shown_sums[0] else 0)))"
            },
            "if": {
              "calc": "end_kind == 'showdown'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "hand_winner"
            },
            "key": "points",
            "value": {
              "calc": "stake"
            },
            "if": {
              "calc": "end_kind in ['elimination', 'showdown'] and hand_winner > 0"
            },
            "text": "Seat {player} wins the hand and gains {stake}."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "hand_winner"
            },
            "key": "hands_won",
            "value": 1,
            "if": {
              "calc": "end_kind in ['elimination', 'showdown'] and hand_winner > 0"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": true,
            "if": {
              "calc": "end_kind != ''"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "end",
      "label": "the showdown",
      "when": {
        "calc": "end_kind == 'showdown'"
      },
      "to": "all",
      "text": "Showdown. Cards [Seat 1, Seat 2]: {shown_cards}. Discard sums [Seat 1, Seat 2]: {shown_sums}. Hand winner: seat {hand_winner} (0 means nobody scored)."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "next turn",
      "do": [
        {
          "set": {
            "key": "starter_seat",
            "value": {
              "calc": "(3 - hand_winner) if hand_winner != 0 else (3 - starter_seat)"
            },
            "if": {
              "calc": "hand_over"
            }
          }
        },
        {
          "set": {
            "key": "new_hand_due",
            "value": true,
            "if": {
              "calc": "hand_over"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "3 - active_seat"
            },
            "if": {
              "calc": "not hand_over"
            }
          }
        },
        {
          "set": {
            "key": "scores",
            "value": {
              "calc": "[p.points for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "match check",
      "when": {
        "calc": "max([p.points for p in players]) >= points_to_win or turn >= max_turns"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "max([p.points for p in players]) >= points_to_win or turn >= max_turns"
      },
      "rank_by": "you.points * 1000 + you.hands_won",
      "text": "Winner: {result}. Final points: Seat 1 {players[0].points}, Seat 2 {players[1].points}; hands won: Seat 1 {players[0].hands_won}, Seat 2 {players[1].hands_won}; target {points_to_win}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS ({deck_size}): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess. Seat 1 and Seat 2 each start with {starting_points} points and {starting_hands_won} hands won. Each round is one turn by one player, the active player. The match lasts at most {max_turns} turns.\n\nSTARTING A HAND: all {deck_size} cards are shuffled. The top {removed_face_up} are removed face up, out of play, and announced. Each player is dealt {cards_dealt_per_player} card face down, starting player first; each sees only their own. The remaining {deck_after_deal} cards stay as the deck; its bottom card is the burned card, never drawn normally. Stake = {starting_stake}, no raise has been made, nobody is protected, and every discard sum = 0. Seat {first_starter_seat} starts hand 1. Afterwards the player who did not win the previous hand starts; if nobody scored, the seat that did not start it starts. The starting player takes the first turn of the hand.\n\nA TURN:\n(1) RAISE: if no raise has been made this hand ({max_raises_per_hand} per hand), the active player, holding one card, chooses 'raise' or 'no raise'. With 'no raise' play goes straight on to the draw. If a raise has already been made this hand, there is no raise question.\n(2) RESPONSE: if they raised, the opponent chooses 'accept' or 'concede'.\n(3) On 'concede', the active player wins the hand and gains {concede_gain} point; the hand ends and the rest of the turn is skipped. On 'accept', the stake becomes {raised_stake}, no further raise is possible this hand, and the turn goes on.\n(4) DRAW: the active player loses any Handmaid protection and takes the top card of the deck.\n(5) PLAY: the active player chooses one of their two cards to discard face up.\n(6) If they hold the Countess together with the King or a Prince, the Countess is discarded instead (you are only offered the 7). The discarded rank is added to their discard sum. A discarded Handmaid protects them until the start of their next turn. A discarded Princess eliminates them.\n(7) Guard: name a number from {guard_guess_min} to {guard_guess_max}. Prince: choose a target, yourself or the opponent; if the opponent is protected you must target yourself.\n(8) EFFECTS. Guard, Priest, Baron and King do nothing if the opponent is protected. Guard: if the opponent's card equals the named number they are eliminated, otherwise nothing happens. Priest: you privately see the opponent's card. Baron: both players privately see each other's cards; the lower card's holder is eliminated; on equal cards nothing happens. Prince: the target discards their card face up without effect and adds its rank to their discard sum; if it was the Princess they are eliminated, otherwise they draw the top card (the burned card if it is the only card left). King: the two players swap cards. Countess, Handmaid, Princess: no further effect.\n(9) Both players are told the card discarded, any Guard number or Prince target, any card discarded by a Prince, any elimination with the eliminated player's card, the stake, both scores and the cards left in the deck.\n(10) HAND END: if a player is eliminated, the other wins the hand and gains points equal to the stake. Otherwise, if the deck holds {hand_end_deck_threshold} card or fewer, both cards are revealed: the higher card wins the hand and gains the stake; on equal cards the higher discard sum for this hand wins; if both are equal nobody scores. If neither happens, the hand goes on. The winner of a hand adds 1 to hands won.\n(11) If a player has {points_to_win} or more points they win the match immediately. Otherwise, after turn {max_turns} the match ends. Otherwise, if the hand ended the next turn starts a new hand; if not, the other player becomes active.\n\nWINNING: the first player to {points_to_win} points wins. If {max_turns} turns pass with neither at {points_to_win}, more points wins, then more hands won; if those are equal too, the match is a draw (shared win)."
}
```
````
