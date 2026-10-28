# 06 coder

- time: 2026-10-28T04:42:36+00:00 (105.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 4c1ebdb4ca0ab07f, reply sha256 4dea5437e377f939

## Sent

````
# Task: write the XColos game file for "Three Pigs: Secret Materials"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- Materials: Straw, Wood, Brick.
- Locations: Fields (Straw), Forest (Wood), Brickyard (Brick). Each starts with a pile of 0.
- Each player is secretly dealt a Favoured Material:
  - 3 players: shuffle one Straw, one Wood and one Brick card and deal one each, so all three differ.
  - 4 players: shuffle two each of Straw, Wood and Brick and deal one each.
- A player's Favoured Material is known only to them.
- Each player starts with 0 Straw, 0 Wood and 0 Brick. A player's stockpile is private, known only to them.

HOUSES
- A house is one material and has three sections, built in order: Floor, Walls, Roof.
- Each section costs 2 of that house's material, or 1 if it is the builder's Favoured Material.
- A player may have at most one unfinished house of each material.
- A player may complete at most 2 houses of any one material.
- Which sections each player has built, and of what material, is public. The cost paid is not shown.

EACH ROUND (up to 15 rounds)
1. Bonus: one location is drawn at random (each 1/3) and announced.
2. Refill: every location's pile gains 3, and the announced location gains 2 more.
3. Talk: everyone writes one short message at the same time, then all messages are shown to everyone. Messages bind no one.
4. Gather choice: everyone simultaneously chooses one of seven options:
   - Fields, Forest, Brickyard, Market;
   - Wolf-Fields, Wolf-Forest, Wolf-Brickyard.
5. Reveal: all choices are shown.
6. Resolve each of the three locations:
   - If any player chose Wolf at that location, nobody gathers there and its pile is unchanged.
   - Otherwise, the pile is divided equally among the players who chose it, rounding down. Each takes their share of that material, and the remainder stays in the pile.
   - If nobody chose the location, the pile stays.
   - Each player is told only their own gain, but the piles and the number of gatherers are public, so gains can be computed by anyone.
7. Market: every player who chose Market gains 1 of their Favoured Material. Any number of players can use the Market without sharing.
8. Players who chose a Wolf gain nothing.
9. Build action 1: everyone simultaneously chooses Build Straw, Build Wood, Build Brick or Pass.
   - A build adds the next section to that player's house of that material, starting a new house at the Floor if none is unfinished, and pays the cost from their stockpile.
   - If the player cannot pay, or the build would start a third house of that material, it counts as Pass.
   - The resulting public build state is shown.
10. Build action 2: exactly as build action 1.
11. Win check: any player with 3 completed houses has finished.
    - If exactly one player has finished, they win.
    - If several have, the finisher with the most total leftover resources wins. If that is tied, it is a draw among them.
    - The game then ends.
12. If round 15 ends with no finisher, the game ends. The winner is the player with the most completed houses, then the most built sections. If still tied, it is a draw.

How the winner is decided: The first player to complete 3 houses (at most 2 of any one material) wins. If several do so in the same round, the one with the most leftover resources wins, and a further tie is a draw. If nobody finishes in 15 rounds, the winner is the player with the most completed houses, then the most sections. Any remaining tie is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Three Pigs: Secret Materials (3 to 4 players, best with 3)

Each player has a secret Favoured Material. Players gather straw, wood and brick from shared piles at the same time, can send the Wolf to stop a location paying out, and build houses section by section. The first to finish 3 houses wins.

STATE (every item below must exist in the file):
  - each player: favoured (text, starts ''); only its owner sees it. Secret Favoured Material: Straw, Wood or Brick, dealt from favour_deck
  - each player: straw (number, starts 0); only its owner sees it. Private stockpile of Straw
  - each player: wood (number, starts 0); only its owner sees it. Private stockpile of Wood
  - each player: brick (number, starts 0); only its owner sees it. Private stockpile of Brick
  - each player: last_gain (text, starts ''); only its owner sees it. This round's gather and market gain, told only to the owner
  - each player: gather_choice (text, starts ''); everyone sees it. This round's gather choice, collected by poll and revealed to all afterwards
  - each player: build_choice (text, starts ''); only its owner sees it. The build choice in the current build action
  - each player: straw_progress (number, starts 0); everyone sees it. Sections built on the unfinished Straw house: 0 none, 1 Floor, 2 Floor and Walls
  - each player: wood_progress (number, starts 0); everyone sees it. Sections built on the unfinished Wood house (0-2)
  - each player: brick_progress (number, starts 0); everyone sees it. Sections built on the unfinished Brick house (0-2)
  - each player: straw_done (number, starts 0); everyone sees it. Completed Straw houses (at most 2)
  - each player: wood_done (number, starts 0); everyone sees it. Completed Wood houses (at most 2)
  - each player: brick_done (number, starts 0); everyone sees it. Completed Brick houses (at most 2)
  - each player: completed (number, starts 0); everyone sees it. Total completed houses: straw_done + wood_done + brick_done
  - each player: sections (number, starts 0); everyone sees it. Total sections ever built, in all houses
  - each player: finished (number, starts 0); everyone sees it. 1 once completed >= 3, otherwise 0
  - the table: favour_deck (list, starts []); hidden from all players. Favoured Material cards: [Straw, Wood, Brick] for 3 players, two of each for 4 players
  - the table: locations (list, starts ['Fields', 'Forest', 'Brickyard']); everyone sees it. The locations the bonus is drawn from
  - the table: round (number, starts 0); everyone sees it. Current round number
  - the table: bonus_location (text, starts ''); everyone sees it. This round's bonus location
  - the table: fields_pile (number, starts 0); everyone sees it. Straw waiting at the Fields
  - the table: forest_pile (number, starts 0); everyone sees it. Wood waiting at the Forest
  - the table: brickyard_pile (number, starts 0); everyone sees it. Brick waiting at the Brickyard
  - the table: fields_gatherers (number, starts 0); everyone sees it. Number of players who chose Fields this round
  - the table: forest_gatherers (number, starts 0); everyone sees it. Number of players who chose Forest this round
  - the table: brickyard_gatherers (number, starts 0); everyone sees it. Number of players who chose Brickyard this round
  - the table: fields_wolves (number, starts 0); everyone sees it. Number of players who chose Wolf-Fields this round
  - the table: forest_wolves (number, starts 0); everyone sees it. Number of players who chose Wolf-Forest this round
  - the table: brickyard_wolves (number, starts 0); everyone sees it. Number of players who chose Wolf-Brickyard this round
  - parameters, each kept as a table attribute: max_rounds = 15, refill_per_location = 3, bonus_extra = 2, bonus_chance_each_location = 0.3333, section_cost = 2, favoured_section_cost = 1, sections_per_house = 3, max_unfinished_per_material = 1, max_completed_per_material = 2, houses_to_finish = 3, market_gain = 1, build_actions_per_round = 2, initial_pile = 0, initial_stock = 0, favour_cards_each_material_3p = 1, favour_cards_each_material_4p = 2, finisher_rank_offset = 100000, completed_weight = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set fields_pile, forest_pile and brickyard_pile to 0.
  2. Fill favour_deck: with 3 players it holds one Straw, one Wood and one Brick; with 4 players it holds two of each.
  3. For each player, draw one card at random from favour_deck, set it as their favoured and remove it from favour_deck. Leftover cards stay hidden.
  4. Every player starts with straw = 0, wood = 0, brick = 0, all house progress and done counts at 0, completed = 0, sections = 0 and finished = 0.
  5. Sync: each player is privately told their favoured material and their stockpile.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; bonus_location = one entry of locations drawn at random (each 1/3).
  2. [tell] all players. What happens: Announce 'Round {round}: the bonus location is {bonus_location}.'
  3. [update] all players. What happens: fields_pile += 3; forest_pile += 3; brickyard_pile += 3; then the pile of bonus_location gains 2 more. Announce the three piles.
  4. [poll] all players answers: short text message. What happens: Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind no one.
  5. [poll] all players answers: one of: Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard. What happens: Each player's gather_choice = their answer. Nobody sees any choice until all are in.
  6. [tell] all players. What happens: Reveal every player's gather_choice to all.
  7. [update] all players. What happens: Count fields_gatherers (gather_choice = Fields), forest_gatherers, brickyard_gatherers, fields_wolves (gather_choice = Wolf-Fields), forest_wolves and brickyard_wolves. Set every player's last_gain = 'nothing'.
  8. [update] all players. What happens: Fields: if fields_wolves = 0 and fields_gatherers > 0, then share = floor(fields_pile / fields_gatherers); each player with gather_choice = Fields gets straw += share and last_gain = share Straw; fields_pile -= share * fields_gatherers. Otherwise fields_pile is unchanged.
  9. [update] all players. What happens: Forest: if forest_wolves = 0 and forest_gatherers > 0, then share = floor(forest_pile / forest_gatherers); each Forest chooser gets wood += share and last_gain = share Wood; forest_pile -= share * forest_gatherers. Otherwise forest_pile is unchanged.
  10. [update] all players. What happens: Brickyard: if brickyard_wolves = 0 and brickyard_gatherers > 0, then share = floor(brickyard_pile / brickyard_gatherers); each Brickyard chooser gets brick += share and last_gain = share Brick; brickyard_pile -= share * brickyard_gatherers. Otherwise brickyard_pile is unchanged.
  11. [update] all players. What happens: Market: each player with gather_choice = Market gains 1 of their favoured material (straw, wood or brick) and last_gain = 1 of that material. Players who chose a Wolf gain nothing.
  12. [tell] all players. What happens: Announce the piles after resolution and the number of gatherers and wolves at each location.
  13. [sync] all players. What happens: Each player privately receives their own last_gain and stockpile (straw, wood, brick).
  14. [poll] all players answers: one of the offered options: Build Straw, Build Wood, Build Brick, Pass. What happens: build_choice = answer (build action 1).
  15. [update] all players. What happens: For each player with build_choice = Build M: cost = 1 if favoured = M, else 2. If stock of M < cost, or (M_done = 2 and M_progress = 0), it counts as Pass. Otherwise stock of M -= cost; M_progress += 1; sections += 1; if M_progress = 3, then M_progress = 0, M_done += 1 and completed += 1.
  16. [tell] all players. What happens: Show every player's public build state: straw/wood/brick progress and done, completed and sections. The cost paid is not shown.
  17. [poll] all players answers: one of the offered options: Build Straw, Build Wood, Build Brick, Pass. What happens: build_choice = answer (build action 2).
  18. [update] all players. What happens: Apply build action 2 exactly as build action 1.
  19. [tell] all players. What happens: Show every player's public build state again.
  20. [update] all players. What happens: For each player, finished = 1 if completed >= 3, otherwise 0.
  21. [check] all players. What happens: End the game if any player has finished = 1, or if round >= 15. Otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When setup runs with 3 players, then favour_deck holds one Straw, one Wood and one Brick and each player is dealt one, so all three favoured materials differ.
  R2. When setup runs with 4 players, then favour_deck holds two Straw, two Wood and two Brick, each player is dealt one, and the 2 undealt cards stay hidden.
  R3. When the game starts, then every pile is 0 and every player has straw = 0, wood = 0 and brick = 0.
  R4. When a player's favoured material or stockpile changes, then only that player is told it.
  R5. When a round begins, then bonus_location is drawn at random from Fields, Forest and Brickyard and announced to all.
  R6. When the refill happens, then each pile gains 3 and the bonus location's pile gains 2 more, so it gains 5 in total.
  R7. When the talk step runs, then every player submits one message at the same time and all messages are shown to everyone.
  R8. When the gather choice is made, then all players choose at the same time from Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest and Wolf-Brickyard, and all choices are revealed afterwards.
  R9. When at least one player chose Wolf at a location, then nobody gathers there and that pile is unchanged.
  R10. When no Wolf is at a location and g >= 1 players chose it, then each of them gains floor(pile / g) of its material and the remainder stays: 5 straw split by 2 gives each 2 and leaves 1.
  R11. When nobody chose a location, then its pile stays and carries over to the next round.
  R12. When a player chose Market, then they gain 1 of their favoured material, however many others also chose Market.
  R13. When a player chose a Wolf option, then they gain nothing that round.
  R14. When gathering is resolved, then each player is privately told their own gain, and the remaining piles and the counts of gatherers and wolves are public.
  R15. When a player builds a section of material M, then it costs 1 M if favoured = M, otherwise 2 M, taken from their stockpile.
  R16. When a player builds M and has an unfinished M house, then the next section is added (Floor, then Walls, then Roof); otherwise a new M house is started at the Floor.
  R17. When a build brings M_progress to 3, then the house is complete: M_done += 1, completed += 1 and M_progress returns to 0.
  R18. When a player cannot pay the cost, or the build would start a third house of material M (M_done = 2), then the build counts as Pass and nothing changes.
  R19. When a section is built, then sections += 1, and the house states are shown to all but the cost paid is not.
  R20. When a round's builds happen, then there are exactly 2 simultaneous build actions, the second resolved after the first.
  R21. When a player has completed >= 3 at the end of a round, then finished = 1 and the game ends after that round.
  R22. When exactly one player has finished, then that player wins.
  R23. When several players finish in the same round, then the one with the most leftover straw + wood + brick wins, and players tied for the most share a draw.
  R24. When round 15 ends with no finisher, then the game ends and the most completed houses wins, then the most sections, and a remaining tie is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all players | options: Any short free-text message.
  - Gather choice | asked: all players | options: Every seat, in every situation: Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard.
  - Build action 1 and build action 2 | asked: all players | options: Pass, always. Build M (Straw, Wood or Brick) only when the seat's stock of M is at least the cost (1 if favoured = M, else 2) and the build would not start a third M house (not M_done = 2). A seat that can afford nothing is offered only Pass.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: count of players with finished = 1 >= 1, or round >= 15
  - each player's standing: you.finished * (100000 + you.straw + you.wood + you.brick) + (1 - you.finished) * (you.completed * 100 + you.sections) (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: If anyone has completed 3 houses, the finishers rank above everyone else and are ordered by total leftover straw + wood + brick. Otherwise players are ranked by completed houses, then by total sections built. The highest value wins, and players level at the top share the win (a draw).
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

- each player: `gather_choice` (text, visible: public, starts ''): This round's gather choice, collected by poll and revealed to all afterwards
- each player: `straw_progress` (number, visible: public, starts 0): Sections built on the unfinished Straw house: 0 none, 1 Floor, 2 Floor and Walls
- each player: `wood_progress` (number, visible: public, starts 0): Sections built on the unfinished Wood house (0-2)
- each player: `brick_progress` (number, visible: public, starts 0): Sections built on the unfinished Brick house (0-2)
- each player: `straw_done` (number, visible: public, starts 0): Completed Straw houses (at most 2)
- each player: `wood_done` (number, visible: public, starts 0): Completed Wood houses (at most 2)
- each player: `brick_done` (number, visible: public, starts 0): Completed Brick houses (at most 2)
- each player: `completed` (number, visible: public, starts 0): Total completed houses: straw_done + wood_done + brick_done
- each player: `sections` (number, visible: public, starts 0): Total sections ever built, in all houses
- each player: `finished` (number, visible: public, starts 0): 1 once completed >= 3, otherwise 0
- the table: `round` (number, visible: public, starts 0): Current round number
- the table: `bonus_location` (text, visible: public, starts ''): This round's bonus location
- the table: `fields_pile` (number, visible: public, starts 0): Straw waiting at the Fields
- the table: `forest_pile` (number, visible: public, starts 0): Wood waiting at the Forest
- the table: `brickyard_pile` (number, visible: public, starts 0): Brick waiting at the Brickyard
- parameters (each must be an attribute holding this value, never a number buried in a step): max_rounds = 15, refill_per_location = 3, bonus_extra = 2, bonus_chance_each_location = 0.3333, section_cost = 2, favoured_section_cost = 1, sections_per_house = 3, max_unfinished_per_material = 1, max_completed_per_material = 2, houses_to_finish = 3, market_gain = 1, build_actions_per_round = 2, initial_pile = 0, initial_stock = 0, favour_cards_each_material_3p = 1, favour_cards_each_material_4p = 2, finisher_rank_offset = 100000, completed_weight = 100
- the game ends with ONE ending whose `rank_by` is `you.finished * (100000 + you.straw + you.wood + you.brick) + (1 - you.finished) * (you.completed * 100 + you.sections)`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "three_pigs_secret_materials",
    "name": "Three Pigs: Secret Materials",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Gather straw, wood and brick from shared piles, send the Wolf, and be first to finish 3 houses with your secret Favoured Material."
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
        "key": "favoured",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "straw",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wood",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brick",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_gain",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "gather_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "build_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "build_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "build_now",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "straw_progress",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wood_progress",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brick_progress",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "straw_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wood_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brick_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "completed",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sections",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "finished",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "favour_deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "share",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "locations",
        "visible": "public",
        "type": "list",
        "initial": [
          "Fields",
          "Forest",
          "Brickyard"
        ]
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bonus_location",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "fields_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "forest_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brickyard_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fields_gatherers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "forest_gatherers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brickyard_gatherers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fields_wolves",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "forest_wolves",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brickyard_wolves",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "refill_per_location",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bonus_extra",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bonus_chance_each_location",
        "visible": "public",
        "type": "number",
        "initial": 0.3333
      },
      {
        "key": "section_cost",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "favoured_section_cost",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sections_per_house",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_unfinished_per_material",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_completed_per_material",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "houses_to_finish",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "market_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "build_actions_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "initial_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_stock",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "favour_cards_each_material_3p",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favour_cards_each_material_4p",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "finisher_rank_offset",
        "visible": "public",
        "type": "number",
        "initial": 100000
      },
      {
        "key": "completed_weight",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "empty piles",
      "do": [
        {
          "set": {
            "key": "fields_pile",
            "value": {
              "calc": "initial_pile"
            }
          }
        },
        {
          "set": {
            "key": "forest_pile",
            "value": {
              "calc": "initial_pile"
            }
          }
        },
        {
          "set": {
            "key": "brickyard_pile",
            "value": {
              "calc": "initial_pile"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "fill the favour deck",
      "do": [
        {
          "set": {
            "key": "favour_deck",
            "value": {
              "calc": "['Straw', 'Wood', 'Brick'] + (['Straw', 'Wood', 'Brick'] if len(players) >= 4 and favour_cards_each_material_4p >= 2 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal favoured materials",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4 and len(favour_deck) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4 and len(favour_deck) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting stock",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "straw",
            "value": {
              "calc": "initial_stock"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wood",
            "value": {
              "calc": "initial_stock"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "brick",
            "value": {
              "calc": "initial_stock"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "straw_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wood_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "brick_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "straw_done",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wood_done",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "brick_done",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "completed",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sections",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "finished",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your secret",
      "mode": "self",
      "to": "all",
      "fields": [
        "favoured",
        "straw",
        "wood",
        "brick"
      ],
      "text": "Your secret Favoured Material and your stockpile:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "bonus",
      "label": "new round and bonus draw",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "bonus_location",
            "value": {
              "calc": "locations[min(int(uniform(0, len(locations))), len(locations) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "gather_choice",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bonus",
      "label": "bonus announced",
      "to": "all",
      "text": "Round {round}: the bonus location is {bonus_location}."
    },
    {
      "use": "update",
      "phase": "refill",
      "label": "refill",
      "do": [
        {
          "adjust": {
            "key": "fields_pile",
            "value": {
              "calc": "refill_per_location + (bonus_extra if bonus_location == 'Fields' else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "forest_pile",
            "value": {
              "calc": "refill_per_location + (bonus_extra if bonus_location == 'Forest' else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "brickyard_pile",
            "value": {
              "calc": "refill_per_location + (bonus_extra if bonus_location == 'Brickyard' else 0)"
            }
          }
        }
      ],
      "text": "Piles after the refill: Fields {fields_pile} Straw, Forest {forest_pile} Wood, Brickyard {brickyard_pile} Brick."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table. Messages bind no one."
    },
    {
      "use": "poll",
      "phase": "gather",
      "label": "gather choice",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Fields",
          "Forest",
          "Brickyard",
          "Market",
          "Wolf-Fields",
          "Wolf-Forest",
          "Wolf-Brickyard"
        ]
      },
      "store": "gather_choice",
      "text": "Choose where to go this round: Fields, Forest, Brickyard, Market, or send the Wolf to a location (Wolf-Fields, Wolf-Forest, Wolf-Brickyard). Nobody sees any choice until all are in. Piles: Fields {fields_pile}, Forest {forest_pile}, Brickyard {brickyard_pile}."
    },
    {
      "use": "tell",
      "phase": "gather",
      "label": "reveal choices",
      "to": "all",
      "text": "Gather choices [seat, choice]: {[[p.seat, p.gather_choice] for p in players]}"
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve gathering",
      "do": [
        {
          "set": {
            "key": "fields_gatherers",
            "value": {
              "calc": "count(p.gather_choice == 'Fields' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "forest_gatherers",
            "value": {
              "calc": "count(p.gather_choice == 'Forest' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "brickyard_gatherers",
            "value": {
              "calc": "count(p.gather_choice == 'Brickyard' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "fields_wolves",
            "value": {
              "calc": "count(p.gather_choice == 'Wolf-Fields' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "forest_wolves",
            "value": {
              "calc": "count(p.gather_choice == 'Wolf-Forest' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "brickyard_wolves",
            "value": {
              "calc": "count(p.gather_choice == 'Wolf-Brickyard' for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_gain",
            "value": "nothing"
          }
        },
        {
          "set": {
            "key": "share",
            "value": {
              "calc": "int(fields_pile / max(fields_gatherers, 1)) if fields_wolves == 0 and fields_gatherers > 0 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Fields' and fields_wolves == 0"
            },
            "key": "last_gain",
            "value": {
              "calc": "('0123456789'[int(share / 10)] if share >= 10 else '') + '0123456789'[share - int(share / 10) * 10] + ' Straw'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Fields' and fields_wolves == 0"
            },
            "key": "straw",
            "value": {
              "calc": "share"
            }
          }
        },
        {
          "adjust": {
            "key": "fields_pile",
            "value": {
              "calc": "-share * fields_gatherers"
            },
            "if": {
              "calc": "fields_wolves == 0 and fields_gatherers > 0"
            }
          }
        },
        {
          "set": {
            "key": "share",
            "value": {
              "calc": "int(forest_pile / max(forest_gatherers, 1)) if forest_wolves == 0 and forest_gatherers > 0 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Forest' and forest_wolves == 0"
            },
            "key": "last_gain",
            "value": {
              "calc": "('0123456789'[int(share / 10)] if share >= 10 else '') + '0123456789'[share - int(share / 10) * 10] + ' Wood'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Forest' and forest_wolves == 0"
            },
            "key": "wood",
            "value": {
              "calc": "share"
            }
          }
        },
        {
          "adjust": {
            "key": "forest_pile",
            "value": {
              "calc": "-share * forest_gatherers"
            },
            "if": {
              "calc": "forest_wolves == 0 and forest_gatherers > 0"
            }
          }
        },
        {
          "set": {
            "key": "share",
            "value": {
              "calc": "int(brickyard_pile / max(brickyard_gatherers, 1)) if brickyard_wolves == 0 and brickyard_gatherers > 0 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Brickyard' and brickyard_wolves == 0"
            },
            "key": "last_gain",
            "value": {
              "calc": "('0123456789'[int(share / 10)] if share >= 10 else '') + '0123456789'[share - int(share / 10) * 10] + ' Brick'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Brickyard' and brickyard_wolves == 0"
            },
            "key": "brick",
            "value": {
              "calc": "share"
            }
          }
        },
        {
          "adjust": {
            "key": "brickyard_pile",
            "value": {
              "calc": "-share * brickyard_gatherers"
            },
            "if": {
              "calc": "brickyard_wolves == 0 and brickyard_gatherers > 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Market' and you.favoured == 'Straw'"
            },
            "key": "straw",
            "value": {
              "calc": "market_gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Market' and you.favoured == 'Wood'"
            },
            "key": "wood",
            "value": {
              "calc": "market_gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Market' and you.favoured == 'Brick'"
            },
            "key": "brick",
            "value": {
              "calc": "market_gain"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Market'"
            },
            "key": "last_gain",
            "value": {
              "calc": "'0123456789'[market_gain] + ' ' + you.favoured"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "piles after gathering",
      "to": "all",
      "text": "After gathering: Fields {fields_pile} Straw left ({fields_gatherers} gatherers, {fields_wolves} wolves); Forest {forest_pile} Wood left ({forest_gatherers} gatherers, {forest_wolves} wolves); Brickyard {brickyard_pile} Brick left ({brickyard_gatherers} gatherers, {brickyard_wolves} wolves)."
    },
    {
      "use": "sync",
      "phase": "resolve",
      "label": "your gain",
      "mode": "self",
      "to": "all",
      "fields": [
        "last_gain",
        "straw",
        "wood",
        "brick"
      ],
      "text": "Your gain this round and your stockpile:"
    },
    {
      "use": "update",
      "phase": "build",
      "label": "build offers 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "build_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "build_offer",
            "value": {
              "calc": "['Pass'] + (['Build Straw'] if you.straw >= (favoured_section_cost if you.favoured == 'Straw' else section_cost) and not (you.straw_done >= max_completed_per_material and you.straw_progress == 0) else []) + (['Build Wood'] if you.wood >= (favoured_section_cost if you.favoured == 'Wood' else section_cost) and not (you.wood_done >= max_completed_per_material and you.wood_progress == 0) else []) + (['Build Brick'] if you.brick >= (favoured_section_cost if you.favoured == 'Brick' else section_cost) and not (you.brick_done >= max_completed_per_material and you.brick_progress == 0) else [])"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "build",
      "label": "build action 1",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "build_offer"
        }
      },
      "store": "build_choice",
      "text": "Build action 1 of {build_actions_per_round}: build the next section of a house, or Pass. You are offered only the builds you can pay for."
    },
    {
      "use": "update",
      "phase": "build",
      "label": "apply build 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "build_now
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `locations` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "three_pigs_secret_materials",
    "name": "Three Pigs: Secret Materials",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Gather straw, wood and brick from shared piles, send the Wolf, and be first to finish 3 houses with your secret Favoured Material."
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
        "key": "favoured",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "straw",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wood",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brick",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_gain",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "gather_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "build_choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "build_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "build_now",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "straw_progress",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wood_progress",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brick_progress",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "straw_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wood_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brick_done",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "completed",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sections",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "finished",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "favour_deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "share",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "locations",
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
        "key": "bonus_location",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "fields_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "forest_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brickyard_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fields_gatherers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "forest_gatherers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brickyard_gatherers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fields_wolves",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "forest_wolves",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "brickyard_wolves",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "refill_per_location",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "bonus_extra",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bonus_chance_each_location",
        "visible": "public",
        "type": "number",
        "initial": 0.3333
      },
      {
        "key": "section_cost",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "favoured_section_cost",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "sections_per_house",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_unfinished_per_material",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_completed_per_material",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "houses_to_finish",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "market_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "build_actions_per_round",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "initial_pile",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_stock",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "favour_cards_each_material_3p",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favour_cards_each_material_4p",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "finisher_rank_offset",
        "visible": "public",
        "type": "number",
        "initial": 100000
      },
      {
        "key": "completed_weight",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "empty piles and locations",
      "do": [
        {
          "set": {
            "key": "locations",
            "value": [
              "Fields",
              "Forest",
              "Brickyard"
            ]
          }
        },
        {
          "set": {
            "key": "fields_pile",
            "value": {
              "calc": "initial_pile"
            }
          }
        },
        {
          "set": {
            "key": "forest_pile",
            "value": {
              "calc": "initial_pile"
            }
          }
        },
        {
          "set": {
            "key": "brickyard_pile",
            "value": {
              "calc": "initial_pile"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "fill the favour deck",
      "do": [
        {
          "set": {
            "key": "favour_deck",
            "value": {
              "calc": "['Straw', 'Wood', 'Brick'] + (['Straw', 'Wood', 'Brick'] if len(players) >= 4 and favour_cards_each_material_4p >= 2 else [])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal favoured materials",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favour_deck[min(int(uniform(0, len(favour_deck))), len(favour_deck) - 1)]"
            },
            "if": {
              "calc": "len(players) >= 4 and len(favour_deck) > 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "favoured",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favour_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4 and len(favour_deck) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "starting stock",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "straw",
            "value": {
              "calc": "initial_stock"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wood",
            "value": {
              "calc": "initial_stock"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "brick",
            "value": {
              "calc": "initial_stock"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "straw_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wood_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "brick_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "straw_done",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wood_done",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "brick_done",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "completed",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "sections",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "finished",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your secret",
      "mode": "self",
      "to": "all",
      "fields": [
        "favoured",
        "straw",
        "wood",
        "brick"
      ],
      "text": "Your secret Favoured Material and your stockpile:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "bonus",
      "label": "new round and bonus draw",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "bonus_location",
            "value": {
              "calc": "locations[min(int(uniform(0, len(locations))), len(locations) - 1)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "gather_choice",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "bonus",
      "label": "bonus announced",
      "to": "all",
      "text": "Round {round}: the bonus location is {bonus_location}."
    },
    {
      "use": "update",
      "phase": "refill",
      "label": "refill",
      "do": [
        {
          "adjust": {
            "key": "fields_pile",
            "value": {
              "calc": "refill_per_location + (bonus_extra if bonus_location == 'Fields' else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "forest_pile",
            "value": {
              "calc": "refill_per_location + (bonus_extra if bonus_location == 'Forest' else 0)"
            }
          }
        },
        {
          "adjust": {
            "key": "brickyard_pile",
            "value": {
              "calc": "refill_per_location + (bonus_extra if bonus_location == 'Brickyard' else 0)"
            }
          }
        }
      ],
      "text": "Piles after the refill: Fields {fields_pile} Straw, Forest {forest_pile} Wood, Brickyard {brickyard_pile} Brick."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Say one short thing to the table. Messages bind no one."
    },
    {
      "use": "poll",
      "phase": "gather",
      "label": "gather choice",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Fields",
          "Forest",
          "Brickyard",
          "Market",
          "Wolf-Fields",
          "Wolf-Forest",
          "Wolf-Brickyard"
        ]
      },
      "store": "gather_choice",
      "text": "Choose where to go this round: Fields, Forest, Brickyard, Market, or send the Wolf to a location (Wolf-Fields, Wolf-Forest, Wolf-Brickyard). Nobody sees any choice until all are in. Piles: Fields {fields_pile}, Forest {forest_pile}, Brickyard {brickyard_pile}."
    },
    {
      "use": "tell",
      "phase": "gather",
      "label": "reveal choices",
      "to": "all",
      "text": "Gather choices [seat, choice]: {[[p.seat, p.gather_choice] for p in players]}"
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve gathering",
      "do": [
        {
          "set": {
            "key": "fields_gatherers",
            "value": {
              "calc": "count(p.gather_choice == 'Fields' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "forest_gatherers",
            "value": {
              "calc": "count(p.gather_choice == 'Forest' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "brickyard_gatherers",
            "value": {
              "calc": "count(p.gather_choice == 'Brickyard' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "fields_wolves",
            "value": {
              "calc": "count(p.gather_choice == 'Wolf-Fields' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "forest_wolves",
            "value": {
              "calc": "count(p.gather_choice == 'Wolf-Forest' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "brickyard_wolves",
            "value": {
              "calc": "count(p.gather_choice == 'Wolf-Brickyard' for p in players)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_gain",
            "value": "nothing"
          }
        },
        {
          "set": {
            "key": "share",
            "value": {
              "calc": "int(fields_pile / max(fields_gatherers, 1)) if fields_wolves == 0 and fields_gatherers > 0 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Fields' and fields_wolves == 0"
            },
            "key": "last_gain",
            "value": {
              "calc": "('0123456789'[int(share / 10)] if share >= 10 else '') + '0123456789'[share - int(share / 10) * 10] + ' Straw'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Fields' and fields_wolves == 0"
            },
            "key": "straw",
            "value": {
              "calc": "share"
            }
          }
        },
        {
          "adjust": {
            "key": "fields_pile",
            "value": {
              "calc": "-share * fields_gatherers"
            },
            "if": {
              "calc": "fields_wolves == 0 and fields_gatherers > 0"
            }
          }
        },
        {
          "set": {
            "key": "share",
            "value": {
              "calc": "int(forest_pile / max(forest_gatherers, 1)) if forest_wolves == 0 and forest_gatherers > 0 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Forest' and forest_wolves == 0"
            },
            "key": "last_gain",
            "value": {
              "calc": "('0123456789'[int(share / 10)] if share >= 10 else '') + '0123456789'[share - int(share / 10) * 10] + ' Wood'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Forest' and forest_wolves == 0"
            },
            "key": "wood",
            "value": {
              "calc": "share"
            }
          }
        },
        {
          "adjust": {
            "key": "forest_pile",
            "value": {
              "calc": "-share * forest_gatherers"
            },
            "if": {
              "calc": "forest_wolves == 0 and forest_gatherers > 0"
            }
          }
        },
        {
          "set": {
            "key": "share",
            "value": {
              "calc": "int(brickyard_pile / max(brickyard_gatherers, 1)) if brickyard_wolves == 0 and brickyard_gatherers > 0 else 0"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Brickyard' and brickyard_wolves == 0"
            },
            "key": "last_gain",
            "value": {
              "calc": "('0123456789'[int(share / 10)] if share >= 10 else '') + '0123456789'[share - int(share / 10) * 10] + ' Brick'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Brickyard' and brickyard_wolves == 0"
            },
            "key": "brick",
            "value": {
              "calc": "share"
            }
          }
        },
        {
          "adjust": {
            "key": "brickyard_pile",
            "value": {
              "calc": "-share * brickyard_gatherers"
            },
            "if": {
              "calc": "brickyard_wolves == 0 and brickyard_gatherers > 0"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Market' and you.favoured == 'Straw'"
            },
            "key": "straw",
            "value": {
              "calc": "market_gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Market' and you.favoured == 'Wood'"
            },
            "key": "wood",
            "value": {
              "calc": "market_gain"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.gather_choice == 'Market' and you.favoured == 'Brick'"
            },
            "key": "brick",
            "value": {
              "calc": "market_gain"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.gather_choice == 'Market'"
            },
            "key": "last_gain",
            "value": {
              "calc": "'0123456789'[market_gain] + ' ' + you.favoured"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "piles after gathering",
      "to": "all",
      "text": "After gathering: Fields {fields_pile} Straw left ({fields_gatherers} gatherers, {fields_wolves} wolves); Forest {forest_pile} Wood left ({forest_gatherers} gatherers, {forest_wolves} wolves); Brickyard {brickyard_pile} Brick left ({brickyard_gatherers} gatherers, {brickyard_wolves} wolves)."
    },
    {
      "use": "sync",
      "phase": "resolve",
      "label": "your gain",
      "mode": "self",
      "to": "all",
      "fields": [
        "last_gain",
        "straw",
        "wood",
        "brick"
      ],
      "text": "Your gain this round and your stockpile:"
    },
    {
      "use": "update",
      "phase": "build",
      "label": "build offers 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "build_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "build_offer",
            "value": {
              "calc": "['Pass'] + (['Build Straw'] if you.straw >= (favoured_section_cost if you.favoured == 'Straw' else section_cost) and not (you.straw_done >= max_completed_per_material and you.straw_progress == 0) else []) + (['Build Wood'] if you.wood >= (favoured_section_cost if you.favoured == 'Wood' else section_cost) and not (you.wood_done >= max_completed_per_material and you.wood_progress == 0) else []) + (['Build Brick'] if you.brick >= (favoured_section_cost if you.favoured == 'Brick' else section_cost) and not (you.brick_done >= max_completed_per_material and you.brick_progress == 0) else [])"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "build",
      "label": "build action 1",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "build_offer"
        }
      },
      "store": "build_choice",
      "text": "Build action 1 of {build_actions_per_round}: build the next section of a house, or Pass. You are offered only the builds you can pay for."
    },
    {
      "use": "update",
      "phase": "build",
      "label": "apply build 1",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "build_now",
            "value": {
              "calc": "'Straw' if you.build_choice == 'Build Straw' and you.straw >= (favoured_section_cost if you.favoured == 'Straw' else section_cost) and not (you.straw_done >= max_completed_per_material and you.straw_progress == 0) else ('Wood' if you.build_choice == 'Build Wood' and you.wood >= (favoured_section_cost if you.favoured == 'Wood' else section_cost) and not (you.wood_done >= max_completed_per_material and you.wood_progress == 0) else ('Brick' if you.build_choice == 'Build Brick' and you.brick >= (favoured_section_cost if you.favoured == 'Brick' else section_cost) and not (you.brick_done >= max_completed_per_material and you.brick_progress == 0) else ''))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Straw'"
            },
            "key": "straw",
            "value": {
              "calc": "-(favoured_section_cost if you.favoured == 'Straw' else section_cost)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Straw'"
            },
            "key": "straw_progress",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Wood'"
            },
            "key": "wood",
            "value": {
              "calc": "-(favoured_section_cost if you.favoured == 'Wood' else section_cost)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Wood'"
            },
            "key": "wood_progress",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Brick'"
            },
            "key": "brick",
            "value": {
              "calc": "-(favoured_section_cost if you.favoured == 'Brick' else section_cost)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Brick'"
            },
            "key": "brick_progress",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now != ''"
            },
            "key": "sections",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.straw_progress >= sections_per_house"
            },
            "key": "straw_done",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.wood_progress >= sections_per_house"
            },
            "key": "wood_done",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.brick_progress >= sections_per_house"
            },
            "key": "brick_done",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "completed",
            "value": {
              "calc": "you.straw_done + you.wood_done + you.brick_done"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.straw_progress >= sections_per_house"
            },
            "key": "straw_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.wood_progress >= sections_per_house"
            },
            "key": "wood_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.brick_progress >= sections_per_house"
            },
            "key": "brick_progress",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "build",
      "label": "build state 1",
      "to": "all",
      "text": "Build state after action 1 [seat, straw progress, straw done, wood progress, wood done, brick progress, brick done, completed, sections]: {[[p.seat, p.straw_progress, p.straw_done, p.wood_progress, p.wood_done, p.brick_progress, p.brick_done, p.completed, p.sections] for p in players]}"
    },
    {
      "use": "update",
      "phase": "build",
      "label": "build offers 2",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "build_choice",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "build_offer",
            "value": {
              "calc": "['Pass'] + (['Build Straw'] if you.straw >= (favoured_section_cost if you.favoured == 'Straw' else section_cost) and not (you.straw_done >= max_completed_per_material and you.straw_progress == 0) else []) + (['Build Wood'] if you.wood >= (favoured_section_cost if you.favoured == 'Wood' else section_cost) and not (you.wood_done >= max_completed_per_material and you.wood_progress == 0) else []) + (['Build Brick'] if you.brick >= (favoured_section_cost if you.favoured == 'Brick' else section_cost) and not (you.brick_done >= max_completed_per_material and you.brick_progress == 0) else [])"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "build",
      "label": "build action 2",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "build_offer"
        }
      },
      "store": "build_choice",
      "text": "Build action 2 of {build_actions_per_round}: build the next section of a house, or Pass. You are offered only the builds you can pay for."
    },
    {
      "use": "update",
      "phase": "build",
      "label": "apply build 2",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "build_now",
            "value": {
              "calc": "'Straw' if you.build_choice == 'Build Straw' and you.straw >= (favoured_section_cost if you.favoured == 'Straw' else section_cost) and not (you.straw_done >= max_completed_per_material and you.straw_progress == 0) else ('Wood' if you.build_choice == 'Build Wood' and you.wood >= (favoured_section_cost if you.favoured == 'Wood' else section_cost) and not (you.wood_done >= max_completed_per_material and you.wood_progress == 0) else ('Brick' if you.build_choice == 'Build Brick' and you.brick >= (favoured_section_cost if you.favoured == 'Brick' else section_cost) and not (you.brick_done >= max_completed_per_material and you.brick_progress == 0) else ''))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Straw'"
            },
            "key": "straw",
            "value": {
              "calc": "-(favoured_section_cost if you.favoured == 'Straw' else section_cost)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Straw'"
            },
            "key": "straw_progress",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Wood'"
            },
            "key": "wood",
            "value": {
              "calc": "-(favoured_section_cost if you.favoured == 'Wood' else section_cost)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Wood'"
            },
            "key": "wood_progress",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Brick'"
            },
            "key": "brick",
            "value": {
              "calc": "-(favoured_section_cost if you.favoured == 'Brick' else section_cost)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now == 'Brick'"
            },
            "key": "brick_progress",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.build_now != ''"
            },
            "key": "sections",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.straw_progress >= sections_per_house"
            },
            "key": "straw_done",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.wood_progress >= sections_per_house"
            },
            "key": "wood_done",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.brick_progress >= sections_per_house"
            },
            "key": "brick_done",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "completed",
            "value": {
              "calc": "you.straw_done + you.wood_done + you.brick_done"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.straw_progress >= sections_per_house"
            },
            "key": "straw_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.wood_progress >= sections_per_house"
            },
            "key": "wood_progress",
            "value": 0
          }
        },
        {
          "set": {
            "players": {
              "where": "you.brick_progress >= sections_per_house"
            },
            "key": "brick_progress",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "build",
      "label": "build state 2",
      "to": "all",
      "text": "Build state after action 2 [seat, straw progress, straw done, wood progress, wood done, brick progress, brick done, completed, sections]: {[[p.seat, p.straw_progress, p.straw_done, p.wood_progress, p.wood_done, p.brick_progress, p.brick_done, p.completed, p.sections] for p in players]}"
    },
    {
      "use": "update",
      "phase": "end",
      "label": "who has finished",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "finished",
            "value": {
              "calc": "1 if you.completed >= houses_to_finish else 0"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "win check",
      "when": {
        "calc": "count(p.finished == 1 for p in players) >= 1 or round >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "count(p.finished == 1 for p in players) >= 1 or round >= max_rounds"
      },
      "rank_by": "you.finished * (100000 + you.straw + you.wood + you.brick) + (1 - you.finished) * (you.completed * 100 + you.sections)",
      "text": "Winner: {result}. Final figures [seat, finished, completed houses, sections, leftover resources]: {[[p.seat, p.finished, p.completed, p.sections, p.straw + p.wood + p.brick] for p in players]}."
    }
  },
  "limits": {
    "rounds": 15,
    "rounds_max": 16,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Materials are Straw, Wood and Brick. The locations are {locations}: Fields gives Straw, Forest gives Wood, Brickyard gives Brick. Each pile starts at {initial_pile}.\n\nEach player is secretly dealt a Favoured Material. With 3 players one Straw, one Wood and one Brick card are shuffled and dealt, so all three differ; with 4 players two of each are shuffled and one dealt to each, and the undealt cards stay hidden. Your Favoured Material is known only to you. Everyone starts with {initial_stock} Straw, Wood and Brick; your stockpile is private.\n\nHOUSES: a house is one material and has {sections_per_house} sections, built in order: Floor, Walls, Roof. Each section costs {section_cost} of that house's material, or {favoured_section_cost} if it is your Favoured Material. You may have at most {max_unfinished_per_material} unfinished house of each material, and may complete at most {max_completed_per_material} houses of any one material. Which sections each player has built, and of what material, is public; the cost paid is not shown.\n\nEACH ROUND (up to {max_rounds} rounds):\n1. Bonus: one location is drawn at random (each 1/3) and announced.\n2. Refill: every pile gains {refill_per_location}, and the bonus location gains {bonus_extra} more.\n3. Talk: everyone writes one short message at the same time; all messages are shown to everyone. Messages bind no one.\n4. Gather choice: everyone simultaneously chooses one of Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard.\n5. Reveal: all choices are shown.\n6. Resolve each location: if any player chose Wolf at that location, nobody gathers there and its pile is unchanged. Otherwise the pile is divided equally among the players who chose it, rounding down; each takes their share and the remainder stays in the pile (5 split by 2 gives each 2 and leaves 1). If nobody chose a location, its pile stays and carries over. Each player is told only their own gain, but the piles and the numbers of gatherers and wolves are public.\n7. Market: every player who chose Market gains {market_gain} of their Favoured Material, however many others chose Market.\n8. Players who chose a Wolf gain nothing.\n9. Build action 1: everyone simultaneously chooses Build Straw, Build Wood, Build Brick or Pass. A build adds the next section to your house of that material, starting a new house at the Floor if none is unfinished, and pays the cost from your stockpile. If you cannot pay, or the build would start a third house of that material, it counts as Pass and nothing changes; you are only offered the builds you can make, and Pass is always offered. When a Roof is built the house is complete. The public build state is then shown.\n10. Build action 2: exactly as build action 1 ({build_actions_per_round} build actions per round).\n11. Win check: any player with {houses_to_finish} completed houses has finished. If exactly one player has finished, they win. If several have, the finisher with the most total leftover resources (Straw + Wood + Brick) wins; if that is tied, it is a draw among them. The game then ends.\n12. If round {max_rounds} ends with no finisher, the game ends: the player with the most completed houses wins, then the most built sections; if still tied, it is a draw."
}
```
````
