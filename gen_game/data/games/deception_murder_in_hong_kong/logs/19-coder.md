# 19 coder

- time: 2026-10-28T02:05:00+00:00 (144.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 fa0e5575845fa113, reply sha256 01636e1f11723996

## Sent

````
# Task: write the XColos game file for "Deception: Five Clues"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 6 to 8; set `meta.players` to {"min": 6, "max": 8, "suggested": 7} (the suggested size is the one the game plays best at).

ROLES. One player is publicly the Forensic Scientist (seat 1). The engine secretly and randomly deals the other players these roles: 1 Murderer, 1 Accomplice, 1 Witness, and Investigators for the rest (2, 3 or 4 Investigators with 6, 7 or 8 players). The Murderer and Accomplice are the Murderer side. The Scientist, Witness and Investigators are the Investigator side. The Accomplice is told who the Murderer is. The Witness is told who the Murderer and Accomplice are, but not which of the two is which, and not the solution. The Scientist is told all roles.

CARDS. Every player except the Scientist is dealt, face up for all to see, 2 Clue words from the Clue list and 2 Means words from the Means list, with no repeats.
- Clue list (16): Glove, Train Ticket, Lipstick, Key, Diary, Ring, Cigarette, Phone, Wallet, Photo, Watch, Umbrella, Receipt, Hair, Button, Mask.
- Means list (16): Rope, Poison, Knife, Pillow, Hammer, Pistol, Insulin, Brick, Drowning, Electric Wire, Scarf, Bare Hands, Fire, Bottle, Axe, Car.

SOLUTION. The Murderer privately chooses one of their own 2 Clues as the Key Evidence and one of their own 2 Means as the Means of Murder. The engine then privately tells the Scientist and the Accomplice the solution.

SCENE TILES. Each tile lists 6 options.
- Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident.
- Location: Living Room, Bedroom, Bathroom, Kitchen, Street, Office.
The Deck holds 6 tiles:
- Time of Death: Dawn, Morning, Noon, Afternoon, Evening, Night.
- Weather: Sunny, Stormy, Dry, Humid, Cold, Hot.
- Victim's Build: Large, Thin, Tall, Short, Disfigured, Fit.
- Trace at Scene: Fingerprint, Footprint, Bruise, Blood Stain, Body Fluid, Scar.
- Corpse Condition: Still Warm, Stiff, Decayed, Incomplete, Intact, Twisted.
- Duration of Crime: Instant, Brief, Gradual, Prolonged, Days, Unclear.

BADGES. Every player except the Scientist starts with 1 badge.

EACH ROUND (5 rounds):
1. Tile. In round 1 the tile is Cause of Death. In round 2 it is Location. In rounds 3, 4 and 5, one tile is drawn at random from the Deck and removed.
2. Marker. The Scientist privately chooses exactly one of the tile's 6 options, and the marked option is announced to all. The Scientist may never send any other message.
3. Talk. Every player except the Scientist writes one short message at the same time. All messages are then shown to everyone.
4. Accusation. Every player who still has a badge chooses at the same time either PASS or one accusation: one Clue word and one Means word currently on the table. Anyone who accuses loses their badge.
5. Resolution. Every accusation is announced with its accuser. An accusation is correct only if its Clue is the Key Evidence and its Means is the Means of Murder, and each is announced as correct or wrong. A pair taken from two different players' cards is always wrong. If any accusation is correct, the case is SOLVED and play moves to the Witness Hunt. Otherwise the next round begins.

WITNESS HUNT. When the case is solved, the Murderer privately names one player other than the Scientist, the Accomplice and themself. If that player is the Witness, the Murderer side wins. Otherwise the Investigator side wins.

END. If the case is not solved by the end of round 5, the Murderer side wins.

How the winner is decided: Team win, decided purely by matching. If any accusation exactly matches the secret Clue and Means, and the Murderer then fails to name the Witness, the Scientist, the Witness and all Investigators win. If the Murderer names the Witness correctly after a solve, or if no correct accusation happens within 5 rounds, the Murderer and Accomplice win. There are no draws.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Deception: Five Clues (6 to 8 players, best with 7)

A hidden-role deduction game. A public Forensic Scientist marks scene-tile options to steer Investigators towards the Murderer's secret Clue and Means. The Murderer side wins by evading for 5 rounds, or by finding the Witness after the case is solved.

STATE (every item below must exist in the file):
  - each player: role (text, starts 'dealt: Scientist for seat 1; for the other seats a random one of Murderer, Accomplice, Witness, or Investigator (player count minus 4 Investigators)'); only its owner sees it. secret role; the Scientist's role is publicly known
  - each player: side (text, starts 'murderer for Murderer and Accomplice, investigator otherwise'); only its owner sees it. team
  - each player: intel (text, starts "Accomplice: the Murderer's seat; Witness: the two seats of the Murderer and Accomplice in random order; Scientist: every seat's role; others: empty"); only its owner sees it. private role knowledge given at setup
  - each player: solution_known (text, starts ''); only its owner sees it. Key Evidence and Means of Murder, filled in for the Scientist and the Accomplice
  - each player: clues (list, starts '2 Clue words drawn from clue_deck (empty for seat 1)'); everyone sees it. face-up Clue cards
  - each player: means (list, starts '2 Means words drawn from means_deck (empty for seat 1)'); everyone sees it. face-up Means cards
  - each player: badge (number, starts '1 (0 for seat 1)'); everyone sees it. accusations remaining
  - each player: acc_clue (text, starts ''); everyone sees it. this round's accused Clue, or PASS; revealed at resolution
  - each player: acc_means (text, starts ''); everyone sees it. this round's accused Means; revealed at resolution
  - each player: won (number, starts 0); everyone sees it. 1 if this player's side won
  - the table: clue_deck (list, starts ['Glove', 'Train Ticket', 'Lipstick', 'Key', 'Diary', 'Ring', 'Cigarette', 'Phone', 'Wallet', 'Photo', 'Watch', 'Umbrella', 'Receipt', 'Hair', 'Button', 'Mask']); hidden from all players. undealt Clue words
  - the table: means_deck (list, starts ['Rope', 'Poison', 'Knife', 'Pillow', 'Hammer', 'Pistol', 'Insulin', 'Brick', 'Drowning', 'Electric Wire', 'Scarf', 'Bare Hands', 'Fire', 'Bottle', 'Axe', 'Car']); hidden from all players. undealt Means words
  - the table: tile_deck (list, starts ['Time of Death', 'Weather', "Victim's Build", 'Trace at Scene', 'Corpse Condition', 'Duration of Crime']); hidden from all players. undrawn scene tiles
  - the table: current_tile (text, starts ''); everyone sees it. this round's scene tile
  - the table: marker (text, starts ''); everyone sees it. option the Scientist marked this round
  - the table: key_evidence (text, starts ''); hidden from all players. the Murderer's chosen Clue
  - the table: means_of_murder (text, starts ''); hidden from all players. the Murderer's chosen Means
  - the table: round (number, starts 0); everyone sees it. current round number
  - the table: solved (bool, starts False); everyone sees it. a correct accusation has been made
  - the table: hunt_target (number, starts 0); everyone sees it. seat named by the Murderer in the Witness Hunt
  - the table: game_over (number, starts 0); everyone sees it. 1 when the game has ended
  - parameters, each kept as a table attribute: rounds = 5, scientist_seat = 1, clue_list_size = 16, means_list_size = 16, clues_per_player = 2, means_per_player = 2, starting_badges = 1, options_per_tile = 6, deck_tiles = 6, deck_draws = 3, murderers = 1, accomplices = 1, witnesses = 1, investigators_formula_offset = 4, win_value = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is publicly the Forensic Scientist.
  2. The engine secretly and randomly deals the other seats 1 Murderer, 1 Accomplice, 1 Witness and (player count minus 4) Investigators into role, and sets side.
  3. Intel is set: the Accomplice learns the Murderer's seat; the Witness learns the two seats of the Murderer and Accomplice without learning which is which; the Scientist learns every role.
  4. Each seat except seat 1 draws 2 Clue words from clue_deck into clues and 2 Means words from means_deck into means, at random and without repeats. These cards are public.
  5. Each seat except seat 1 gets badge 1.
  6. The Murderer is asked privately to choose one of their own clues as key_evidence and one of their own means as means_of_murder.
  7. solution_known of seat 1 and of the Accomplice is set to the key_evidence and the means_of_murder.
  8. Every player is sent their own state (sync).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; current_tile = 'Cause of Death' if round==1, 'Location' if round==2, otherwise a random tile removed from tile_deck; every acc_clue and acc_means is cleared; current_tile is announced with its 6 options
  2. [ask] seat 1 answers: one of the 6 options of current_tile. What happens: marker = the chosen option; the marker is announced to all
  3. [poll] every player except seat 1 answers: short text. What happens: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}
  4. [poll] every player with badge == 1 answers: PASS, or one Clue word currently in any player's clues. What happens: acc_clue = the answer; hidden until resolution
  5. [poll] every player whose acc_clue is not PASS answers: one Means word currently in any player's means. What happens: acc_means = the answer; badge -= 1 for each such player; hidden until resolution
  6. [update] table. What happens: each accusation is announced with its accuser and marked correct if acc_clue == key_evidence and acc_means == means_of_murder, wrong otherwise; solved = true if any accusation is correct
  7. [ask] the player whose role is Murderer, when solved == true answers: a seat other than seat 1, the Accomplice and the Murderer. What happens: hunt_target = the chosen seat
  8. [update] table. What happens: when solved == true: if the role of hunt_target is Witness, won = 1 for side murderer, else won = 1 for side investigator; game_over = 1. Else when round == 5: won = 1 for side murderer; game_over = 1
  9. [check] table. What happens: end the game if game_over == 1, otherwise continue to the next round

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Seat 1 is always the Forensic Scientist, and that role is public.
  R2. When the game starts with N players, then the other N-1 seats are dealt exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators at random.
  R3. When roles are dealt, then the Accomplice's intel names the Murderer's seat.
  R4. When roles are dealt, then the Witness's intel names the two seats of the Murderer and the Accomplice without saying which is which, and the Witness does not get the solution.
  R5. When roles are dealt, then the Scientist's intel lists every seat's role.
  R6. When cards are dealt, then every seat except seat 1 holds 2 Clue words and 2 Means words, all public, with no word appearing twice at the table.
  R7. When the Murderer chooses the solution, then key_evidence must be one of the Murderer's own 2 clues and means_of_murder must be one of their own 2 means.
  R8. When the solution is chosen, then the Scientist and the Accomplice are told it, and no one else is.
  R9. When the game starts, then every seat except seat 1 has badge 1 and seat 1 has badge 0.
  R10. When round is 1, then current_tile is Cause of Death; when round is 2, then it is Location.
  R11. When round is 3, 4 or 5, then current_tile is drawn at random from tile_deck and removed from it.
  R12. When the Scientist marks, then exactly one of current_tile's 6 options becomes marker and is announced to all.
  R13. The Scientist never writes a talk message or makes an accusation.
  R14. When talk happens, then every player except seat 1 writes one message at the same time, and all messages are shown to everyone afterwards.
  R15. When accusations are made, then only players with badge 1 are asked, all at the same time, to choose PASS or one Clue on the table and one Means on the table.
  R16. When a player accuses, then their badge drops from 1 to 0 and they are not asked to accuse again.
  R17. When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong.
  R18. When an accusation pairs a Clue and a Means from two different players' cards, then it is always wrong.
  R19. When solved is true, then the Murderer names one seat other than seat 1, the Accomplice and themself.
  R20. When the named seat is the Witness, then the Murderer and the Accomplice get won = 1; otherwise the Scientist, the Witness and all Investigators get won = 1.
  R21. When round 5 ends with solved still false, then the Murderer and the Accomplice get won = 1 and the game ends.
  R22. When no accusation is correct in rounds 1 to 4, then the next round begins.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Murderer's choice of Key Evidence (setup) | asked: the Murderer | options: the 2 Clue words in the Murderer's own clues
  - Murderer's choice of Means of Murder (setup) | asked: the Murderer | options: the 2 Means words in the Murderer's own means
  - Marker | asked: seat 1 | options: the 6 options of current_tile
  - Talk | asked: every seat except seat 1 | options: short free text
  - Accusation: Clue | asked: every seat with badge 1 (never seat 1) | options: PASS, or any Clue word in any player's clues
  - Accusation: Means | asked: every seat that chose a Clue | options: any Means word in any player's means
  - Witness Hunt | asked: the Murderer, only when solved is true | options: every seat except seat 1, the Accomplice and the Murderer

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == 1
  - each player's standing: you.won (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - min_to_win: 1 (a player whose standing is below it cannot win; if none reaches it, the match ends with no winner)
  - how the result is decided: Team win: every player on the winning side has won = 1 and shares the win; the losing side has 0.
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

