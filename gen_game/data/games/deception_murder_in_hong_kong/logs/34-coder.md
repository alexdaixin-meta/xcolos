# 34 coder

- time: 2026-10-28T02:40:51+00:00 (212.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 4263307f488c68ae, reply sha256 fc8f7ad9b0fffb0f

## Sent

````
# Task: write the XColos game file for "Deception: Four Tiles"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 6 to 8; set `meta.players` to {"min": 6, "max": 8, "suggested": 7} (the suggested size is the one the game plays best at).

COMPONENTS.
- Clue words (16): Glove, Key, Diary, Ring, Cigarette, Phone, Wallet, Mask, Train Ticket, Lipstick, Receipt, Hair, Button, Watch, Letter, Coin.
- Means words (16): Rope, Poison, Knife, Pillow, Insulin, Pistol, Electric Wire, Scarf, Bottle, Axe, Hammer, Candlestick, Brick, Razor, Bag, Ice.
- Scene tiles (8), each with a name and 6 items:
  - Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident
  - Location: Living Room, Bedroom, Bathroom, Kitchen, Street, Office
  - Time of Death: Dawn, Morning, Noon, Afternoon, Evening, Night
  - Weather: Sunny, Stormy, Dry, Humid, Cold, Hot
  - Victim's Build: Large, Thin, Tall, Short, Disfigured, Fit
  - Trace at Scene: Fingerprint, Footprint, Bruise, Blood Stain, Body Fluid, Scar
  - Corpse Condition: Still Warm, Stiff, Decayed, Incomplete, Intact, Twisted
  - Duration of Crime: Instant, Brief, Gradual, Prolonged, Days, Unclear

GAME STATE, set once before setup and never reset by setup:
- solved = false
- hunt_target = 0
- key_evidence and means_of_murder are empty unless given
- Every player starts with badge 0, won 0, acc_clue empty and acc_means empty.

SETUP.
1. Seat 1 is always the Forensic Scientist. This is public. The Scientist gets no cards and badge 0.
2. Seats 2..N receive exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators.
   - A role already given to a seat is kept.
   - Remaining roles are dealt at random to seats without a role.
   - Sides: Murderer and Accomplice are on the Murderer side. Scientist, Witness and Investigators are on the Investigator side.
3. Each of seats 2..N holds exactly 2 Clue cards and 2 Means cards, face up for everyone to see.
   - Cards already given are kept and removed from the decks first.
   - Missing cards are dealt at random from the remaining decks.
   - Undealt words stay in the clue deck and means deck. They are not 'on the table'.
   - Seats 2..N get badge 1.
4. Unless already given, the Murderer secretly chooses one of their own 2 Clues as key_evidence, then one of their own 2 Means as means_of_murder.
5. Private intel, written from the final roles:
   - The Scientist learns every role, key_evidence and means_of_murder.
   - The Accomplice learns the Murderer's seat.
   - The Witness learns the two Murderer-side seats, but not which is which.
   - The Murderer learns the Accomplice's seat.
   - Investigators learn nothing.

EACH ROUND (rounds 1 to 4):
1. Tile. Round 1 reveals Cause of Death. Rounds 2-4 each reveal one tile drawn at random from the tiles not yet revealed. This is the only random draw in a round.
2. Marker. The Scientist privately chooses one of the 6 items on the new tile, and the marked item is announced to all. The Scientist never speaks.
3. Talk. Every seat 2..N writes one short message at the same time, without seeing the others. All messages are then shown to everyone.
4. Accusation, Poll A. All seats with badge 1 are asked at the same time to choose PASS or one Clue word. The only Clue words offered are those currently in the clues lists of seats 2..N. The answer is stored in acc_clue (PASS leaves it empty).
5. Accusation, Poll B. All seats that named a Clue in Poll A this round are asked at the same time to choose one Means word. The only Means words offered are those currently in the means lists of seats 2..N. The answer is stored in acc_means.
6. Every seat with a non-empty acc_clue has badge set to 0. It will never be asked to accuse again.
7. Resolution. Each accusation (acc_clue, acc_means) is announced with its seat.
   - If acc_clue equals key_evidence and acc_means equals means_of_murder, it is announced as correct and solved becomes true.
   - Otherwise it is announced as wrong.
   - solved, once true, stays true.
8. acc_clue and acc_means are cleared for all players.
9. Witness Hunt. This happens only if solved became true this round. The Murderer chooses one seat from seats 2..N other than their own, stored as hunt_target.
10. End check. The game ends if solved is true or round 4 has finished. Otherwise the next round begins.

SCORING at the end:
- If solved is true and hunt_target is the Witness's seat, every Murderer-side player gets won = 1.
- If solved is true and hunt_target is not the Witness's seat, every Investigator-side player (including the Scientist) gets won = 1.
- If solved is false after round 4, every Murderer-side player gets won = 1.

How the winner is decided: Team win, decided by arithmetic on the stored values.
- Investigator side wins if some accusation exactly matched key_evidence and means_of_murder and the Murderer's hunt_target is not the Witness's seat.
- Murderer side wins if the case is never solved in 4 rounds, or if it is solved and hunt_target equals the Witness's seat.
- The winners are the players with won = 1. There are no draws.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Deception: Four Tiles (6 to 8 players, best with 7)

A hidden-role deduction game: a silent Forensic Scientist marks scene items to steer the Investigators toward the Murderer's secret clue and means within 4 rounds, and if the case is solved the Murderer gets one guess at the Witness to steal the win.

STATE (every item below must exist in the file):
  - each player: role (text, starts ''); only its owner sees it. scientist, murderer, accomplice, witness or investigator. The Scientist's role is also announced publicly through the table attribute scientist_seat.
  - each player: side (text, starts ''); only its owner sees it. murderer (Murderer and Accomplice) or investigator (Scientist, Witness and Investigators)
  - each player: clues (list, starts []); everyone sees it. the seat's 2 face-up Clue cards (empty for the Scientist)
  - each player: means (list, starts []); everyone sees it. the seat's 2 face-up Means cards (empty for the Scientist)
  - each player: badge (number, starts 0); everyone sees it. 1 if the seat may still accuse, 0 if not
  - each player: acc_clue (text, starts ''); everyone sees it. the Clue named in this round's accusation (empty means PASS)
  - each player: acc_means (text, starts ''); everyone sees it. the Means named in this round's accusation
  - each player: intel (text, starts ''); only its owner sees it. the private information given at setup
  - each player: won (number, starts 0); everyone sees it. 1 if this player is on the winning side
  - the table: scientist_seat (number, starts 1); everyone sees it. the public seat of the Forensic Scientist
  - the table: solved (bool, starts False); everyone sees it. true once an accusation exactly matched key_evidence and means_of_murder; never reset
  - the table: solved_this_round (bool, starts False); hidden from all players. true if solved became true in the current round
  - the table: hunt_target (number, starts 0); everyone sees it. the seat the Murderer named in the Witness Hunt (0 means no hunt)
  - the table: key_evidence (text, starts ''); hidden from all players. the Murderer's secret Clue
  - the table: means_of_murder (text, starts ''); hidden from all players. the Murderer's secret Means
  - the table: murderer_seat (number, starts 0); hidden from all players. the seat of the Murderer
  - the table: accomplice_seat (number, starts 0); hidden from all players. the seat of the Accomplice
  - the table: witness_seat (number, starts 0); hidden from all players. the seat of the Witness
  - the table: role_deck (list, starts []); hidden from all players. the roles still to be dealt to seats 2..N
  - the table: clue_deck (list, starts ['Glove', 'Key', 'Diary', 'Ring', 'Cigarette', 'Phone', 'Wallet', 'Mask', 'Train Ticket', 'Lipstick', 'Receipt', 'Hair', 'Button', 'Watch', 'Letter', 'Coin']); hidden from all players. undealt Clue words
  - the table: means_deck (list, starts ['Rope', 'Poison', 'Knife', 'Pillow', 'Insulin', 'Pistol', 'Electric Wire', 'Scarf', 'Bottle', 'Axe', 'Hammer', 'Candlestick', 'Brick', 'Razor', 'Bag', 'Ice']); hidden from all players. undealt Means words
  - the table: tile_deck (list, starts ['Location', 'Time of Death', 'Weather', "Victim's Build", 'Trace at Scene', 'Corpse Condition', 'Duration of Crime']); hidden from all players. scene tiles not yet revealed (Cause of Death is revealed in round 1)
  - the table: current_tile (text, starts ''); everyone sees it. the tile revealed this round
  - the table: revealed_tiles (list, starts []); everyone sees it. the tiles revealed so far
  - the table: marked_items (list, starts []); everyone sees it. the items marked by the Scientist, one per revealed tile
  - the table: round (number, starts 0); everyone sees it. the current round number (1 to 4)
  - parameters, each kept as a table attribute: clue_words = 16, means_words = 16, scene_tiles = 8, items_per_tile = 6, rounds = 4, clues_per_seat = 2, means_per_seat = 2, scientist_seat = 1, murderers = 1, accomplices = 1, witnesses = 1, investigators_formula_offset = 4, starting_badge_cardholder = 1, starting_badge_scientist = 0, accusations_per_seat = 1, win_value = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is given role scientist and side investigator, and badge 0, no Clue cards and no Means cards. It is announced to all that seat 1 is the Forensic Scientist.
  2. role_deck is set to 1 murderer, 1 accomplice, 1 witness and N-4 investigator. Any role already given to a seat is kept and removed from role_deck. Each of seats 2..N without a role draws one role at random from role_deck.
  3. Each seat's side is set: murderer for the Murderer and the Accomplice, investigator for everyone else. murderer_seat, accomplice_seat and witness_seat are recorded.
  4. Cards already given to seats are removed from clue_deck and means_deck. Each of seats 2..N then draws at random from clue_deck until it holds 2 Clues, and from means_deck until it holds 2 Means, all face up (public). Undealt words stay in the decks and are not on the table.
  5. Seats 2..N get badge 1.
  6. Unless already given, the Murderer is asked privately to choose one of their own 2 clues, which is stored as key_evidence, then one of their own 2 means, which is stored as means_of_murder.
  7. Private intel is written to each seat's intel. The Scientist learns every seat's role, key_evidence and means_of_murder. The Accomplice learns murderer_seat. The Witness learns murderer_seat and accomplice_seat as an unordered pair. The Murderer learns accomplice_seat. Investigators learn nothing.
  8. Each player is sent their own state (sync).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; solved_this_round = false. If round == 1, current_tile = 'Cause of Death'. Otherwise one tile is drawn at random from tile_deck, removed from it, and stored as current_tile. current_tile is appended to revealed_tiles and announced with its 6 items.
  2. [ask] seat 1 (Scientist) answers: one of the 6 items on current_tile. What happens: the chosen item is appended to marked_items and announced to all as the marker on current_tile
  3. [poll] seats 2..N answers: short text. What happens: all messages are revealed together, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}; no state change
  4. [poll] all seats with badge == 1 answers: PASS or one Clue word currently in the clues of seats 2..N. What happens: a Clue answer is stored in acc_clue; PASS leaves acc_clue empty
  5. [poll] all seats whose acc_clue is non-empty answers: one Means word currently in the means of seats 2..N. What happens: stored in acc_means
  6. [update] all players. What happens: for each seat with acc_clue != '': badge = 0
  7. [update] all players. What happens: each accusation (acc_clue, acc_means) with its seat is announced. If acc_clue == key_evidence and acc_means == means_of_murder, it is announced correct, and if solved was false, then solved = true and solved_this_round = true. Otherwise it is announced wrong. solved never returns to false.
  8. [update] all players. What happens: acc_clue = '' and acc_means = '' for every player
  9. [ask] the Murderer (seat murderer_seat), only when solved_this_round == true answers: one seat from 2..N other than murderer_seat. What happens: hunt_target = the chosen seat; it is announced
  10. [update] all players, only when solved == true or round >= 4. What happens: if solved == true and hunt_target == witness_seat: won = 1 for every player with side == murderer. If solved == true and hunt_target != witness_seat: won = 1 for every player with side == investigator. If solved == false: won = 1 for every player with side == murderer. All roles are revealed.
  11. [check] table. What happens: the game ends if solved == true or round >= 4; otherwise the next round begins

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game sets up, then seat 1 is the Forensic Scientist, publicly, with badge 0 and empty clues and means.
  R2. When the game sets up with N players, then seats 2..N hold exactly 1 murderer, 1 accomplice, 1 witness and N-4 investigators, and any pre-given role is kept.
  R3. When roles are dealt, then the Murderer and the Accomplice have side murderer, and the Scientist, the Witness and the Investigators have side investigator.
  R4. When the game sets up, then each of seats 2..N holds exactly 2 public clues and 2 public means, and pre-given cards are kept and removed from the decks first.
  R5. When cards are dealt, then no word appears twice across hands and decks, and undealt words remain in clue_deck or means_deck.
  R6. When setup finishes, then seats 2..N have badge 1.
  R7. When the Murderer chooses, then key_evidence is one of the Murderer's own 2 clues and means_of_murder is one of the Murderer's own 2 means.
  R8. When intel is written, then the Scientist learns all roles, key_evidence and means_of_murder, the Accomplice learns murderer_seat, the Witness learns the two murderer-side seats unordered, the Murderer learns accomplice_seat, and Investigators learn nothing.
  R9. When round 1 starts, then current_tile is Cause of Death.
  R10. When rounds 2, 3 or 4 start, then one tile not yet revealed is drawn at random from tile_deck and removed from it.
  R11. When a tile is revealed, then the Scientist chooses exactly one of its 6 items, and that item is announced and appended to marked_items.
  R12. When the Talk step runs, then only seats 2..N write a message, simultaneously, and all messages are shown to everyone afterward; the Scientist never speaks.
  R13. When Poll A runs, then only seats with badge 1 are asked, and each may choose PASS or a Clue currently in the clues of seats 2..N.
  R14. When a seat names a Clue in Poll A, then in Poll B it must choose a Means currently in the means of seats 2..N; a seat that passed is not asked in Poll B.
  R15. When a seat has made an accusation (acc_clue non-empty), then its badge becomes 0 and it is never asked to accuse again.
  R16. When an accusation has acc_clue == key_evidence and acc_means == means_of_murder, then it is announced correct and solved becomes true.
  R17. When an accusation matches only one of the two words or neither, then it is announced wrong and solved is unchanged.
  R18. When solved is true, then it stays true for the rest of the game.
  R19. When resolution finishes, then acc_clue and acc_means are cleared for all players.
  R20. When solved became true this round, then the Murderer chooses hunt_target from seats 2..N other than their own seat; otherwise no hunt happens and hunt_target stays 0.
  R21. When solved is true or round 4 has finished, then the game ends.
  R22. When the game ends with solved true and hunt_target == witness_seat, then the Murderer and the Accomplice get won = 1 and all others keep won = 0.
  R23. When the game ends with solved true and hunt_target != witness_seat, then the Scientist, the Witness and every Investigator get won = 1.
  R24. When round 4 ends with solved false, then the Murderer and the Accomplice get won = 1.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Setup: the Murderer's choice of key_evidence | asked: the Murderer | options: the 2 Clue words in the Murderer's own clues
  - Setup: the Murderer's choice of means_of_murder | asked: the Murderer | options: the 2 Means words in the Murderer's own means
  - Marker | asked: seat 1 (Scientist) | options: the 6 items of current_tile, e.g. for Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident
  - Talk | asked: seats 2..N | options: one short free-text message; the Scientist is not asked
  - Accusation Poll A | asked: every seat with badge 1 (never seat 1, never a seat that already accused) | options: PASS, or any Clue word currently in the clues of seats 2..N, including the asker's own
  - Accusation Poll B | asked: every seat that named a Clue in Poll A this round | options: any Means word currently in the means of seats 2..N, including the asker's own; PASS is not offered
  - Witness Hunt | asked: the Murderer, only in the round solved became true | options: every seat from 2..N except the Murderer's own seat

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: solved == true or round >= 4
  - each player's standing: you.won (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - min_to_win: 1 (a player whose standing is below it cannot win; if none reaches it, the match ends with no winner)
  - how the result is decided: A team win. Every player whose side won has won = 1 and shares the win. The Investigator side wins if the case is solved and hunt_target is not the Witness's seat. The Murderer side wins if the case is unsolved after 4 rounds, or if it is solved and hunt_target is the Witness's seat.
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

