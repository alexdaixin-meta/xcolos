# Task: write the XColos game file for "Dungeon Dare"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

COMPONENTS.

Monster deck of 13 cards (name: strength):
- Goblin 1 (x2)
- Skeleton 2 (x2)
- Orc 3 (x2)
- Vampire 4 (x2)
- Golem 5 (x2)
- Lich 6 (x1)
- Demon 7 (x1)
- Dragon 9 (x1)

Adventurer base HP: 3.

Equipment (4 items, all present at the start of each dungeon):
- ARMOR: +4 HP.
- SHIELD: +3 HP.
- TORCH: defeats every monster of strength 3 or less.
- SPEAR: defeats every monster of strength 7 or more.

Each player has a point total starting at 0.

SEATS AND TURNS.
Seats are 1, 2 and 3. The game is played as a series of turns, at most 40. Turns are grouped into dungeons.

STARTING A DUNGEON.
1. At the start of each dungeon, shuffle all 13 monsters into a face-down deck. This shuffle is the only random event.
2. Return all 4 items to the adventurer.
3. Empty the dungeon pile and all players' set-aside piles.
4. Mark all three players as IN, and clear every player's 'added' mark.
5. The leader acts first. Dungeon 1 is led by seat 1, dungeon 2 by seat 2, dungeon 3 by seat 3, dungeon 4 by seat 1, and so on.
6. Turns then pass in seat order (1, 2, 3, 1, ...), skipping players who are OUT.

A TURN (for the active player, who is IN).
(a) Forced pass check: if the deck holds 2 or fewer cards, the active player must PASS this turn. Skip to (d).
(b) Draw: the active player privately looks at the top card of the deck. Only they see it.
(c) Talk: every player, in or out, writes one short message at the same time without seeing the others. Then all messages are shown to everyone. Messages bind no one and may be lies.
(d) Action: the active player chooses one option from this list, in this order, offering only the legal ones.
    - PASS: you become OUT for this dungeon. The card you drew, if any, goes back on top of the deck, unseen by others.
    - ADD: put the drawn monster face-down on the dungeon pile, and mark yourself as 'added' for this dungeon.
    - SACRIFICE_ARMOR, SACRIFICE_SHIELD, SACRIFICE_TORCH, SACRIFICE_SPEAR: available only for items still present. Remove that item from the adventurer for this dungeon. Put the drawn monster face-down in your own set-aside pile; it is out of play and seen only by you. This does NOT mark you as 'added'.
(e) Announcement: everyone learns which option was chosen, which item was removed if any, and how many cards are in the dungeon pile. Nobody learns which monster was drawn.
(f) If exactly one player is still IN, that player becomes the RUNNER and the run happens now (see below). Otherwise the turn passes to the next IN player.

THE RUN.
1. The runner's HP = 3, +4 if ARMOR remains, +3 if SHIELD remains.
2. Reveal every card in the dungeon pile, then the top 2 cards of the deck. All of these are the monsters faced.
3. Each monster is defeated with no damage if TORCH remains and its strength is 3 or less, or if SPEAR remains and its strength is 7 or more. Otherwise it deals damage equal to its strength.
4. If total damage is less than HP, the run SUCCEEDS: the runner gains 2 points.
5. Otherwise the run FAILS:
    - The runner loses 1 point (never below 0).
    - Every OUT player who is marked 'added' for this dungeon gains 1 point.
6. All revealed cards are announced. The dungeon ends, and the next turn starts a new dungeon.

END OF GAME.
- After any run, if any player has 4 or more points, the game ends.
- The game also ends after turn 40, even mid-dungeon. An unfinished dungeon is not scored.

How the winner is decided: When the game ends, the player with the most points wins. If two or more players tie for the most points, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Dungeon Dare (3 to 3 players, best with 3)

Three players push their luck through a shuffled monster deck. Each turn they add the monster they drew to a hidden dungeon, strip the adventurer of an item, or pass out; the last player left must survive the run.

