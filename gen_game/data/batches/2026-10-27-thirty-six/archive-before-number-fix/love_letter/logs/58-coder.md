# 58 coder

- time: 2026-10-27T19:51:34+00:00 (178.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 0368c1b8f405fd6e, reply sha256 7a522dfde4676935

## Sent

````
# Task: write the XColos game file for "Love Letter Duel: Long Courtship"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS (16): rank 1 Guard x5, rank 2 Priest x2, rank 3 Baron x2, rank 4 Handmaid x2, rank 5 Prince x2, rank 6 King x1, rank 7 Countess x1, rank 8 Princess x1.

ZONES: deck (hidden order); out_of_play (6 cards: position 1 is the face-down burned card, positions 2-6 are face up); each player's hand (hidden, seen only by its owner); each player's discards (public). Every card is always in exactly one zone, so the zones total 16.

HIDDEN ELEMENTS: hands, deck order, burned card.

GAME STATE: deck, out_of_play, deck_count, active_seat (starts 1), hand_over (starts 1), discard_choice, guess.

PLAYER STATE: hand, discards, discard_sum (reset each hand), career_sum (whole game, starts 0), tokens (start 0), protected, eliminated.

The game lasts exactly 40 rounds. Each round is one turn of the active player:
1. NEW HAND (only if hand_over = 1). Return all cards to the deck and shuffle it; this is the round's only random draw. Move the top 6 cards to out_of_play (the first one to position 1, face down). Deal 1 card to each player's hand. Set deck_count = 8. Set protected, eliminated and discard_sum to 0 for both players. Set hand_over = 0.
2. If a new hand was just dealt, announce: 'The face-up out-of-play cards are ranks a, b, c, d, e' (positions 2-6).
3. START TURN. Set the active player's protected to 0. They take the top deck card, and deck_count goes down by 1. Privately tell them: 'You kept rank X and just drew rank Y.'
4. CHOICE. The active player chooses which of their two ranks to discard; store it in discard_choice.
5. COUNTESS. If they hold rank 7 together with rank 5 or rank 6, set discard_choice = 7.
6. DISCARD. Move the chosen card to their discards. Add its rank to their discard_sum and career_sum. Announce 'Seat s discards rank r (name).'
7. GUARD GUESS (if discard_choice = 1). The active player names a rank from 2 to 8; store it in guess.
8. GUARD RESOLVE (if discard_choice = 1). If the opponent is protected, announce that the card has no effect. Otherwise, if the opponent's card equals guess, set the opponent's eliminated = 1 and announce a hit; if not, announce a miss.
9. PRIEST (if discard_choice = 2). If the opponent is protected, announce no effect. Otherwise, privately tell the active player the opponent's rank, and announce publicly that Seat s looked at Seat o's card.
10. BARON (if discard_choice = 3). If the opponent is protected, announce no effect. Otherwise compare the two hand cards: the owner of the lower one gets eliminated = 1, and the result is announced with the losing rank. If the cards are equal, announce a tie and nobody is out.
11. HANDMAID (if discard_choice = 4). Set the active player's protected = 1 and announce it.
12. PRINCE (if discard_choice = 5). The target is the opponent, or the active player if the opponent is protected. The target moves their hand card to their discards, adds its rank to their discard_sum and career_sum, and the rank is announced. If that card was rank 8, the target's eliminated = 1. Otherwise the target draws the top deck card if deck_count > 0 (deck_count goes down by 1), or else takes the burned card from out_of_play position 1.
13. KING (if discard_choice = 6). If the opponent is protected, announce no effect. Otherwise the two players swap hand cards, and the swap is announced.
14. PRINCESS (if discard_choice = 8). The active player's eliminated = 1; announce it.
15. SHOWDOWN (if nobody is eliminated and (deck_count = 0 or this is round 40)). Announce both hand ranks. The owner of the lower card gets eliminated = 1. If the cards are equal, the owner of the lower discard_sum gets eliminated = 1. If those are also equal, announce that the hand is tied and set hand_over = 1.
16. AWARD (if exactly one player is eliminated). The other player gains 1 token; announce the new total. Set hand_over = 1. The eliminated player becomes active_seat for the next hand.
17. PASS (if no token was awarded this round). active_seat switches to the other seat.
18. END CHECK. After round 40 the game ends.

How the winner is decided: After round 40, the player with more tokens wins. If tokens are equal, the player with the higher career_sum (total ranks they discarded over the whole game, including cards a Prince forced them to discard) wins. If both are equal, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Love Letter Duel: Long Courtship (2 to 2 players, best with 2)

A two-player Love Letter duel over exactly 40 turns. Each turn one player draws, discards one of two cards and resolves its effect. Winning a hand earns a token; most tokens wins, with total discarded ranks as the tie-break.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. Ranks of the cards in this player's hand: 1 card between turns, 2 during their own turn.
  - each player: discards (list, starts []); everyone sees it. Ranks this player has discarded this hand, in order.
  - each player: discard_sum (number, starts 0); everyone sees it. Sum of ranks discarded this hand; reset at each new hand.
  - each player: career_sum (number, starts 0); everyone sees it. Sum of all ranks discarded over the whole game, including cards a Prince forced out.
  - each player: tokens (number, starts 0); everyone sees it. Hands won.
  - each player: protected (number, starts 0); everyone sees it. 1 if protected by a Handmaid until this player's next turn starts.
  - each player: eliminated (number, starts 0); everyone sees it. 1 if knocked out of the current hand.
  - the table: deck (list, starts [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]); hidden from all players. Ranks of the undrawn cards; order is hidden.
  - the table: burned_card (list, starts []); hidden from all players. Out-of-play position 1: the face-down burned card (0 or 1 rank).
  - the table: face_up (list, starts []); everyone sees it. Out-of-play positions 2-6: five face-up ranks.
  - the table: deck_count (number, starts 0); everyone sees it. Number of cards left in the deck.
  - the table: active_seat (number, starts 1); everyone sees it. Seat taking this round's turn.
  - the table: hand_over (number, starts 1); everyone sees it. 1 if a new hand must be dealt at the start of the next round.
  - the table: discard_choice (number, starts 0); everyone sees it. Rank the active player discards this turn.
  - the table: guess (number, starts 0); everyone sees it. Rank named with a Guard.
  - the table: round_number (number, starts 0); everyone sees it. Current round, from 1 to 40.
  - the table: new_hand (number, starts 0); hidden from all players. Scratch flag: 1 if a hand was dealt this round.
  - the table: token_awarded (number, starts 0); hidden from all players. Scratch flag: 1 if a token was awarded this round.
  - parameters, each kept as a table attribute: total_rounds = 40, deck_size = 16, guard_count = 5, priest_count = 2, baron_count = 2, handmaid_count = 2, prince_count = 2, king_count = 1, countess_count = 1, princess_count = 1, guard_rank = 1, priest_rank = 2, baron_rank = 3, handmaid_rank = 4, prince_rank = 5, king_rank = 6, countess_rank = 7, princess_rank = 8, out_of_play_size = 6, face_up_out_of_play = 5, burned_cards = 1, cards_dealt_per_player = 1, deck_count_after_deal = 8, guard_guess_min = 2, guard_guess_max = 8, tokens_per_hand_won = 1, starting_tokens = 0, starting_career_sum = 0, starting_active_seat = 1, rank_tiebreak_multiplier = 1000

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Two seats are filled. Each player starts with tokens 0 and career_sum 0, an empty hand and empty discards.
  2. The table starts with active_seat 1, hand_over 1 and round_number 0. The deck holds all 16 ranks: 1 x5, 2 x2, 3 x2, 4 x2, 5 x2, 6, 7, 8.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_number += 1; new_hand = 0; token_awarded = 0.
  2. [update] all players. What happens: When hand_over = 1: empty every hand, every player's discards, burned_card and face_up, and set deck to all 16 ranks. Draw 1 random rank from deck into burned_card, then 5 random ranks from deck into face_up. Draw 1 random rank from deck into each player's hand. Set deck_count = 8. For both players set protected = 0, eliminated = 0 and discard_sum = 0. Set hand_over = 0 and new_hand = 1.
  3. [tell] all players. What happens: When new_hand = 1, announce: 'The face-up out-of-play cards are ranks {face_up}.'
  4. [update] seat active_seat. What happens: Set the active player's protected = 0. Move 1 random rank from deck to the active player's hand; deck_count -= 1. Privately tell the active player: 'You kept rank X and just drew rank Y.'
  5. [ask] seat active_seat answers: one of the ranks in their hand. What happens: Store the chosen rank in discard_choice.
  6. [update] seat active_seat. What happens: Countess: if the active player's hand contains 7 and also contains 5 or 6, set discard_choice = 7.
  7. [update] seat active_seat. What happens: Move one card of rank discard_choice from the active player's hand to their discards. Add discard_choice to their discard_sum and career_sum. Announce 'Seat s discards rank r (name).'
  8. [ask] seat active_seat answers: a whole number from 2 to 8. What happens: When discard_choice = 1: store the number in guess.
  9. [update] all players. What happens: When discard_choice = 1: if the opponent's protected = 1, announce no effect. Otherwise, if the opponent's hand card = guess, set the opponent's eliminated = 1 and announce a hit; if not, announce a miss.
  10. [update] seat active_seat. What happens: When discard_choice = 2: if the opponent's protected = 1, announce no effect. Otherwise privately tell the active player the opponent's hand rank, and announce 'Seat s looked at Seat o's card.'
  11. [update] all players. What happens: When discard_choice = 3: if the opponent's protected = 1, announce no effect. Otherwise compare the two hand cards. The owner of the lower one gets eliminated = 1, and the loser and the losing rank are announced. If the cards are equal, announce a tie and nobody is out.
  12. [update] seat active_seat. What happens: When discard_choice = 4: set the active player's protected = 1 and announce it.
  13. [update] all players. What happens: When discard_choice = 5: the target is the opponent, or the active player if the opponent's protected = 1. Move the target's hand card to their discards, add its rank to their discard_sum and career_sum, and announce the rank. If the rank was 8, set the target's eliminated = 1. Otherwise, if deck_count > 0, move 1 random rank from deck to the target's hand and deck_count -= 1; if deck_count = 0, move the burned_card rank to the target's hand.
  14. [update] all players. What happens: When discard_choice = 6: if the opponent's protected = 1, announce no effect. Otherwise swap the two players' hand lists and announce the swap.
  15. [update] seat active_seat. What happens: When discard_choice = 8: set the active player's eliminated = 1 and announce it.
  16. [update] all players. What happens: Showdown, when the sum of eliminated = 0 and (deck_count = 0 or round_number = 40): announce both hand ranks. The owner of the lower hand card gets eliminated = 1. If the cards are equal, the owner of the lower discard_sum gets eliminated = 1. If those are also equal, announce that the hand is tied and set hand_over = 1.
  17. [update] all players. What happens: Award, when the sum of eliminated = 1: the player with eliminated = 0 gains tokens += 1, and the new total is announced. Set hand_over = 1, token_awarded = 1, and active_seat = the seat of the eliminated player.
  18. [update] all players. What happens: Pass, when token_awarded = 0: active_seat = 3 - active_seat.
  19. [check] all players. What happens: End the game if round_number = 40; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The deck has 16 cards: rank 1 x5, rank 2 x2, rank 3 x2, rank 4 x2, rank 5 x2, rank 6 x1, rank 7 x1, rank 8 x1.
  R2. When hand_over = 1 at the start of a round, then all 16 cards are gathered, 1 goes to burned_card, 5 go face up to face_up, each player gets 1 card, deck_count = 8, protected, eliminated and discard_sum are 0 for both players, and hand_over = 0.
  R3. When a new hand is dealt, then the 5 face_up ranks are announced and the burned card stays hidden.
  R4. When a turn starts, then the active player's protected = 0, they draw 1 card from the deck, deck_count drops by 1, and they are privately told the rank they kept and the rank they drew.
  R5. When the active player chooses a rank, then it is stored in discard_choice.
  R6. When the active player holds rank 7 together with rank 5 or rank 6, then discard_choice = 7.
  R7. When a card is discarded, then it moves to the player's discards, its rank is added to discard_sum and career_sum, and 'Seat s discards rank r (name)' is announced.
  R8. When discard_choice = 1, then the active player names a rank from 2 to 8 as guess.
  R9. When a Guard is played against a protected opponent, then it has no effect.
  R10. When a Guard's guess equals an unprotected opponent's card, then the opponent's eliminated = 1 and a hit is announced; otherwise a miss is announced.
  R11. When a Priest is played against an unprotected opponent, then the active player is privately told the opponent's rank and the look is announced publicly; against a protected opponent it has no effect.
  R12. When a Baron is played against an unprotected opponent, then the holder of the lower hand card gets eliminated = 1 and the losing rank is announced; on equal cards a tie is announced and nobody is out.
  R13. When a Handmaid is played, then the active player's protected = 1 until their next turn starts.
  R14. When a Prince is played, then its target is the opponent, or the active player if the opponent is protected.
  R15. When a Prince target discards, then the rank is added to the target's discard_sum and career_sum and announced; if it was rank 8, the target's eliminated = 1.
  R16. When a Prince target did not discard rank 8, then the target draws from the deck if deck_count > 0 (deck_count drops by 1); otherwise the target takes the burned card.
  R17. When a King is played against an unprotected opponent, then the two hand cards are swapped and the swap is announced; against a protected opponent it has no effect.
  R18. When a Princess is discarded by the active player, then their eliminated = 1.
  R19. When nobody is eliminated and (deck_count = 0 or it is round 40), then both hands are revealed and the lower card's owner gets eliminated = 1.
  R20. When showdown cards are equal, then the lower discard_sum is eliminated; if discard_sum is also equal, then the hand is tied, no token is awarded, and hand_over = 1.
  R21. When exactly one player is eliminated, then the other gains 1 token, hand_over = 1, and the eliminated player is active_seat for the next hand.
  R22. When no token was awarded in a round, then active_seat switches to the other seat.
  R23. When round 40 ends, then the game ends; more tokens wins, then higher career_sum, and if both are equal it is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Which rank to discard | asked: the active seat | options: If the hand contains 7 together with 5 or 6: only 7. Otherwise: each distinct rank in their two-card hand (one option if both cards are the same rank).
  - Guard guess | asked: the active seat, only when discard_choice = 1 | options: any whole number from 2 to 8

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number = 40
  - each player's standing: you.tokens * 1000 + you.career_sum (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with more tokens wins. If tokens are equal, the higher career_sum wins. If both are equal, the players share the result as a draw.
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

- each player: `discards` (list, visible: public, starts []): Ranks this player has discarded this hand, in order.
- each player: `career_sum` (number, visible: public, starts 0): Sum of all ranks discarded over the whole game, including cards a Prince forced out.
- each player: `tokens` (number, visible: public, starts 0): Hands won.
- the table: `face_up` (list, visible: public, starts []): Out-of-play positions 2-6: five face-up ranks.
- the table: `deck_count` (number, visible: public, starts 0): Number of cards left in the deck.
- the table: `round_number` (number, visible: public, starts 0): Current round, from 1 to 40.
- parameters (each must be an attribute holding this value, never a number buried in a step): total_rounds = 40, deck_size = 16, guard_count = 5, priest_count = 2, baron_count = 2, handmaid_count = 2, prince_count = 2, king_count = 1, countess_count = 1, princess_count = 1, guard_rank = 1, priest_rank = 2, baron_rank = 3, handmaid_rank = 4, prince_rank = 5, king_rank = 6, countess_rank = 7, princess_rank = 8, out_of_play_size = 6, face_up_out_of_play = 5, burned_cards = 1, cards_dealt_per_player = 1, deck_count_after_deal = 8, guard_guess_min = 2, guard_guess_max = 8, tokens_per_hand_won = 1, starting_tokens = 0, starting_career_sum = 0, starting_active_seat = 1, rank_tiebreak_multiplier = 1000
- the game ends with ONE ending whose `rank_by` is `you.tokens * 1000 + you.career_sum`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1. Make the Guard guess a choice whose options are the literal numbers guard_guess_min..guard_guess_max (2, 3, 4, 5, 6, 7, 8), built from those parameter attributes. Store the chosen value in `guess`, then compare it with the unprotected opponent's hand card. On a match, set the opponent's eliminated = 1 so that AWARD gives the active player tokens_per_hand_won.
2. Always offer both held ranks, the kept card and the drawn card, as the discard options. Do not filter out rank 5 or 6 when rank 7 is also held.
3. Apply the Countess rule after the choice, as a conditional step: if the hand contains countess_rank and also contains prince_rank or king_rank, set discard_choice = countess_rank, whatever was chosen.
4. Check that the guess step runs only when discard_choice = guard_rank, and that it is offered to the active seat.

````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "love_letter_duel_long_courtship",
    "name": "Love Letter Duel: Long Courtship",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "A two-player Love Letter duel over exactly 40 turns: draw, discard one of two cards, resolve it; most tokens wins."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "discards",
        "visible": "public",
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
        "key": "career_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "protected",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
      },
      {
        "key": "burned_card",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "face_up",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_count",
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
        "key": "hand_over",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "discard_choice",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "new_hand",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "token_awarded",
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
        "key": "kept",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "opp",
        "visible": "none",
        "type": "number",
        "initial": 2
      },
      {
        "key": "card_name",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "effect",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "seen",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "target",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "refill",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "held",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "sd1",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sd2",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_tokens",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "guard_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "priest_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "baron_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "handmaid_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "prince_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "king_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "countess_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "princess_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "guard_rank",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "priest_rank",
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
        "key": "handmaid_rank",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "prince_rank",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "king_rank",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "countess_rank",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "princess_rank",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "out_of_play_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "face_up_out_of_play",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "burned_cards",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "cards_dealt_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_count_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 8
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
        "key": "tokens_per_hand_won",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_career_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 1000
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the table is laid",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "tokens",
            "value": {
              "calc": "starting_tokens"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "career_sum",
            "value": {
              "calc": "starting_career_sum"
            }
          }
        },
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
            "players": "all",
            "key": "discards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "starting_active_seat"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": 1
          }
        },
        {
          "set": {
            "key": "round_number",
            "value": 0
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "sorted(deck)"
            }
          }
        },
        {
          "set": {
            "key": "guess_options",
            "value": {
              "calc": "[r for r in [priest_rank, baron_rank, handmaid_rank, prince_rank, king_rank, countess_rank, princess_rank] if r >= guard_guess_min and r <= guard_guess_max]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the starting state",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the round begins",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 0
          }
        },
        {
          "set": {
            "key": "token_awarded",
            "value": 0
          }
        },
        {
          "set": {
            "key": "opp",
            "value": {
              "calc": "3 - active_seat"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "deal",
      "label": "a new hand",
      "when": {
        "calc": "hand_over == 1"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "deck + burned_card + face_up + players[0].hand + players[1].hand + players[0].discards + players[1].discards"
            }
          }
        },
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
            "players": "all",
            "key": "discards",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "burned_card",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "key": "face_up",
            "value": {
              "calc": "[]"
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
            "key": "burned_card",
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
            "key": "face_up",
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
            "key": "face_up",
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
            "key": "face_up",
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
            "key": "face_up",
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
            "key": "face_up",
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
            "key": "deck_count",
            "value": {
              "calc": "deck_count_after_deal"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "eliminated",
            "value": 0
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
            "key": "hand_over",
            "value": 0
          }
        },
        {
          "set": {
            "key": "new_hand",
            "value": 1
          }
        }
      ],
      "text": "A new hand is dealt. Each player holds one card."
    },
    {
      "use": "tell",
      "phase": "deal",
      "label": "the face-up cards",
      "when": {
        "calc": "new_hand == 1"
      },
      "to": "all",
      "text": "The face-up out-of-play cards are ranks {face_up}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "start turn",
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": 0
          }
        },
        {
          "set": {
            "key": "kept",
            "value": {
              "calc": "players[active_seat - 1].hand[0]"
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
            "player": {
              "calc": "active_seat"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "text": "You kept rank {kept} and just drew rank {pick}.",
            "announce_to": {
              "where": "you.seat == active_seat"
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
          "adjust": {
            "key": "deck_count",
            "value": -1
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "choose a discard",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "hand"
        }
      },
      "verify": {
        "bind": "d"
      },
      "text": "Your turn. Choose which rank in your hand to discard; you keep the other. If you hold the Countess (7) with the Prince (5) or King (6), the Countess is discarded whatever you choose."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "store the choice and apply the Countess",
      "do": [
        {
          "set": {
            "key": "discard_choice",
            "value": {
              "calc": "int($d)"
            }
          }
        },
        {
          "set": {
            "key": "discard_choice",
            "value": {
              "calc": "countess_rank"
            },
            "if": {
              "calc": "countess_rank in players[active_seat - 1].hand and (prince_rank in players[active_seat - 1].hand or king_rank in players[active_seat - 1].hand)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "discard",
      "do": [
        {
          "set": {
            "key": "card_name",
            "value": {
              "calc": "['Guard', 'Priest', 'Baron', 'Handmaid', 'Prince', 'King', 'Countess', 'Princess'][discard_choice - 1]"
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
              "calc": "discard_choice"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "discards",
            "value": {
              "calc": "discard_choice"
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
              "calc": "discard_choice"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "career_sum",
            "value": {
              "calc": "discard_choice"
            }
          }
        }
      ],
      "text": "Seat {active_seat} discards rank {discard_choice} ({card_name})."
    },
    {
      "use": "ask",
      "phase": "effect",
      "label": "guard guess",
      "when": {
        "calc": "discard_choice == guard_rank"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "guess_options"
        }
      },
      "verify": {
        "bind": "g"
      },
      "text": "You played the Guard. Name a rank from 2 to 8. If your unprotected opponent holds that rank, they are out of the hand; otherwise nothing happens."
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "guard resolve",
      "when": {
        "calc": "discard_choice == guard_rank"
      },
      "do": [
        {
          "set": {
            "key": "guess",
            "value": {
              "calc": "int($g)"
            }
          }
        },
        {
          "set": {
            "key": "effect",
            "value": "blocked",
            "if": {
              "calc": "players[opp - 1].protected == 1"
            },
            "text": "Seat {opp} is protected by a Handmaid: the Guard has no effect."
          }
        },
        {
          "set": {
            "player": {
              "calc": "opp"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[opp - 1].hand[0] == guess"
            },
            "text": "Hit! Seat {opp} holds rank {guess} and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "opp"
            },
            "to": "out",
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[opp - 1].hand[0] == guess"
            }
          }
        },
        {
          "set": {
            "key": "effect",
            "value": "miss",
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[opp - 1].hand[0] != guess"
            },
            "text": "Miss: Seat {opp} does not hold rank {guess}."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "priest",
      "when": {
        "calc": "discard_choice == priest_rank"
      },
      "do": [
        {
          "set": {
            "key": "effect",
            "value": "blocked",
            "if": {
              "calc": "players[opp - 1].protected == 1"
            },
            "text": "Seat {opp} is protected by a Handmaid: the Priest has no effect."
          }
        },
        {
          "set": {
            "key": "seen",
            "value": {
              "calc": "players[opp - 1].hand[0]"
            },
            "if": {
              "calc": "players[opp - 1].protected == 0"
            },
            "text": "Seat {opp} holds rank {seen}.",
            "announce_to": {
              "where": "you.seat == active_seat"
            }
          }
        },
        {
          "set": {
            "key": "effect",
            "value": "looked",
            "if": {
              "calc": "players[opp - 1].protected == 0"
            },
            "text": "Seat {active_seat} looked at Seat {opp}'s card."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "baron",
      "when": {
        "calc": "discard_choice == baron_rank"
      },
      "do": [
        {
          "set": {
            "key": "effect",
            "value": "blocked",
            "if": {
              "calc": "players[opp - 1].protected == 1"
            },
            "text": "Seat {opp} is protected by a Handmaid: the Baron has no effect."
          }
        },
        {
          "set": {
            "key": "seen",
            "value": {
              "calc": "min(players[active_seat - 1].hand[0], players[opp - 1].hand[0])"
            },
            "if": {
              "calc": "players[opp - 1].protected == 0"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[active_seat - 1].hand[0] < players[opp - 1].hand[0]"
            },
            "text": "Baron: Seat {active_seat} has the lower card, rank {seen}, and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "active_seat"
            },
            "to": "out",
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[active_seat - 1].hand[0] < players[opp - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "opp"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[opp - 1].hand[0] < players[active_seat - 1].hand[0]"
            },
            "text": "Baron: Seat {opp} has the lower card, rank {seen}, and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "opp"
            },
            "to": "out",
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[opp - 1].hand[0] < players[active_seat - 1].hand[0]"
            }
          }
        },
        {
          "set": {
            "key": "effect",
            "value": "tie",
            "if": {
              "calc": "players[opp - 1].protected == 0 and players[opp - 1].hand[0] == players[active_seat - 1].hand[0]"
            },
            "text": "Baron: the cards are equal. It is a tie and nobody is out."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "handmaid",
      "when": {
        "calc": "discard_choice == handmaid_rank"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "protected",
            "value": 1,
            "text": "Seat {active_seat} is protected by the Handmaid until their next turn starts."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "prince",
      "when": {
        "calc": "discard_choice == prince_rank"
      },
      "do": [
        {
          "set": {
            "key": "target",
            "value": {
              "calc": "opp if players[opp - 1].protected == 0 else active_seat"
            }
          }
        },
        {
          "set": {
            "key": "seen",
            "value": {
              "calc": "players[target - 1].hand[0]"
            }
          }
        },
        {
          "remove": {
            "player": {
              "calc": "target"
            },
            "key": "hand",
            "value": {
              "calc": "seen"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "target"
            },
            "key": "discards",
            "value": {
              "calc": "seen"
            },
            "text": "Prince: Seat {target} discards rank {seen}."
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "target"
            },
            "key": "discard_sum",
            "value": {
              "calc": "seen"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "target"
            },
            "key": "career_sum",
            "value": {
              "calc": "seen"
            }
          }
        },
        {
          "set": {
            "key": "refill",
            "value": {
              "calc": "0 if seen == princess_rank else (1 if deck_count > 0 else 2)"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "target"
            },
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "refill == 0"
            },
            "text": "Seat {target} discarded the Princess and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "target"
            },
            "to": "out",
            "if": {
              "calc": "refill == 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "refill == 1"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "target"
            },
            "key": "hand",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "refill == 1"
            },
            "text": "Seat {target} draws a new card from the deck."
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "refill == 1"
            }
          }
        },
        {
          "adjust": {
            "key": "deck_count",
            "value": -1,
            "if": {
              "calc": "refill == 1"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "target"
            },
            "key": "hand",
            "value": {
              "calc": "burned_card[0]"
            },
            "if": {
              "calc": "refill == 2 and len(burned_card) > 0"
            },
            "text": "The deck is empty: Seat {target} takes the burned card."
          }
        },
        {
          "remove": {
            "key": "burned_card",
            "value": {
              "calc": "burned_card[0]"
            },
            "if": {
              "calc": "refill == 2 and len(burned_card) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "king",
      "when": {
        "calc": "discard_choice == king_rank"
      },
      "do": [
        {
          "set": {
            "key": "effect",
            "value": "blocked",
            "if": {
              "calc": "players[opp - 1].protected == 1"
            },
            "text": "Seat {opp} is protected by a Handmaid: the King has no effect."
          }
        },
        {
          "set": {
            "key": "held",
            "value": {
              "calc": "[c for c in players[active_seat - 1].hand]"
            },
            "if": {
              "calc": "players[opp - 1].protected == 0"
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
              "calc": "[c for c in players[opp - 1].hand]"
            },
            "if": {
              "calc": "players[opp - 1].protected == 0"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "opp"
            },
            "key": "hand",
            "value": {
              "calc": "[c for c in held]"
            },
            "if": {
              "calc": "players[opp - 1].protected == 0"
            },
            "text": "King: Seat {active_seat} and Seat {opp} swap hand cards."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "effect",
      "label": "princess",
      "when": {
        "calc": "discard_choice == princess_rank"
      },
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "eliminated",
            "value": 1,
            "text": "Seat {active_seat} discarded the Princess and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": {
              "calc": "active_seat"
            },
            "to": "out"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end of turn",
      "label": "showdown",
      "when": {
        "calc": "sum([p.eliminated for p in players]) == 0 and (deck_count == 0 or round_number == total_rounds)"
      },
      "do": [
        {
          "set": {
            "key": "sd1",
            "value": {
              "calc": "players[0].hand[0]"
            }
          }
        },
        {
          "set": {
            "key": "sd2",
            "value": {
              "calc": "players[1].hand[0]"
            },
            "text": "Showdown: Seat 1 holds rank {sd1}, Seat 2 holds rank {sd2}."
          }
        },
        {
          "set": {
            "player": 1,
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "sd1 < sd2 or (sd1 == sd2 and players[0].discard_sum < players[1].discard_sum)"
            },
            "text": "Seat 1 loses the showdown and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": 1,
            "to": "out",
            "if": {
              "calc": "sd1 < sd2 or (sd1 == sd2 and players[0].discard_sum < players[1].discard_sum)"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "eliminated",
            "value": 1,
            "if": {
              "calc": "sd2 < sd1 or (sd1 == sd2 and players[1].discard_sum < players[0].discard_sum)"
            },
            "text": "Seat 2 loses the showdown and is out of the hand."
          }
        },
        {
          "set_status": {
            "player": 2,
            "to": "out",
            "if": {
              "calc": "sd2 < sd1 or (sd1 == sd2 and players[1].discard_sum < players[0].discard_sum)"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": 1,
            "if": {
              "calc": "sd1 == sd2 and players[0].discard_sum == players[1].discard_sum"
            },
            "text": "Equal cards and equal discard sums: the hand is tied and no token is awarded."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end of turn",
      "label": "award",
      "when": {
        "calc": "sum([p.eliminated for p in players]) == 1"
      },
      "do": [
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[p.seat for p in players if p.eliminated == 0][0]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "tokens",
            "value": {
              "calc": "tokens_per_hand_won"
            }
          }
        },
        {
          "set": {
            "key": "winner_tokens",
            "value": {
              "calc": "players[winner_seat - 1].tokens"
            }
          }
        },
        {
          "set": {
            "key": "hand_over",
            "value": 1
          }
        },
        {
          "set": {
            "key": "token_awarded",
            "value": 1
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "[p.seat for p in players if p.eliminated == 1][0]"
            }
          }
        }
      ],
      "text": "Seat {winner_seat} wins the hand and now has {winner_tokens} tokens. Seat {active_seat} starts the next hand."
    },
    {
      "use": "update",
      "phase": "end of turn",
      "label": "pass",
      "when": {
        "calc": "token_awarded == 0"
      },
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "3 - active_seat"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end of turn",
      "label": "after round 40",
      "when": {
        "calc": "round_number >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round_number >= total_rounds"
      },
      "rank_by": "you.tokens * 1000 + you.career_sum",
      "text": "Winner: {result}. Tokens: Seat 1 {players[0].tokens}, Seat 2 {players[1].tokens}; career sums: Seat 1 {players[0].career_sum}, Seat 2 {players[1].career_sum}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 3000,
    "deadline_s": 120
  },
  "rules": "A two-player Love Letter duel lasting exactly {total_rounds} rounds; each round is one turn of the active player (seat {starting_active_seat} goes first). The deck has {deck_size} cards: rank 1 Guard x{guard_count}, rank 2 Priest x{priest_count}, rank 3 Baron x{baron_count}, rank 4 Handmaid x{handmaid_count}, rank 5 Prince x{prince_count}, rank 6 King x{king_count}, rank 7 Countess x{countess_count}, rank 8 Princess x{princess_count}. Your hand is seen only by you; discards are public.\n\nNEW HAND: when a hand is over, all cards are gathered and shuffled. {out_of_play_size} cards go out of play: {burned_cards} face down (the burned card, kept hidden) and {face_up_out_of_play} face up, which are announced. Each player is dealt {cards_dealt_per_player} card, leaving {deck_count_after_deal} in the deck. Protection, eliminations and each player's discard_sum reset to 0.\n\nTURN: the active player's protection ends, they draw the top card (you are told the rank you kept and the rank you drew) and choose which of their two ranks to discard. If you hold the Countess (7) together with the Prince (5) or the King (6), the Countess is discarded whatever you chose. The discarded rank goes to your discards and is added to your discard_sum and career_sum, and the discard is announced. Then its effect:\n- Guard (1): name a rank from {guard_guess_min} to {guard_guess_max}. If the opponent is protected, no effect. Otherwise, if the opponent's card is that rank, they are out of the hand (a hit); if not, a miss and nothing happens.\n- Priest (2): if the opponent is protected, no effect. Otherwise you privately see the opponent's card, and the table is told you looked.\n- Baron (3): if the opponent is protected, no effect. Otherwise compare hand cards: the lower card's owner is out, and the losing rank is announced; on equal cards it is a tie and nobody is out.\n- Handmaid (4): you are protected until your next turn starts.\n- Prince (5): the target is the opponent, or yourself if the opponent is protected. The target discards their hand card (announced, and added to their discard_sum and career_sum). If it was the Princess (8), the target is out. Otherwise the target draws the top deck card if the deck has cards left, or else takes the burned card.\n- King (6): if the opponent is protected, no effect. Otherwise the two players swap hand cards, and the swap is announced.\n- Countess (7): no effect.\n- Princess (8): discarding it puts you out of the hand.\n\nSHOWDOWN: if nobody is out and the deck is empty (or it is round {total_rounds}), both hand cards are revealed and the lower card's owner is out. On equal cards, the lower discard_sum is out. If those are also equal, the hand is tied: no token is awarded and a new hand is dealt next round.\n\nAWARD: when exactly one player is out, the other gains {tokens_per_hand_won} token, a new hand is dealt next round, and the player who was out takes the first turn of it. If no token was awarded this round, the turn passes to the other seat.\n\nEND: after round {total_rounds} the game ends. More tokens wins; if tokens are equal, the higher career_sum (all ranks you discarded over the whole game, including cards a Prince forced out) wins; if both are equal, the game is a draw and the win is shared."
}
````