- each player: `clues` (list, visible: public, starts '2 Clue words drawn from clue_deck (empty for seat 1)'): face-up Clue cards
- each player: `means` (list, visible: public, starts '2 Means words drawn from means_deck (empty for seat 1)'): face-up Means cards
- each player: `badge` (number, visible: public, starts '1 (0 for seat 1)'): accusations remaining
- each player: `won` (number, visible: public, starts 0): 1 if this player's side won
- the table: `current_tile` (text, visible: public, starts ''): this round's scene tile
- the table: `marker` (text, visible: public, starts ''): option the Scientist marked this round
- the table: `round` (number, visible: public, starts 0): current round number
- the table: `solved` (bool, visible: public, starts False): a correct accusation has been made
- the table: `hunt_target` (number, visible: public, starts 0): seat named by the Murderer in the Witness Hunt
- parameters (each must be an attribute holding this value, never a number buried in a step): rounds = 5, scientist_seat = 1, clue_list_size = 16, means_list_size = 16, clues_per_player = 2, means_per_player = 2, starting_badges = 1, options_per_tile = 6, deck_tiles = 6, deck_draws = 3, murderers = 1, accomplices = 1, witnesses = 1, investigators_formula_offset = 4, win_value = 1
- the game ends with ONE ending whose `rank_by` is `you.won`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- that ending's `min_to_win` is `1`: a player below it cannot win, and if nobody reaches it the match ends with no winner
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

