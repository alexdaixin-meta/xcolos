# 40 design

- time: 2026-10-28T02:54:53+00:00 (51.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c9ecf44710e4f658, reply sha256 a0502144d570f20b

## Sent

````
Original game: Deception: Murder in Hong Kong
Players in the original: 4 to 12

Original rules:
Players get secret roles: 1 Forensic Scientist, 1 Murderer, optional Accomplice and Witness, rest Investigators. Each non-scientist has 4 Clue and 4 Means cards displayed outward. Secretly, with eyes closed, Murderer points to one of their own Clue as Key Evidence and one Means as Means of Murder; Accomplice and Witness learn identities via the Scientist. Then for three rounds Scientist reveals 6 Scene tiles and places bullet markers on one item per tile as clues to the solution, possibly replacing one tile each round after the first. Between markers players discuss publicly and in turn present their guess for 30 seconds. Any player may spend their badge to attempt to solve by naming one Clue and one Means on the table. If correct, Investigators and Scientist win, unless Witness rule triggers: if Murderer was identified but then correctly names Witness, Murderer side wins. Otherwise after third presentation if never solved correctly, Murderer side wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: The rules are otherwise complete:
- Accusation menu is (N-2)x4+pass options.
- The Murderer can never match the case_file because they cannot accuse their own seat.
- If badges run out, the round-4 poll is empty and the game ends unsolved.
- The hunt excludes self and seat 1.
- Winner cases are exhaustive with no draws.
- The game is finite at 4 rounds and decided by arithmetic on solved, the case_file and hunt_target.

Talk is placed correctly. It is simultaneous, and the Murderer and Witness disagree with investigators about what to say, so following a claim can cost.

Complexity: 4 rounds (<=40), 1 random draw at setup (<=1), hidden elements are roles and case_file (2, <=3), about 12 attributes (<=20), 8 listed steps (<=20).

Failure: the flat round step list contains FIVE player-input steps: (1) Murderer's pick, (2) Scientist's hint, (4) Talk, (5) Accusation poll, (7) Witness Hunt. The limit is choice_steps_per_round <= 4. Conditions mean at most 4 fire in any single round, but the engine's step list is flat and the same every round, so all 5 exist in it. The designer's stated 4 understates this. The pick is a one-time action that belongs in setup.
- change: Move the Murderer's pick out of the round step list into SETUP, so the case_file is written once before round 1. That leaves 4 choice steps per round (hint, talk, accusation, hunt) and makes choice_steps_per_round = 4 accurate. Alternatively, fold the hunt into an end-of-game step outside the per-round list.
The variation that was reviewed: Deception: Case File: SETUP.
Seat 1 is always the Forensic Scientist, and everyone knows this. Among seats 2..N, roles are dealt at random and secretly: 1 Murderer, 1 Witness (only if N >= 5), and the rest Investigators. Each player sees only their own role. The Witness is privately told the Murderer's seat number. The Scientist is not told who anyone is.
Shuffle the Clue list and the Means list. Deal each seat 2..N two Clues (labelled C1, C2) and two Means (labelled M1, M2). All cards are face up and public.
Clue list (16): Fingerprint, Lipstick, Train Ticket, Diary, Wine Bottle, Hair Strand, Muddy Boots, Receipt, Cigarette Butt, Glove, Necklace, Photograph, Key, Letter, Wedding Ring, Map.
Means list (16): Knife, Poison, Rope, Pistol, Brick, Drowning, Electric Shock, Fire, Pillow, Push from Height, Car Crash, Injection, Axe, Strangling Scarf, Sleeping Pills, Bare Hands.
Each seat 2..N starts with 2 badges, which are public.

FIXED TILE SCHEDULE (rule constants). Each tile has 4 options:
- Round 1: Cause of Death (Suffocation / Severe Injury / Loss of Blood / Poisoning or Illness) and Location of Crime (Home / Outdoors / Public Venue / Workplace).
- Round 2: Victim's Expression (Calm / Terrified / Angry / Confused) and Trace at the Scene (Fingermarks / Footprints / Bruises / Nothing Visible).
- Round 3: Murderer's Personality (Cold / Greedy / Jealous / Desperate) and Time of Death (Morning / Afternoon / Evening / Night).
- Round 4: Hint on Corpse (Head / Chest / Hands / Legs) and Duration of Crime (Instant / Minutes / An Hour / Long Planned).

EACH ROUND r = 1..4, in this order:
1. (Round 1 only) Murderer's pick, private poll. The Murderer chooses one of C1+M1, C1+M2, C2+M1, C2+M2 from their own cards. The result is written to the Scientist's private case_file as 'Seat s: Cx + My', visible only to the Scientist.
2. Scientist's hint, private poll. The Scientist picks one option on each of this round's two tiles (16 combined choices).
3. Announce. current_hint is set to the two chosen options and shown to all.
4. Talk. Every seat except the Scientist writes one short message at the same time. All messages are then shown together. The Scientist never speaks.
5. Accusation poll (rounds 2-4 only, simultaneous, for seats with at least 1 badge). Each such seat chooses 'pass' or one accusation 'Seat s: Cx + My', where s is any seat 2..N other than their own. In round 4, 'pass' is not offered. Choices are stored privately until resolved.
6. Resolution. If any accusation equals the case_file, set solved = 1. Every seat that did not pass loses 1 badge. All accusations made are then revealed.
7. Witness Hunt (only if solved = 1 and a Witness exists). The Murderer chooses one seat other than themselves and seat 1. That seat is written to hunt_target.
8. End check. The game ends if solved = 1, or if r = 4.

The case_file, all roles and hunt_target are revealed at the end. Winner: Team win, decided by arithmetic on the tracked values.
- If solved = 1 and either there is no Witness or hunt_target is not the Witness's seat, the Scientist and all Investigators and the Witness win, and the Murderer loses.
- If solved = 1 and hunt_target is the Witness's seat, the Murderer wins and everyone else loses.
- If the game ends after round 4 with solved = 0, the Murderer wins and everyone else loses.
There are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Deception: Murder in Hong Kong is a hidden-role deduction game. A secret Murderer picks one of their own face-up Clue and Means cards as the solution. A Forensic Scientist who knows the answer but cannot speak gives clues only by marking options on Scene tiles. Investigators discuss and spend one-shot badges to name the pair. An optional Witness knows the Murderer, and the Murderer can snatch a win by identifying the Witness.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies can all lose.\n- A Scientist who always marks the first option gives no information, so investigators fall back to guessing and the Murderer usually wins.\n- Investigators who always pass lose for certain.\n- A Murderer who always hunts the lowest eligible seat finds the Witness only about 1 time in N-2.\n- Seat roles are random, and seat 1 (the Scientist) is on the investigators' side.\nThe Murderer's choice of solution, the Scientist's hints, the timing of accusations and the hunt all change who wins."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The only chance event is the deal at setup. After that the result depends on:\n- how well the Scientist encodes the answer in tile options;\n- how well investigators decode the hints and read the table talk;\n- how well the Murderer and Witness bluff;\n- how well the Murderer reads who the Witness is.\nA player who guesses blindly lands about 1 in 16 per accusation."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Hint encoding is open-ended: one sentence-like signal must point at one of up to 28 face-up cards. Talk allows bluffing and Witness concealment. Badge timing trades information against tempo. Weak investigators still win sometimes by guessing, and a weak Murderer can still survive or find the Witness."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hidden roles plus a hidden case file make it so.\n- Investigators must infer the solution from noisy semantic hints and from who argues for what.\n- The Murderer must infer which seat is the Witness.\n- The Witness must steer the table without revealing themselves.\n- The Scientist must plan hints across 4 rounds against a fixed tile schedule."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner follows from three tracked values: solved, the case file and hunt_target. Interpreting the hints is the players' reasoning, never a judge's ruling."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The previous variation is turn-based, text-only, has no board and lasts 4 rounds. However, its flat per-round step list held five player-input steps (Murderer's pick, hint, talk, accusation, hunt), which exceeds the limit of 4 choice steps per round. The pick happens once and belongs in setup."
    }
  ],
  "problems": [
    "The original's eyes-closed setup, 30-second spoken presentations, physical bullet markers and tile replacement are real-time or physical. The optional Accomplice adds a second hidden ally for little gain.",
    "The previous variation listed the Murderer's one-time pick as step 1 of the per-round list. That gives 5 choice steps per round (pick, hint, talk, accusation, hunt), over the limit of 4, and its own complexity report understated this.",
    "The previous variation's player range was not tied to the deck size: 2 Clues per seat from a 16-card list caps the game at 8 players."
  ],
  "changes": [
    {
      "what": "The Murderer's pick of Clue+Means becomes a setup step, done once before round 1 and written to the private case_file. The per-round list keeps only four choice steps: hint, talk, accusation and Witness hunt.",
      "why": "A one-time action should not sit in the repeating round list. This brings choice_steps_per_round to exactly 4.",
      "fixes": "The previous variation listed the Murderer's one-time pick as step 1 of the per-round list. That gives 5 choice steps per round (pick, hint, talk, accusation, hunt), over the limit of 4, and its own complexity report understated this."
    },
    {
      "what": "Player count is fixed at 4 to 8.",
      "why": "At most 7 non-Scientist seats each take 2 Clues and 2 Means from 16-card lists.",
      "fixes": "The previous variation's player range was not tied to the deck size: 2 Clues per seat from a 16-card list caps the game at 8 players."
    },
    {
      "what": "These carry over from the previous version and stay:\n- a fixed tile schedule of 2 tiles per round with 4 options each;\n- simultaneous one-message talk instead of timed presentations;\n- 2 badges per seat instead of 1;\n- no Accomplice.",
      "why": "They keep the game text-only and turn-based, and keep one strong hidden element (roles) plus the case file.",
      "fixes": "The original's eyes-closed setup, 30-second spoken presentations, physical bullet markers and tile replacement are real-time or physical. The optional Accomplice adds a second hidden ally for little gain."
    }
  ],
  "keeps": [
    "A mute Forensic Scientist who knows the answer and can only point at Scene-tile options.",
    "A secret Murderer who chooses the solution from their own face-up Clue and Means cards.",
    "Investigators spend limited badges to name a Clue+Means pair. One correct accusation solves the case.",
    "A Witness who knows the Murderer. A Murderer who is caught can still win by naming the Witness.",
    "The Murderer wins if the case goes unsolved through the last round.",
    "Public discussion between hints, where the Murderer bluffs."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation was sound except for its step layout. Moving the one-time pick into setup fixes the only playability failure and leaves the deduction, bluffing and Witness-hunt core intact."
  },
  "variation": {
    "name": "Deception: Case File",
    "summary": "A 4-round hidden-role deduction game. A mute Scientist steers investigators toward the Murderer's secret Clue+Means through fixed scene tiles. Investigators spend 2 badges each to accuse. A caught Murderer can still win by unmasking the Witness.",
    "players": {
      "min": 4,
      "max": 8,
      "suggested": 6
    },
    "rules": "SETUP (done once, before round 1)\n\nS1. Roles. Seat 1 is always the Forensic Scientist, and everyone knows this. Among seats 2..N, roles are dealt at random and secretly:\n- 1 Murderer;\n- 1 Witness (only if N >= 5);\n- the rest Investigators.\nEach player sees only their own role. The Witness is privately told the Murderer's seat number. The Scientist is not told anyone's role.\n\nS2. Cards. Shuffle the Clue list and the Means list. Deal each seat 2..N two Clues (labelled C1, C2) and two Means (labelled M1, M2). All cards are face up and public.\n- Clue list (16): Fingerprint, Lipstick, Train Ticket, Diary, Wine Bottle, Hair Strand, Muddy Boots, Receipt, Cigarette Butt, Glove, Necklace, Photograph, Key, Letter, Wedding Ring, Map.\n- Means list (16): Knife, Poison, Rope, Pistol, Brick, Drowning, Electric Shock, Fire, Pillow, Push from Height, Car Crash, Injection, Axe, Strangling Scarf, Sleeping Pills, Bare Hands.\n\nS3. Badges. Each seat 2..N starts with 2 badges. Badge counts are public. Set solved = 0 and hunt_target = 0.\n\nS4. Murderer's pick (private poll, once). The Murderer chooses one of C1+M1, C1+M2, C2+M1 or C2+M2 from their own cards. The result is written to the case_file as 'Seat s: Cx + My'. Only the Scientist can see the case_file.\n\nFIXED TILE SCHEDULE (rule constants). Each tile has 4 options.\n- Round 1: Cause of Death (Suffocation / Severe Injury / Loss of Blood / Poisoning or Illness) and Location of Crime (Home / Outdoors / Public Venue / Workplace).\n- Round 2: Victim's Expression (Calm / Terrified / Angry / Confused) and Trace at the Scene (Fingermarks / Footprints / Bruises / Nothing Visible).\n- Round 3: Murderer's Personality (Cold / Greedy / Jealous / Desperate) and Time of Death (Morning / Afternoon / Evening / Night).\n- Round 4: Hint on Corpse (Head / Chest / Hands / Legs) and Duration of Crime (Instant / Minutes / An Hour / Long Planned).\n\nEACH ROUND r = 1..4, in this order:\n\n1. Scientist's hint (private poll). The Scientist picks one option on each of this round's two tiles, for 16 combined choices.\n\n2. Announce. current_hint is set to the two chosen options and shown to everyone.\n\n3. Talk. Every seat except the Scientist writes one short message at the same time. All messages are then shown together. The Scientist never speaks.\n\n4. Accusation poll. This happens in rounds 2-4 only and is simultaneous. It is open to every seat 2..N with at least 1 badge.\n- Each such seat chooses either 'pass' or one accusation 'Seat s: Cx + My', where s is any seat 2..N other than their own.\n- In round 4, 'pass' is not offered.\n- Choices stay hidden until resolution.\n\n5. Resolution (rounds 2-4).\n- If any accusation equals the case_file, set solved = 1.\n- Every seat that did not pass loses 1 badge.\n- All accusations made are then revealed.\n\n6. Witness Hunt (private poll). This happens only if solved = 1 and a Witness exists. The Murderer chooses one seat that is neither themselves nor seat 1. That seat is written to hunt_target.\n\n7. End check. The game ends if solved = 1 or r = 4. Otherwise the next round begins.\n\nAt the end, the case_file, all roles and hunt_target are revealed.",
    "objective": "The game is a team win, decided by arithmetic on the tracked values.\n- If solved = 1 and either there is no Witness or hunt_target is not the Witness's seat: the Scientist, all Investigators and the Witness win, and the Murderer loses.\n- If solved = 1 and hunt_target equals the Witness's seat: the Murderer wins and everyone else loses.\n- If the game ends after round 4 with solved = 0: the Murderer wins and everyone else loses.\nThere are no draws.",
    "expected_effect": "Play is the same as the previous variation, but now buildable within limits.\n\nThe Scientist plans a 4-round hint sequence on fixed tiles. The Murderer picks a pair that those tiles describe poorly.\n\nInvestigators decide when to spend badges: early guesses waste badges, but waiting risks round 4.\n\nThe players genuinely disagree in talk:\n- The Murderer wants accusations steered toward wrong pairs.\n- The Witness wants the right seat accused without appearing to know it.\n- Investigators want to find out who is reliable.\n\nA player who simply follows the loudest claim can spend both badges on a Murderer's misdirection. A Witness who speaks too plainly gets hunted after the solve, which hands the win to the Murderer. Talk is simultaneous, so no one can echo an earlier speaker."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 7,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 4
  }
}
```
````
