# Variation: Deception: Four Tiles

A hidden-role deduction game over 4 rounds. A mute Scientist marks one item on a new Scene tile each round, players talk simultaneously, and badge holders may make one two-part accusation in a simultaneous poll. An unmasked Murderer can still win by naming the Witness.

Players: 6 to 8, best with 7

## Review of the original

Deception: Murder in Hong Kong is a hidden-role deduction game. A Forensic Scientist who knows the murderer's secret Clue and Means may only hint through Scene tile markers, and Investigators must name the exact Clue and Means pair before time runs out, while the Murderer and Accomplice mislead them and a Witness tries to help without being unmasked.

- **non_degenerate**: good. Always passing hands the win to the Murderer side. Always accusing at random wastes every badge on long odds. A Murderer who names a random seat in the Witness Hunt hits only about 1 in 4. Every simple policy can lose, and the outcome turns on what is marked, said and accused.
- **skill_sensitive**: good. Reading the Scientist's markers against the cards on the table, spotting misleading talk and timing badges decide the result. The random deal only fixes who knows what.
- **headroom**: good. Weak investigators can still get lucky with a badge. Strong play involves Scientist marker choice, Witness camouflage, decoy accusations by the Murderer side and Hunt inference, so it does not saturate.
- **reasoning_dependent**: good. The solution and the roles are hidden. Players infer them from indirect hints, from what others say and from who accuses what.
- **verifiable**: weak. The original's win is mechanical, but its timed presentations and free placement of markers are not. The previous build also mis-scored: `solved` toggled during setup, a correct accusation left `solved` false, and given roles were overwritten.
- **fits_platform**: weak. Timed 30-second talks, eyes-closed signalling, six tiles per round and tile replacement do not fit. The previous build also offered deck words such as 'Mask' as accusation options, asked a non-badge seat, and failed to drop the badge after an accusation.

## Problems

- P1: The accusation step offered words that were still in the deck (e.g. 'Mask') instead of only the Clue and Means cards actually held by players.
- P2: The accusation was not a clean two-part simultaneous poll. Some accusing seats were never asked for the Means, so `acc_means` stayed empty.
- P3: An accuser's badge did not drop to 0, so the same seat could be asked again.
- P4: Resolution did not compare `acc_clue` and `acc_means` with the stored Key Evidence and Means of Murder. `solved` and `hunt_target` were set and reset during setup, so a correct accusation ended with `solved` false.
- P5: The random deal overwrote roles and cards given in a scenario, leaving `intel` inconsistent with `role`.
- P6: The original's real-time elements (timed presentations, six tiles per round, tile replacement, eyes-closed pointing) cannot run on a turn-based text engine within the step limits.
- P7: Talk in turn order would let later speakers copy earlier ones.

## Changes

- The accusation poll offers PASS plus exactly the Clue words in the `clues` lists of seats 2..N. It never offers words from the clue deck or the full word list. The Means poll likewise offers exactly the words in the `means` lists of seats 2..N. (fixes: P1): Accusers can only name cards that are on the table.
- Accusation is two simultaneous polls each round. Poll A asks only seats with badge 1 to choose PASS or a table Clue, stored in `acc_clue`. Poll B asks only the seats that named a Clue in Poll A this round to choose a table Means, stored in `acc_means`. (fixes: P2): Every accuser is really asked for both parts, and both parts are recorded.
- Right after Poll B, every seat with a non-empty `acc_clue` has `badge` set to 0. (fixes: P3): Each seat gets one accusation for the whole game.
- `solved` (false) and `hunt_target` (0) are set exactly once, before the deal, and are never written again during setup. In Resolution, `solved` becomes true if any accuser's `acc_clue` equals `key_evidence` and their `acc_means` equals `means_of_murder`. Once true it is never reset. The Witness Hunt then writes `hunt_target`, and `won` is scored from it. (fixes: P4): A correct accusation reliably solves the case, and the Hunt result is scored from stored values.
- The deal only fills empty slots. A role, card list, Key Evidence or Means of Murder already present is kept, its cards are removed from the decks, and roles are drawn only from what remains. Intel is written after the deal, from the final roles. (fixes: P5): Scenario givens survive, and intel always matches roles.
- Four rounds, each revealing one Scene tile (Cause of Death first, then one random draw per round). The Scientist marks one item on each tile. Each non-Scientist holds 2 Clues and 2 Means. There are no timers and no tile replacement. (fixes: P6): The game fits a turn-based engine and the step limits, while keeping the hint-deduction core.
- Talk is simultaneous: every non-Scientist writes one message without seeing the others, then all messages are shown, then the accusation polls run. (fixes: P7): Nobody can copy an earlier speaker, and bluffs must be committed blind.

## Kept from the original

- Secret roles: a public Forensic Scientist, a Murderer, an Accomplice, a Witness and Investigators
- The Murderer secretly chooses one of their own Clues and one of their own Means as the solution
- The Scientist can only hint through markers on Scene tiles and may not talk
- One badge per player, a single exact Clue + Means accusation each
- The Witness Hunt: an unmasked Murderer can still steal the win by naming the Witness
- The Murderer side wins if the case is never solved

## The variation's rules

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

Objective: Team win, decided by arithmetic on the stored values.
- Investigator side wins if some accusation exactly matched key_evidence and means_of_murder and the Murderer's hunt_target is not the Witness's seat.
- Murderer side wins if the case is never solved in 4 rounds, or if it is solved and hunt_target equals the Witness's seat.
- The winners are the players with won = 1. There are no draws.

Expected effect: Accusations now behave exactly as written: one shot per badge, only table words, both parts recorded and correctly resolved, and scenario roles preserved.

Talk passes both tests. The sides genuinely disagree: the Murderer and Accomplice want accusations spread onto wrong pairs or badges wasted early. The Witness wants the Murderer's seat targeted while hiding their own knowledge from the Hunt. An Investigator who just follows the most confident proposal can burn their only badge on a decoy pushed by the Accomplice, and a Witness who argues too pointedly gets named in the Hunt and loses the game even after the case is solved.

The Scientist must pick markers that separate one seat's 4 possible pairs from the others. Badge timing is a real trade-off: accusing early wastes information, while waiting risks running out of rounds. Always passing, always accusing the first option and random Hunt targets all lose regularly.

## Complexity (the designer's count, against the limits)

- steps_per_round: 20 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 4 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