STATE (every item below must exist in the file):
  - each player: points (number, starts 0); everyone sees it. The player's point total.
  - each player: in_dungeon (bool, starts True); everyone sees it. True if the player is IN the current dungeon; false once they PASS (OUT).
  - each player: added (bool, starts False); everyone sees it. True if the player chose ADD at least once in the current dungeon. It is public because each chosen option is announced.
  - each player: drawn_card (list, starts []); only its owner sees it. The monster strength the player privately drew this turn (empty if none). Only the owner sees it.
  - each player: set_aside (list, starts []); only its owner sees it. Monsters this player removed with a sacrifice in the current dungeon. They are out of play and seen only by the owner.
  - the table: deck (list, starts []); hidden from all players. Face-down monster deck as an ordered list of strengths. The first element is the top card.
  - the table: dungeon_pile (list, starts []); hidden from all players. Face-down monsters added to the dungeon this dungeon.
  - the table: dungeon_count (number, starts 0); everyone sees it. Number of cards in the dungeon pile, as announced.
  - the table: armor (bool, starts True); everyone sees it. ARMOR still with the adventurer.
  - the table: shield (bool, starts True); everyone sees it. SHIELD still with the adventurer.
  - the table: torch (bool, starts True); everyone sees it. TORCH still with the adventurer.
  - the table: spear (bool, starts True); everyone sees it. SPEAR still with the adventurer.
  - the table: turn (number, starts 0); everyone sees it. Number of turns started so far (at most 40).
  - the table: dungeon_number (number, starts 0); everyone sees it. Index of the current dungeon, starting at 1.
  - the table: leader_seat (number, starts 1); everyone sees it. Seat that leads the current dungeon: ((dungeon_number - 1) mod 3) + 1.
  - the table: active_seat (number, starts 1); everyone sees it. Seat of the player taking this turn.
  - the table: new_dungeon (bool, starts True); hidden from all players. Scratch flag: true when the next turn must start a new dungeon.
  - the table: forced_pass (bool, starts False); everyone sees it. True this turn if the deck held 2 or fewer cards at the start of the turn.
  - the table: last_action (text, starts ''); everyone sees it. Option chosen by the active player this turn, as announced.
  - the table: in_count (number, starts 3); everyone sees it. Number of players still IN.
  - the table: runner_seat (number, starts 0); everyone sees it. Seat of the runner when a run happens, else 0.
  - the table: faced (list, starts []); everyone sees it. Monsters revealed in the last run: the dungeon pile plus the top 2 deck cards.
  - the table: run_hp (number, starts 0); everyone sees it. Runner's HP in the last run.
  - the table: run_damage (number, starts 0); everyone sees it. Total damage taken in the last run.
  - parameters, each kept as a table attribute: seats = 3, deck_size = 13, goblin_strength = 1, goblin_count = 2, skeleton_strength = 2, skeleton_count = 2, orc_strength = 3, orc_count = 2, vampire_strength = 4, vampire_count = 2, golem_strength = 5, golem_count = 2, lich_strength = 6, lich_count = 1, demon_strength = 7, demon_count = 1, dragon_strength = 9, dragon_count = 1, base_hp = 3, armor_hp = 4, shield_hp = 3, torch_max_strength = 3, spear_min_strength = 7, item_count = 4, forced_pass_deck_max = 2, run_extra_cards = 2, success_points = 2, fail_penalty = 1, added_bonus = 1, points_floor = 0, win_points = 4, max_turns = 40, starting_points = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 each start with points = 0.
  2. Set turn = 0, dungeon_number = 0 and new_dungeon = true, so the first turn starts dungeon 1 led by seat 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Applies only when new_dungeon is true. Set dungeon_number += 1 and leader_seat = ((dungeon_number - 1) mod 3) + 1. Set deck = the 13 strengths [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order; this seeded shuffle is the only random event. Set armor, shield, torch and spear = true. Set dungeon_pile = [] and dungeon_count = 0. For every player set set_aside = [], drawn_card = [], in_dungeon = true and added = false. Set in_count = 3, runner_seat = 0, active_seat = leader_seat and new_dungeon = false.
  2. [update] all players. What happens: Set turn += 1. Set forced_pass = (length(deck) <= 2). If forced_pass is false, move the first element of deck into the active player's drawn_card; that player privately sees it.
  3. [sync] the active player. What happens: The active player is shown their drawn_card, unless forced_pass is true.
  4. [poll] all players answers: short text message. What happens: Applies only when forced_pass is false. Every player, IN or OUT, writes one message at the same time. All are then broadcast as {"to": "all", "text": "Seat {seat} says: {value}"}. Messages bind no one.
  5. [ask] the active player (seat active_seat) answers: one of: PASS, ADD, SACRIFICE_ARMOR, SACRIFICE_SHIELD, SACRIFICE_TORCH, SACRIFICE_SPEAR (only the legal ones, in this order). What happens: Sets last_action to the chosen option.
  6. [update] the active player. What happens: If last_action = PASS: set in_dungeon = false, in_count -= 1, and put drawn_card (if any) back as the first element of deck. If ADD: append drawn_card to dungeon_pile, set dungeon_count += 1 and added = true. If SACRIFICE_X: set item X = false and append drawn_card to the player's set_aside. In every case clear drawn_card.
  7. [tell] all players. What happens: Announce: 'Seat {active_seat} chose {last_action}. Dungeon pile: {dungeon_count} cards. Items left: armor {armor}, shield {shield}, torch {torch}, spear {spear}.' The drawn monster is not revealed.
  8. [update] all players. What happens: Applies only when in_count = 1 (the run). Set runner_seat = the seat with in_dungeon = true. Set run_hp = 3 + 4*armor + 3*shield. Set faced = dungeon_pile + the first 2 elements of deck. Set run_damage = the sum over faced of strength s, except that s is counted as 0 if (torch and s <= 3) or (spear and s >= 7). If run_damage < run_hp, the runner gets points += 2. Otherwise the runner gets points = max(0, points - 1), and every player with in_dungeon = false and added = true gets points += 1. Set new_dungeon = true.
  9. [tell] all players. What happens: Applies only when a run happened this turn. Announce: 'Seat {runner_seat} ran: monsters {faced}, HP {run_hp}, damage {run_damage}.' Then announce success or failure and the new points.
  10. [update] all players. What happens: Applies only when new_dungeon is false. Set active_seat = the next seat after active_seat in the order 1, 2, 3, 1, ... that has in_dungeon = true.
  11. [check] all players. What happens: End the game if (a run happened this turn and some player has points >= 4) or turn >= 40. Otherwise run the next turn.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a dungeon starts, then the deck is set to the 13 monsters [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order, all 4 items are present, the dungeon pile and all set-aside piles are empty, all 3 players are IN and no player is marked added.
  R2. When dungeon number d starts, then its leader is seat ((d - 1) mod 3) + 1 and that seat takes the first turn (dungeon 1: seat 1, dungeon 2: seat 2, dungeon 4: seat 1).
  R3. When a turn ends without a run, then the next active seat is the next seat in the order 1, 2, 3, 1 that is still IN, skipping OUT seats.
  R4. When the deck holds 2 or fewer cards at the start of a turn, then the active player draws nothing, there is no talk, and PASS is the only option offered.
  R5. When the deck holds 3 or more cards at the start of a turn, then the active player privately receives the top card of the deck in drawn_card, and no one else sees it.
  R6. When the active player has drawn, then every player, IN or OUT, submits one message simultaneously, and all messages are shown to everyone afterwards.
  R7. When the active player chooses PASS, then they become OUT (in_dungeon = false) and any drawn card returns to the top of the deck.
  R8. When the active player chooses ADD, then the drawn card is appended to the dungeon pile, dungeon_count increases by 1, and the player is marked added = true.
  R9. When the active player chooses SACRIFICE_X for an item X still present, then X is removed for this dungeon, the drawn card goes to that player's set_aside, and added is not changed.
  R10. When an item has been removed this dungeon, then its SACRIFICE option is not offered.
  R11. When an action is taken, then everyone is told the option chosen, any item removed and the dungeon pile count, but not the drawn monster.
  R12. When exactly one player is IN after an action, then that player is the runner and the run happens immediately.
  R13. When a run happens, then the runner's HP is 3, plus 4 if ARMOR remains, plus 3 if SHIELD remains (maximum 10).
  R14. When a run happens, then the monsters faced are every card in the dungeon pile plus the top 2 cards of the deck, and all of them are announced.
  R15. When a faced monster has strength 3 or less and TORCH remains, or strength 7 or more and SPEAR remains, then it deals 0 damage; otherwise it deals damage equal to its strength.
  R16. When total damage is less than the runner's HP, then the run succeeds and the runner gains 2 points.
  R17. When total damage is at least the runner's HP, then the run fails and the runner loses 1 point, never going below 0.
  R18. When a run fails, then every OUT player marked added gains 1 point.
  R19. When a run ends, then the dungeon ends and the next turn starts a new dungeon.
  R20. When, after a run, any player has 4 or more points, then the game ends.
  R21. When turn 40 has been played, then the game ends, even mid-dungeon, and the unfinished dungeon is not scored.
  R22. When the game ends, then the player with the most points wins, and players tied for the most share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each turn | asked: all three seats, IN or OUT, only when the active player drew a card | options: free short text
  - Action of the active player | asked: the active seat only | options: If the deck held 2 or fewer cards at the start of the turn: PASS only. Otherwise: PASS, ADD, then SACRIFICE_ARMOR if armor remains, SACRIFICE_SHIELD if shield remains, SACRIFICE_TORCH if torch remains, SACRIFICE_SPEAR if spear remains.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (new_dungeon = true and max over players of points >= 4) or turn >= 40
  - each player's standing: you.points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their point total; the most points wins. Players tied for the most share the result, which the source calls a draw.
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

- each player: `points` (number, visible: public, starts 0): The player's point total.
- each player: `in_dungeon` (bool, visible: public, starts True): True if the player is IN the current dungeon; false once they PASS (OUT).
- each player: `added` (bool, visible: public, starts False): True if the player chose ADD at least once in the current dungeon. It is public because each chosen option is announced.
- the table: `dungeon_count` (number, visible: public, starts 0): Number of cards in the dungeon pile, as announced.
- the table: `armor` (bool, visible: public, starts True): ARMOR still with the adventurer.
- the table: `shield` (bool, visible: public, starts True): SHIELD still with the adventurer.
- the table: `torch` (bool, visible: public, starts True): TORCH still with the adventurer.
- the table: `spear` (bool, visible: public, starts True): SPEAR still with the adventurer.
- the table: `turn` (number, visible: public, starts 0): Number of turns started so far (at most 40).
- the table: `dungeon_number` (number, visible: public, starts 0): Index of the current dungeon, starting at 1.
- the table: `faced` (list, visible: public, starts []): Monsters revealed in the last run: the dungeon pile plus the top 2 deck cards.
- parameters (each must be an attribute holding this value, never a number buried in a step): seats = 3, deck_size = 13, goblin_strength = 1, goblin_count = 2, skeleton_strength = 2, skeleton_count = 2, orc_strength = 3, orc_count = 2, vampire_strength = 4, vampire_count = 2, golem_strength = 5, golem_count = 2, lich_strength = 6, lich_count = 1, demon_strength = 7, demon_count = 1, dragon_strength = 9, dragon_count = 1, base_hp = 3, armor_hp = 4, shield_hp = 3, torch_max_strength = 3, spear_min_strength = 7, item_count = 4, forced_pass_deck_max = 2, run_extra_cards = 2, success_points = 2, fail_penalty = 1, added_bonus = 1, points_floor = 0, win_points = 4, max_turns = 40, starting_points = 0
- the game ends with ONE ending whose `rank_by` is `you.points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
