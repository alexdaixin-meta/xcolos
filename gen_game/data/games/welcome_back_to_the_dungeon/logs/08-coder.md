# 08 coder

- time: 2026-10-28T05:52:07+00:00 (93.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 ec29be0a2aa7441c, reply sha256 73519756dc7460d8

## Sent

````
# Task: write the XColos game file for "Back to the Dungeon: Single Delve"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

COMPONENTS
- The adventurer has base HP 3 and five equipment items:
  - Armor: +5 HP.
  - Shield: +3 HP.
  - Torch: defeats every monster of strength 3 or less.
  - Holy Water: defeats Vampires and the Lich.
  - Dragon Spear: defeats the Dragon.
- Monster deck (13 cards): Goblin 1 x2, Skeleton 2 x2, Orc 3 x2, Vampire 4 x2, Golem 5 x2, Lich 6 x1, Demon 7 x1, Dragon 9 x1.
- Each player tracks successes (start 0) and failures (start 0).

SETUP
- Seat players in a fixed order. Player 1 begins the first dungeon.
- Shuffle the deck. The dungeon starts empty. All five items are present. No one has passed.

EACH ROUND (one turn)
1. Announcement. The engine announces to everyone:
   - whose turn it is (the active player);
   - the number of cards in the dungeon;
   - which equipment items remain;
   - the number of cards left in the deck;
   - who has passed;
   - everyone's successes and failures.
2. Talk. Every surviving (not eliminated) player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Pass or draw. The active player chooses PASS or DRAW.
   - If the deck is empty, the active player must PASS.
   - PASS: the player sits out the rest of this dungeon.
4. Secret draw. If the player chose DRAW, they privately see the top card of the deck, which leaves the deck. They then choose one of:
   - ADD: the card goes face-down into the dungeon. Only this player knows what it is.
   - SACRIFICE an item: one remaining equipment item (the player names which) is permanently removed for this dungeon, and the card is discarded unseen by others. This is allowed only if at least one item remains.
5. Advance. The turn passes to the next player clockwise who is neither eliminated nor passed in this dungeon.

THE RUN
- The run happens at the end of a round as soon as exactly one non-eliminated player has not passed. That player is the runner.
- HP = 3, plus 5 if Armor remains, plus 3 if Shield remains.
- Damage = the sum of the strengths of all dungeon cards, minus the strength of each card defeated by a remaining item:
  - Torch defeats strength 1, 2 and 3.
  - Holy Water defeats Vampires and the Lich.
  - Dragon Spear defeats the Dragon.
- All dungeon cards are then revealed to everyone, along with the damage and HP.
- If damage < HP, the runner gains 1 success. Otherwise the runner gains 1 failure.
- A player with 2 failures is eliminated and takes no further part.

NEW DUNGEON
- After a run, reshuffle all 13 monsters into a new deck.
- Empty the dungeon, restore all five items, and clear all passes.
- The next active player is the first surviving player clockwise from the runner.

GAME END
- The game ends immediately when:
  - a player reaches 2 successes (that player wins); or
  - only one player is not eliminated (that player wins).
- Otherwise the game ends after round 40. The surviving player with the most successes wins. If tied, the one among them with the fewest failures wins. If still tied, the game is a draw.

How the winner is decided: The first player to reach 2 successes wins. A player is also the winner if every other player has been eliminated by 2 failures. If neither happens by the end of round 40: among non-eliminated players, the highest successes wins, then the fewest failures; any remaining tie is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Back to the Dungeon: Single Delve (3 to 4 players, best with 3)

Players take turns drawing monsters and either secretly add them to a shared dungeon or sacrifice equipment. The last player who has not passed must run the dungeon. The first to 2 successful runs wins; 2 failures eliminate a player.

STATE (every item below must exist in the file):
  - each player: successes (number, starts 0); everyone sees it. successful runs
  - each player: failures (number, starts 0); everyone sees it. failed runs
  - each player: eliminated (bool, starts False); everyone sees it. true once the player has 2 failures
  - each player: passed (bool, starts False); everyone sees it. the player has passed in the current dungeon
  - each player: drawn_card (text, starts ''); only its owner sees it. the monster this player just drew and is deciding on; empty otherwise
  - each player: added_cards (list, starts []); only its owner sees it. the monsters this player has added face-down to the current dungeon (only they know them)
  - the table: deck (list, starts ['Goblin', 'Goblin', 'Skeleton', 'Skeleton', 'Orc', 'Orc', 'Vampire', 'Vampire', 'Golem', 'Golem', 'Lich', 'Demon', 'Dragon']); hidden from all players. the shuffled monster deck
  - the table: dungeon (list, starts []); hidden from all players. the face-down monsters in the current dungeon
  - the table: items (list, starts ['Armor', 'Shield', 'Torch', 'Holy Water', 'Dragon Spear']); everyone sees it. the equipment items remaining in this dungeon
  - the table: active_seat (number, starts 1); everyone sees it. the seat whose turn it is
  - the table: deck_count (number, starts 13); everyone sees it. cards left in the deck
  - the table: dungeon_count (number, starts 0); everyone sees it. cards in the dungeon
  - the table: drawn_strength (number, starts 0); hidden from all players. strength of the card just drawn (scratch)
  - the table: dungeon_total (number, starts 0); hidden from all players. sum of the strengths of the dungeon cards
  - the table: dungeon_low (number, starts 0); hidden from all players. sum of the strengths of dungeon cards of strength 3 or less (Torch targets)
  - the table: dungeon_undead (number, starts 0); hidden from all players. sum of the strengths of dungeon Vampires and the Lich (Holy Water targets)
  - the table: dungeon_dragon (number, starts 0); hidden from all players. strength of the Dragon if it is in the dungeon (Dragon Spear target)
  - the table: runner_seat (number, starts 0); everyone sees it. the seat that ran the last dungeon
  - the table: last_hp (number, starts 0); everyone sees it. the runner's HP in the last run
  - the table: last_damage (number, starts 0); everyone sees it. the damage in the last run
  - the table: round (number, starts 0); everyone sees it. rounds completed
  - parameters, each kept as a table attribute: base_hp = 3, armor_hp = 5, shield_hp = 3, torch_max_strength = 3, goblin_strength = 1, goblin_count = 2, skeleton_strength = 2, skeleton_count = 2, orc_strength = 3, orc_count = 2, vampire_strength = 4, vampire_count = 2, golem_strength = 5, golem_count = 2, lich_strength = 6, lich_count = 1, demon_strength = 7, demon_count = 1, dragon_strength = 9, dragon_count = 1, deck_size = 13, item_count = 5, successes_to_win = 2, failures_to_eliminate = 2, max_rounds = 40, initial_successes = 0, initial_failures = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the players in a fixed order, seats 1 to N; clockwise means increasing seat number, wrapping around.
  2. Set every player's successes and failures to 0, eliminated to false, passed to false, drawn_card empty and added_cards empty.
  3. Fill the deck with the 13 monsters (Goblin x2, Skeleton x2, Orc x2, Vampire x2, Golem x2, Lich, Demon, Dragon); every draw is random, which shuffles it.
  4. The dungeon starts empty, items holds all five items, and every dungeon counter is 0.
  5. Set active_seat to 1 and deck_count to 13.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce active_seat, dungeon_count, items, deck_count, which seats have passed = true, and every seat's successes and failures.
  2. [poll] all players with eliminated = false answers: short text. What happens: Every message is broadcast to all players: 'Seat {seat} says: {value}'. Talk is not binding.
  3. [ask] seat active_seat answers: choice: PASS or DRAW (only PASS when deck_count = 0). What happens: If PASS: set the active player's passed = true.
  4. [update] seat active_seat, when they chose DRAW. What happens: Pick one card at random from deck, put it in the active player's drawn_card (privately shown to them), remove it from deck, and set deck_count -= 1. Set drawn_strength to its strength: Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9.
  5. [ask] seat active_seat, when they chose DRAW answers: choice: ADD, or SACRIFICE <item> for each item still in items. What happens: Records the decision.
  6. [update] seat active_seat, when they chose DRAW. What happens: If ADD: append drawn_card to dungeon and to the active player's added_cards; dungeon_count += 1; dungeon_total += drawn_strength; if drawn_strength <= 3 then dungeon_low += drawn_strength; if drawn_card is Vampire or Lich then dungeon_undead += drawn_strength; if drawn_card is Dragon then dungeon_dragon += 9. If SACRIFICE X: remove X from items and discard the card unseen. In both cases set drawn_card to empty.
  7. [update] table. What happens: Set active_seat to the next seat clockwise after active_seat whose eliminated = false and passed = false.
  8. [update] table. What happens: round += 1.
  9. [update] table, when exactly one player has eliminated = false and passed = false. What happens: runner_seat = that player's seat. last_hp = 3 + (5 if Armor is in items) + (3 if Shield is in items). last_damage = dungeon_total - (dungeon_low if Torch is in items) - (dungeon_undead if Holy Water is in items) - (dungeon_dragon if Dragon Spear is in items).
  10. [tell] all players, when a run happened this round. What happens: Reveal every card in dungeon, together with last_damage and last_hp, for runner_seat.
  11. [update] seat runner_seat, when a run happened this round. What happens: If last_damage < last_hp then the runner's successes += 1, otherwise the runner's failures += 1. If the runner's failures >= 2, set the runner's eliminated = true.
  12. [check] table. What happens: End the game if any player has successes >= 2, or if exactly one player has eliminated = false.
  13. [update] table, when a run happened this round. What happens: New dungeon: refill deck with all 13 monsters; deck_count = 13; dungeon = []; dungeon_count = 0; dungeon_total = dungeon_low = dungeon_undead = dungeon_dragon = 0; items = all five; every player's passed = false and added_cards = []; active_seat = the first seat clockwise after runner_seat with eliminated = false.
  14. [check] table. What happens: End the game if round >= 40.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a run happens, the runner's HP is 3, plus 5 if Armor is in items, plus 3 if Shield is in items, so all five items give HP 11.
  R2. When a run happens, damage is the sum of the dungeon card strengths (Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9).
  R3. When Torch is in items at a run, every dungeon card of strength 3 or less adds 0 damage.
  R4. When Holy Water is in items at a run, every dungeon Vampire and Lich adds 0 damage.
  R5. When Dragon Spear is in items at a run, the Dragon adds 0 damage.
  R6. When damage < HP, the runner's successes increase by 1; otherwise (damage >= HP) the runner's failures increase by 1.
  R7. When a player's failures reach 2, eliminated becomes true and they are no longer asked anything.
  R8. When the active player chooses PASS, their passed becomes true for the rest of this dungeon.
  R9. When deck_count is 0, the active player is offered only PASS.
  R10. When the active player chooses DRAW, one card leaves deck, deck_count drops by 1, and only that player sees it.
  R11. When the player chooses ADD, the card joins dungeon face-down, dungeon_count rises by 1, and it is added to that player's added_cards.
  R12. When the player chooses SACRIFICE X, X is removed from items and the card is discarded unseen; SACRIFICE is offered only for items still in items.
  R13. When a turn ends, active_seat moves to the next seat clockwise with eliminated = false and passed = false.
  R14. When, at the end of a round, exactly one non-eliminated player has passed = false, that player runs the dungeon.
  R15. When a run happens, all dungeon cards, the damage and the HP are revealed to everyone.
  R16. When a run ends without ending the game, the deck is refilled to 13, the dungeon is emptied, all 5 items are restored, all passes are cleared, and active_seat becomes the first surviving seat clockwise from the runner.
  R17. When a player reaches 2 successes, the game ends and that player wins.
  R18. When only one player is not eliminated, the game ends and that player wins.
  R19. When round 40 ends with no winner, the non-eliminated player with the most successes wins, ties are broken by fewer failures, and any remaining tie is shared.
  R20. Each round, every non-eliminated player sends one short message at the same time, and all messages are then shown to everyone.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat with eliminated = false | options: one short free-text message
  - Pass or draw | asked: seat active_seat | options: when deck_count > 0: PASS, DRAW; when deck_count = 0: PASS only
  - Add or sacrifice | asked: seat active_seat after a DRAW | options: ADD, plus SACRIFICE <item> for each item still in items (Armor, Shield, Torch, Holy Water, Dragon Spear); when items is empty: ADD only

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: any player has successes >= 2, OR the count of players with eliminated = false is 1, OR round >= 40
  - each player's standing: (1 - you.eliminated) * 1000 + you.successes * 10 + (2 - you.failures) (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Non-eliminated players rank above eliminated ones. Among them, more successes ranks higher, then fewer failures. A player with 2 successes, or the sole survivor, therefore wins. Players level at the top share the win, which stands for the source's draw.
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

- each player: `successes` (number, visible: public, starts 0): successful runs
- each player: `failures` (number, visible: public, starts 0): failed runs
- each player: `eliminated` (bool, visible: public, starts False): true once the player has 2 failures
- each player: `passed` (bool, visible: public, starts False): the player has passed in the current dungeon
- the table: `items` (list, visible: public, starts ['Armor', 'Shield', 'Torch', 'Holy Water', 'Dragon Spear']): the equipment items remaining in this dungeon
- the table: `active_seat` (number, visible: public, starts 1): the seat whose turn it is
- the table: `deck_count` (number, visible: public, starts 13): cards left in the deck
- the table: `dungeon_count` (number, visible: public, starts 0): cards in the dungeon
- the table: `runner_seat` (number, visible: public, starts 0): the seat that ran the last dungeon
- the table: `last_hp` (number, visible: public, starts 0): the runner's HP in the last run
- the table: `last_damage` (number, visible: public, starts 0): the damage in the last run
- the table: `round` (number, visible: public, starts 0): rounds completed
- parameters (each must be an attribute holding this value, never a number buried in a step): base_hp = 3, armor_hp = 5, shield_hp = 3, torch_max_strength = 3, goblin_strength = 1, goblin_count = 2, skeleton_strength = 2, skeleton_count = 2, orc_strength = 3, orc_count = 2, vampire_strength = 4, vampire_count = 2, golem_strength = 5, golem_count = 2, lich_strength = 6, lich_count = 1, demon_strength = 7, demon_count = 1, dragon_strength = 9, dragon_count = 1, deck_size = 13, item_count = 5, successes_to_win = 2, failures_to_eliminate = 2, max_rounds = 40, initial_successes = 0, initial_failures = 0
- the game ends with ONE ending whose `rank_by` is `(1 - you.eliminated) * 1000 + you.successes * 10 + (2 - you.failures)`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "back_to_the_dungeon_single_delve",
    "name": "Back to the Dungeon: Single Delve",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Draw monsters, hide them in the dungeon or sacrifice gear; the last player who has not passed must run it. Two successes win, two failures eliminate."
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
        "key": "successes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "failures",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "passed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "drawn_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "added_cards",
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Goblin",
          "Goblin",
          "Skeleton",
          "Skeleton",
          "Orc",
          "Orc",
          "Vampire",
          "Vampire",
          "Golem",
          "Golem",
          "Lich",
          "Demon",
          "Dragon"
        ]
      },
      {
        "key": "all_monsters",
        "visible": "none",
        "type": "list",
        "initial": [
          "Goblin",
          "Goblin",
          "Skeleton",
          "Skeleton",
          "Orc",
          "Orc",
          "Vampire",
          "Vampire",
          "Golem",
          "Golem",
          "Lich",
          "Demon",
          "Dragon"
        ]
      },
      {
        "key": "dungeon",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "items",
        "visible": "public",
        "type": "list",
        "initial": [
          "Armor",
          "Shield",
          "Torch",
          "Holy Water",
          "Dragon Spear"
        ]
      },
      {
        "key": "all_items",
        "visible": "none",
        "type": "list",
        "initial": [
          "Armor",
          "Shield",
          "Torch",
          "Holy Water",
          "Dragon Spear"
        ]
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "dungeon_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "drawn_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "dungeon_total",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dungeon_low",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dungeon_undead",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dungeon_dragon",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "next_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ran",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "turns_done",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "runner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_hp",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_damage",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_dungeon",
        "visible": "public",
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
        "key": "base_hp",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "armor_hp",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "shield_hp",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "torch_max_strength",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "goblin_strength",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "goblin_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "skeleton_strength",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "skeleton_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "orc_strength",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "orc_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "vampire_strength",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "vampire_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "golem_strength",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "golem_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "lich_strength",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "lich_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "demon_strength",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "demon_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dragon_strength",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "dragon_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "item_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "successes_to_win",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "failures_to_eliminate",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "initial_successes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_failures",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "prepare the first dungeon",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "successes",
            "value": {
              "calc": "initial_successes"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "failures",
            "value": {
              "calc": "initial_failures"
            }
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
            "key": "passed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "drawn_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "added_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_monsters"
            }
          }
        },
        {
          "set": {
            "key": "dungeon",
            "value": []
          }
        },
        {
          "set": {
            "key": "items",
            "value": {
              "calc": "all_items"
            }
          }
        },
        {
          "set": {
            "key": "dungeon_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_low",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_undead",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_dragon",
            "value": 0
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
            "key": "deck_count",
            "value": {
              "calc": "deck_size"
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
      "phase": "turn",
      "label": "prepare the turn",
      "do": [
        {
          "set": {
            "key": "ran",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['PASS'] + (['DRAW'] if deck_count > 0 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "turn",
      "label": "announcement",
      "to": "all",
      "text": "It is seat {active_seat}'s turn. Dungeon: {dungeon_count} cards. Items remaining: {items}. Deck: {deck_count} cards. Seats that have passed: {[p.seat for p in players if p.passed]}. Successes and failures [seat, successes, failures]: {[[p.seat, p.successes, p.failures] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": {
        "where": "you.eliminated == False"
      },
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table. Talk is not binding."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "pass or draw",
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
        "bind": "choice1"
      },
      "text": "Your turn. PASS to sit out the rest of this dungeon, or DRAW the top monster card (only PASS is possible when the deck is empty)."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "pass or secret draw",
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "passed",
            "value": true,
            "if": {
              "calc": "$choice1 == 'PASS'"
            },
            "text": "Seat {player} passes and sits out the rest of this dungeon."
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "drawn_card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
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
              "calc": "$choice1 == 'DRAW'"
            }
          }
        },
        {
          "adjust": {
            "key": "deck_count",
            "value": -1,
            "if": {
              "calc": "$choice1 == 'DRAW'"
            },
            "text": "Seat {active_seat} draws a card."
          }
        },
        {
          "set": {
            "key": "drawn_strength",
            "value": {
              "calc": "goblin_strength if pick == 'Goblin' else skeleton_strength if pick == 'Skeleton' else orc_strength if pick == 'Orc' else vampire_strength if pick == 'Vampire' else golem_strength if pick == 'Golem' else lich_strength if pick == 'Lich' else demon_strength if pick == 'Demon' else dragon_strength"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
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
              "calc": "['ADD'] + ['SACRIFICE ' + i for i in items]"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "show the drawn card",
      "when": {
        "calc": "$choice1 == 'DRAW'"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "fields": [
        "drawn_card"
      ],
      "text": "The card you drew (only you see it):"
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "add or sacrifice",
      "when": {
        "calc": "$choice1 == 'DRAW'"
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
        "bind": "choice2"
      },
      "text": "You have just privately seen the card you drew (your drawn_card). ADD it face-down to the dungeon (only you will know it), or SACRIFICE one remaining item to discard the card unseen (the item is lost for this dungeon)."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "resolve the card",
      "when": {
        "calc": "$choice1 == 'DRAW'"
      },
      "do": [
        {
          "append": {
            "key": "dungeon",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "$choice2 == 'ADD'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "added_cards",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "$choice2 == 'ADD'"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_count",
            "value": 1,
            "if": {
              "calc": "$choice2 == 'ADD'"
            },
            "text": "Seat {active_seat} adds a card face-down to the dungeon."
          }
        },
        {
          "adjust": {
            "key": "dungeon_total",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD'"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_low",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD' and drawn_strength <= torch_max_strength"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_undead",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD' and pick in ['Vampire', 'Lich']"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_dragon",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD' and pick == 'Dragon'"
            }
          }
        },
        {
          "set": {
            "key": "items",
            "value": {
              "calc": "[i for i in items if 'SACRIFICE ' + i != $choice2]"
            },
            "if": {
              "calc": "$choice2 != 'ADD'"
            },
            "text": "Seat {active_seat} sacrifices an item and discards the card unseen. Items remaining: {items}."
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "drawn_card",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "advance the turn",
      "do": [
        {
          "set": {
            "key": "next_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > active_seat and not p.eliminated and not p.passed] + [p.seat + len(players) for p in players if not p.eliminated and not p.passed] + [active_seat])"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "next_seat - len(players) if next_seat > len(players) else next_seat"
            }
          }
        },
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "adjust": {
            "key": "turns_done",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "run",
      "label": "the run is set",
      "when": {
        "calc": "count(not p.eliminated and not p.passed for p in players) == 1"
      },
      "do": [
        {
          "set": {
            "key": "ran",
            "value": true
          }
        },
        {
          "set": {
            "key": "runner_seat",
            "value": {
              "calc": "min([p.seat for p in players if not p.eliminated and not p.passed])"
            }
          }
        },
        {
          "set": {
            "key": "last_hp",
            "value": {
              "calc": "base_hp + (armor_hp if 'Armor' in items else 0) + (shield_hp if 'Shield' in items else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_damage",
            "value": {
              "calc": "dungeon_total - (dungeon_low if 'Torch' in items else 0) - (dungeon_undead if 'Holy Water' in items else 0) - (dungeon_dragon if 'Dragon Spear' in items else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_dungeon",
            "value": {
              "calc": "dungeon"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "run",
      "label": "the reveal",
      "when": {
        "calc": "ran"
      },
      "to": "all",
      "text": "Seat {runner_seat} runs the dungeon with items {items}. Dungeon cards: {last_dungeon}. Damage {last_damage} against HP {last_hp}."
    },
    {
      "use": "update",
      "phase": "run",
      "label": "the run's result",
      "when": {
        "calc": "ran"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == runner_seat"
            },
            "key": "successes",
            "value": 1,
            "if": {
              "calc": "last_damage < last_hp"
            },
            "text": "Seat {player} survives the dungeon and gains a success."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == runner_seat"
            },
            "key": "failures",
            "value": 1,
            "if": {
              "calc": "last_damage >= last_hp"
            },
            "text": "Seat {player} falls in the dungeon and gains a failure."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == runner_seat and you.failures >= failures_to_eliminate"
            },
            "key": "eliminated",
            "value": true
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.seat == runner_seat and you.failures >= failures_to_eliminate"
            },
            "to": "out",
            "text": "Seat {player} has {failures_to_eliminate} failures and is eliminated."
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "run",
      "label": "after the run",
      "when": {
        "calc": "any(p.successes >= successes_to_win for p in players) or count(not p.eliminated for p in players) == 1"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "run",
      "label": "new dungeon",
      "when": {
        "calc": "ran"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_monsters"
            }
          }
        },
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "deck_size"
            }
          }
        },
        {
          "set": {
            "key": "dungeon",
            "value": []
          }
        },
        {
          "set": {
            "key": "dungeon_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_low",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_undead",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_dragon",
            "value": 0
          }
        },
        {
          "set": {
            "key": "items",
            "value": {
              "calc": "all_items"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "passed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "added_cards",
            "value": []
          }
        },
        {
          "set": {
       
... (cut)

Why it was refused: it plays, but part of it does nothing: player attribute `successes` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; player attribute `failures` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; player attribute `eliminated` is never changed in 3 random matches, so nothing updates it. Steps that name it: prepare the first dungeon, the run's result. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `all_monsters` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "back_to_the_dungeon_single_delve",
    "name": "Back to the Dungeon: Single Delve",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Draw monsters, hide them in the dungeon or sacrifice gear; the last player who has not passed must run it. Two successes win, two failures eliminate."
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
        "key": "successes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "failures",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "eliminated",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "passed",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "drawn_card",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "added_cards",
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Goblin",
          "Goblin",
          "Skeleton",
          "Skeleton",
          "Orc",
          "Orc",
          "Vampire",
          "Vampire",
          "Golem",
          "Golem",
          "Lich",
          "Demon",
          "Dragon"
        ]
      },
      {
        "key": "all_monsters",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "dungeon",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "items",
        "visible": "public",
        "type": "list",
        "initial": [
          "Armor",
          "Shield",
          "Torch",
          "Holy Water",
          "Dragon Spear"
        ]
      },
      {
        "key": "all_items",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_count",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "dungeon_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "drawn_strength",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "dungeon_total",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dungeon_low",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dungeon_undead",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "dungeon_dragon",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "next_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "ran",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "runner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_hp",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_damage",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_dungeon",
        "visible": "public",
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
        "key": "base_hp",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "armor_hp",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "shield_hp",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "torch_max_strength",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "goblin_strength",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "goblin_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "skeleton_strength",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "skeleton_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "orc_strength",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "orc_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "vampire_strength",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "vampire_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "golem_strength",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "golem_count",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "lich_strength",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "lich_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "demon_strength",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "demon_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dragon_strength",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "dragon_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "item_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "successes_to_win",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "failures_to_eliminate",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "initial_successes",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_failures",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "prepare the first dungeon",
      "do": [
        {
          "set": {
            "key": "all_monsters",
            "value": {
              "calc": "deck"
            }
          }
        },
        {
          "set": {
            "key": "all_items",
            "value": {
              "calc": "items"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "successes",
            "value": {
              "calc": "initial_successes"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "failures",
            "value": {
              "calc": "initial_failures"
            }
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
            "key": "passed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "drawn_card",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "added_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "dungeon",
            "value": []
          }
        },
        {
          "set": {
            "key": "dungeon_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_low",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_undead",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_dragon",
            "value": 0
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
            "key": "deck_count",
            "value": {
              "calc": "deck_size"
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
      "phase": "turn",
      "label": "prepare the turn",
      "do": [
        {
          "set": {
            "key": "ran",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['PASS'] + (['DRAW'] if deck_count > 0 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "turn",
      "label": "announcement",
      "to": "all",
      "text": "It is seat {active_seat}'s turn. Dungeon: {dungeon_count} cards. Items remaining: {items}. Deck: {deck_count} cards. Seats that have passed: {[p.seat for p in players if p.passed]}. Successes and failures [seat, successes, failures]: {[[p.seat, p.successes, p.failures] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": {
        "where": "you.eliminated == False"
      },
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table. Talk is not binding."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "pass or draw",
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
        "bind": "choice1"
      },
      "text": "Your turn. PASS to sit out the rest of this dungeon, or DRAW the top monster card (only PASS is possible when the deck is empty)."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "pass or secret draw",
      "do": [
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "passed",
            "value": true,
            "if": {
              "calc": "$choice1 == 'PASS'"
            },
            "text": "Seat {player} passes and sits out the rest of this dungeon."
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "drawn_card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
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
              "calc": "$choice1 == 'DRAW'"
            }
          }
        },
        {
          "adjust": {
            "key": "deck_count",
            "value": -1,
            "if": {
              "calc": "$choice1 == 'DRAW'"
            },
            "text": "Seat {active_seat} draws a card."
          }
        },
        {
          "set": {
            "key": "drawn_strength",
            "value": {
              "calc": "goblin_strength if pick == 'Goblin' else skeleton_strength if pick == 'Skeleton' else orc_strength if pick == 'Orc' else vampire_strength if pick == 'Vampire' else golem_strength if pick == 'Golem' else lich_strength if pick == 'Lich' else demon_strength if pick == 'Demon' else dragon_strength"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
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
              "calc": "['ADD'] + ['SACRIFICE ' + i for i in items]"
            },
            "if": {
              "calc": "$choice1 == 'DRAW'"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "show the drawn card",
      "when": {
        "calc": "$choice1 == 'DRAW'"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "mode": "self",
      "fields": [
        "drawn_card"
      ],
      "text": "The card you drew (only you see it):"
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "add or sacrifice",
      "when": {
        "calc": "$choice1 == 'DRAW'"
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
        "bind": "choice2"
      },
      "text": "You have just privately seen the card you drew (your drawn_card). ADD it face-down to the dungeon (only you will know it), or SACRIFICE one remaining item to discard the card unseen (the item is lost for this dungeon)."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "resolve the card",
      "when": {
        "calc": "$choice1 == 'DRAW'"
      },
      "do": [
        {
          "append": {
            "key": "dungeon",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "$choice2 == 'ADD'"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "active_seat"
            },
            "key": "added_cards",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "$choice2 == 'ADD'"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_count",
            "value": 1,
            "if": {
              "calc": "$choice2 == 'ADD'"
            },
            "text": "Seat {active_seat} adds a card face-down to the dungeon."
          }
        },
        {
          "adjust": {
            "key": "dungeon_total",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD'"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_low",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD' and drawn_strength <= torch_max_strength"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_undead",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD' and pick in ['Vampire', 'Lich']"
            }
          }
        },
        {
          "adjust": {
            "key": "dungeon_dragon",
            "value": {
              "calc": "drawn_strength"
            },
            "if": {
              "calc": "$choice2 == 'ADD' and pick == 'Dragon'"
            }
          }
        },
        {
          "set": {
            "key": "items",
            "value": {
              "calc": "[i for i in items if 'SACRIFICE ' + i != $choice2]"
            },
            "if": {
              "calc": "$choice2 != 'ADD'"
            },
            "text": "Seat {active_seat} sacrifices an item and discards the card unseen. Items remaining: {items}."
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "drawn_card",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "advance the turn",
      "do": [
        {
          "set": {
            "key": "next_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > active_seat and not p.eliminated and not p.passed] + [p.seat + len(players) for p in players if not p.eliminated and not p.passed] + [999])"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "active_seat if next_seat == 999 else (next_seat - len(players) if next_seat > len(players) else next_seat)"
            }
          }
        },
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "run",
      "label": "the run is set",
      "when": {
        "calc": "count(not p.eliminated and not p.passed for p in players) == 1"
      },
      "do": [
        {
          "set": {
            "key": "ran",
            "value": true
          }
        },
        {
          "set": {
            "key": "runner_seat",
            "value": {
              "calc": "min([p.seat for p in players if not p.eliminated and not p.passed])"
            }
          }
        },
        {
          "set": {
            "key": "last_hp",
            "value": {
              "calc": "base_hp + (armor_hp if 'Armor' in items else 0) + (shield_hp if 'Shield' in items else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_damage",
            "value": {
              "calc": "dungeon_total - (dungeon_low if 'Torch' in items else 0) - (dungeon_undead if 'Holy Water' in items else 0) - (dungeon_dragon if 'Dragon Spear' in items else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_dungeon",
            "value": {
              "calc": "dungeon"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "run",
      "label": "the reveal",
      "when": {
        "calc": "ran"
      },
      "to": "all",
      "text": "Seat {runner_seat} runs the dungeon with items {items}. Dungeon cards: {last_dungeon}. Damage {last_damage} against HP {last_hp}."
    },
    {
      "use": "update",
      "phase": "run",
      "label": "the run's result",
      "when": {
        "calc": "ran"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == runner_seat"
            },
            "key": "successes",
            "value": 1,
            "if": {
              "calc": "last_damage < last_hp"
            },
            "text": "Seat {player} survives the dungeon and gains a success."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == runner_seat"
            },
            "key": "failures",
            "value": 1,
            "if": {
              "calc": "last_damage >= last_hp"
            },
            "text": "Seat {player} falls in the dungeon and gains a failure."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == runner_seat and you.failures >= failures_to_eliminate"
            },
            "key": "eliminated",
            "value": true
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.seat == runner_seat and you.failures >= failures_to_eliminate"
            },
            "to": "out",
            "text": "Seat {player} has {failures_to_eliminate} failures and is eliminated."
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "run",
      "label": "after the run",
      "when": {
        "calc": "any(p.successes >= successes_to_win for p in players) or count(not p.eliminated for p in players) == 1"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "run",
      "label": "new dungeon",
      "when": {
        "calc": "ran"
      },
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "all_monsters"
            }
          }
        },
        {
          "set": {
            "key": "deck_count",
            "value": {
              "calc": "deck_size"
            }
          }
        },
        {
          "set": {
            "key": "dungeon",
            "value": []
          }
        },
        {
          "set": {
            "key": "dungeon_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_low",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_undead",
            "value": 0
          }
        },
        {
          "set": {
            "key": "dungeon_dragon",
            "value": 0
          }
        },
        {
          "set": {
            "key": "items",
            "value": {
              "calc": "all_items"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "passed",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "added_cards",
            "value": []
          }
        },
        {
          "set": {
            "key": "next_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > runner_seat and not p.eliminated] + [p.seat + len(players) for p in players if not p.eliminated] + [999])"
            }
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "active_seat if next_seat == 999 else (next_seat - len(players) if next_seat > len(players) else next_seat)"
            }
          }
        }
      ],
      "text": "A new dungeon begins: the deck is reshuffled to {deck_size} cards, all {item_count} items are restored and all passes are cleared. Seat {active_seat} starts."
    },
    {
      "use": "check",
      "phase": "run",
      "label": "round limit",
      "when": {
        "calc": "round >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "any(p.successes >= successes_to_win for p in players) or count(not p.eliminated for p in players) == 1 or round >= max_rounds"
      },
      "rank_by": "(1 - you.eliminated) * 1000 + you.successes * 10 + (2 - you.failures)",
      "text": "Winner: {result}. Final [seat, successes, failures, eliminated]: {[[p.seat, p.successes, p.failures, p.eliminated] for p in players]}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "The adventurer has base HP {base_hp} and five equipment items: Armor (+{armor_hp} HP), Shield (+{shield_hp} HP), Torch (defeats every monster of strength {torch_max_strength} or less), Holy Water (defeats Vampires and the Lich) and Dragon Spear (defeats the Dragon). The monster deck has {deck_size} cards: Goblin {goblin_strength} x{goblin_count}, Skeleton {skeleton_strength} x{skeleton_count}, Orc {orc_strength} x{orc_count}, Vampire {vampire_strength} x{vampire_count}, Golem {golem_strength} x{golem_count}, Lich {lich_strength} x{lich_count}, Demon {demon_strength} x{demon_count}, Dragon {dragon_strength} x{dragon_count}. Each player tracks successes and failures, both starting at 0.\n\nSeat 1 begins the first dungeon. The deck is shuffled, the dungeon starts empty, all {item_count} items are present and no one has passed.\n\nEach round is one turn. 1) The table is told whose turn it is, the number of cards in the dungeon, the items remaining, the cards left in the deck, who has passed, and everyone's successes and failures. 2) Talk: every player who is not eliminated writes one short message at the same time, without seeing the others; all messages are then shown to everyone. Talk is not binding. 3) The active player chooses PASS or DRAW. If the deck is empty, only PASS is offered. PASS: you sit out the rest of this dungeon. 4) DRAW: you privately see the top card of the deck, which leaves the deck. Then choose ADD (the card goes face-down into the dungeon; only you know what it is) or SACRIFICE an item (one remaining item you name is removed for this dungeon and the card is discarded unseen by others; offered only for items still remaining). 5) The turn passes to the next player clockwise (increasing seat number, wrapping around) who is neither eliminated nor passed in this dungeon.\n\nTHE RUN: at the end of a round, as soon as exactly one non-eliminated player has not passed, that player is the runner. HP = {base_hp}, plus {armor_hp} if Armor remains, plus {shield_hp} if Shield remains. Damage = the sum of the strengths of all dungeon cards, minus the strength of each card defeated by a remaining item (Torch: strength 1, 2 and 3; Holy Water: Vampires and the Lich; Dragon Spear: the Dragon). All dungeon cards are then revealed to everyone, with the damage and HP. If damage < HP, the runner gains 1 success; otherwise (damage >= HP) the runner gains 1 failure. A player with {failures_to_eliminate} failures is eliminated and takes no further part.\n\nNEW DUNGEON: after a run, all {deck_size} monsters are reshuffled into a new deck, the dungeon is emptied, all {item_count} items are restored and all passes are cleared. The next active player is the first surviving player clockwise from the runner.\n\nGAME END: the game ends immediately when a player reaches {successes_to_win} successes (that player wins) or only one player is not eliminated (that player wins). Otherwise it ends after round {max_rounds}: the surviving player with the most successes wins; if tied, the one with the fewest failures; any remaining tie is shared."
}
````