- each player: `clues` (list, visible: public, starts []): the seat's 2 face-up Clue cards (empty for the Scientist)
- each player: `means` (list, visible: public, starts []): the seat's 2 face-up Means cards (empty for the Scientist)
- each player: `badge` (number, visible: public, starts 0): 1 if the seat may still accuse, 0 if not
- each player: `won` (number, visible: public, starts 0): 1 if this player is on the winning side
- the table: `scientist_seat` (number, visible: public, starts 1): the public seat of the Forensic Scientist
- the table: `solved` (bool, visible: public, starts False): true once an accusation exactly matched key_evidence and means_of_murder; never reset
- the table: `hunt_target` (number, visible: public, starts 0): the seat the Murderer named in the Witness Hunt (0 means no hunt)
- the table: `current_tile` (text, visible: public, starts ''): the tile revealed this round
- the table: `revealed_tiles` (list, visible: public, starts []): the tiles revealed so far
- the table: `marked_items` (list, visible: public, starts []): the items marked by the Scientist, one per revealed tile
- the table: `round` (number, visible: public, starts 0): the current round number (1 to 4)
- parameters (each must be an attribute holding this value, never a number buried in a step): clue_words = 16, means_words = 16, scene_tiles = 8, items_per_tile = 6, rounds = 4, clues_per_seat = 2, means_per_seat = 2, scientist_seat = 1, murderers = 1, accomplices = 1, witnesses = 1, investigators_formula_offset = 4, starting_badge_cardholder = 1, starting_badge_scientist = 0, accusations_per_seat = 1, win_value = 1
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

