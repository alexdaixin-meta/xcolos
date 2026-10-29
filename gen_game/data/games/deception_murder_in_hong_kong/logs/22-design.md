# 22 design

- time: 2026-10-28T02:10:14+00:00 (92.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c96087bb17fbc252, reply sha256 81848ebb80ba1854

## Sent

````
Original game: Deception: Murder in Hong Kong
Players in the original: 4 to 12

Original rules:
Players get secret roles: 1 Forensic Scientist, 1 Murderer, optional Accomplice and Witness, rest Investigators. Each non-scientist has 4 Clue and 4 Means cards displayed outward. Secretly, with eyes closed, Murderer points to one of their own Clue as Key Evidence and one Means as Means of Murder; Accomplice and Witness learn identities via the Scientist. Then for three rounds Scientist reveals 6 Scene tiles and places bullet markers on one item per tile as clues to the solution, possibly replacing one tile each round after the first. Between markers players discuss publicly and in turn present their guess for 30 seconds. Any player may spend their badge to attempt to solve by naming one Clue and one Means on the table. If correct, Investigators and Scientist win, unless Witness rule triggers: if Murderer was identified but then correctly names Witness, Murderer side wins. Otherwise after third presentation if never solved correctly, Murderer side wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rework the Accusation step as one simultaneous poll.
1. Ask only the players whose `badge` is 1.
2. Offer each of them PASS plus the Clue and Means words actually on the table. Build these options from the union of the players' `clues` and `means` lists, never from the full 16-word lists or the leftover decks.
3. If one answer covers both words, or the accusation is a two-part choice, make sure each accusing seat really is asked for the Clue and then the Means, and record them in `acc_clue` and `acc_means`.
4. Any player who does not PASS must have `badge` set to 0.

In Resolution:
- Compare each accusation's `acc_clue` with the Key Evidence and its `acc_means` with the Means of Murder, as stored from the Murderer's private choice.
- If both match, set `solved` to true. Do not reset it after setup; the trace shows `solved` and `hunt_target` toggling during initialisation.
- Then run the Witness Hunt: the Murderer names a seat, which is stored in `hunt_target`.
- Score `won` from that.

Also make sure roles and cards given in a scenario are not overwritten by the random deal. The final state shows `intel` disagreeing with `role`.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `Only badge holders are asked to accuse, and only clues on the table are offered` failed: rule R15 is broken: When accusations are made, then only players with badge 1 are asked, all at the same time, to choose PASS or one Clue on the table and one Means on the table.; seat 6 was offered 'Mask', but must not be
- scenario `A wrong accuser's badge drops to 0, and the game goes on` failed: rule R16 is broken: When a player accuses, then their badge drops from 1 to 0 and they are not asked to accuse again.; seat 5 badge: expected 0, got 1; Eli: the rule for 'Wallet' was never matched (the game never put that option to this seat); Eli: the rule for 'Insulin' was never matched (the game 
- scenario `Correct accusation Glove + Rope solves the case` failed: rule R17 is broken: When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong.; game solved: expected True, got False; game hunt_target: expected 6, got 0; Blaise: the rule for 6 was
- scenario `Right clue with the wrong means (Glove + Poison) is wrong` failed: rule R17 is broken: When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong.; Eli: the rule for 'Poison' was never matched (the game never put that option to this seat)
- what the game did on `Only badge holders are asked to accuse, and only clues on the table are offered`: moves played: r1 seat 2: 'Glove'; r1 seat 2: 'Rope'; r1 seat 1: 'Suffocation'; r1 seat 2: 'PASS'; r1 seat 3: 'PASS'; r1 seat 4: 'PASS'; r1 seat 6: 'PASS'. First attribute changes: seat 1 role: '' -> 'Scientist'; table current_tile: '' -> 'not drawn yet'; table marker: '' -> 'not marked yet'; table solved: False -> True; table solved: True -> False; table hunt_target: 0 -> -1; table hunt_target: -1 -> 0; table seat_names: [] -> ['seat 1', 'seat 2', 'seat 3', 'seat 4', 'seat 5', 'seat 6', 'seat 7', 'seat 8']; table tile_table: [] -> [['Cause of Death', 'Suffocation', 'Severe Injury', 'Loss of Blood', 'Illness', 'Poisoning', 'Accident'], ['Location', 'Living Room', 'Bedroom', 'Bathroom', 'Kitchen', 'Street', 'Office'], ['Time of Death', 'Dawn', 'Morning', 'Noon', 'Afternoon', 'Evening', 'Night'], ['Weather', 'Sunny', 'Stormy', 'Dry', 'Humid', 'Cold', 'Hot'], ["Victim's Build", 'Large', 'Thin', 'Tall', 'Short', 'Disfigured', 'Fit'], ['Trace at Scene', 'Fingerprint', 'Footprint', 'Bruise', 'Blood Stain', 'Body Fluid', 'Scar'], ['Corpse Condition', 'Still Warm', 'Stiff', 'Decayed', 'Incomplete', 'Intact', 'Twisted'], ['Duration of Crime', 'Instant', 'Brief', 'Gradual', 'Prolonged', 'Days', 'Unclear']]; table role_pool: [] -> ['Murderer', 'Accomplice', 'Witness', 'Investigator', 'Investigator']; table pick: '' -> 'Investigator'; seat 2 role: '' -> 'Investigator'; table role_pool: ['Murderer', 'Accomplice', 'Witness', 'Investigator', 'Investigator'] -> ['Murderer', 'Accomplice', 'Witness', 'Investigator']; table pick: 'Investigator' -> 'Murderer' .... Final: players {"seat 1": {"role": "Scientist", "side": "investigator", "intel": "Roles: seat 1 Scientist; seat 2 Investigator; seat 3 Murderer; seat 4 Witness; seat 5 Investigator; seat 6 Accomplice.", "solution_known": "Key Evidence: Glove; Means of Murder: Rope", "clues": [], "means": [], "badge": 0, "acc_clue": "", "acc_means": "", "won": 0, "pick_clue": "", "pick_means": "", "verdict": ""}, "seat 2": {"role": "Murderer", "side; table {"clue_deck": ["Train Ticket", "Lipstick", "Receipt", "Hair", "Button", "Mask"], "means_deck": ["Poison", "Knife", "Pistol", "Electric Wire", "Scarf", "Bottle"], "tile_deck": ["Time of Death", "Weather", "Victim's Build", "Trace at Scene", "Corpse Condition", "Duration of Crime"], "tile_table": [["Cause of Death", "Suffocation", "Severe Injury", "Loss of Blood", "Illness", "Poisoning", "Accident"], ["Location", "Livi
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "Seat 1 is the Scientist: no cards and no badge",
  "rule": "R1",
  "players": 6,
  "seed": 1,
  "rounds": 1,
  "rules": [
   {
    "seat": 2,
    "options_include": "PASS"
   }
  ],
  "expect": {
   "players": {
    "1": {
     "badge": 0,
     "won": 0
    }
   },
   "lens": {
    "players": {
     "1": {
      "clues": 0,
      "means": 0
     }
    }
   },
   "not_offered": [
    {
     "seat": 1,
     "option": "PASS"
    }
   ]
  },
  "rule_text": "Seat 1 is always the Forensic Scientist, and that role is public."
 },
 {
  "name": "7 players: the 6 non-Scientist seats are each dealt cards, so 12 clue words leave the deck (roles hidden, only counts asserted)",
  "rule": "R2",
  "players": 7,
  "seed": 2,
  "rounds": 1,
  "rules": [
   {
    "seat": 2,
    "options_include": "PASS"
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "clue_deck": 4,
     "means_deck": 4
    },
    "players": {
     "1": {
      "clues": 0
     },
     "2": {
      "clues": 2
     },
     "3": {
      "clues": 2
     },
     "4": {
      "clues": 2
     },
     "5": {
      "clues": 2
     },
     "6": {
      "clues": 2
     },
     "7": {
      "clues": 2
     }
    }
   }
  },
  "rule_text": "When the game starts with N players, then the other N-1 seats are dealt exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators at random."
 },
 {
  "name": "8 players: setup deals 7 seats (intel hidden, only observable state asserted)",
  "rule": "R3",
  "players": 8,
  "seed": 3,
  "rounds": 1,
  "rules": [
   {
    "seat": 2,
    "options_include": "PASS"
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "clue_deck": 2,
     "means_deck": 2
    }
   },
   "game": {
    "round": 1,
    "solved": false
   }
  },
  "rule_text": "When roles are dealt, then the Accomplice's intel names the Murderer's seat."
 },
 {
  "name": "With stated roles, a round of passes leaves the case unsolved and nobody has won",
  "rule": "R4",
  "players": 6,
  "seed": 4,
  "rounds": 1,
  "given": {
   "players": {
    "1": {
     "role": "Scientist",
     "side": "investigator"
    },
    "2": {
     "role": "Murderer",
     "side": "murderer",
     "clues": [
      "Glove",
      "Key"
     ],
     "means": [
      "Rope",
      "Poison"
     ]
    },
    "3": {
     "role": "Accomplice",
     "side": "murderer",
     "clues": [
      "Diary",
      "Ring"
     ],
     "means": [
      "Knife",
      "Pillow"
     ]
    },
    "4": {
     "role": "Witness",
     "side": "investigator",
     "clues": [
      "Cigarette",
      "Phone"
     ],
     "means": [
      "

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Deception: Murder in Hong Kong is a hidden-role deduction game. A Forensic Scientist who knows the murderer's secret Clue and Means may only hint through Scene tile markers, and Investigators must name the exact Clue and Means pair before time runs out, while the Murderer and Accomplice mislead them and a Witness tries to help without being unmasked.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Always passing hands the win to the Murderer side. Always accusing at random wastes every badge on long odds. A Murderer who names a random seat in the Witness Hunt hits only about 1 in 4. Every simple policy can lose, and the outcome turns on what is marked, said and accused."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Reading the Scientist's markers against the cards on the table, spotting misleading talk and timing badges decide the result. The random deal only fixes who knows what."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak investigators can still get lucky with a badge. Strong play involves Scientist marker choice, Witness camouflage, decoy accusations by the Murderer side and Hunt inference, so it does not saturate."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The solution and the roles are hidden. Players infer them from indirect hints, from what others say and from who accuses what."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "The original's win is mechanical, but its timed presentations and free placement of markers are not. The previous build also mis-scored: `solved` toggled during setup, a correct accusation left `solved` false, and given roles were overwritten."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Timed 30-second talks, eyes-closed signalling, six tiles per round and tile replacement do not fit. The previous build also offered deck words such as 'Mask' as accusation options, asked a non-badge seat, and failed to drop the badge after an accusation."
    }
  ],
  "problems": [
    "P1: The accusation step offered words that were still in the deck (e.g. 'Mask') instead of only the Clue and Means cards actually held by players.",
    "P2: The accusation was not a clean two-part simultaneous poll. Some accusing seats were never asked for the Means, so `acc_means` stayed empty.",
    "P3: An accuser's badge did not drop to 0, so the same seat could be asked again.",
    "P4: Resolution did not compare `acc_clue` and `acc_means` with the stored Key Evidence and Means of Murder. `solved` and `hunt_target` were set and reset during setup, so a correct accusation ended with `solved` false.",
    "P5: The random deal overwrote roles and cards given in a scenario, leaving `intel` inconsistent with `role`.",
    "P6: The original's real-time elements (timed presentations, six tiles per round, tile replacement, eyes-closed pointing) cannot run on a turn-based text engine within the step limits.",
    "P7: Talk in turn order would let later speakers copy earlier ones."
  ],
  "changes": [
    {
      "what": "The accusation poll offers PASS plus exactly the Clue words in the `clues` lists of seats 2..N. It never offers words from the clue deck or the full word list. The Means poll likewise offers exactly the words in the `means` lists of seats 2..N.",
      "why": "Accusers can only name cards that are on the table.",
      "fixes": "P1"
    },
    {
      "what": "Accusation is two simultaneous polls each round. Poll A asks only seats with badge 1 to choose PASS or a table Clue, stored in `acc_clue`. Poll B asks only the seats that named a Clue in Poll A this round to choose a table Means, stored in `acc_means`.",
      "why": "Every accuser is really asked for both parts, and both parts are recorded.",
      "fixes": "P2"
    },
    {
      "what": "Right after Poll B, every seat with a non-empty `acc_clue` has `badge` set to 0.",
      "why": "Each seat gets one accusation for the whole game.",
      "fixes": "P3"
    },
    {
      "what": "`solved` (false) and `hunt_target` (0) are set exactly once, before the deal, and are never written again during setup. In Resolution, `solved` becomes true if any accuser's `acc_clue` equals `key_evidence` and their `acc_means` equals `means_of_murder`. Once true it is never reset. The Witness Hunt then writes `hunt_target`, and `won` is scored from it.",
      "why": "A correct accusation reliably solves the case, and the Hunt result is scored from stored values.",
      "fixes": "P4"
    },
    {
      "what": "The deal only fills empty slots. A role, card list, Key Evidence or Means of Murder already present is kept, its cards are removed from the decks, and roles are drawn only from what remains. Intel is written after the deal, from the final roles.",
      "why": "Scenario givens survive, and intel always matches roles.",
      "fixes": "P5"
    },
    {
      "what": "Four rounds, each revealing one Scene tile (Cause of Death first, then one random draw per round). The Scientist marks one item on each tile. Each non-Scientist holds 2 Clues and 2 Means. There are no timers and no tile replacement.",
      "why": "The game fits a turn-based engine and the step limits, while keeping the hint-deduction core.",
      "fixes": "P6"
    },
    {
      "what": "Talk is simultaneous: every non-Scientist writes one message without seeing the others, then all messages are shown, then the accusation polls run.",
      "why": "Nobody can copy an earlier speaker, and bluffs must be committed blind.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "Secret roles: a public Forensic Scientist, a Murderer, an Accomplice, a Witness and Investigators",
    "The Murderer secretly chooses one of their own Clues and one of their own Means as the solution",
    "The Scientist can only hint through markers on Scene tiles and may not talk",
    "One badge per player, a single exact Clue + Means accusation each",
    "The Witness Hunt: an unmasked Murderer can still steal the win by naming the Witness",
    "The Murderer side wins if the case is never solved"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core works on the platform. Only the accusation and resolution mechanics and the scenario handling needed exact, buildable wording."
  },
  "variation": {
    "name": "Deception: Four Tiles",
    "summary": "A hidden-role deduction game over 4 rounds. A mute Scientist marks one item on a new Scene tile each round, players talk simultaneously, and badge holders may make one two-part accusation in a simultaneous poll. An unmasked Murderer can still win by naming the Witness.",
    "players": {
      "min": 6,
      "max": 8,
      "suggested": 7
    },
    "rules": "COMPONENTS.\n- Clue words (16): Glove, Key, Diary, Ring, Cigarette, Phone, Wallet, Mask, Train Ticket, Lipstick, Receipt, Hair, Button, Watch, Letter, Coin.\n- Means words (16): Rope, Poison, Knife, Pillow, Insulin, Pistol, Electric Wire, Scarf, Bottle, Axe, Hammer, Candlestick, Brick, Razor, Bag, Ice.\n- Scene tiles (8), each with a name and 6 items:\n  - Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident\n  - Location: Living Room, Bedroom, Bathroom, Kitchen, Street, Office\n  - Time of Death: Dawn, Morning, Noon, Afternoon, Evening, Night\n  - Weather: Sunny, Stormy, Dry, Humid, Cold, Hot\n  - Victim's Build: Large, Thin, Tall, Short, Disfigured, Fit\n  - Trace at Scene: Fingerprint, Footprint, Bruise, Blood Stain, Body Fluid, Scar\n  - Corpse Condition: Still Warm, Stiff, Decayed, Incomplete, Intact, Twisted\n  - Duration of Crime: Instant, Brief, Gradual, Prolonged, Days, Unclear\n\nGAME STATE, set once before setup and never reset by setup:\n- solved = false\n- hunt_target = 0\n- key_evidence and means_of_murder are empty unless given\n- Every player starts with badge 0, won 0, acc_clue empty and acc_means empty.\n\nSETUP.\n1. Seat 1 is always the Forensic Scientist. This is public. The Scientist gets no cards and badge 0.\n2. Seats 2..N receive exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators.\n   - A role already given to a seat is kept.\n   - Remaining roles are dealt at random to seats without a role.\n   - Sides: Murderer and Accomplice are on the Murderer side. Scientist, Witness and Investigators are on the Investigator side.\n3. Each of seats 2..N holds exactly 2 Clue cards and 2 Means cards, face up for everyone to see.\n   - Cards already given are kept and removed from the decks first.\n   - Missing cards are dealt at random from the remaining decks.\n   - Undealt words stay in the clue deck and means deck. They are not 'on the table'.\n   - Seats 2..N get badge 1.\n4. Unless already given, the Murderer secretly chooses one of their own 2 Clues as key_evidence, then one of their own 2 Means as means_of_murder.\n5. Private intel, written from the final roles:\n   - The Scientist learns every role, key_evidence and means_of_murder.\n   - The Accomplice learns the Murderer's seat.\n   - The Witness learns the two Murderer-side seats, but not which is which.\n   - The Murderer learns the Accomplice's seat.\n   - Investigators learn nothing.\n\nEACH ROUND (rounds 1 to 4):\n1. Tile. Round 1 reveals Cause of Death. Rounds 2-4 each reveal one tile drawn at random from the tiles not yet revealed. This is the only random draw in a round.\n2. Marker. The Scientist privately chooses one of the 6 items on the new tile, and the marked item is announced to all. The Scientist never speaks.\n3. Talk. Every seat 2..N writes one short message at the same time, without seeing the others. All messages are then shown to everyone.\n4. Accusation, Poll A. All seats with badge 1 are asked at the same time to choose PASS or one Clue word. The only Clue words offered are those currently in the clues lists of seats 2..N. The answer is stored in acc_clue (PASS leaves it empty).\n5. Accusation, Poll B. All seats that named a Clue in Poll A this round are asked at the same time to choose one Means word. The only Means words offered are those currently in the means lists of seats 2..N. The answer is stored in acc_means.\n6. Every seat with a non-empty acc_clue has badge set to 0. It will never be asked to accuse again.\n7. Resolution. Each accusation (acc_clue, acc_means) is announced with its seat.\n   - If acc_clue equals key_evidence and acc_means equals means_of_murder, it is announced as correct and solved becomes true.\n   - Otherwise it is announced as wrong.\n   - solved, once true, stays true.\n8. acc_clue and acc_means are cleared for all players.\n9. Witness Hunt. This happens only if solved became true this round. The Murderer chooses one seat from seats 2..N other than their own, stored as hunt_target.\n10. End check. The game ends if solved is true or round 4 has finished. Otherwise the next round begins.\n\nSCORING at the end:\n- If solved is true and hunt_target is the Witness's seat, every Murderer-side player gets won = 1.\n- If solved is true and hunt_target is not the Witness's seat, every Investigator-side player (including the Scientist) gets won = 1.\n- If solved is false after round 4, every Murderer-side player gets won = 1.",
    "objective": "Team win, decided by arithmetic on the stored values.\n- Investigator side wins if some accusation exactly matched key_evidence and means_of_murder and the Murderer's hunt_target is not the Witness's seat.\n- Murderer side wins if the case is never solved in 4 rounds, or if it is solved and hunt_target equals the Witness's seat.\n- The winners are the players with won = 1. There are no draws.",
    "expected_effect": "Accusations now behave exactly as written: one shot per badge, only table words, both parts recorded and correctly resolved, and scenario roles preserved.\n\nTalk passes both tests. The sides genuinely disagree: the Murderer and Accomplice want accusations spread onto wrong pairs or badges wasted early. The Witness wants the Murderer's seat targeted while hiding their own knowledge from the Hunt. An Investigator who just follows the most confident proposal can burn their only badge on a decoy pushed by the Accomplice, and a Witness who argues too pointedly gets named in the Hunt and loses the game even after the case is solved.\n\nThe Scientist must pick markers that separate one seat's 4 possible pairs from the others. Badge timing is a real trade-off: accusing early wastes information, while waiting risks running out of rounds. Always passing, always accusing the first option and random Hunt targets all lose regularly."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 20,
    "choice_steps_per_round": 4,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 4
  }
}
```
````
