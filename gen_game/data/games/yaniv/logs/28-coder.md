# 28 coder

- time: 2026-10-28T06:21:16+00:00 (165.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 a39bae997d2b3973, reply sha256 e44f9779aaa74fec

## Sent

````
# Task: write the XColos game file for "Simultaneous Yaniv"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

CARDS
- Card values: Joker = 0, Ace = 1, 2 to 10 = face value, J/Q/K = 10.
- Every random card is drawn from a 54-card shoe: two 0s, four each of 1 to 9, and sixteen 10s.
- The shoe is full for every draw, so it never runs out.
- A hand is a list of values. hand_sum is the sum of the hand. hand_size is the number of cards in it.

PARAMETERS
call_limit = 7; asaf_penalty = 30; end_total = 100; max_rounds = 30.

SETUP
- Every total is 0.
- In one deal operation, each player is dealt 5 random cards, seen only by that player.
- Each player's hand_sum is computed. Each hand_size (5) is public.

EACH ROUND (rounds 1 to 30)
1. Options. Each player's first-choice options are listed in this order:
   - 'CALL', only if their current hand_sum is 7 or less;
   - then 'discard V' for each distinct value V in their hand, V ascending.
   The current hand_sum is the one computed at the end of the previous round (step 10, or after a redeal in step 4), or at setup in round 1.
2. Talk. Everyone writes one short message at the same time without seeing the others; all messages are then shown to everyone.
3. First choice. Everyone answers at the same time with one of their options. An invalid answer counts as follows:
   - CALL if the player's hand is empty;
   - otherwise 'discard H', where H is the highest value in their hand.
4. Showdown, if at least one player chose CALL:
   a. All hands are revealed. L = the lowest hand_sum among all players.
   b. A caller scores 0 if every other player's hand_sum is strictly greater than theirs. Otherwise (Asaf) they score hand_sum + 30.
   c. A non-caller scores 0 if their hand_sum equals L, otherwise their hand_sum.
   d. Each score is added to that player's total. Discards chosen this round are ignored.
   e. If any total is now 100 or more, or this is round 30, the game ends now.
   f. Otherwise, in one deal operation (the round's only random draw), every player's hand is replaced by 5 new random cards, seen only by that player. hand_sums are recomputed, hand_sizes reset to 5 publicly, and the round ends (steps 5 to 11 are skipped).
5. Discard, if no one called:
   - Each player removes every card of their chosen value V from their hand; the hand may become empty. These cards leave play.
   - Each player's V and the number of cards they shed are announced publicly. Each player's offer is one card of value V.
6. Claim options. Each player's options are listed in this order:
   - 'BLIND';
   - then 'value V' for each distinct value offered this round by at least one OTHER player, V ascending.
7. Claim choice. Everyone answers at the same time. An invalid answer counts as BLIND.
8. Resolve claims.
   - A claim on V succeeds if exactly one player claimed V; that player adds one card of value V to their hand.
   - If two or more players claimed the same V, all of them fail.
9. Blind draw. One random card value B is drawn (the round's only random draw).
   - Every player who chose BLIND or whose claim failed adds one card of value B to their hand.
   - Each such player is told B privately.
10. Announce.
   - Every hand_sum is recomputed; this is the value step 1 of the next round uses.
   - Announced publicly for each player: discarded value, number shed, claimed value, success or failure, whether they took the blind card, and new hand_size.
   - B and hand contents stay private.
11. Final showdown, if this is round 30 and no one called this round:
   - All hands are revealed.
   - Each player scores 0 if their hand_sum equals the lowest hand_sum, otherwise their hand_sum. This is added to their total.
   - The game ends.

How the winner is decided: The game ends either after a showdown that leaves any total at 100 or more, or after a showdown in round 30 (from a call or the final showdown). The player with the lowest total wins. If two or more players share the lowest total, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Simultaneous Yaniv (3 to 5 players, best with 4)

Each round, every player secretly chooses at the same time to discard a set of equal cards or to call. Claims on cards others discarded collide, and showdowns score hand sums. The lowest total after a showdown that pushes anyone to 100, or after round 30, wins.

STATE (every item below must exist in the file):
  - each player: total (number, starts 0); everyone sees it. running penalty total; lowest wins
  - each player: hand (list, starts []); only its owner sees it. card values held, seen only by the owner
  - each player: hand_sum (number, starts 0); only its owner sees it. sum of hand, recomputed at setup, at a redeal, and at step 10 (announce); this is what decides whether CALL is offered
  - each player: hand_size (number, starts 5); everyone sees it. number of cards in hand
  - each player: revealed_hand (list, starts []); everyone sees it. copy of the hand shown to all at a showdown; empty otherwise
  - each player: first_choice (text, starts ''); everyone sees it. this round's first choice: CALL or 'discard V', revealed after the simultaneous answer
  - each player: called (bool, starts False); everyone sees it. player chose CALL this round
  - each player: discard_value (number, starts -1); everyone sees it. value V discarded this round (-1 if none); also the value of the one card this player offers
  - each player: shed_count (number, starts 0); everyone sees it. number of cards removed this round
  - each player: claim (text, starts ''); everyone sees it. claim choice: BLIND or 'value V'
  - each player: claim_success (bool, starts False); everyone sees it. claim on an offered value succeeded
  - each player: took_blind (bool, starts False); everyone sees it. player received the blind card this round
  - each player: blind_seen (number, starts -1); only its owner sees it. the blind value B, told privately to those who took it
  - each player: round_score (number, starts 0); everyone sees it. score added at the last showdown
  - the table: shoe (list, starts '[0,0, 1x4, 2x4, 3x4, 4x4, 5x4, 6x4, 7x4, 8x4, 9x4, 10x16] (54 values)'); hidden from all players. the shoe; draws pick a random element and never remove it, so it is always full
  - the table: round (number, starts 0); everyone sees it. current round number, 1 to 30
  - the table: any_call (bool, starts False); everyone sees it. at least one player chose CALL this round
  - the table: lowest_sum (number, starts 0); everyone sees it. L, the lowest hand_sum at a showdown
  - the table: lowest_count (number, starts 0); everyone sees it. number of players whose hand_sum equals L
  - the table: blind_value (number, starts -1); hidden from all players. B, this round's blind card value
  - the table: game_over (bool, starts False); everyone sees it. set true when a showdown happens in round 30
  - parameters, each kept as a table attribute: call_limit = 7, asaf_penalty = 30, end_total = 100, max_rounds = 30, hand_cards = 5, shoe_size = 54, shoe_zeros = 2, shoe_each_1_to_9 = 4, shoe_tens = 16, joker_value = 0, ace_value = 1, face_value = 10, caller_safe_score = 0, lowest_noncaller_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's total is set to 0 and game.round to 0.
  2. game.shoe is filled with the 54 values: two 0s, four each of 1 to 9, and sixteen 10s.
  3. In one deal operation, each player's hand receives 5 values drawn at random from game.shoe, without removing them from the shoe; each hand is visible only to its owner.
  4. Each player's hand_sum is computed as the sum of their hand, and hand_size is set to 5 publicly.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: game.round += 1; game.any_call = false; for each player: called = false, first_choice = '', discard_value = -1, shed_count = 0, claim = '', claim_success = false, took_blind = false, blind_seen = -1, revealed_hand = []
  2. [poll] all players answers: short text message. What happens: messages are gathered simultaneously and then broadcast to all as 'Seat {seat} says: {value}'
  3. [poll] all players answers: one of: 'CALL' (only if hand_sum <= 7), then 'discard V' for each distinct V in hand, V ascending. What happens: set first_choice. An invalid answer becomes CALL if hand is empty, otherwise 'discard H' with H = max(hand). called = (first_choice == 'CALL'); game.any_call = (count of players with called) >= 1; all first choices revealed publicly
  4. [update] all players. What happens: when game.any_call: revealed_hand = hand for every player (public); game.lowest_sum = min over players of hand_sum; game.lowest_count = count of players with hand_sum == game.lowest_sum
  5. [update] all players. What happens: when game.any_call: for each player, round_score = if called then (if hand_sum == game.lowest_sum and game.lowest_count == 1 then 0 else hand_sum + 30) else (if hand_sum == game.lowest_sum then 0 else hand_sum); total += round_score; if game.round == 30 then game.game_over = true; announce each round_score and total publicly; discards chosen this round are ignored
  6. [check] all players. What happens: end the game if game.any_call and (max over players of total >= 100 or game.game_over)
  7. [update] all players. What happens: when game.any_call: in one deal operation, each hand is replaced by 5 random values from game.shoe (shoe not depleted), visible only to the owner; hand_sum = sum(hand); hand_size = 5 (public); revealed_hand = []. Steps 8 to 13 are skipped because each carries the condition not game.any_call
  8. [update] all players. What happens: when not game.any_call: V = value in first_choice; discard_value = V; shed_count = count of V in hand; remove every V from hand (the cards leave play); announce publicly each player's discard_value and shed_count. Each player offers one card of value discard_value
  9. [poll] all players answers: one of: 'BLIND', then 'value V' for each distinct V offered as discard_value by at least one OTHER player, V ascending. What happens: when not game.any_call: set claim; an invalid answer becomes 'BLIND'
  10. [update] all players. What happens: when not game.any_call: for each player with claim 'value V': claim_success = (count of players with claim == 'value V') == 1; if claim_success, append V to hand
  11. [update] all players. What happens: when not game.any_call: game.blind_value = one random value from game.shoe (not removed); for each player with claim == 'BLIND' or not claim_success: append game.blind_value to hand, took_blind = true, blind_seen = game.blind_value (told privately)
  12. [update] all players. What happens: when not game.any_call: hand_sum = sum(hand); hand_size = length(hand); announce publicly for each player: discard_value, shed_count, claim, claim_success, took_blind, hand_size. B and hand contents stay private
  13. [update] all players. What happens: when not game.any_call and game.round == 30: revealed_hand = hand for all; game.lowest_sum = min hand_sum; round_score = if hand_sum == game.lowest_sum then 0 else hand_sum; total += round_score; game.game_over = true; announce publicly
  14. [check] all players. What happens: end the game if game.game_over or max over players of total >= 100

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Card values are Joker = 0, Ace = 1, 2 to 10 at face value, and J/Q/K = 10. The shoe holds two 0s, four each of 1 to 9, and sixteen 10s (54 cards).
  R2. Every random draw picks a value from the full 54-card shoe; the shoe never shrinks or runs out.
  R3. At setup, every total is 0, each player is dealt 5 private cards, hand_sum is their sum, and hand_size 5 is public.
  R4. When a player's current hand_sum is 7 or less, 'CALL' is offered first; otherwise it is not offered.
  R5. A player is offered 'discard V' for each distinct value V in their hand, in ascending order.
  R6. Before the first choice, every player writes one message simultaneously, and all messages are then shown to everyone.
  R7. First choices are made simultaneously. An invalid answer becomes CALL if the hand is empty, otherwise 'discard H' where H is the highest value in the hand.
  R8. When at least one player calls, all hands are revealed and L is the lowest hand_sum.
  R9. When a caller's hand_sum is strictly lower than every other player's, the caller scores 0.
  R10. When a caller's hand_sum is tied with or above another player's, the caller scores hand_sum + 30 (Asaf); for example, a caller with 5 tied by another 5 scores 35.
  R11. When a non-caller's hand_sum equals L, they score 0; otherwise they score their hand_sum.
  R12. When anyone calls, discards chosen that round are ignored.
  R13. When a showdown leaves any total at 100 or more, the game ends.
  R14. When a call happens in round 30, the game ends after that showdown.
  R15. When a showdown does not end the game, every hand is replaced by 5 new random cards, hand_size is reset to 5, and the round ends with no discard, claim or blind draw.
  R16. When no one calls, each player removes every card of their chosen value V; the hand may become empty.
  R17. When no one calls, each player's V and the number of cards shed are announced publicly.
  R18. Claim options are 'BLIND' followed by 'value V' for each distinct V offered by at least one other player, in ascending order; a player is never offered only their own offered value.
  R19. Claims are made simultaneously, and an invalid claim counts as BLIND.
  R20. When exactly one player claims value V, that player adds one card of value V to their hand.
  R21. When two or more players claim the same V, all of their claims fail.
  R22. One blind value B is drawn per no-call round; every player who chose BLIND or whose claim failed adds one card of value B and is told B privately.
  R23. After claims, hand_sum and hand_size are recomputed, and each player's discarded value, number shed, claim, success, whether they took the blind card, and hand_size are announced; B and hands stay private.
  R24. When round 30 ends with no call, all hands are revealed, each player scores 0 if their hand_sum equals the lowest hand_sum and otherwise their hand_sum, and the game ends.
  R25. When the game ends, the lowest total wins, and players tied at the lowest total share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all players | options: any short text
  - First choice | asked: all players | options: a seat with hand_sum <= 7: 'CALL', then 'discard V' for each distinct value in its hand, ascending; a seat with hand_sum > 7: only the 'discard V' options; a seat with an empty hand: only 'CALL'
  - Claim choice | asked: all players (only in rounds with no call) | options: 'BLIND', then 'value V' for each distinct discard_value offered by at least one other seat, ascending; a value offered only by this seat is not listed

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.game_over == true or max over players of total >= 100
  - each player's standing: 0 - you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total, and lower is better. The player with the lowest total wins, and players tied at the lowest total share the win (a draw among them).
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

- each player: `total` (number, visible: public, starts 0): running penalty total; lowest wins
- each player: `hand_size` (number, visible: public, starts 5): number of cards in hand
- each player: `revealed_hand` (list, visible: public, starts []): copy of the hand shown to all at a showdown; empty otherwise
- each player: `called` (bool, visible: public, starts False): player chose CALL this round
- each player: `discard_value` (number, visible: public, starts -1): value V discarded this round (-1 if none); also the value of the one card this player offers
- each player: `shed_count` (number, visible: public, starts 0): number of cards removed this round
- each player: `claim` (text, visible: public, starts ''): claim choice: BLIND or 'value V'
- each player: `claim_success` (bool, visible: public, starts False): claim on an offered value succeeded
- each player: `took_blind` (bool, visible: public, starts False): player received the blind card this round
- each player: `round_score` (number, visible: public, starts 0): score added at the last showdown
- the table: `round` (number, visible: public, starts 0): current round number, 1 to 30
- the table: `any_call` (bool, visible: public, starts False): at least one player chose CALL this round
- the table: `lowest_sum` (number, visible: public, starts 0): L, the lowest hand_sum at a showdown
- the table: `game_over` (bool, visible: public, starts False): set true when a showdown happens in round 30
- parameters (each must be an attribute holding this value, never a number buried in a step): call_limit = 7, asaf_penalty = 30, end_total = 100, max_rounds = 30, hand_cards = 5, shoe_size = 54, shoe_zeros = 2, shoe_each_1_to_9 = 4, shoe_tens = 16, joker_value = 0, ace_value = 1, face_value = 10, caller_safe_score = 0, lowest_noncaller_score = 0
- the game ends with ONE ending whose `rank_by` is `0 - you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "simultaneous_yaniv",
    "name": "Simultaneous Yaniv",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Everyone secretly discards a set of equal cards or calls at the same moment; claims on discards collide, and showdowns score hand sums. Lowest total wins."
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
        "key": "total",
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
        "key": "hand_sum",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "revealed_hand",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "first_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "called",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "discard_value",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "shed_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "claim",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "claim_success",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "took_blind",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "blind_seen",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "round_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "claim_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "shoe",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "any_call",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "lowest_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lowest_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blind_value",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "call_limit",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "asaf_penalty",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "end_total",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "hand_cards",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "shoe_size",
        "visible": "public",
        "type": "number",
        "initial": 54
      },
      {
        "key": "shoe_zeros",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "shoe_each_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "shoe_tens",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "joker_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ace_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "face_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "caller_safe_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lowest_noncaller_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_values",
        "visible": "none",
        "type": "list",
        "initial": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      },
      {
        "key": "discard_labels",
        "visible": "none",
        "type": "list",
        "initial": [
          "discard 0",
          "discard 1",
          "discard 2",
          "discard 3",
          "discard 4",
          "discard 5",
          "discard 6",
          "discard 7",
          "discard 8",
          "discard 9",
          "discard 10"
        ]
      },
      {
        "key": "claim_labels",
        "visible": "none",
        "type": "list",
        "initial": [
          "value 0",
          "value 1",
          "value 2",
          "value 3",
          "value 4",
          "value 5",
          "value 6",
          "value 7",
          "value 8",
          "value 9",
          "value 10"
        ]
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the shoe",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "shoe",
            "value": [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "hand_cards"
            }
          }
        }
      ],
      "text": "Each player is dealt {hand_cards} private cards."
    },
    {
      "use": "sync",
      "label": "your starting hand",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "any_call",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "first_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard_value",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shed_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_success",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "took_blind",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blind_seen",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "first_offer",
            "value": {
              "calc": "(['CALL'] if you.hand_sum <= call_limit else []) + [discard_labels[v] for v in card_values if v in you.hand]"
            }
          }
        }
      ],
      "text": "Round {round} of {max_rounds} begins."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Round {round}. Say one short thing to the table. Everyone writes at the same time; all messages are then shown to everyone."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "first choice",
      "to": {
        "where": "len(you.first_offer) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "first_offer"
        }
      },
      "store": "first_choice",
      "text": "Round {round}. Choose at the same time as everyone else: CALL (only offered when your hand sum is {call_limit} or less) or 'discard V' to discard every card of value V in your hand."
    },
    {
      "use": "update",
      "phase": "choose",
      "label": "first choices revealed",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "first_choice",
            "value": {
              "calc": "you.first_choice if you.first_choice in you.first_offer else ('CALL' if len(you.hand) == 0 else discard_labels[max(you.hand)])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": {
              "calc": "you.first_choice == 'CALL'"
            }
          }
        },
        {
          "set": {
            "key": "any_call",
            "value": {
              "calc": "count(p.called for p in players) >= 1"
            }
          }
        }
      ],
      "text": "First choices [seat, choice]: {[[p.seat, p.first_choice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "showdown",
      "when": {
        "calc": "any_call"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": {
              "calc": "you.hand"
            }
          }
        },
        {
          "set": {
            "key": "lowest_sum",
            "value": {
              "calc": "min([p.hand_sum for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "lowest_count",
            "value": {
              "calc": "count(p.hand_sum == lowest_sum for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "round_score",
            "value": {
              "calc": "(caller_safe_score if (you.hand_sum == lowest_sum and lowest_count == 1) else you.hand_sum + asaf_penalty) if you.called else (lowest_noncaller_score if you.hand_sum == lowest_sum else you.hand_sum)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.round_score"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": {
              "calc": "round >= max_rounds"
            }
          }
        }
      ],
      "text": "Showdown! Lowest hand sum L = {lowest_sum}. Discards this round are ignored. [seat, hand, hand sum, score, total]: {[[p.seat, p.revealed_hand, sum(p.revealed_hand), p.round_score, p.total] for p in players]}."
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "redeal",
      "when": {
        "calc": "any_call and not game_over and max([p.total for p in players]) < end_total"
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
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "hand_cards"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": []
          }
        }
      ],
      "text": "Every hand is replaced by {hand_cards} new cards. The round ends."
    },
    {
      "use": "update",
      "phase": "discard",
      "label": "discard",
      "when": {
        "calc": "not any_call"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "discard_value",
            "value": {
              "calc": "max([v for v in card_values if discard_labels[v] == you.first_choice] + [-1])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shed_count",
            "value": {
              "calc": "count(c == you.discard_value for c in you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in you.hand if c != you.discard_value]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_offer",
            "value": {
              "calc": "['BLIND'] + [claim_labels[v] for v in card_values if count(p.discard_value == v and p.seat != you.seat for p in players) > 0]"
            }
          }
        }
      ],
      "text": "Discards [seat, value, cards shed]: {[[p.seat, p.discard_value, p.shed_count] for p in players]}. Each player offers one card of the value they discarded."
    },
    {
      "use": "poll",
      "phase": "claim",
      "label": "claim choice",
      "when": {
        "calc": "not any_call"
      },
      "to": {
        "where": "len(you.claim_offer) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "claim_offer"
        }
      },
      "store": "claim",
      "text": "Claim at the same time as everyone else: BLIND to take the blind card, or 'value V' to claim a card of value V offered by another player. A claim succeeds only if nobody else claims the same value; if it fails you take the blind card instead."
    },
    {
      "use": "update",
      "phase": "claim",
      "label": "resolve claims and blind draw",
      "when": {
        "calc": "not any_call"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "claim",
            "value": {
              "calc": "you.claim if you.claim in you.claim_offer else 'BLIND'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_success",
            "value": {
              "calc": "you.claim != 'BLIND' and count(p.claim == you.claim for p in players) == 1"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.claim_success"
            },
            "key": "hand",
            "value": {
              "calc": "max([v for v in card_values if claim_labels[v] == you.claim] + [-1])"
            }
          }
        },
        {
          "set": {
            "key": "blind_value",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "not you.claim_success"
            },
            "key": "hand",
            "value": {
              "calc": "blind_value"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.claim_success"
            },
            "key": "took_blind",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.claim_success"
            },
            "key": "blind_seen",
            "value": {
              "calc": "blind_value"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ],
      "text": "Round {round} results [seat, discarded, shed, claim, claim succeeded, took blind, hand size]: {[[p.seat, p.discard_value, p.shed_count, p.claim, p.claim_success, p.took_blind, p.hand_size] for p in players]}."
    },
    {
      "use": "tell",
      "phase": "claim",
      "label": "your blind card",
      "when": {
        "calc": "not any_call"
      },
      "to": {
        "where": "you.took_blind"
      },
      "text": "You took the blind card. Its value is {blind_seen}."
    },
    {
      "use": "update",
      "phase": "final",
      "label": "final showdown",
      "when": {
        "calc": "not any_call and round >= max_rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": {
              "calc": "you.hand"
            }
          }
        },
        {
          "set": {
            "key": "lowest_sum",
            "value": {
              "calc": "min([p.hand_sum for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "lowest_count",
            "value": {
              "calc": "count(p.hand_sum == lowest_sum for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "round_score",
            "value": {
              "calc": "lowest_noncaller_score if you.hand_sum == lowest_sum else you.hand_sum"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.round_score"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": true
          }
        }
      ],
      "text": "Final showdown! Lowest hand sum = {lowest_sum}. [seat, hand, hand sum, score, total]: {[[p.seat, p.revealed_hand, sum(p.revealed_hand), p.round_score, p.total] for p in players]}."
    },
    {
      "use": "check",
      "phase": "final",
      "label": "end of round",
      "when": {
        "calc": "game_over or round >= max_rounds or max([p.total for p in players]) >= end_total"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "game_over or round >= max_rounds or max([p.total for p in players]) >= end_total"
      },
      "rank_by": "0 - you.total",
      "text": "Winner: {result} (lowest total). Final totals [seat, total]: {[[p.seat, p.total] for p in players]}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "CARDS. Card values: Joker = {joker_value}, Ace = {ace_value}, 2 to 10 at face value, J/Q/K = {face_value}. Every random card is drawn from a {shoe_size}-card shoe: {shoe_zeros} zeros, {shoe_each_1_to_9} each of 1 to 9, and {shoe_tens} tens. The shoe is full for every draw, so it never runs out. Your hand is a list of values; your hand sum is its total and only you see it. Everyone sees each hand size.\n\nSETUP. Every total starts at 0. Each player is dealt {hand_cards} private cards.\n\nEACH ROUND (up to {max_rounds} rounds):\n1. Options. You are offered 'CALL' first only if your current hand sum is {call_limit} or less (otherwise CALL is not offered), then 'discard V' for each distinct value V in your hand, ascending. With an empty hand you are offered only CALL. If you have only one possible option, it is taken for you.\n2. Talk. Everyone writes one short message at the same time; all messages are then shown to everyone.\n3. First choice. Everyone answers at the same time with one of their options. An invalid answer counts as CALL if your hand is empty, otherwise as 'discard H' where H is the highest value in your hand. All first choices are revealed.\n4. Showdown, if at least one player chose CALL: all hands are revealed a
... (cut)

Why it was refused: playing it with random seats failed: seed 2, 5 players: the match did not end (abandoned: turn cap of 400 reached)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "simultaneous_yaniv",
    "name": "Simultaneous Yaniv",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Everyone secretly discards a set of equal cards or calls at the same moment; claims on discards collide, and showdowns score hand sums. Lowest total wins."
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
        "key": "total",
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
        "key": "hand_sum",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "revealed_hand",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "first_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "called",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "discard_value",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "shed_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "claim",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "claim_success",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "took_blind",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "blind_seen",
        "visible": "ally",
        "type": "number",
        "initial": -1
      },
      {
        "key": "round_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "first_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "claim_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "shoe",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "any_call",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "lowest_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lowest_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blind_value",
        "visible": "none",
        "type": "number",
        "initial": -1
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "call_limit",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "asaf_penalty",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "end_total",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "hand_cards",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "shoe_size",
        "visible": "public",
        "type": "number",
        "initial": 54
      },
      {
        "key": "shoe_zeros",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "shoe_each_1_to_9",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "shoe_tens",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "joker_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ace_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "face_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "caller_safe_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lowest_noncaller_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_values",
        "visible": "none",
        "type": "list",
        "initial": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10
        ]
      },
      {
        "key": "discard_labels",
        "visible": "none",
        "type": "list",
        "initial": [
          "discard 0",
          "discard 1",
          "discard 2",
          "discard 3",
          "discard 4",
          "discard 5",
          "discard 6",
          "discard 7",
          "discard 8",
          "discard 9",
          "discard 10"
        ]
      },
      {
        "key": "claim_labels",
        "visible": "none",
        "type": "list",
        "initial": [
          "value 0",
          "value 1",
          "value 2",
          "value 3",
          "value 4",
          "value 5",
          "value 6",
          "value 7",
          "value 8",
          "value 9",
          "value 10"
        ]
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the shoe",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "shoe",
            "value": [
              0, 0,
              1, 1, 1, 1,
              2, 2, 2, 2,
              3, 3, 3, 3,
              4, 4, 4, 4,
              5, 5, 5, 5,
              6, 6, 6, 6,
              7, 7, 7, 7,
              8, 8, 8, 8,
              9, 9, 9, 9,
              10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10
            ]
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "hand_cards"
            }
          }
        }
      ],
      "text": "Each player is dealt {hand_cards} private cards."
    },
    {
      "use": "sync",
      "label": "your starting hand",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "a new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "any_call",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "first_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "discard_value",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shed_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_success",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "took_blind",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blind_seen",
            "value": -1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "first_offer",
            "value": {
              "calc": "(['CALL'] if (you.hand_sum <= call_limit or len(you.hand) == 0) else []) + [discard_labels[v] for v in card_values if v in you.hand]"
            }
          }
        }
      ],
      "text": "Round {round} of {max_rounds} begins."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Round {round}. Say one short thing to the table. Everyone writes at the same time; all messages are then shown to everyone."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "first choice",
      "to": {
        "where": "len(you.first_offer) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "first_offer"
        }
      },
      "store": "first_choice",
      "text": "Round {round}. Choose at the same time as everyone else: CALL (only offered when your hand sum is {call_limit} or less) or 'discard V' to discard every card of value V in your hand."
    },
    {
      "use": "update",
      "phase": "choose",
      "label": "first choices revealed",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "first_choice",
            "value": {
              "calc": "you.first_choice if you.first_choice in you.first_offer else ('CALL' if len(you.hand) == 0 else discard_labels[max(you.hand)])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "called",
            "value": {
              "calc": "you.first_choice == 'CALL'"
            }
          }
        },
        {
          "set": {
            "key": "any_call",
            "value": {
              "calc": "count(p.called for p in players) >= 1"
            }
          }
        }
      ],
      "text": "First choices [seat, choice]: {[[p.seat, p.first_choice] for p in players]}."
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "showdown",
      "when": {
        "calc": "any_call"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": {
              "calc": "you.hand"
            }
          }
        },
        {
          "set": {
            "key": "lowest_sum",
            "value": {
              "calc": "min([p.hand_sum for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "lowest_count",
            "value": {
              "calc": "count(p.hand_sum == lowest_sum for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "round_score",
            "value": {
              "calc": "(caller_safe_score if (you.hand_sum == lowest_sum and lowest_count == 1) else you.hand_sum + asaf_penalty) if you.called else (lowest_noncaller_score if you.hand_sum == lowest_sum else you.hand_sum)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.round_score"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": {
              "calc": "round >= max_rounds"
            }
          }
        }
      ],
      "text": "Showdown! Lowest hand sum L = {lowest_sum}. Discards this round are ignored. [seat, hand, hand sum, score, total]: {[[p.seat, p.revealed_hand, sum(p.revealed_hand), p.round_score, p.total] for p in players]}."
    },
    {
      "use": "update",
      "phase": "showdown",
      "label": "redeal",
      "when": {
        "calc": "any_call and not game_over and max([p.total for p in players]) < end_total"
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
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "hand_cards"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": []
          }
        }
      ],
      "text": "Every hand is replaced by {hand_cards} new cards. The round ends."
    },
    {
      "use": "update",
      "phase": "discard",
      "label": "discard",
      "when": {
        "calc": "not any_call"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "discard_value",
            "value": {
              "calc": "max([v for v in card_values if discard_labels[v] == you.first_choice] + [-1])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shed_count",
            "value": {
              "calc": "count(c == you.discard_value for c in you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[c for c in you.hand if c != you.discard_value]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_offer",
            "value": {
              "calc": "['BLIND'] + [claim_labels[v] for v in card_values if count(p.discard_value == v and p.seat != you.seat for p in players) > 0]"
            }
          }
        }
      ],
      "text": "Discards [seat, value, cards shed]: {[[p.seat, p.discard_value, p.shed_count] for p in players]}. Each player offers one card of the value they discarded."
    },
    {
      "use": "poll",
      "phase": "claim",
      "label": "claim choice",
      "when": {
        "calc": "not any_call"
      },
      "to": {
        "where": "len(you.claim_offer) > 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "claim_offer"
        }
      },
      "store": "claim",
      "text": "Claim at the same time as everyone else: BLIND to take the blind card, or 'value V' to claim a card of value V offered by another player. A claim succeeds only if nobody else claims the same value; if it fails you take the blind card instead."
    },
    {
      "use": "update",
      "phase": "claim",
      "label": "resolve claims and blind draw",
      "when": {
        "calc": "not any_call"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "claim",
            "value": {
              "calc": "you.claim if you.claim in you.claim_offer else 'BLIND'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "claim_success",
            "value": {
              "calc": "you.claim != 'BLIND' and count(p.claim == you.claim for p in players) == 1"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.claim_success"
            },
            "key": "hand",
            "value": {
              "calc": "max([v for v in card_values if claim_labels[v] == you.claim] + [-1])"
            }
          }
        },
        {
          "set": {
            "key": "blind_value",
            "value": {
              "calc": "shoe[min(int(uniform(0, len(shoe))), len(shoe) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "not you.claim_success"
            },
            "key": "hand",
            "value": {
              "calc": "blind_value"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.claim_success"
            },
            "key": "took_blind",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.claim_success"
            },
            "key": "blind_seen",
            "value": {
              "calc": "blind_value"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_sum",
            "value": {
              "calc": "sum(you.hand)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand_size",
            "value": {
              "calc": "len(you.hand)"
            }
          }
        }
      ],
      "text": "Round {round} results [seat, discarded, shed, claim, claim succeeded, took blind, hand size]: {[[p.seat, p.discard_value, p.shed_count, p.claim, p.claim_success, p.took_blind, p.hand_size] for p in players]}."
    },
    {
      "use": "tell",
      "phase": "claim",
      "label": "your blind card",
      "when": {
        "calc": "not any_call"
      },
      "to": {
        "where": "you.took_blind"
      },
      "text": "You took the blind card. Its value is {blind_seen}."
    },
    {
      "use": "update",
      "phase": "final",
      "label": "final showdown",
      "when": {
        "calc": "not any_call and round >= max_rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "revealed_hand",
            "value": {
              "calc": "you.hand"
            }
          }
        },
        {
          "set": {
            "key": "lowest_sum",
            "value": {
              "calc": "min([p.hand_sum for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "lowest_count",
            "value": {
              "calc": "count(p.hand_sum == lowest_sum for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "round_score",
            "value": {
              "calc": "lowest_noncaller_score if you.hand_sum == lowest_sum else you.hand_sum"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "you.round_score"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": true
          }
        }
      ],
      "text": "Final showdown! Lowest hand sum = {lowest_sum}. [seat, hand, hand sum, score, total]: {[[p.seat, p.revealed_hand, sum(p.revealed_hand), p.round_score, p.total] for p in players]}."
    },
    {
      "use": "check",
      "phase": "final",
      "label": "end of round",
      "when": {
        "calc": "game_over or round >= max_rounds or max([p.total for p in players]) >= end_total"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "game_over or round >= max_rounds or max([p.total for p in players]) >= end_total"
      },
      "rank_by": "0 - you.total",
      "text": "Winner: {result} (lowest total). Final totals [seat, total]: {[[p.seat, p.total] for p in players]}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 10000,
    "deadline_s": 120
  },
  "rules": "CARDS. Card values: Joker = {joker_value}, Ace = {ace_value}, 2 to 10 at face value, J/Q/K = {face_value}. Every random card is drawn from a {shoe_size}-card shoe: {shoe_zeros} zeros, {shoe_each_1_to_9} each of 1 to 9, and {shoe_tens} tens. The shoe is full for every draw, so it never runs out. Your hand is a list of values; your hand sum is its total and only you see it. Everyone sees each hand size.\n\nSETUP. Every total starts at 0. Each player is dealt {hand_cards} private cards; hand sizes ({hand_cards}) are public.\n\nEACH ROUND (up to {max_rounds} rounds):\n1. Options. You are offered 'CALL' first only if your current hand sum is {call_limit} or less (otherwise CALL is not offered), then 'discard V' for each distinct value V in your hand, ascending. With an empty hand you are offered only CALL. If you have only one possible option, it is taken for you.\n2. Talk. Everyone writes one short message at the same time without seeing the others; all messages are then shown to everyone.\n3. First choice. Everyone answers at the same time with one of their options. An invalid answer counts as CALL if your hand is empty, otherwise as 'discard H' where H is the highest value in your hand. All first choices are revealed.\n4. Showdown, if at least one player chose CALL: all hands are revealed and L is the lowest hand sum. A caller scores {caller_safe_score} if every other player's hand sum is strictly greater than theirs; otherwise (Asaf) the caller scores hand sum + {asaf_penalty} (a caller with 5 tied by another 5 scores 35). A non-caller scores {lowest_noncaller_score} if their hand sum equals L, otherwise their hand sum. Each score is added to that player's total. Discards chosen this round are ignored. If any total is now {end_total} or more, or this is round {max_rounds}, the game ends. Otherwise every hand is replaced by {hand_cards} new random cards, hand sizes reset to {hand_cards}, and the round ends with no discard, claim or blind draw.\n5. Discard, if no one called: each player removes every card of their chosen value V from their hand; the hand may become empty. These cards leave play. Each player's V and the number of cards they shed are announced publicly. Each player offers one card of value V.\n6. Claim options: 'BLIND', then 'value V' for each distinct value offered this round by at least one OTHER player, ascending. A value offered only by you is not listed. If BLIND is your only option it is taken for you.\n7. Claim choice. Everyone answers at the same time. An invalid answer counts as BLIND.\n8. Resolve claims. A claim on V succeeds if exactly one player claimed V: that player adds one card of value V to their hand. If two or more players claimed the same V, all of their claims fail and none of them gets that card.\n9. Blind draw. One random card value B is drawn. Every player who chose BLIND or whose claim failed adds one card of value B to their hand and is told B privately. A player whose claim succeeded does not take the blind card.\n10. Announce. Every hand sum is recomputed (this is the hand sum the next round's CALL option uses). Announced publicly for each player: discarded value, number shed, claimed value, success or failure, whether they took the blind card, and new hand size. B and hand contents stay private.\n11. Final showdown, if this is round {max_rounds} and no one called this round: all hands are revealed; each player scores 0 if their hand sum equals the lowest hand sum, otherwise their hand sum, added to their total. The game ends.\n\nWINNING. The game ends after a showdown that leaves any total at {end_total} or more, or after a showdown in round {max_rounds} (from a call or the final showdown). The player with the lowest total wins; players tied at the lowest total share the win."
}
````
