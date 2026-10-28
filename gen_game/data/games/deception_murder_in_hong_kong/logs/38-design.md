# 38 design

- time: 2026-10-28T02:51:50+00:00 (111.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 8c5f9eeaf984b835, reply sha256 8d4f47778d23c99a

## Sent

````
Original game: Deception: Murder in Hong Kong
Players in the original: 4 to 12

Original rules:
Players get secret roles: 1 Forensic Scientist, 1 Murderer, optional Accomplice and Witness, rest Investigators. Each non-scientist has 4 Clue and 4 Means cards displayed outward. Secretly, with eyes closed, Murderer points to one of their own Clue as Key Evidence and one Means as Means of Murder; Accomplice and Witness learn identities via the Scientist. Then for three rounds Scientist reveals 6 Scene tiles and places bullet markers on one item per tile as clues to the solution, possibly replacing one tile each round after the first. Between markers players discuss publicly and in turn present their guess for 30 seconds. Any player may spend their badge to attempt to solve by naming one Clue and one Means on the table. If correct, Investigators and Scientist win, unless Witness rule triggers: if Murderer was identified but then correctly names Witness, Murderer side wins. Otherwise after third presentation if never solved correctly, Murderer side wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Make solving reachable in ordinary play while keeping the deduction. (1) Two-step accusation: an accuser first names a seat (2..N, not their own). Poll B then offers only that seat's 2 Clues and 2 Means, so a guess is choosing a suspect plus one of 4 combinations rather than one of about 64. (2) Remove PASS in round 4: every seat still holding badge 1 must accuse then. (3) Optionally, give each seat 2 accusations instead of 1. Keep everything else as it is: solved never resets, the Witness Hunt runs only when the case is solved this round, and scoring is unchanged. Note for the coder in the next build: write the Witness Hunt step that sets hunt_target. Hide internal fields (acc_clue, acc_means, intel, verdict, solved_this_round, tile_catalog) as bookkeeping (`none` on the table, `ally` on a player), or make tile_catalog a fixed parameter and not a changing attribute.
the game file could not be built. What the checks found on the attempts:
- attempt 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (acc_clue, acc_means, current_tile) in `your_starting_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 2: it plays, but part of it does nothing: game attribute `solved` is never changed in 3 random matches, so nothing updates it. Steps that name it: resolution. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `solved_this_round` is never changed in 3 random matches, so nothing updates it. Steps that name it: the tile, resolution. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `hunt_target` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `tile_catalog` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- attempt 3: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (acc_clue, acc_means, intel, verdict); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- attempt 4: it plays, but part of it does nothing: game attribute `solved` is never changed in 3 random matches, so nothing updates it. Steps that name it: resolution. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `solved_this_round` is never changed in 3 random matches, so nothing updates it. Steps that name it: the tile, resolution. They never change it: their `

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Deception: Murder in Hong Kong is a social-deduction game. A silent Forensic Scientist knows which of the secret Murderer's face-up Clue and Means cards are the solution, and hints at them by placing markers on Scene tiles. Investigators, hampered by a hidden Murderer and sometimes an Accomplice, discuss and spend one badge each to name the solution. If they solve it, the Murderer can still win by identifying the hidden Witness.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Thoughtless policies lose. Never accusing hands the win to the Murderer side, and random accusing almost never hits one combination out of about 64. No seat has a built-in edge apart from the fixed Scientist role, and the Scientist's choice of markers decides whether a solve is possible. In the previous build, though, solving was so rare that random matches never solved at all."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The outcome depends on how well the Scientist encodes the solution and how well investigators decode it, read the Murderer's misdirection and time their badge use. Roles are dealt at random, but the teams are fixed by role, so luck has little effect on who wins within a match."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Hint encoding, reading the Murderer's misleading arguments and the Witness's need to guide without being spotted can all improve without limit. A weak investigator still contributes by voting sensibly."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "There is hidden state (the Murderer's identity and the solution cards) and hidden allegiance. Players must infer from ambiguous signals and plan when to spend their only badge."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The win follows from whether a named Clue and Means match the secret pair, and whether the Murderer's Witness guess is correct. No judge is needed, even though hints are interpreted semantically."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Several things break the platform's limits: eyes-closed setup, 30-second timed presentations, 6 tiles per round with replacements, 4 Clue and 4 Means cards for up to 11 players, and accusations at any moment. All of these need restructuring into polls. The previous variation also failed to build: the state contained blank bookkeeping fields, and `solved`, `solved_this_round`, `hunt_target` and `tile_catalog` were never changed in random play."
    }
  ],
  "problems": [
    "P1: Solving was practically unreachable in random play. Accusations were optional and there were many card combinations, so the 'solved' flag never changed in test matches, and nothing downstream of it ran either.",
    "P2: hunt_target was never written by any step, because the Witness Hunt step was missing.",
    "P3: tile_catalog was a stored attribute that never changed. It is really a fixed list of tiles.",
    "P4: solved_this_round was redundant bookkeeping that never flipped.",
    "P5: Internal fields (acc_clue, acc_means, intel, verdict, current_tile) were shown to players as blanks.",
    "P6: The original needs real-time features and a large setup: eyes-closed pointing, 30-second speeches, accusations at any moment, 6 tiles per round with replacements, and 4+4 cards per player.",
    "P7: The two-step accusation (name a seat, then a second poll for the cards) added a choice step and pushed the round past 4 choice steps once the Murderer's pick, the hint, the talk and the hunt were counted.",
    "P8: An Accomplice role plus a Witness plus the solution would mean too many hidden elements for the build limits."
  ],
  "changes": [
    {
      "what": "Each non-Scientist holds only 2 Clue and 2 Means cards. A single accusation poll offers 'pass' or one entry of the form 'Seat s: Clue x + Means y' for every other non-Scientist seat (about 12 options with 5 players). A player can never accuse their own seat.",
      "why": "This keeps the suspect-plus-cards deduction while making a hit reachable (1 in 12 at random). It also merges the two accusation polls into one.",
      "fixes": "P1"
    },
    {
      "what": "No accusations in round 1. In round 4, 'pass' is removed for every seat that still holds a badge. Each seat gets 2 badges.",
      "why": "Investigators see a first hint before guessing, and random play now solves often enough that 'solved' and the Witness Hunt actually run.",
      "fixes": "P1"
    },
    {
      "what": "Write an explicit Witness Hunt step. When solved = 1 and the game has a Witness, the Murderer names one seat, and the step writes that seat into hunt_target (initial value 'not run').",
      "why": "This gives every attribute a step that changes it.",
      "fixes": "P2"
    },
    {
      "what": "The tile schedule is a fixed rule (two named tiles per round, listed in the rules), not a stored attribute. Only the Scientist's chosen options are written, to current_hint.",
      "why": "This removes a field that never changes.",
      "fixes": "P3"
    },
    {
      "what": "Delete solved_this_round. The game ends in the same round that solved becomes 1, so 'solved = 1' alone triggers the Witness Hunt and the end.",
      "why": "This removes redundant state that never changed.",
      "fixes": "P4"
    },
    {
      "what": "Remove acc_clue, acc_means, intel and verdict. The only private bookkeeping left is 'accusation' (visibility none) and 'case_file' (visible only to the Scientist). Every field shown to players starts with a readable value: current_hint 'No tile yet', hunt_target 'not run', case_file 'not chosen'.",
      "why": "Players no longer see blank internal fields.",
      "fixes": "P5"
    },
    {
      "what": "Replace speeches and free accusations with one simultaneous message per round (the Scientist is silent) and one simultaneous accusation poll. The Murderer's eyes-closed point becomes a private poll in round 1. Each round has 2 fixed tiles marked by one Scientist choice, with no replacements.",
      "why": "This makes the game turn-based and text-only within the step limits.",
      "fixes": "P6"
    },
    {
      "what": "The accusation is a single poll. The Murderer's pick runs only in round 1, which has no accusation or hunt, so no round executes more than 4 choice steps.",
      "why": "This keeps each round within the choice-step limit.",
      "fixes": "P7"
    },
    {
      "what": "Drop the Accomplice. The Witness appears only with 5 or more players, and the Witness's knowledge is fixed at setup.",
      "why": "This keeps hidden elements to two: roles and the case file.",
      "fixes": "P8"
    }
  ],
  "keeps": [
    "A silent Forensic Scientist who knows the solution and can only communicate through Scene-tile markers.",
    "A secret Murderer who chooses their own Key Evidence and Means of Murder from their face-up cards and argues to mislead.",
    "Public Clue and Means cards in front of each player, with the solution being one Clue plus one Means belonging to the same player.",
    "Limited badges for accusations, where a wrong accusation wastes a badge.",
    "The Witness, who knows the Murderer, and the Witness Hunt that can steal the win after a correct solve.",
    "A team win: the Investigators and the Scientist against the Murderer side, with the Murderer winning if the case goes unsolved by the end."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction-and-deception core fits text play well once accusations are a single poll with a reachable solve rate and every state field is written by a step that runs."
  },
  "variation": {
    "name": "Deception: Case File",
    "summary": "Over 4 rounds, a silent Scientist marks two Scene tiles per round to point at the secret Murderer's chosen Clue and Means. Everyone else talks once per round, then may spend one of 2 badges to accuse a seat plus card pair. A correct accusation solves the case, but the Murderer can still win by unmasking the Witness.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP.\nSeat 1 is always the Forensic Scientist, and everyone knows this. Among seats 2..N, roles are dealt at random and secretly: 1 Murderer, 1 Witness (only if N >= 5), and the rest Investigators. Each player sees only their own role. The Witness is privately told the Murderer's seat number. The Scientist is not told who anyone is.\nShuffle the Clue list and the Means list. Deal each seat 2..N two Clues (labelled C1, C2) and two Means (labelled M1, M2). All cards are face up and public.\nClue list (16): Fingerprint, Lipstick, Train Ticket, Diary, Wine Bottle, Hair Strand, Muddy Boots, Receipt, Cigarette Butt, Glove, Necklace, Photograph, Key, Letter, Wedding Ring, Map.\nMeans list (16): Knife, Poison, Rope, Pistol, Brick, Drowning, Electric Shock, Fire, Pillow, Push from Height, Car Crash, Injection, Axe, Strangling Scarf, Sleeping Pills, Bare Hands.\nEach seat 2..N starts with 2 badges, which are public.\n\nFIXED TILE SCHEDULE (rule constants). Each tile has 4 options:\n- Round 1: Cause of Death (Suffocation / Severe Injury / Loss of Blood / Poisoning or Illness) and Location of Crime (Home / Outdoors / Public Venue / Workplace).\n- Round 2: Victim's Expression (Calm / Terrified / Angry / Confused) and Trace at the Scene (Fingermarks / Footprints / Bruises / Nothing Visible).\n- Round 3: Murderer's Personality (Cold / Greedy / Jealous / Desperate) and Time of Death (Morning / Afternoon / Evening / Night).\n- Round 4: Hint on Corpse (Head / Chest / Hands / Legs) and Duration of Crime (Instant / Minutes / An Hour / Long Planned).\n\nEACH ROUND r = 1..4, in this order:\n1. (Round 1 only) Murderer's pick, private poll. The Murderer chooses one of C1+M1, C1+M2, C2+M1, C2+M2 from their own cards. The result is written to the Scientist's private case_file as 'Seat s: Cx + My', visible only to the Scientist.\n2. Scientist's hint, private poll. The Scientist picks one option on each of this round's two tiles (16 combined choices).\n3. Announce. current_hint is set to the two chosen options and shown to all.\n4. Talk. Every seat except the Scientist writes one short message at the same time. All messages are then shown together. The Scientist never speaks.\n5. Accusation poll (rounds 2-4 only, simultaneous, for seats with at least 1 badge). Each such seat chooses 'pass' or one accusation 'Seat s: Cx + My', where s is any seat 2..N other than their own. In round 4, 'pass' is not offered. Choices are stored privately until resolved.\n6. Resolution. If any accusation equals the case_file, set solved = 1. Every seat that did not pass loses 1 badge. All accusations made are then revealed.\n7. Witness Hunt (only if solved = 1 and a Witness exists). The Murderer chooses one seat other than themselves and seat 1. That seat is written to hunt_target.\n8. End check. The game ends if solved = 1, or if r = 4.\n\nThe case_file, all roles and hunt_target are revealed at the end.",
    "objective": "Team win, decided by arithmetic on the tracked values.\n- If solved = 1 and either there is no Witness or hunt_target is not the Witness's seat, the Scientist and all Investigators and the Witness win, and the Murderer loses.\n- If solved = 1 and hunt_target is the Witness's seat, the Murderer wins and everyone else loses.\n- If the game ends after round 4 with solved = 0, the Murderer wins and everyone else loses.\nThere are no draws.",
    "expected_effect": "Solving is now reachable: the forced round-4 accusation and the 1-in-12 option set mean random play solves in a meaningful share of matches, so solved, hunt_target and the end-of-game paths all run. Strong play turns on the Scientist encoding a suspect and a card pair through 8 tile choices, and on investigators decoding them while discounting the Murderer.\n\nTalk passes both tests. Players genuinely disagree: the Murderer wants the table to settle on a wrong seat or card pair, and to waste badges. The Witness wants a correct solve but loses if the Murderer spots them. A player who simply follows a confident proposal can be led by the hidden Murderer into burning a badge, or into a forced wrong accusation in round 4.\n\nTalk is simultaneous, so nobody can just echo the first speaker. The Witness must hint subtly, which creates a real trade-off. There are 2 badges per seat, but each wrong accusation costs one, so timing matters. Outcomes should land near even between the teams; seat 1's results simply track the Investigator side."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 4
  }
}
```
````
