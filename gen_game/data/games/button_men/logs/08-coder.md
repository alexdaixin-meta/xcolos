# 08 coder

- time: 2026-10-28T05:20:46+00:00 (149.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 87cbfd8bd2d91e7a, reply sha256 6158228bd6720020

## Sent

````
# Task: write the XColos game file for "Loaded Button Men"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DICE. Each player owns four dice: a d4, a d6, a d8 and a d12.
- A die's SIZE is its number of sides (4, 6, 8 or 12). Sizes are public.
- A die's VALUE is a whole number from 1 to its size. A player always knows their own values. A player is never told the opponent's values, except as stated below.
- Each player has a SCORE that starts at 0 and carries over between legs.

MATCH STRUCTURE.
- The match has two legs: leg 1 is turns 1 to 20 and leg 2 is turns 21 to 40.
- Before turn 1, one player is chosen at random to be First.
- Leg 1: First acts on odd turns (1, 3, ..., 19) and the other player, Second, acts on even turns (2, 4, ..., 20).
- Leg 2: Second acts on odd turns (21, 23, ..., 39) and First acts on even turns (22, ..., 40).

LOADING (at the start of each leg, on turns 1 and 21).
- Both players at the same moment secretly choose a value for each of their four dice.
- Each value must be at least 1 and at most that die's size, and the four values must total exactly 16.
- An invalid loading is replaced by the default loading: d4=2, d6=3, d8=4, d12=7.
- All four dice of both players are in play at the start of each leg. Captures from leg 1 do not carry over, but scores do.

EACH TURN (while the current leg is not over):
1. Public status. Announce the turn number, the leg, whose turn it is, which die sizes each player still has in play, both scores, and whether the previous turn in this leg was a pass.
2. Private status. Tell each player the current values of their own remaining dice.
3. Choice. The active player either PASSES or declares an ATTACK:
   - one of the opponent's remaining dice as TARGET, and
   - either one of their own remaining dice (a POWER attack) or exactly two different dice of their own (a SKILL attack).
   A die may not be listed twice. Any declaration that breaks these rules counts as a pass.
4. Resolution.
   - A power attack succeeds if the attacker's value is greater than or equal to the target's value.
   - A skill attack succeeds if the two attackers' values sum exactly to the target's value.
5. Public result. Announce the pass, or the target size, the attacking die sizes and whether the attack succeeded.
6. Success.
   - The target is captured and removed from the leg.
   - Its value is announced publicly.
   - The attacker's score rises by the target's size.
   - The attacking die (in a skill attack, only the larger-size of the two) is rerolled to a uniformly random value from 1 to its size. Its new value is told only to its owner.
   - In a skill attack the smaller attacker keeps its value.
7. Failure.
   - The attacking die is captured by the defender. In a skill attack, only the larger-size attacker is captured; the smaller stays in play with its value unchanged.
   - The captured die's value is announced publicly.
   - The defender's score rises by the captured die's size.
   - Nothing is rerolled, and the target's value is not revealed.
8. Leg end check. The leg ends immediately if any of these is true:
   - either player has no dice left;
   - this turn and the previous turn in this leg were both passes;
   - this is turn 20 (for leg 1).
   If leg 1 ends early, the remaining turns up to 20 are skipped with no actions.
9. Match end. After turn 40, or when leg 2 ends, the match ends.

NOTES.
- Values change only by loading at the start of a leg or by the reroll after a successful attack.
- Captured dice never return within a leg.
- Captures are not compulsory: a player may always pass.

How the winner is decided: When the match ends, the player with the higher score (total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks) wins. Equal scores are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Loaded Button Men (2 to 2 players, best with 2)

Two players secretly load four dice (d4, d6, d8, d12) to total 16, then take turns capturing each other's dice with power or skill attacks over two 20-turn legs; the higher total of captured sizes wins.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total sizes of all dice this player has captured across both legs
  - each player: is_first (bool, starts False); everyone sees it. True for the player chosen at random to be First
  - each player: in_play (list, starts [4, 6, 8, 12]); everyone sees it. Sizes of this player's dice still in play this leg
  - each player: d4_value (number, starts 2); only its owner sees it. Current value of this player's d4 (1-4)
  - each player: d6_value (number, starts 3); only its owner sees it. Current value of this player's d6 (1-6)
  - each player: d8_value (number, starts 4); only its owner sees it. Current value of this player's d8 (1-8)
  - each player: d12_value (number, starts 7); only its owner sees it. Current value of this player's d12 (1-12)
  - each player: load_d4 (number, starts 0); only its owner sees it. Loading answer for the d4, before validation
  - each player: load_d6 (number, starts 0); only its owner sees it. Loading answer for the d6, before validation
  - each player: load_d8 (number, starts 0); only its owner sees it. Loading answer for the d8, before validation
  - each player: load_d12 (number, starts 0); only its owner sees it. Loading answer for the d12, before validation
  - the table: turn (number, starts 0); everyone sees it. Current turn number, 1 to 40
  - the table: leg (number, starts 1); everyone sees it. Current leg, 1 or 2
  - the table: first_seat (number, starts 0); everyone sees it. Seat of the player who is First
  - the table: active_seat (number, starts 0); everyone sees it. Seat acting this turn
  - the table: previous_was_pass (bool, starts False); everyone sees it. Whether the previous turn in this leg was a pass
  - the table: this_is_pass (bool, starts False); everyone sees it. Whether this turn's action is a pass
  - the table: declaration (text, starts ''); everyone sees it. The active player's chosen declaration this turn
  - the table: target_size (number, starts 0); everyone sees it. Size of the declared target die
  - the table: attacker_large_size (number, starts 0); everyone sees it. Size of the power attacker, or the larger-size skill attacker
  - the table: attacker_small_size (number, starts 0); everyone sees it. Size of the smaller-size skill attacker (0 for a power attack)
  - the table: attack_value (number, starts 0); hidden from all players. Scratch copy of the attacking value (power) or the sum of the two values (skill)
  - the table: target_value (number, starts 0); hidden from all players. Scratch copy of the target's value
  - the table: attack_success (bool, starts False); everyone sees it. Whether this turn's attack succeeded
  - the table: leg_over (bool, starts False); everyone sees it. True once the current leg has ended
  - the table: match_over (bool, starts False); everyone sees it. True once the match has ended
  - parameters, each kept as a table attribute: d4_size = 4, d6_size = 6, d8_size = 8, d12_size = 12, dice_per_player = 4, load_total = 16, default_d4 = 2, default_d6 = 3, default_d8 = 4, default_d12 = 7, legs = 2, turns_per_leg = 20, leg1_first_turn = 1, leg1_last_turn = 20, leg2_first_turn = 21, leg2_last_turn = 40, consecutive_passes_to_end_leg = 2, skill_attack_dice = 2, power_attack_dice = 1, starting_score = 0, min_die_value = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Each player's score is set to 0.
  2. One seat is chosen uniformly at random to be First: first_seat is set to that seat and its is_first is set to true; the other seat is Second.
  3. turn is set to 0 and leg to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: turn += 1; leg = 1 if turn <= 20, otherwise 2. If turn == 21, set leg_over = false. active_seat = first_seat when (turn is odd and leg == 1) or (turn is even and leg == 2); otherwise active_seat = the other seat.
  2. [poll] all players answers: a whole number 1-4 for the d4. What happens: Runs only when turn == 1 or turn == 21. Stores the answer in each player's load_d4. Nobody sees any answer.
  3. [poll] all players answers: a whole number 1-6 for the d6. What happens: Runs only when turn == 1 or turn == 21. Stores the answer in load_d6.
  4. [poll] all players answers: a whole number 1-8 for the d8. What happens: Runs only when turn == 1 or turn == 21. Stores the answer in load_d8.
  5. [poll] all players answers: a whole number 1-12 for the d12. What happens: Runs only when turn == 1 or turn == 21. Stores the answer in load_d12.
  6. [update] all players. What happens: Runs only when turn == 1 or turn == 21. For each player: if load_d4 + load_d6 + load_d8 + load_d12 == 16, then d4_value = load_d4, d6_value = load_d6, d8_value = load_d8 and d12_value = load_d12; otherwise d4_value = 2, d6_value = 3, d8_value = 4 and d12_value = 7. For both players, in_play = [4, 6, 8, 12]. previous_was_pass = false. Announces only that loading is done.
  7. [tell] all players. What happens: Runs only when leg_over == false. Public status: turn, leg, active_seat, each player's in_play, both scores, and previous_was_pass.
  8. [sync] all players. What happens: Runs only when leg_over == false. Each player privately receives the values (d4_value, d6_value, d8_value, d12_value) of the dice in their own in_play.
  9. [ask] seat active_seat answers: one choice: 'pass', or 'power: my dA -> your dT' for each own die A in in_play and each opponent die T in the opponent's in_play, or 'skill: my dA + my dB -> your dT' for each unordered pair of two different own dice A, B in in_play and each opponent die T. What happens: Runs only when leg_over == false. Stores the choice in declaration. Sets this_is_pass, target_size, attacker_large_size (the power die, or the larger of the two skill dice) and attacker_small_size (the smaller skill die, or 0).
  10. [update] all players. What happens: Runs only when leg_over == false and this_is_pass == false. target_value = the defender's value for the die of size target_size. For a power attack, attack_value = the attacker's value for the die of size attacker_large_size, and attack_success = (attack_value >= target_value). For a skill attack, attack_value = the sum of the attacker's values for the dice of sizes attacker_large_size and attacker_small_size, and attack_success = (attack_value == target_value).
  11. [update] all players. What happens: Runs only when leg_over == false, this_is_pass == false and attack_success == true. Remove target_size from the defender's in_play; the attacker's score += target_size; announce publicly that the target (size target_size) was captured and its value target_value. The attacker's die of size attacker_large_size is rerolled to a uniform random value from 1 to attacker_large_size, and its new value is told only to its owner. The smaller skill attacker keeps its value.
  12. [update] all players. What happens: Runs only when leg_over == false, this_is_pass == false and attack_success == false. Remove attacker_large_size from the attacker's in_play; the defender's score += attacker_large_size; announce publicly the captured die's size and value. Nothing is rerolled, the smaller skill attacker keeps its value, and target_value is not revealed.
  13. [tell] all players. What happens: Runs only when leg_over == false. Public result: 'pass', or the target size, the attacking die sizes, and whether the attack succeeded.
  14. [update] all players. What happens: Runs only when leg_over == false. leg_over = true if either player's in_play is empty, or (this_is_pass and previous_was_pass), or turn == 20. Then previous_was_pass = this_is_pass. If leg == 1 and leg_over == true and turn < 20, set turn = 20 (the remaining leg-1 turns are skipped). If leg == 2 and (leg_over == true or turn == 40), set match_over = true.
  15. [check] all players. What happens: End the game if match_over == true; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Each player owns four dice of sizes 4, 6, 8 and 12; the sizes in each player's in_play are public.
  R2. Each player's score starts at 0 and carries over from leg 1 to leg 2.
  R3. Before turn 1, exactly one of the two seats is chosen at random as First (is_first = true).
  R4. In leg 1 (turns 1-20), First acts on odd turns and Second acts on even turns.
  R5. In leg 2 (turns 21-40), Second acts on odd turns and First acts on even turns.
  R6. On turns 1 and 21, both players secretly and simultaneously choose values d4 in 1-4, d6 in 1-6, d8 in 1-8 and d12 in 1-12.
  R7. When a player's four loaded values total exactly 16, those values become the dice values.
  R8. When a player's four loaded values do not total 16, the values become d4=2, d6=3, d8=4, d12=7.
  R9. At the start of each leg, both players' in_play is reset to [4, 6, 8, 12]; captures from leg 1 do not carry over, but scores do.
  R10. Each turn, the public status announces the turn, the leg, the active seat, each player's in_play, both scores, and whether the previous turn in this leg was a pass.
  R11. Each turn, each player is privately told only the values of their own remaining dice and never the opponent's values, except values announced on capture.
  R12. The active player may pass, declare a power attack (one own remaining die against one opponent remaining die), or declare a skill attack (two different own remaining dice against one opponent remaining die).
  R13. When a power attack has attacker value >= target value (for example 5 vs 5), it succeeds; when the attacker value is lower (4 vs 5), it fails.
  R14. When a skill attack's two values sum exactly to the target value (3 + 4 vs 7), it succeeds; any other sum (3 + 4 vs 6 or vs 8) fails.
  R15. When an attack succeeds, the target is removed from the defender's in_play, its value is announced publicly, and the attacker's score rises by the target's size (for example +12 for a d12).
  R16. When an attack succeeds, the attacking die (in a skill attack, only the larger-size one) is rerolled to a uniform value from 1 to its size, told only to its owner; the smaller skill attacker keeps its value.
  R17. When an attack fails, the attacking die (in a skill attack, only the larger-size one) is removed from the attacker's in_play, its value is announced publicly, and the defender's score rises by its size.
  R18. When an attack fails, nothing is rerolled, the smaller skill attacker keeps its value, and the target's value is not revealed.
  R19. When either player's in_play becomes empty, the current leg ends immediately.
  R20. When this turn and the previous turn in the same leg are both passes, the current leg ends immediately.
  R21. When turn 20 is completed, leg 1 ends.
  R22. When leg 1 ends before turn 20, the remaining turns up to 20 are skipped with no actions, and play resumes at turn 21 with leg 2 loading.
  R23. When turn 40 is completed or leg 2 ends early, the match ends.
  R24. When the match ends, the player with the higher score wins; equal scores are a draw.
  R25. Values change only by loading on turns 1 and 21 or by the reroll after a successful attack.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Loading of the d4 (turns 1 and 21) | asked: both seats | options: a whole number from 1 to 4
  - Loading of the d6 (turns 1 and 21) | asked: both seats | options: a whole number from 1 to 6
  - Loading of the d8 (turns 1 and 21) | asked: both seats | options: a whole number from 1 to 8
  - Loading of the d12 (turns 1 and 21) | asked: both seats | options: a whole number from 1 to 12
  - Turn choice | asked: the active seat only | options: 'pass'; 'power: my dA -> your dT' for every own die A in own in_play and every die T in the opponent's in_play; 'skill: my dA + my dB -> your dT' for every unordered pair of two different own dice A, B in own in_play (offered only if at least 2 own dice remain) and every die T in the opponent's in_play. The non-active seat is not asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: match_over == true (set when turn == 40 or when leg 2 ends early)
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their score: the total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks. The higher score wins; equal scores share the win (a draw).
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

- each player: `score` (number, visible: public, starts 0): Total sizes of all dice this player has captured across both legs
- each player: `is_first` (bool, visible: public, starts False): True for the player chosen at random to be First
- each player: `in_play` (list, visible: public, starts [4, 6, 8, 12]): Sizes of this player's dice still in play this leg
- the table: `turn` (number, visible: public, starts 0): Current turn number, 1 to 40
- the table: `leg` (number, visible: public, starts 1): Current leg, 1 or 2
- the table: `match_over` (bool, visible: public, starts False): True once the match has ended
- parameters (each must be an attribute holding this value, never a number buried in a step): d4_size = 4, d6_size = 6, d8_size = 8, d12_size = 12, dice_per_player = 4, load_total = 16, default_d4 = 2, default_d6 = 3, default_d8 = 4, default_d12 = 7, legs = 2, turns_per_leg = 20, leg1_first_turn = 1, leg1_last_turn = 20, leg2_first_turn = 21, leg2_last_turn = 40, consecutive_passes_to_end_leg = 2, skill_attack_dice = 2, power_attack_dice = 1, starting_score = 0, min_die_value = 1
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
    "id": "loaded_button_men",
    "name": "Loaded Button Men",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Secretly load a d4, d6, d8 and d12 to total 16, then capture your opponent's dice with power or skill attacks over two 20-turn legs."
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
        "key": "is_first",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "in_play",
        "visible": "public",
        "type": "list",
        "initial": [4, 6, 8, 12]
      },
      {
        "key": "d4_value",
        "visible": "ally",
        "type": "number",
        "initial": 2
      },
      {
        "key": "d6_value",
        "visible": "ally",
        "type": "number",
        "initial": 3
      },
      {
        "key": "d8_value",
        "visible": "ally",
        "type": "number",
        "initial": 4
      },
      {
        "key": "d12_value",
        "visible": "ally",
        "type": "number",
        "initial": 7
      },
      {
        "key": "load_d4",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "load_d6",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "load_d8",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "load_d12",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer_table",
        "visible": "ally",
        "type": "list",
        "initial": []
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
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leg",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "first_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "previous_was_pass",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "this_is_pass",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "declaration",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "target_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attacker_large_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attacker_small_size",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attack_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "target_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "captured_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attack_success",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "leg_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "match_over",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "d4_size",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "d6_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "d8_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "d12_size",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "dice_per_player",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "load_total",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "default_d4",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "default_d6",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "default_d8",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "default_d12",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "legs",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "turns_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "leg1_first_turn",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leg1_last_turn",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "leg2_first_turn",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "leg2_last_turn",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "consecutive_passes_to_end_leg",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "skill_attack_dice",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "power_attack_dice",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_die_value",
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
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "choose First",
      "do": [
        {
          "set": {
            "key": "first_seat",
            "value": {
              "calc": "min(len(players), 1 + int(uniform(0, len(players))))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == first_seat"
            },
            "key": "is_first",
            "value": true
          }
        }
      ],
      "text": "Seat {first_seat} is chosen at random to be First."
    },
    {
      "use": "update",
      "label": "start the clock",
      "do": [
        {
          "set": {
            "key": "turn",
            "value": 0
          }
        },
        {
          "set": {
            "key": "leg",
            "value": {
              "calc": "leg1_first_turn"
            }
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "turn",
      "label": "advance the turn",
      "do": [
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg",
            "value": {
              "calc": "1 if turn <= leg1_last_turn else legs"
            }
          }
        },
        {
          "set": {
            "key": "leg_over",
            "value": false,
            "if": {
              "calc": "turn == leg2_first_turn"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "first_seat if ((turn % 2 == 1 and leg == 1) or (turn % 2 == 0 and leg == legs)) else [p.seat for p in players if p.seat != first_seat][0]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "load_d4",
            "value": 0,
            "if": {
              "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "load_d6",
            "value": 0,
            "if": {
              "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "load_d8",
            "value": 0,
            "if": {
              "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "load_d12",
            "value": 0,
            "if": {
              "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "loading",
      "label": "load the d4",
      "when": {
        "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_die_value"
        },
        "max": {
          "calc": "d4_size"
        }
      },
      "store": "load_d4",
      "text": "Loading for leg {leg}: choose a secret value for your d4, from {min_die_value} to {d4_size}. Your four values must total exactly {load_total}, or you get the default loading d4={default_d4}, d6={default_d6}, d8={default_d8}, d12={default_d12}."
    },
    {
      "use": "poll",
      "phase": "loading",
      "label": "load the d6",
      "when": {
        "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_die_value"
        },
        "max": {
          "calc": "d6_size"
        }
      },
      "store": "load_d6",
      "text": "Choose a secret value for your d6, from {min_die_value} to {d6_size}. The four values must total exactly {load_total}."
    },
    {
      "use": "poll",
      "phase": "loading",
      "label": "load the d8",
      "when": {
        "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_die_value"
        },
        "max": {
          "calc": "d8_size"
        }
      },
      "store": "load_d8",
      "text": "Choose a secret value for your d8, from {min_die_value} to {d8_size}. The four values must total exactly {load_total}."
    },
    {
      "use": "poll",
      "phase": "loading",
      "label": "load the d12",
      "when": {
        "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_die_value"
        },
        "max": {
          "calc": "d12_size"
        }
      },
      "store": "load_d12",
      "text": "Choose a secret value for your d12, from {min_die_value} to {d12_size}. The four values must total exactly {load_total}."
    },
    {
      "use": "update",
      "phase": "loading",
      "label": "apply the loading",
      "when": {
        "calc": "turn == leg1_first_turn or turn == leg2_first_turn"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "d4_value",
            "value": {
              "calc": "int(you.load_d4) if int(you.load_d4) + int(you.load_d6) + int(you.load_d8) + int(you.load_d12) == load_total else default_d4"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d6_value",
            "value": {
              "calc": "int(you.load_d6) if int(you.load_d4) + int(you.load_d6) + int(you.load_d8) + int(you.load_d12) == load_total else default_d6"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d8_value",
            "value": {
              "calc": "int(you.load_d8) if int(you.load_d4) + int(you.load_d6) + int(you.load_d8) + int(you.load_d12) == load_total else default_d8"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d12_value",
            "value": {
              "calc": "int(you.load_d12) if int(you.load_d4) + int(you.load_d6) + int(you.load_d8) + int(you.load_d12) == load_total else default_d12"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "in_play",
            "value": {
              "calc": "[d4_size, d6_size, d8_size, d12_size]"
            }
          }
        },
        {
          "set": {
            "key": "previous_was_pass",
            "value": false
          }
        }
      ],
      "text": "Loading is done. Leg {leg} begins with all four dice of both players in play."
    },
    {
      "use": "tell",
      "phase": "turn",
      "label": "public status",
      "when": {
        "calc": "leg_over == False"
      },
      "to": "all",
      "text": "Turn {turn}, leg {leg}: seat {active_seat} to act. Dice in play - seat 1: {players[0].in_play}, seat 2: {players[1].in_play}. Scores - seat 1: {players[0].score}, seat 2: {players[1].score}. Previous turn in this leg was a pass: {previous_was_pass}."
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "private status",
      "when": {
        "calc": "leg_over == False"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "in_play",
        "d4_value",
        "d6_value",
        "d8_value",
        "d12_value"
      ],
      "text": "Your dice in play and their current values (only the sizes listed in in_play are still in play):"
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "build the offer",
      "when": {
        "calc": "leg_over == False"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer_table",
            "value": {
              "calc": "[['pass', 0, 0, 0]] + [['power: my ' + ('d4' if a == d4_size else ('d6' if a == d6_size else ('d8' if a == d8_size else 'd12'))) + ' -> your ' + ('d4' if t == d4_size else ('d6' if t == d6_size else ('d8' if t == d8_size else 'd12'))), t, a, 0] for a in you.in_play for p in players if p.seat != you.seat for t in p.in_play] + [['skill: my ' + ('d4' if a == d4_size else ('d6' if a == d6_size else ('d8' if a == d8_size else 'd12'))) + ' + my ' + ('d4' if b == d4_size else ('d6' if b == d6_size else ('d8' if b == d8_size else 'd12'))) + ' -> your ' + ('d4' if t == d4_size else ('d6' if t == d6_size else ('d8' if t == d8_size else 'd12'))), t, b, a] for a in you.in_play for b in you.in_play if a < b for p in players if p.seat != you.seat for t in p.in_play]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[r[0] for r in you.offer_table]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "turn choice",
      "when": {
        "calc": "leg_over == False"
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
        "bind": "decl"
      },
      "text": "Your turn. Pass, or attack one of your opponent's dice. A power attack (one of your dice) succeeds if your value is greater than or equal to the target's value. A skill attack (two of your dice) succeeds if their two values sum exactly to the target's value. On success you capture the target and score its size, and your attacking die (the larger one in a skill attack) is rerolled. On failure your attacking die (the larger one in a skill attack) is captured and your opponent scores its size."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "read the declaration",
      "when": {
        "calc": "leg_over == False"
      },
      "do": [
        {
          "set": {
            "key": "declaration",
            "value": "$decl"
          }
        },
        {
          "set": {
            "key": "target_size",
            "value": {
              "calc": "max([r[1] for p in players if p.seat == active_seat for r in p.offer_table if r[0] == declaration] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "attacker_large_size",
            "value": {
              "calc": "max([r[2] for p in players if p.seat == active_seat for r in p.offer_table if r[0] == declaration] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "attacker_small_size",
            "value": {
              "calc": "max([r[3] for p in players if p.seat == active_seat for r in p.offer_table if r[0] == declaration] + [0])"
            }
          }
        },
        {
          "set": {
            "key": "this_is_pass",
            "value": {
              "calc": "target_size == 0"
            }
          }
        },
        {
          "set": {
            "key": "attack_success",
            "value": false
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the attack",
      "when": {
        "calc": "leg_over == False and this_is_pass == False"
      },
      "do": [
        {
          "set": {
            "key": "target_value",
            "value": {
              "calc": "sum([(p.d4_value if target_size == d4_size else (p.d6_value if target_size == d6_size else (p.d8_value if target_size == d8_size else p.d12_value))) for p in players if p.seat != active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "attack_value",
            "value": {
              "calc": "sum([(p.d4_value if attacker_large_size == d4_size else (p.d6_value if attacker_large_size == d6_size else (p.d8_value if attacker_large_size == d8_size else p.d12_value))) + ((p.d4_value if attacker_small_size == d4_size else (p.d6_value if attacker_small_size == d6_size else (p.d8_value if attacker_small_size == d8_size else p.d12_value))) if attacker_small_size > 0 else 0) for p in players if p.seat == active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "attack_success",
            "value": {
              "calc": "(attack_value >= target_value) if attacker_small_size == 0 else (attack_value == target_value)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "attack succeeds",
      "when": {
        "calc": "leg_over == False and this_is_pass == False and attack_success == True"
      },
      "do": [
        {
          "set": {
            "key": "captured_value",
            "value": {
              "calc": "target_value"
            }
          }
        },
        {
          "remove": {
            "players": {
              "where": "you.seat != active_seat"
            },
            "key": "in_play",
            "value": {
              "calc": "target_size"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "score",
            "value": {
              "calc": "target_size"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "d4_value",
            "value": {
              "calc": "min(d4_size, int(uniform(min_die_value, d4_size + 1)))"
            },
            "if": {
              "calc": "attacker_large_size == d4_size"
            },
            "announce_to": {
              "where": "you.seat == active_seat"
            },
            "text": "Your d4 was rerolled to {d4_value}."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "d6_value",
            "value": {
              "calc": "min(d6_size, int(uniform(min_die_value, d6_size + 1)))"
            },
            "if": {
              "calc": "attacker_large_size == d6_size"
            },
            "announce_to": {
              "where": "you.seat == active_seat"
            },
            "text": "Your d6 was rerolled to {d6_value}."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "d8_value",
            "value": {
              "calc": "min(d8_size, int(uniform(min_die_value, d8_size + 1)))"
            },
            "if": {
              "calc": "attacker_large_size == d8_size"
            },
            "announce_to": {
              "where": "you.seat == active_seat"
            },
            "text": "Your d8 was rerolled to {d8_value}."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "d12_value",
            "value": {
              "calc": "min(d12_size, int(uniform(min_die_value, d12_size + 1)))"
            },
            "if": {
              "calc": "attacker_large_size == d12_size"
            },
            "announce_to": {
              "where": "you.seat == active_seat"
            },
            "text": "Your d12 was rerolled to {d12_value}."
          }
        }
      ],
      "text": "Capture! Seat {active_seat} captures the opponent's d{target_size}, which showed {captured_value}, and scores {target_size}. The attacking d{attacker_large_size} is rerolled in secret."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "attack fails",
      "when": {
        "calc": "leg_over == False and this_is_pass == False and attack_success == False"
      },
      "do": [
        {
          "set": {
            "key": "captured_value",
            "value": {
              "calc": "sum([(p.d4_value if attacker_large_size == d4_size else (p.d6_value if attacker_large_size == d6_size else (p.d8_value if attacker_large_size == d8_size else p.d12_value))) for p in players if p.seat == active_seat])"
            }
          }
        },
        {
          "remove": {
            "players": {
              "where": "you.seat == active_seat"
            },
            "key": "in_play",
            "value": {
              "calc": "attacker_large_size"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != active_seat"
            },
            "key": "score",
            "value": {
              "calc": "attacker_large_size"
            }
          }
        }
      ],
      "text": "The attack fails. Seat {active_seat}'s d{attacker_large_size}, which showed {captured_value}, is captured by the defender, who scores {attacker_large_size}. Nothing is rerolled and the target's value stays secret."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "result: pass",
      "when": {
        "calc": "leg_over == False and this_is_pass == True"
      },
      "to": "all",
      "text": "Turn {turn}: seat {active_seat} passes."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "result: power attack",
      "when": {
        "calc": "leg_over == False and this_is_pass == False and attacker_small_size == 0"
      },
      "to": "all",
      "text": "Turn {turn}: seat {active_seat} made a power attack with its d{attacker_large_size} on the d{target_size}. Succeeded: {attack_success}."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "result: skill attack",
      "when": {
        "calc": "leg_over == False and this_is_pass == False and attacker_small_size > 0"
      },
      "to": "all",
      "text": "Turn {turn}: seat {active_seat} made a skill attack with its d{attacker_small_size} and d{attacker_large_size} on the d{target_size}. Succeeded: {attack_success}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "leg end check",
      "when": {
        "calc": "leg_over == False"
      },
      "do": [
        {
          "set": {
            "key": "leg_over",
            "value": {
              "calc": "any(len(p.in_play) == 0 for p in players) or (this_is_pass and previous_was_pass) or turn == leg1_last_turn or turn == leg2_last_turn"
            }
          }
        },
        {
          "set": {
            "key": "previous_was_pass",
            "value": {
              "calc": "this_is_pass"
            }
          }
        },
        {
          "set": {
            "key": "turn",
            "value": {
              "calc": "leg1_last_turn"
            },
            "if": {
              "calc": "leg == 1 and leg_over and turn < leg1_last_turn"
            },
            "text": "Leg 1 ends early; the remaining turns up to {leg1_last_turn} are skipped."
          }
        },
        {
          "set": {
            "key": "match_over",
            "value": true,
            "if": {
              "calc": "leg == legs and (leg_over or turn >= leg2_last_turn)"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "match end",
      "when": {
        "calc": "match_over == True"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "match_over == True or turn >= leg2_last_turn"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "DICE. Each player owns four dice: a d4, a d6, a d8 and a d12. A die's size is its number of sides ({d4_size}, {d6_size}, {d8_size} or {d12_size}); sizes are public, and each player's dice still in play are shown as in_play. A die's value is a whole number from {min_die_value} to its size. You always know your own values; you are never told your opponent's values, except when a die is captured and its value is announced. Each player has a score that starts at {starting_score} and carries over between legs.\n\nMATCH STRUCTURE. The match has {legs} legs: leg 1 is turns {leg1_first_turn} to {leg1_last_turn} and leg 2 is turns {leg2_first_turn} to {leg2_last_turn}. Before turn 1, one player is chosen at random to be First. In leg 1, First acts on odd turns and Second on even turns. In leg 2, Second acts on odd turns and First on even turns.\n\nLOADING (turns {leg1_first_turn} and {leg2_first_turn}). Both players at the same moment secretly choose a value for each of their four dice: each at least {min_die_value} and at most that die's size. If your four values total exactly {load_total}, they become your dice values. If they do not total {load_total}, your values become the default loading: d4={default_d4}, d6={default_d6}, d8={default_d8}, d12={default_d12}. All four dice of both players are in play at the start of each leg: captures from leg 1 do not carry over, but scores do.\n\nEACH TURN. The turn number, leg, active seat, each player's dice in play, both scores and whether the previous turn in this leg was a pass are announced; each player is privately told the values of their own dice. The active player then either PASSES or declares an ATTACK on one of the opponent's remaining dice (the target), using either one of their own remaining dice (a POWER attack) or two different dice of their own (a SKILL attack). Only legal declarations are offered.\n- A power attack succeeds if the attacker's value is greater than or equal to the target's value (5 vs 5 succeeds); otherwise it fails (4 vs 5 fails).\n- A skill attack succeeds if the two attackers' values sum exactly to the target's value (3 + 4 vs 7 succeeds); any other sum fails (3 + 4 vs 6 or vs 8).\nThe pass, or the target size, attacking die sizes and whether the attack succeeded, is announced.\n\nSUCCESS. The target is captured and removed from the leg, its value is announced publicly, and the attacker's score rises by the target's size. The attacking die (in a skill attack, only the larger-size of the two) is rerolled to a uniformly random value from 1 to its size, told only to its owner. In a skill attack the smaller attacker keeps its value.\n\nFAILURE. The attacking die is captured by the defender; in a skill attack only the larger-size attacker is captured, and the smaller stays in play with its value unchanged. The captured die's value is announced publicly and the defender's score rises by the captured die's size. Nothing is rerolled, and the target's value is not revealed.\n\nLEG END. The leg ends immediately if either player has no dice left, or this turn and the previous turn in this leg were both passes, or this is turn {leg1_last_turn} (for leg 1). If leg 1 ends early, the remaining turns up to {leg1_last_turn} are skipped with no actions and play resumes at turn {leg2_first_turn} with leg 2 loading. After turn {leg2_last_turn}, or when leg 2 ends, the match ends.\n\nNOTES. Values change only by loading at the start of a leg or by the reroll after a successful attack. Captured dice never return within a leg. Captures are not compulsory: you may always pass.\n\nWINNING. When the match ends, the player with the higher score (total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks) wins. Equal scores are a draw (a shared win)."
}
````