1) Remove `seat_names` from the file, or add a step that sets it if something truly needs it.
2) Check the resolution step carefully:
- It must compare each player's `acc_clue` against the hidden `key_evidence` attribute and `acc_means` against `means_of_murder`, using exactly those keys.
- Both comparisons must be equalities on text values, joined by AND.
- When both match, it must set `solved` to true and `solved_this_round` to true.
- Run resolution after Poll B and before `acc_clue`/`acc_means` are cleared.
- Make sure the poll answers are stored as the plain word, without PASS or prefixes, so the comparison can match.
3) Reset `solved_this_round` to false at the start of each round, in the tile step. Give the hunt step a `when` of `solved_this_round` so the Murderer picks a seat from 2..N other than their own and writes it to `hunt_target`.
4) Keep `key_evidence`, `means_of_murder`, `acc_clue`, `acc_means`, `verdict` and `solved_this_round` as hidden bookkeeping (`none`/`ally`).
5) In prompts use only {value}/{seat}; never {acc_clue}.
6) Compute `won` at the end exactly per the scoring rules.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "deception_four_tiles",
    "name": "Deception: Four Tiles",
    "players": {
      "min": 6,
      "max": 8,
      "suggested": 7
    },
    "blurb": "A silent Forensic Scientist marks scene items so the Investigators can name the Murderer's secret clue and means in four rounds; if they do, the Murderer gets one guess at the Witness."
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
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "acc_means",
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
        "key": "won",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "scientist_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "solved_this_round",
        "visible": "none",
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
        "key": "murderer_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "accomplice_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "witness_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "role_deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Glove",
          "Key",
          "Diary",
          "Ring",
          "Cigarette",
          "Phone",
          "Wallet",
          "Mask",
          "Train Ticket",
          "Lipstick",
          "Receipt",
          "Hair",
          "Button",
          "Watch",
          "Letter",
          "Coin"
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
          "Insulin",
          "Pistol",
          "Electric Wire",
          "Scarf",
          "Bottle",
          "Axe",
          "Hammer",
          "Candlestick",
          "Brick",
          "Razor",
          "Bag",
          "Ice"
        ]
      },
      {
        "key": "tile_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Location",
          "Time of Death",
          "Weather",
          "Victim's Build",
          "Trace at Scene",
          "Corpse Condition",
          "Duration of Crime"
        ]
      },
      {
        "key": "tile_catalog",
        "visible": "none",
        "type": "list",
        "initial": [
          [
            "Cause of Death",
            [
              "Suffocation",
              "Severe Injury",
              "Loss of Blood",
              "Illness",
              "Poisoning",
              "Accident"
            ]
          ],
          [
            "Location",
            [
              "Living Room",
              "Bedroom",
              "Bathroom",
              "Kitchen",
              "Street",
              "Office"
            ]
          ],
          [
            "Time of Death",
            [
              "Dawn",
              "Morning",
              "Noon",
              "Afternoon",
              "Evening",
              "Night"
            ]
          ],
          [
            "Weather",
            [
              "Sunny",
              "Stormy",
              "Dry",
              "Humid",
              "Cold",
              "Hot"
            ]
          ],
          [
            "Victim's Build",
            [
              "Large",
              "Thin",
              "Tall",
              "Short",
              "Disfigured",
              "Fit"
            ]
          ],
          [
            "Trace at Scene",
            [
              "Fingerprint",
              "Footprint",
              "Bruise",
              "Blood Stain",
              "Body Fluid",
              "Scar"
            ]
          ],
          [
            "Corpse Condition",
            [
              "Still Warm",
              "Stiff",
              "Decayed",
              "Incomplete",
              "Intact",
              "Twisted"
            ]
          ],
          [
            "Duration of Crime",
            [
              "Instant",
              "Brief",
              "Gradual",
              "Prolonged",
              "Days",
              "Unclear"
            ]
          ]
        ]
      },
      {
        "key": "tile_items",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "means_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "accusation_report",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "current_tile",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed_tiles",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "marked_items",
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
        "key": "clue_words",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "means_words",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "scene_tiles",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "items_per_tile",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "clues_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "means_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
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
        "key": "starting_badge_cardholder",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_badge_scientist",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "accusations_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
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
      "label": "seat 1 is the Forensic Scientist",
      "do": [
        {
          "set": {
            "player": 1,
            "key": "role",
            "value": "scientist"
          }
        },
        {
          "set": {
            "player": 1,
            "key": "side",
            "value": "investigator"
          }
        },
        {
          "set": {
            "player": 1,
            "key": "badge",
            "value": {
              "calc": "starting_badge_scientist"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "clues",
            "value": []
          }
        },
        {
          "set": {
            "player": 1,
            "key": "means",
            "value": []
          }
        }
      ],
      "text": "Seat 1 is the Forensic Scientist."
    },
    {
      "use": "update",
      "label": "deal the roles",
      "do": [
        {
          "set": {
            "key": "role_deck",
            "value": {
              "calc": "(['murderer'] if count(p.role == 'murderer' for p in players) < murderers else []) + (['accomplice'] if count(p.role == 'accomplice' for p in players) < accomplices else []) + (['witness'] if count(p.role == 'witness' for p in players) < witnesses else []) + ['investigator' for p in players if p.seat > investigators_formula_offset + count(q.role == 'investigator' for q in players)]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 2 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 3 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 4 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 5 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 5 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 6 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 6 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 7 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 7 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[int(uniform(0, len(role_deck)))] if any(p.seat == 8 and p.role == '' for p in players) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 8 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "sides and seats",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.role in ['murderer', 'accomplice']"
            },
            "key": "side",
            "value": "murderer"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role not in ['murderer', 'accomplice']"
            },
            "key": "side",
            "value": "investigator"
          }
        },
        {
          "set": {
            "key": "murderer_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.role == 'murderer'])"
            }
          }
        },
        {
          "set": {
            "key": "accomplice_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.role == 'accomplice'])"
            }
          }
        },
        {
          "set": {
            "key": "witness_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.role == 'witness'])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "pre-given cards leave the decks",
      "do": [
        {
          "set": {
            "key": "clue_deck",
            "value": {
              "calc": "[c for c in clue_deck if not any(c in p.clues for p in players)]"
            }
          }
        },
        {
          "set": {
            "key": "means_deck",
            "value": {
              "calc": "[m for m in means_deck if not any(m in p.means for p in players)]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 2",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[int(uniform(0, len(clue_deck)))] if any(p.seat == 2 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[int(uniform(0, len(clue_deck)))] if any(p.seat == 2 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[int(uniform(0, len(means_deck)))] if any(p.seat == 2 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[int(uniform(0, len(means_deck)))] if any(p.seat == 2 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 3",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[int(uniform(0, len(clue_deck)))] if any(p.seat == 3 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[int(uniform(0, len(clue_deck)))] if any(p.seat == 3 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[int(uniform(0, len(means_deck)))] if any(p.seat == 3 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[int(uniform(0, len(means_deck)))] if any(p.seat == 3 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.means) < means_per_seat"
            },
            "key": "means",
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `solved` is never changed in 3 random matches, so nothing updates it. Steps that name it: resolution. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `solved_this_round` is never changed in 3 random matches, so nothing updates it. Steps that name it: the tile, resolution. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `hunt_target` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `tile_catalog` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "deception_four_tiles",
    "name": "Deception: Four Tiles",
    "players": {
      "min": 6,
      "max": 8,
      "suggested": 7
    },
    "blurb": "A silent Forensic Scientist marks scene items to guide the Investigators to the Murderer's secret clue and means in four rounds; if they solve it, the Murderer gets one guess at the Witness."
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
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "acc_means",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "verdict",
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
        "key": "won",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "scientist_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "solved_this_round",
        "visible": "none",
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
        "key": "murderer_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "accomplice_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "witness_seat",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "role_deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Glove",
          "Key",
          "Diary",
          "Ring",
          "Cigarette",
          "Phone",
          "Wallet",
          "Mask",
          "Train Ticket",
          "Lipstick",
          "Receipt",
          "Hair",
          "Button",
          "Watch",
          "Letter",
          "Coin"
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
          "Insulin",
          "Pistol",
          "Electric Wire",
          "Scarf",
          "Bottle",
          "Axe",
          "Hammer",
          "Candlestick",
          "Brick",
          "Razor",
          "Bag",
          "Ice"
        ]
      },
      {
        "key": "tile_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Location",
          "Time of Death",
          "Weather",
          "Victim's Build",
          "Trace at Scene",
          "Corpse Condition",
          "Duration of Crime"
        ]
      },
      {
        "key": "tile_catalog",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "tile_items",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "clue_offer",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "means_offer",
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
        "key": "current_tile",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed_tiles",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "marked_items",
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
        "key": "clue_words",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "means_words",
        "visible": "public",
        "type": "number",
        "initial": 16
      },
      {
        "key": "scene_tiles",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "items_per_tile",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "clues_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "means_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
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
        "key": "starting_badge_cardholder",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_badge_scientist",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "accusations_per_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
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
      "label": "seat 1 is the Forensic Scientist",
      "do": [
        {
          "set": {
            "player": 1,
            "key": "role",
            "value": "scientist"
          }
        },
        {
          "set": {
            "player": 1,
            "key": "side",
            "value": "investigator"
          }
        },
        {
          "set": {
            "player": 1,
            "key": "badge",
            "value": {
              "calc": "starting_badge_scientist"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "clues",
            "value": []
          }
        },
        {
          "set": {
            "player": 1,
            "key": "means",
            "value": []
          }
        }
      ],
      "text": "Seat {scientist_seat} is the Forensic Scientist."
    },
    {
      "use": "update",
      "label": "the scene tiles",
      "do": [
        {
          "set": {
            "key": "tile_catalog",
            "value": {
              "calc": "[['Cause of Death', ['Suffocation', 'Severe Injury', 'Loss of Blood', 'Illness', 'Poisoning', 'Accident']], ['Location', ['Living Room', 'Bedroom', 'Bathroom', 'Kitchen', 'Street', 'Office']], ['Time of Death', ['Dawn', 'Morning', 'Noon', 'Afternoon', 'Evening', 'Night']], ['Weather', ['Sunny', 'Stormy', 'Dry', 'Humid', 'Cold', 'Hot']], [\"Victim's Build\", ['Large', 'Thin', 'Tall', 'Short', 'Disfigured', 'Fit']], ['Trace at Scene', ['Fingerprint', 'Footprint', 'Bruise', 'Blood Stain', 'Body Fluid', 'Scar']], ['Corpse Condition', ['Still Warm', 'Stiff', 'Decayed', 'Incomplete', 'Intact', 'Twisted']], ['Duration of Crime', ['Instant', 'Brief', 'Gradual', 'Prolonged', 'Days', 'Unclear']]]"
            }
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
            "key": "role_deck",
            "value": {
              "calc": "['murderer' for p in players if p.seat <= murderers - count(q.role == 'murderer' for q in players)] + ['accomplice' for p in players if p.seat <= accomplices - count(q.role == 'accomplice' for q in players)] + ['witness' for p in players if p.seat <= witnesses - count(q.role == 'witness' for q in players)] + ['investigator' for p in players if p.seat <= len(players) - investigators_formula_offset - count(q.role == 'investigator' for q in players)]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 2 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 3 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 4 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 5 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 5 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 6 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 6 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 7 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 7 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "role_deck[min(len(role_deck) - 1, int(uniform(0, len(role_deck))))] if (len(role_deck) > 0 and any(p.seat == 8 and p.role == '' for p in players)) else ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 8 and you.role == ''"
            },
            "key": "role",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "role_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "sides and seats",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.role in ['murderer', 'accomplice']"
            },
            "key": "side",
            "value": "murderer"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role not in ['murderer', 'accomplice']"
            },
            "key": "side",
            "value": "investigator"
          }
        },
        {
          "set": {
            "key": "murderer_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.role == 'murderer'])"
            }
          }
        },
        {
          "set": {
            "key": "accomplice_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.role == 'accomplice'])"
            }
          }
        },
        {
          "set": {
            "key": "witness_seat",
            "value": {
              "calc": "sum([p.seat for p in players if p.role == 'witness'])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "pre-given cards leave the decks",
      "do": [
        {
          "set": {
            "key": "clue_deck",
            "value": {
              "calc": "[c for c in clue_deck if not any(c in p.clues for p in players)]"
            }
          }
        },
        {
          "set": {
            "key": "means_deck",
            "value": {
              "calc": "[m for m in means_deck if not any(m in p.means for p in players)]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 2",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 2 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 2 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 2 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 2 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 2 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 3",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 3 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 3 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 3 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 3 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 3 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 4",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 4 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 4 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 4 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 4 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 4 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 4 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 4 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 4 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 5",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 5 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 5 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 5 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 5 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 5 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 5 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 5 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 5 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 6",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 6 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 6 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 6 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 6 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 6 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 6 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 6 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 6 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 7",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 7 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 7 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 7 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 7 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 7 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 7 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 7 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 7 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal cards to seat 8",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 8 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 8 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "clue_deck[min(len(clue_deck) - 1, int(uniform(0, len(clue_deck))))] if any(p.seat == 8 and len(p.clues) < clues_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 8 and len(you.clues) < clues_per_seat"
            },
            "key": "clues",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "clue_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 8 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 8 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "means_deck[min(len(means_deck) - 1, int(uniform(0, len(means_deck))))] if any(p.seat == 8 and len(p.means) < means_per_seat for p in players) else ''"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == 8 and len(you.means) < means_per_seat"
            },
            "key": "means",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        },
        {
          "remove": {
            "key": "means_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "pick != ''"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "badges",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat != scientist_seat"
            },
            "key": "badge",
            "value": {
              "calc": "starting_badge_cardholder"
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
      "use": "ask",
      "phase": "secret",
      "label": "the Murderer chooses the key evidence",
      "when": {
        "calc": "round == 0 and key_evidence == ''"
      },
      "to": {
        "where": "you.role == 'murderer'"
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
      "text": "You are the Murderer. Secretly choose one of your own two Clue cards as the key evidence. Nobody but the Forensic Scientist will learn it."
    },
    {
      "use": "ask",
      "phase": "secret",
      "label": "the Murderer chooses the means of murder",
      "when": {
        "calc": "round == 0 and means_of_murder == ''"
      },
      "to": {
        "where": "you.role == 'murderer'"
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
      "text": "Now secretly choose one of your own two Means cards as the means of murder. Nobody but the Forensic Scientist will learn it."
    },
    {
      "use": "update",
      "phase": "secret",
      "label": "the secret and the intel",
      "when": {
        "calc": "round == 0"
      },
      "do": [
        {
          "set": {
            "key": "key_evidence",
            "value": "$ke",
            "if": {
              "calc": "key_evidence == ''"
            }
          }
        },
        {
          "set": {
            "key": "means_of_murder",
            "value": "$mm",
            "if": {
              "calc": "means_of_murder == ''"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'scientist'"
            },
            "key": "intel",
            "value": {
              "calc": "'Roles: seat 1 ' + players[0].role + '; seat 2 ' + players[1].role + '; seat 3 ' + players[2].role + '; seat 4 ' + players[3].role + '; seat 5 ' + players[4].role + '; seat 6 ' + players[5].role + ('; seat 7 ' + players[6].role if len(players) >= 7 else '') + ('; seat 8 ' + players[7].role if len(players) >= 8 else '') + '. Key evidence: ' + key_evidence + '. Means of murder: ' + means_of_murder + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'accomplice'"
            },
            "key": "intel",
            "value": {
              "calc": "'The Murderer is ' + ['', 'seat 1', 'seat 2', 'seat 3', 'seat 4', 'seat 5', 'seat 6', 'seat 7', 'seat 8'][murderer_seat] + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'witness'"
            },
            "key": "intel",
            "value": {
              "calc": "'The Murderer and the Accomplice are ' + ['', 'seat 1', 'seat 2', 'seat 3', 'seat 4', 'seat 5', 'seat 6', 'seat 7', 'seat 8'][min(murderer_seat, accomplice_seat)] + ' and ' + ['', 'seat 1', 'seat 2', 'seat 3', 'seat 4', 'seat 5', 'seat 6', 'seat 7', 'seat 8'][max(murderer_seat, accomplice_seat)] + ', in no particular order.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'murderer'"
            },
            "key": "intel",
            "value": {
              "calc": "'Your Accomplice is ' + ['', 'seat 1', 'seat 2', 'seat 3', 'seat 4', 'seat 5', 'seat 6', 'seat 7', 'seat 8'][accomplice_seat] + '.'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.role == 'investigator'"
            },
            "key": "intel",
            "value": "You have no private information."
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "secret",
      "label": "private intel",
      "when": {
        "calc": "round == 0"
      },
      "mode": "self",
      "to": "all",
      "fields": [
        "role",
        "side",
        "intel"
      ],
      "text": "Your role and private information:"
    },
    {
      "use": "update",
      "phase": "tile",
      "label": "the tile",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "solved_this_round",
            "value": false
          }
        },
        {
          "set": {
            "key": "current_tile",
            "value": {
              "calc": "'Cause of Death' if round == 1 else tile_deck[min(len(tile_deck) - 1, int(uniform(0, len(tile_deck))))]"
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
              "calc": "round > 1"
            }
          }
        },
        {
          "append": {
            "key": "revealed_tiles",
            "value": {
              "calc": "current_tile"
            }
          }
        },
        {
          "set": {
            "key": "tile_items",
            "value": {
              "calc": "[t[1] for t in tile_catalog if t[0] == current_tile][0]"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds}: the {current_tile} tile is revealed. Its items: {tile_items}."
    },
    {
      "use": "ask",
      "phase": "marker",
      "label": "the Scientist marks an item",
      "to": {
        "where": "you.seat == scientist_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "tile_items"
        }
      },
      "verify": {
        "bind": "mark"
      },
      "text": "You are the Forensic Scientist. Choose one item on the {current_tile} tile to mark, to steer the Investigators toward the key evidence and the means of murder. You never speak."
    },
    {
      "use": "update",
      "phase": "marker",
      "label": "the marker",
      "do": [
        {
          "append": {
            "key": "marked_items",
            "value": "$mark"
          }
        }
      ],
      "text": "The Forensic Scientist marks {mark} on the {current_tile} tile. Marked so far: {marked_items}."
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
      "text": "Say one short thing to the table about the case. Everyone writes at the same time; all messages are shown together afterwards."
    },
    {
      "use": "update",
      "phase": "accuse",
      "label": "the accusation offers",
      "do": [
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
            "key": "clue_offer",
            "value": {
              "calc": "['PASS'] + [c for p in players if p.seat != scientist_seat for c in p.clues]"
            }
          }
        },
        {
          "set": {
            "key": "means_offer",
            "value": {
              "calc": "[m for p in players if p.seat != scientist_seat for m in p.means]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "accuse",
      "label": "accusation poll A",
      "to": {
        "where": "you.badge == 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "clue_offer"
        }
      },
      "store": "acc_clue",
      "text": "Accuse now or PASS. To accuse, name the Clue you think is the key evidence; you will then name a Means. You may accuse only once in the whole game: after accusing, right or wrong, your badge is gone. PASS keeps your badge for a later round."
    },
    {
      "use": "poll",
      "phase": "accuse",
      "label": "accusation poll B",
      "to": {
        "where": "you.acc_clue != '' and you.acc_clue != 'PASS'"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "means_offer"
        }
      },
      "store": "acc_means",
      "text": "You named a Clue. Now name the Means you think is the means of murder."
    },
    {
      "use": "update",
      "phase": "accuse",
      "label": "badges are spent",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.acc_clue == 'PASS'"
            },
            "key": "acc_clue",
            "value": ""
          }
        },
        {
          "set": {
            "players": {
              "where": "you.acc_clue != ''"
            },
            "key": "badge",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "accuse",
      "label": "resolution",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.acc_clue != ''"
            },
            "key": "verdict",
            "value": {
              "calc": "you.acc_clue + ' with ' + you.acc_means + ': ' + ('CORRECT' if (you.acc_clue == key_evidence and you.acc_means == means_of_murder) else 'wrong')"
            },
            "text": "Seat {player} accuses {value}.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "key": "solved_this_round",
            "value": true,
            "if": {
              "calc": "(not solved) and any(p.acc_clue != '' and p.acc_clue == key_evidence and p.acc_means == means_of_murder for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "solved",
            "value": true,
            "if": {
              "calc": "(not solved) and any(p.acc_clue != '' and p.acc_clue == key_evidence and p.acc_means == means_of_murder for p in players)"
            },
            "text": "The case is solved!",
            "announce_to": "all"
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "accuse",
      "label": "clear the accusations",
      "do": [
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
        }
      ]
    },
    {
      "use": "ask",
      "phase": "hunt",
      "label": "the Witness Hunt",
      "when": {
        "calc": "solved_this_round"
      },
      "to": {
        "where": "you.role == 'murderer'"
      },
      "answer": {
        "type": "player",
        "exclude_self": true,
        "exclude": {
          "where": "you.seat == scientist_seat"
        }
      },
      "verify": {
        "bind": "hunt"
      },
      "text": "The case is solved. You are the Murderer: name the seat you believe is the Witness. If you are right, the Murderer side wins; if you are wrong, the Investigator side wins."
    },
    {
      "use": "update",
      "phase": "hunt",
      "label": "the hunt target",
      "when": {
        "calc": "solved_this_round"
      },
      "do": [
        {
          "set": {
            "key": "hunt_target",
            "value": "$hunt"
          }
        }
      ],
      "text": "The Murderer names seat {hunt_target} as the Witness."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "scoring",
      "when": {
        "calc": "solved or round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "won",
            "value": {
              "calc": "win_value if ((solved and hunt_target == witness_seat and you.side == 'murderer') or (solved and hunt_target != witness_seat and you.side == 'investigator') or ((not solved) and you.side == 'murderer')) else 0"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "end",
      "label": "end check",
      "when": {
        "calc": "solved or round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "solved or round >= rounds"
      },
      "rank_by": "you.won",
      "min_to_win": 1,
      "reveal": [
        "role"
      ],
      "text": "Winner: {result}. Case solved: {solved}; hunt target seat {hunt_target}; the Witness was seat {witness_seat}."
    }
  },
  "limits": {
    "rounds": 5,
    "rounds_max": 5,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "Seat {scientist_seat} is the Forensic Scientist, and everyone knows it. The Scientist holds no cards, has no badge and never speaks. Seats 2 and up are dealt exactly 1 Murderer, 1 Accomplice, 1 Witness and the rest Investigators, in secret. The Murderer and the Accomplice are the Murderer side; the Scientist, the Witness and the Investigators are the Investigator side.\n\nEach of seats 2 and up holds {clues_per_seat} Clue cards and {means_per_seat} Means cards, face up for everyone (from {clue_words} Clue words and {means_words} Means words). Undealt words are not on the table. Before round 1 the Murderer secretly chooses one of their own Clues as the key evidence and one of their own Means as the means of murder. The Scientist learns every role, the key evidence and the means of murder. The Accomplice learns the Murderer's seat. The Witness learns the two Murderer-side seats, but not which is which. The Murderer learns the Accomplice's seat. Investigators learn nothing. Seats 2 and up start with badge {starting_badge_cardholder}.\n\nThe game lasts at most {rounds} rounds. Each round:\n1. Tile. Round 1 reveals Cause of Death; rounds 2-4 each reveal one random tile not yet revealed (there are {scene_tiles} tiles of {items_per_tile} items).\n2. Marker. The Scientist privately chooses one item on the new tile, and the marked item is announced to all.\n3. Talk. Every seat 2 and up writes one short message at the same time; all messages are then shown to everyone.\n4. Accusation A. Every seat with badge 1 chooses, at the same time, PASS or one Clue word from the clues held by seats 2 and up (its own included).\n5. Accusation B. Every seat that named a Clue then chooses one Means word from the means held by seats 2 and up (its own included). PASS is not offered here.\n6. Every seat that accused loses its badge (badge 0) and is never asked to accuse again ({accusations_per_seat} accusation per seat). A seat that passed keeps its badge.\n7. Resolution. Each accusation is announced with its seat. If its Clue is the key evidence AND its Means is the means of murder, it is announced correct and the case is solved. Otherwise (one word right or neither) it is announced wrong and nothing changes. Once solved, the case stays solved.\n8. Accusations are cleared.\n9. Witness Hunt. Only if the case was solved this round, the Murderer names one seat from 2 and up other than their own.\n10. The game ends if the case is solved or round {rounds} has finished; otherwise the next round begins.\n\nWinning: if the case is solved and the Murderer named the Witness, the Murderer and the Accomplice win. If the case is solved and the Murderer named anyone else, the Investigator side wins (Scientist, Witness and Investigators). If the case is still unsolved after round {rounds}, the Murderer and the Accomplice win. Winners get won = {win_value}; there are no draws."
}
```
````