1) Build the accusation options from the players' current `clues` and `means` attributes. The Clue choice offers every Clue word on any seat's cards plus PASS. The Means choice offers every Means word on any seat's cards. Do not take options from clue_deck or means_deck (the undealt words) or from the accuser's own cards only. Ask for the Means only when the accuser did not PASS. 2) Make dealing consistent. Remove each dealt word from the deck lists, and build the Scientist's and Accomplice's intel and the solution from the seats' actual `role`, `clues` and `means`. Do this after roles and cards are final, so that preset or given roles and cards are not overwritten or contradicted. 3) Initialise `solved` to False and `hunt_target` to 0 directly, with no True or -1 placeholder. 4) In resolution, mark an accusation correct when acc_clue == key_evidence and acc_means == means_of_murder. In that case set solved = true. Set the accuser's badge to 0 for every accusation, right or wrong, and never ask a badgeless seat again. 5) When solved, ask the Murderer for hunt_target. Offer only seats other than the Scientist, the Accomplice and the Murderer. Then set won = win_value for the winning side's players, as R20 says.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "deception_five_clues",
    "name": "Deception: Five Clues",
    "players": {
      "min": 6,
      "max": 8,
      "suggested": 7
    },
    "blurb": "A public Forensic Scientist marks scene tiles to steer the Investigators to the Murderer's secret Clue and Means, while the Murderer side hides and hunts the Witness."
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
        "key": "role",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "side",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "intel",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "solution_known",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clues",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "means",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "badge",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "acc_clue",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "acc_means",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick_clue",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pick_means",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "verdict",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "clue_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Glove",
          "Train Ticket",
          "Lipstick",
          "Key",
          "Diary",
          "Ring",
          "Cigarette",
          "Phone",
          "Wallet",
          "Photo",
          "Watch",
          "Umbrella",
          "Receipt",
          "Hair",
          "Button",
          "Mask"
        ]
      },
      {
        "key": "means_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Rope",
          "Poison",
          "Knife",
          "Pillow",
          "Hammer",
          "Pistol",
          "Insulin",
          "Brick",
          "Drowning",
          "Electric Wire",
          "Scarf",
          "Bare Hands",
          "Fire",
          "Bottle",
          "Axe",
          "Car"
        ]
      },
      {
        "key": "tile_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Time of Death",
          "Weather",
          "Victim's Build",
          "Trace at Scene",
          "Corpse Condition",
          "Duration of Crime"
        ]
      },
      {
        "key": "tile_table",
        "visible": "none",
        "type": "list",
        "initial": [
          ["Cause of Death", "Suffocation", "Severe Injury", "Loss of Blood", "Illness", "Poisoning", "Accident"],
          ["Location", "Living Room", "Bedroom", "Bathroom", "Kitchen", "Street", "Office"],
          ["Time of Death", "Dawn", "Morning", "Noon", "Afternoon", "Evening", "Night"],
          ["Weather", "Sunny", "Stormy", "Dry", "Humid", "Cold", "Hot"],
          ["Victim's Build", "Large", "Thin", "Tall", "Short", "Disfigured", "Fit"],
          ["Trace at Scene", "Fingerprint", "Footprint", "Bruise", "Blood Stain", "Body Fluid", "Scar"],
          ["Corpse Condition", "Still Warm", "Stiff", "Decayed", "Incomplete", "Intact", "Twisted"],
          ["Duration of Crime", "Instant", "Brief", "Gradual", "Prolonged", "Days", "Unclear"]
        ]
      },
      {
        "key": "tile_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "means_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "role_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "seat_names",
        "visible": "none",
        "type": "list",
        "initial": ["seat 1", "seat 2", "seat 3", "seat 4", "seat 5", "seat 6", "seat 7", "seat 8"]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "current_tile",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "marker",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "key_evidence",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "means_of_murder",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hunt_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "scientist_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "clue_list_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "means_list_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "clues_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "means_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_badges",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "options_per_tile",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_tiles",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_draws",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "murderers",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "accomplices",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "witnesses",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "investigators_formula_offset",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "win_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the Scientist",
      "do": [
        {
          "set": {
            "player": {
              "calc": "scientist_seat"
            },
            "key": "role",
            "value": "Scientist",
            "text": "Seat {player} is the Forensic Scientist.",
            "announce_to": "all"
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the roles",
      "do": [
        {
          "set": {
            "key": "role_pool",
            "value": {
              "calc": "['Murderer' for p in players if p.seat <= murderers] + ['Accomplice' for p in players if p.seat <= accomplices] + ['Witness' for p in players if p.seat <= witnesses] + ['Investigator' for p in players if p.seat > investigators_formula_offset]"
            }
          }
        },
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 2, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 3, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 4, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 5, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 6, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"player": 7, "key": "role", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"set": {"player": 8, "key": "role", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {
          "set": {
            "players": "all",
            "key": "side",
            "value": {
              "calc": "'murderer' if you.role in ['Murderer', 'Accomplice'] else 'investigator'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the clue cards",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 2, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 2, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 3, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 3, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 4, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 4, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 5, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 5, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 6, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 6, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal the means cards",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 2, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 2, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 3, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 3, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 4, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 4, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 5, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 5, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 6, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 6, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {
          "set": {
            "key": "clue_options",
            "value": {
              "calc": "['PASS'] + [c for p in players for c in p.clues]"
            }
          }
        },
        {
          "set": {
            "key": "means_options",
            "value": {
              "calc": "[m for p in players for m in p.means]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "intel and badges",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.role == 'Accomplice'"
            },
            "key": "intel",
            "value": {
              "calc": "'The Murderer is ' + seat_names[min([p.seat for p in players if p.role == 'Murderer']) - 1] + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'Witness'"
            },
            "key": "intel",
            "value": {
              "calc": "'The Murderer and the Accomplice are ' + (seat_names[min([p.seat for p in players if p.role == 'Murderer']) - 1] + ' and ' + seat_names[min([p.seat for p in players if p.role == 'Accomplice']) - 1] if uniform(0, 1) < 0.5 else seat_names[min([p.seat for p in players if p.role == 'Accomplice']) - 1] + ' and ' + seat_names[min([p.seat for p in players if p.role == 'Murderer']) - 1]) + ', in no particular order: you do not know which is which.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'Scientist'"
            },
            "key": "intel",
            "value": {
              "calc": "'Roles: seat 1 Scientist' + max(['; seat 2 ' + p.role for p in players if p.seat == 2] + ['']) + max(['; seat 3 ' + p.role for p in players if p.seat == 3] + ['']) + max(['; seat 4 ' + p.role for p in players if p.seat == 4] + ['']) + max(['; seat 5 ' + p.role for p in players if p.seat == 5] + ['']) + max(['; seat 6 ' + p.role for p in players if p.seat == 6] + ['']) + max(['; seat 7 ' + p.role for p in players if p.seat == 7] + ['']) + max(['; seat 8 ' + p.role for p in players if p.seat == 8] + ['']) + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != scientist_seat"
            },
            "key": "badge",
            "value": {
              "calc": "starting_badges"
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
      "fields": [
        "role",
        "side",
        "intel",
        "clues",
        "means",
        "badge"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "ask",
      "phase": "solution",
      "label": "choose the Key Evidence",
      "when": {
        "calc": "round == 0"
      },
      "to": {
        "where": "you.role == 'Murderer'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "clues"
        }
      },
      "verify": {
        "bind": "ke"
      },
      "text": "You are the Murderer. Privately choose one of your own Clue cards as the Key Evidence."
    },
    {
      "use": "ask",
      "phase": "solution",
      "label": "choose the Means of Murder",
      "when": {
        "calc": "round == 0"
      },
      "to": {
        "where": "you.role == 'Murderer'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "means"
        }
      },
      "verify": {
        "bind": "mm"
      },
      "text": "Privately choose one of your own Means cards as the Means of Murder."
    },
    {
      "use": "update",
      "phase": "solution",
      "label": "record the solution",
      "when": {
        "calc": "round == 0"
      },
      "do": [
        {
          "set": {
            "key": "key_evidence",
            "value": "$ke"
          }
        },
        {
          "set": {
            "key": "means_of_murder",
            "value": "$mm"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role in ['Scientist', 'Accomplice']"
            },
            "key": "solution_known",
            "value": {
              "calc": "'Key Evidence: ' + key_evidence + '; Means of Murder: ' + means_of_murder"
            }
          }
        }
      ],
      "text": "The Murderer has chosen the solution in secret."
    },
    {
      "use": "tell",
      "phase": "solution",
      "label": "tell the solution",
      "when": {
        "calc": "round == 0"
      },
      "to": {
        "where": "you.role in ['Scientist', 'Accomplice']"
      },
      "text": "Private: the solution is {solution_known}."
    },
    {
      "use": "update",
      "phase": "tile",
      "label": "the scene tile",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "current_tile",
            "value": {
              "calc": "'Cause of Death' if round == 1 else ('Location' if round == 2 else tile_deck[int(unifor
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (current_tile, marker); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "deception_five_clues",
    "name": "Deception: Five Clues",
    "players": {
      "min": 6,
      "max": 8,
      "suggested": 7
    },
    "blurb": "A public Forensic Scientist marks scene tiles to steer the Investigators to the Murderer's secret Clue and Means, while the Murderer side hides and hunts the Witness."
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
        "key": "role",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "side",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "intel",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "solution_known",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "clues",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "means",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "badge",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "acc_clue",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "acc_means",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "won",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick_clue",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "pick_means",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "verdict",
        "visible": "ally",
        "type": "text",
        "initial": "none"
      }
    ],
    "game": [
      {
        "key": "clue_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Glove",
          "Train Ticket",
          "Lipstick",
          "Key",
          "Diary",
          "Ring",
          "Cigarette",
          "Phone",
          "Wallet",
          "Photo",
          "Watch",
          "Umbrella",
          "Receipt",
          "Hair",
          "Button",
          "Mask"
        ]
      },
      {
        "key": "means_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Rope",
          "Poison",
          "Knife",
          "Pillow",
          "Hammer",
          "Pistol",
          "Insulin",
          "Brick",
          "Drowning",
          "Electric Wire",
          "Scarf",
          "Bare Hands",
          "Fire",
          "Bottle",
          "Axe",
          "Car"
        ]
      },
      {
        "key": "tile_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Time of Death",
          "Weather",
          "Victim's Build",
          "Trace at Scene",
          "Corpse Condition",
          "Duration of Crime"
        ]
      },
      {
        "key": "tile_table",
        "visible": "none",
        "type": "list",
        "initial": [
          [
            "Cause of Death",
            "Suffocation",
            "Severe Injury",
            "Loss of Blood",
            "Illness",
            "Poisoning",
            "Accident"
          ],
          [
            "Location",
            "Living Room",
            "Bedroom",
            "Bathroom",
            "Kitchen",
            "Street",
            "Office"
          ],
          [
            "Time of Death",
            "Dawn",
            "Morning",
            "Noon",
            "Afternoon",
            "Evening",
            "Night"
          ],
          [
            "Weather",
            "Sunny",
            "Stormy",
            "Dry",
            "Humid",
            "Cold",
            "Hot"
          ],
          [
            "Victim's Build",
            "Large",
            "Thin",
            "Tall",
            "Short",
            "Disfigured",
            "Fit"
          ],
          [
            "Trace at Scene",
            "Fingerprint",
            "Footprint",
            "Bruise",
            "Blood Stain",
            "Body Fluid",
            "Scar"
          ],
          [
            "Corpse Condition",
            "Still Warm",
            "Stiff",
            "Decayed",
            "Incomplete",
            "Intact",
            "Twisted"
          ],
          [
            "Duration of Crime",
            "Instant",
            "Brief",
            "Gradual",
            "Prolonged",
            "Days",
            "Unclear"
          ]
        ]
      },
      {
        "key": "tile_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "means_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "role_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "seat_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "seat 1",
          "seat 2",
          "seat 3",
          "seat 4",
          "seat 5",
          "seat 6",
          "seat 7",
          "seat 8"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "current_tile",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "marker",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "key_evidence",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "means_of_murder",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "hunt_target",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "game_over",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "scientist_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "clue_list_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "means_list_size",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "clues_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "means_per_player",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "starting_badges",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "options_per_tile",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_tiles",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_draws",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "murderers",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "accomplices",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "witnesses",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "investigators_formula_offset",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "win_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the Scientist",
      "do": [
        {
          "set": {
            "player": {
              "calc": "scientist_seat"
            },
            "key": "role",
            "value": "Scientist",
            "text": "Seat {player} is the Forensic Scientist.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "key": "current_tile",
            "value": "not drawn yet"
          }
        },
        {
          "set": {
            "key": "marker",
            "value": "not marked yet"
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the roles",
      "do": [
        {
          "set": {
            "key": "role_pool",
            "value": {
              "calc": "['Murderer' for p in players if p.seat <= murderers] + ['Accomplice' for p in players if p.seat <= accomplices] + ['Witness' for p in players if p.seat <= witnesses] + ['Investigator' for p in players if p.seat > investigators_formula_offset]"
            }
          }
        },
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 2, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 3, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 4, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 5, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}}},
        {"set": {"player": 6, "key": "role", "value": {"calc": "pick"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"player": 7, "key": "role", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "role_pool[int(uniform(0, len(role_pool)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"set": {"player": 8, "key": "role", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "role_pool", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {
          "set": {
            "players": "all",
            "key": "side",
            "value": {
              "calc": "'murderer' if you.role in ['Murderer', 'Accomplice'] else 'investigator'"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the clue cards",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 2, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 2, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 3, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 3, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 4, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 4, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 5, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 5, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 6, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}}},
        {"append": {"player": 6, "key": "clues", "value": {"calc": "pick"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"set": {"key": "pick", "value": {"calc": "clue_deck[int(uniform(0, len(clue_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "clues", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "clue_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal the means cards",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 2, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 2, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 3, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 3, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 4, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 4, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 5, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 5, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 6, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}}},
        {"append": {"player": 6, "key": "means", "value": {"calc": "pick"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 7"}}},
        {"append": {"player": 7, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 7"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"set": {"key": "pick", "value": {"calc": "means_deck[int(uniform(0, len(means_deck)))]"}, "if": {"calc": "len(players) >= 8"}}},
        {"append": {"player": 8, "key": "means", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {"remove": {"key": "means_deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 8"}}},
        {
          "set": {
            "key": "clue_options",
            "value": {
              "calc": "['PASS'] + [c for p in players for c in p.clues]"
            }
          }
        },
        {
          "set": {
            "key": "means_options",
            "value": {
              "calc": "[m for p in players for m in p.means]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "intel and badges",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.role == 'Accomplice'"
            },
            "key": "intel",
            "value": {
              "calc": "'The Murderer is ' + seat_names[min([p.seat for p in players if p.role == 'Murderer']) - 1] + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'Witness'"
            },
            "key": "intel",
            "value": {
              "calc": "'The Murderer and the Accomplice are ' + (seat_names[min([p.seat for p in players if p.role == 'Murderer']) - 1] + ' and ' + seat_names[min([p.seat for p in players if p.role == 'Accomplice']) - 1] if uniform(0, 1) < 0.5 else seat_names[min([p.seat for p in players if p.role == 'Accomplice']) - 1] + ' and ' + seat_names[min([p.seat for p in players if p.role == 'Murderer']) - 1]) + ', in no particular order: you do not know which is which.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'Scientist'"
            },
            "key": "intel",
            "value": {
              "calc": "'Roles: seat 1 Scientist' + max(['; seat 2 ' + p.role for p in players if p.seat == 2] + ['']) + max(['; seat 3 ' + p.role for p in players if p.seat == 3] + ['']) + max(['; seat 4 ' + p.role for p in players if p.seat == 4] + ['']) + max(['; seat 5 ' + p.role for p in players if p.seat == 5] + ['']) + max(['; seat 6 ' + p.role for p in players if p.seat == 6] + ['']) + max(['; seat 7 ' + p.role for p in players if p.seat == 7] + ['']) + max(['; seat 8 ' + p.role for p in players if p.seat == 8] + ['']) + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != scientist_seat"
            },
            "key": "badge",
            "value": {
              "calc": "starting_badges"
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
      "fields": [
        "role",
        "side",
        "intel",
        "clues",
        "means",
        "badge"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "ask",
      "phase": "solution",
      "label": "choose the Key Evidence",
      "when": {
        "calc": "round == 0"
      },
      "to": {
        "where": "you.role == 'Murderer'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "clues"
        }
      },
      "verify": {
        "bind": "ke"
      },
      "text": "You are the Murderer. Privately choose one of your own Clue cards as the Key Evidence."
    },
    {
      "use": "ask",
      "phase": "solution",
      "label": "choose the Means of Murder",
      "when": {
        "calc": "round == 0"
      },
      "to": {
        "where": "you.role == 'Murderer'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "means"
        }
      },
      "verify": {
        "bind": "mm"
      },
      "text": "Privately choose one of your own Means cards as the Means of Murder."
    },
    {
      "use": "update",
      "phase": "solution",
      "label": "record the solution",
      "when": {
        "calc": "round == 0"
      },
      "do": [
        {
          "set": {
            "key": "key_evidence",
            "value": "$ke"
          }
        },
        {
          "set": {
            "key": "means_of_murder",
            "value": "$mm"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role in ['Scientist', 'Accomplice']"
            },
            "key": "solution_known",
            "value": {
              "calc": "'Key Evidence: ' + key_evidence + '; Means of Murder: ' + means_of_murder"
            }
          }
        }
      ],
      "text": "The Murderer has chosen the solution in secret."
    },
    {
      "use": "tell",
      "phase": "solution",
      "label": "tell the solution",
      "when": {
        "calc": "round == 0"
      },
      "to": {
        "where": "you.role in ['Scientist', 'Accomplice']"
      },
      "text": "Private: the solution is {solution_known}."
    },
    {
      "use": "update",
      "phase": "tile",
      "label": "the scene tile",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "current_tile",
            "value": {
              "calc": "'Cause of Death' if round == 1 else ('Location' if round == 2 else tile_deck[int(uniform(0, len(tile_deck)))])"
            }
          }
        },
        {
          "remove": {
            "key": "tile_deck",
            "value": {
              "calc": "current_tile"
            },
            "if": {
              "calc": "round >= 3"
            }
          }
        },
        {
          "set": {
            "key": "tile_options",
            "value": {
              "calc": "[o for r in tile_table if r[0] == current_tile for o in r if o != current_tile]"
            }
          }
        },
        {
          "set": {
            "key": "marker",
            "value": "not marked yet"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "acc_clue",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "acc_means",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_clue",
            "value": "none"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_means",
            "value": "none"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "verdict",
            "value": "none"
          }
        }
      ],
      "text": "Round {round} of {rounds}. The scene tile is {current_tile}, with options: {tile_options}."
    },
    {
      "use": "ask",
      "phase": "marker",
      "label": "the marker",
      "to": {
        "where": "you.seat == scientist_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "tile_options"
        }
      },
      "verify": {
        "bind": "mk"
      },
      "text": "You are the Forensic Scientist. Mark exactly one option of the {current_tile} tile to steer the Investigators toward the Key Evidence and the Means of Murder. This is the only way you may communicate."
    },
    {
      "use": "update",
      "phase": "marker",
      "label": "announce the marker",
      "do": [
        {
          "set": {
            "key": "marker",
            "value": "$mk"
          }
        }
      ],
      "text": "The Scientist marks {marker} on the {current_tile} tile."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": {
        "where": "you.seat != scientist_seat"
      },
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table about the case. Everyone writes at the same time; all messages are shown afterwards."
    },
    {
      "use": "poll",
      "phase": "accusation",
      "label": "accusation clue",
      "to": {
        "where": "you.badge >= 1 and you.seat != scientist_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "clue_options"
        }
      },
      "store": "pick_clue",
      "text": "You hold a badge. Answer PASS to keep it, or name the Clue word of your accusation (any Clue on the table). If you accuse, you will then name a Means word and you lose your badge whether you are right or wrong."
    },
    {
      "use": "poll",
      "phase": "accusation",
      "label": "accusation means",
      "to": {
        "where": "you.pick_clue != 'none' and you.pick_clue != 'PASS'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "means_options"
        }
      },
      "store": "pick_means",
      "text": "Name the Means word of your accusation (any Means on the table). Your accusation is revealed at resolution."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "resolution",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.pick_clue == 'PASS'"
            },
            "key": "acc_clue",
            "value": "PASS"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick_clue != 'none' and you.pick_clue != 'PASS'"
            },
            "key": "acc_clue",
            "value": {
              "calc": "you.pick_clue"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick_clue != 'none' and you.pick_clue != 'PASS'"
            },
            "key": "acc_means",
            "value": {
              "calc": "you.pick_means"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick_clue != 'none' and you.pick_clue != 'PASS'"
            },
            "key": "verdict",
            "value": {
              "calc": "you.pick_clue + ' with ' + you.pick_means + ': ' + ('CORRECT' if you.pick_clue == key_evidence and you.pick_means == means_of_murder else 'wrong')"
            },
            "text": "Seat {player} accuses {value}.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.pick_clue != 'none' and you.pick_clue != 'PASS' and you.badge >= 1"
            },
            "key": "badge",
            "value": 0
          }
        },
        {
          "set": {
            "key": "solved",
            "value": true,
            "if": {
              "calc": "any(p.pick_clue == key_evidence and p.pick_means == means_of_murder for p in players)"
            },
            "text": "The case is SOLVED. The Murderer now hunts the Witness.",
            "announce_to": "all"
          }
        }
      ],
      "text": "Accusations for round {round} are revealed."
    },
    {
      "use": "ask",
      "phase": "hunt",
      "label": "witness hunt",
      "when": {
        "calc": "solved"
      },
      "to": {
        "where": "you.role == 'Murderer'"
      },
      "answer": {
        "type": "player",
        "exclude_self": true,
        "exclude": {
          "where": "you.role in ['Scientist', 'Accomplice']"
        }
      },
      "verify": {
        "bind": "ht"
      },
      "text": "The case is solved. Name the seat you believe is the Witness (not the Scientist, the Accomplice or yourself). If you are right, your side wins; if not, the Investigator side wins."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "hunt result",
      "when": {
        "calc": "solved"
      },
      "do": [
        {
          "set": {
            "key": "hunt_target",
            "value": "$ht",
            "text": "The Murderer names seat {value} as the Witness.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.side == 'murderer'"
            },
            "key": "won",
            "value": {
              "calc": "win_value"
            },
            "if": {
              "calc": "any(p.seat == hunt_target and p.role == 'Witness' for p in players)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.side == 'investigator'"
            },
            "key": "won",
            "value": {
              "calc": "win_value"
            },
            "if": {
              "calc": "not any(p.seat == hunt_target and p.role == 'Witness' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end",
      "label": "the Murderer escapes",
      "when": {
        "calc": "not solved and round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.side == 'murderer'"
            },
            "key": "won",
            "value": {
              "calc": "win_value"
            }
          }
        },
        {
          "set": {
            "key": "game_over",
            "value": 1
          }
        }
      ],
      "text": "Round {rounds} ends unsolved. The Murderer side escapes."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "is it over",
      "when": {
        "calc": "game_over == 1"
      },
      "against": [
        "closed"
      ]
    }
  ],
  "end": {
    "closed": {
      "when": {
        "calc": "game_over == 1"
      },
      "rank_by": "you.won",
      "min_to_win": 1,
      "reveal": [
        "role"
      ],
      "text": "Winner: {result}. Solved: {solved}; Key Evidence {key_evidence}, Means of Murder {means_of_murder}; Witness Hunt named seat {hunt_target}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "Seat {scientist_seat} is publicly the Forensic Scientist. The other players are secretly and randomly dealt {murderers} Murderer, {accomplices} Accomplice, {witnesses} Witness, and Investigators for the rest (player count minus {investigators_formula_offset}). The Murderer and Accomplice are the Murderer side; the Scientist, Witness and Investigators are the Investigator side. The Accomplice is told who the Murderer is. The Witness is told the two seats of the Murderer and Accomplice, but not which is which, and not the solution. The Scientist is told all roles.\n\nEvery player except the Scientist is dealt, face up for all to see, {clues_per_player} Clue words and {means_per_player} Means words, with no repeats. The Murderer privately chooses one of their own Clues as the Key Evidence and one of their own Means as the Means of Murder; the Scientist and the Accomplice are then told the solution, and no one else. Every player except the Scientist starts with {starting_badges} badge.\n\nEach round ({rounds} rounds):\n1. Tile. Round 1 is Cause of Death, round 2 is Location; in rounds 3, 4 and 5 a tile is drawn at random from the Deck and removed. Each tile has {options_per_tile} options.\n2. Marker. The Scientist privately chooses exactly one of the tile's options, and the marked option is announced to all. The Scientist may never send any other message.\n3. Talk. Every player except the Scientist writes one short message at the same time; all messages are then shown to everyone.\n4. Accusation. Every player who still has a badge chooses at the same time either PASS or one accusation: one Clue word and one Means word currently on the table. Anyone who accuses loses their badge, whether right or wrong; passing keeps it.\n5. Resolution. Every accusation is announced with its accuser. An accusation is correct only if its Clue is the Key Evidence and its Means is the Means of Murder; otherwise it is wrong. A pair taken from two different players' cards is always wrong. If any accusation is correct, the case is SOLVED and play moves to the Witness Hunt. Otherwise the next round begins.\n\nWITNESS HUNT. When the case is solved, the Murderer privately names one player other than the Scientist, the Accomplice and themself. If that player is the Witness, the Murderer side wins. Otherwise the Investigator side wins.\n\nEND. If the case is not solved by the end of round {rounds}, the Murderer side wins. Every player on the winning side shares the win; there are no draws."
}
```
````
