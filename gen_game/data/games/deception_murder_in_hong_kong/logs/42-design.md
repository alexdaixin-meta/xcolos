# 42 design

- time: 2026-10-28T02:57:10+00:00 (130.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4c4948b7457afe5e, reply sha256 b53126e51c17e787

## Sent

````
Original game: Deception: Murder in Hong Kong
Players in the original: 4 to 12

Original rules:
Players get secret roles: 1 Forensic Scientist, 1 Murderer, optional Accomplice and Witness, rest Investigators. Each non-scientist has 4 Clue and 4 Means cards displayed outward. Secretly, with eyes closed, Murderer points to one of their own Clue as Key Evidence and one Means as Means of Murder; Accomplice and Witness learn identities via the Scientist. Then for three rounds Scientist reveals 6 Scene tiles and places bullet markers on one item per tile as clues to the solution, possibly replacing one tile each round after the first. Between markers players discuss publicly and in turn present their guess for 30 seconds. Any player may spend their badge to attempt to solve by naming one Clue and one Means on the table. If correct, Investigators and Scientist win, unless Witness rule triggers: if Murderer was identified but then correctly names Witness, Murderer side wins. Otherwise after third presentation if never solved correctly, Murderer side wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: Work out play when everyone plays well. The Scientist hints well, and Investigators split coverage in talk. After the Round 1 hints (Cause of Death narrows the Means; the second tile partly narrows the Clue) and the revealed wrong accusations, 10 guesses over the remaining plausible candidates at N=8 (4 at N=5) solve the case most of the time without any help from the Witness.

The Witness therefore plays best by saying nothing useful, never accusing the murderer's seat, and making a deliberately wrong forced accusation in round 4. In that case the Witness is indistinguishable from an Investigator. The Murderer's hunt becomes a uniform guess among N-2 seats, a hidden-type lottery:
- N=5: 33%
- N=6: 25%
- N=7: 20%
- N=8: 17%

In solved games under good play, then, the winner is decided by whether an uninformed guess hits a randomly dealt role. That fails the 'all play well' test.

The second chance source is the card deal. Some Clue/Means pairs map poorly onto the tiles; for example, Location of Crime and Time of Death say little about Receipt or Map. Rough estimate: 30-40% of outcomes are chance.

There is real inference: reading hints, spotting the Murderer's talk, and pruning with revealed accusations. But the brute-force badge budget makes the Witness's private knowledge unnecessary, and that is exactly what turns the hunt into a coin toss.
- change: Cut blind coverage so the Investigators need the Witness's information. Options:
- give each seat 1 badge instead of 2; or
- use a shared team pool of N-3 badges (minimum 2), spent one per accusation.
This drops blind coverage to about 10-18% (e.g. 5/28 at N=8). Solving then usually needs signals from the Witness, and those signals give the Murderer real evidence for the hunt.
- change: Make the Witness Hunt informed rather than a lottery. Before the hunt, publicly reveal which seat or seats made the correct accusation. Also allow an option that grows with information, e.g. the Murderer also wins if they correctly name the Witness *and* the Witness's talk is cited. The simplest arithmetic fix is to let the Murderer name 2 seats at N>=7 and 1 seat otherwise, but only if the badge change above holds, so the Witness must leak to win.
- change: Reduce deal luck. Either let the Scientist replace one tile per round from a fixed list of 4 alternative tiles (one option-set choice, all arithmetic), or require each dealt Clue and Means to be tagged with matching tile options in a public lookup list, so every case file is hintable.
The variation that was reviewed: Deception: Case File: SETUP (done once, before round 1)

S1. Roles. Seat 1 is always the Forensic Scientist, and everyone knows this. Among seats 2..N, roles are dealt at random and secretly:
- 1 Murderer;
- 1 Witness (only if N >= 5);
- the rest Investigators.
Each player sees only their own role. The Witness is privately told the Murderer's seat number. The Scientist is not told anyone's role.

S2. Cards. Shuffle the Clue list and the Means list. Deal each seat 2..N two Clues (labelled C1, C2) and two Means (labelled M1, M2). All cards are face up and public.
- Clue list (16): Fingerprint, Lipstick, Train Ticket, Diary, Wine Bottle, Hair Strand, Muddy Boots, Receipt, Cigarette Butt, Glove, Necklace, Photograph, Key, Letter, Wedding Ring, Map.
- Means list (16): Knife, Poison, Rope, Pistol, Brick, Drowning, Electric Shock, Fire, Pillow, Push from Height, Car Crash, Injection, Axe, Strangling Scarf, Sleeping Pills, Bare Hands.

S3. Badges. Each seat 2..N starts with 2 badges. Badge counts are public. Set solved = 0 and hunt_target = 0.

S4. Murderer's pick (private poll, once). The Murderer chooses one of C1+M1, C1+M2, C2+M1 or C2+M2 from their own cards. The result is written to the case_file as 'Seat s: Cx + My'. Only the Scientist can see the case_file.

FIXED TILE SCHEDULE (rule constants). Each tile has 4 options.
- Round 1: Cause of Death (Suffocation / Severe Injury / Loss of Blood / Poisoning or Illness) and Location of Crime (Home / Outdoors / Public Venue / Workplace).
- Round 2: Victim's Expression (Calm / Terrified / Angry / Confused) and Trace at the Scene (Fingermarks / Footprints / Bruises / Nothing Visible).
- Round 3: Murderer's Personality (Cold / Greedy / Jealous / Desperate) and Time of Death (Morning / Afternoon / Evening / Night).
- Round 4: Hint on Corpse (Head / Chest / Hands / Legs) and Duration of Crime (Instant / Minutes / An Hour / Long Planned).

EACH ROUND r = 1..4, in this order:

1. Scientist's hint (private poll). The Scientist picks one option on each of this round's two tiles, for 16 combined choices.

2. Announce. current_hint is set to the two chosen options and shown to everyone.

3. Talk. Every seat except the Scientist writes one short message at the same time. All messages are then shown together. The Scientist never speaks.

4. Accusation poll. This happens in rounds 2-4 only and is simultaneous. It is open to every seat 2..N with at least 1 badge.
- Each such seat chooses either 'pass' or one accusation 'Seat s: Cx + My', where s is any seat 2..N other than their own.
- In round 4, 'pass' is not offered.
- Choices stay hidden until resolution.

5. Resolution (rounds 2-4).
- If any accusation equals the case_file, set solved = 1.
- Every seat that did not pass loses 1 badge.
- All accusations made are then revealed.

6. Witness Hunt (private poll). This happens only if solved = 1 and a Witness exists. The Murderer chooses one seat that is neither themselves nor seat 1. That seat is written to hunt_target.

7. End check. The game ends if solved = 1 or r = 4. Otherwise the next round begins.

At the end, the case_file, all roles and hunt_target are revealed. Winner: The game is a team win, decided by arithmetic on the tracked values.
- If solved = 1 and either there is no Witness or hunt_target is not the Witness's seat: the Scientist, all Investigators and the Witness win, and the Murderer loses.
- If solved = 1 and hunt_target equals the Witness's seat: the Murderer wins and everyone else loses.
- If the game ends after round 4 with solved = 0: the Murderer wins and everyone else loses.
There are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Deception: Murder in Hong Kong is a hidden-role deduction game. A silent Forensic Scientist knows which Clue and Means card the secret Murderer chose, and gives coded hints on scene tiles. Investigators discuss and spend badges to name the pair, while the Murderer misdirects, and an optional Witness, who knows the Murderer, must not be exposed or the Murderer wins anyway. The variation reviewed here is the previous XColos adaptation ('Case File'), with fixed tiles, 2 badges per seat and a single Witness hunt.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Seats have no built-in edge: seat 1 is always the Scientist and all other roles are random. Each simple policy can lose. 'Always pass' hands the Murderer the win, and 'Witness names the murderer at once' gets hunted. But the best play for the Witness collapses to 'stay silent and look like an Investigator', because 2 badges per seat (up to 14 accusations at N=8) can brute-force the remaining candidates without the Witness. The Witness's private knowledge, the central choice of the original, then changes nothing."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The testers estimated 30-40% of outcomes are chance. Under good play the Murderer's hunt is a uniform guess among N-2 seats: 33% at N=5 and 17% at N=8. The free-form tiles also map unevenly onto some cards. For example, Location of Crime and Time of Death say little about a Receipt or a Map, so some case files are barely hintable whatever the Scientist does."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "The Investigators' side is close to solved: hint plus blanket coverage. The Witness side has no headroom, since the right play is to do nothing. The Murderer's skill is capped by a hunt that has no evidence to work with."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "There is real inference: reading hints, pruning with the wrong accusations that get revealed, and spotting the Murderer's talk. But the information-rich parts (the Witness's knowledge and the Murderer's reading of who leaked) are made pointless by the badge budget. The hint reading itself depends on loose meanings rather than on a public structure that can be worked out."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The 'solved' flag compares an accusation string with the case file, the hunt compares seat numbers, and the team outcome follows by arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is turn-based text with simultaneous talk and polls, a flat step list, 4 rounds and no board. It fits the limits. The free-text accusation format is the only fragile point."
    }
  ],
  "problems": [
    "P1 Brute-force coverage: 2 badges per seat lets Investigators cover all plausible candidates without the Witness, so the Witness's private knowledge is unnecessary.",
    "P2 Lottery hunt: because the Witness plays best by staying invisible, the Murderer's hunt is an uninformed guess among N-2 seats, and in solved games the winner is decided by the role deal.",
    "P3 Deal luck in hints: the tiles have no defined link to the cards, so some dealt Clue/Means pairs can hardly be hinted, and solvability depends on the deal rather than on play.",
    "P4 Uncoordinated accusations: independent simultaneous accusations by every seat reward spreading guesses blindly rather than agreeing a case through talk. They also give the Murderer no vote to sway and the table no record of who backed what."
  ],
  "changes": [
    {
      "what": "Replace per-seat badges with a small shared team pool: 1 test at N=5-6, 2 tests at N=7-8. At most one accusation is tested per round, chosen by a public vote.",
      "why": "After the two hints there are about 3-4 plausible candidates at N=5 and about 5-6 at N=8. With these pool sizes blind solving drops to roughly 30-40%, so the team usually needs the Witness's steer to win reliably.",
      "fixes": "P1 Brute-force coverage"
    },
    {
      "what": "Accusations become a simultaneous vote. Each seat 2..N votes for one accusation or passes. The accusation with the most votes, needing at least 2, is tested and costs 1 from the pool. Ties go to the tied accusation backed by the lowest-numbered seat. Every vote is revealed afterwards.",
      "why": "The table has to converge through talk. The Murderer can try to split the vote. Who backed the correct accusation first, and when, becomes public evidence.",
      "fixes": "P4 Uncoordinated accusations"
    },
    {
      "what": "The Witness hunt uses the public record: all talk messages and all revealed votes. The Murderer names 1 seat at N=5-6 and 2 seats at N=7-8.",
      "why": "A Witness who wants the case solved must steer talk or votes, which leaves traces. Investigators can provide cover by backing candidates and voting with the table. The hunt becomes an inference about who knew too early, not a lottery.",
      "fixes": "P2 Lottery hunt"
    },
    {
      "what": "Every Means and Clue card carries a fixed public tag: exactly 2 of the 4 options on its tile. The tags are given in a lookup table, and each option appears on exactly 8 of the 16 cards. There are two hint tiles: Cause of Death for Means and Location for Clues.",
      "why": "Every case file can be hinted to the same degree. Pruning is exact arithmetic over a public table. The Scientist reasons about which of the two true options removes more decoys, and the Murderer reasons about which of their four combos is hardest to isolate.",
      "fixes": "P3 Deal luck in hints"
    },
    {
      "what": "The game is cut to 3 rounds. Round 1 has the Means hint and talk. Round 2 has the Clue hint, talk and a vote. Round 3 has talk and a final vote.",
      "why": "With exact tags, 2 hints are enough to narrow the case without solving it. A third hint would let hints alone finish the job and push out the Witness again. The extra talk-and-vote round lets the Witness react to a failed test.",
      "fixes": "P1 Brute-force coverage"
    }
  ],
  "keeps": [
    "A silent Forensic Scientist who knows the solution and can only hint through scene tiles.",
    "A hidden Murderer who chooses their own Clue+Means combination and misdirects in open discussion.",
    "A Witness who knows the Murderer and must help without being exposed; the Murderer still wins by naming the Witness after being caught.",
    "Accusations naming one Clue and one Means, a limited budget for them, and the Murderer winning if the case goes unsolved.",
    "The same Clue and Means card lists and the Cause of Death and Location of Crime tiles."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core tension of the Witness (leak enough to solve, not enough to be found) survives once blind coverage is scarce, hints are exact over a public table, and the hunt reads a public vote record. All of this fits in 3 rounds and about 10 steps."
  },
  "variation": {
    "name": "Deception: Tagged Case File",
    "summary": "A team hidden-role deduction game for 5-8 players. A silent Scientist gives two exact hints over a public tag table. The table votes on at most 1-2 accusations, so a secret Witness must steer the vote, and a caught Murderer can still win by reading the talk and vote record to find the Witness.",
    "players": {
      "min": 5,
      "max": 8,
      "suggested": 7
    },
    "rules": "SETUP (once, before round 1)\nS1. Roles. Seat 1 is always the Forensic Scientist, and everyone knows this. Among seats 2..N, roles are dealt at random and in secret: 1 Murderer, 1 Witness, and the rest Investigators. Each player sees only their own role. The Witness is privately told the Murderer's seat number. The Scientist is not told any roles.\n\nS2. Cards. Shuffle the 16 Clues and the 16 Means. Deal each seat 2..N two Clues (labelled C1, C2) and two Means (labelled M1, M2). All dealt cards are public.\n\nS3. Public tag table. Each card has exactly two tags on its tile.\nCause of Death options are Breathing, Blunt, Bleeding and Chemical. Means tags:\n- Breathing+Blunt: Rope, Bare Hands, Pillow.\n- Breathing+Bleeding: Knife, Axe, Strangling Scarf.\n- Breathing+Chemical: Drowning, Fire.\n- Blunt+Bleeding: Brick, Push from Height.\n- Blunt+Chemical: Electric Shock, Car Crash, Sleeping Pills.\n- Bleeding+Chemical: Poison, Injection, Pistol.\nLocation options are Home, Outdoors, Public Venue and Workplace. Clue tags:\n- Home+Outdoors: Muddy Boots, Glove, Key.\n- Home+Public Venue: Lipstick, Wine Bottle, Necklace.\n- Home+Workplace: Diary, Photograph.\n- Outdoors+Public Venue: Train Ticket, Map.\n- Outdoors+Workplace: Cigarette Butt, Fingerprint, Hair Strand.\n- Public Venue+Workplace: Receipt, Letter, Wedding Ring.\nA card is consistent with a hint if the hinted option is one of its two tags.\n\nS4. Counters. The team pool is 1 at N=5-6 and 2 at N=7-8, and it is public. solved = 0. The hunt list is empty.\n\nS5. Murderer's pick (private poll, once). The Murderer chooses one of C1+M1, C1+M2, C2+M1 or C2+M2 from their own cards. It is recorded as the case file 'Seat s: Cx + My'. Only the Scientist sees the case file.\n\nEACH ROUND r = 1..3, in this order:\n1. Scientist's hint (private poll; rounds 1 and 2 only). In round 1 the Scientist picks one Cause of Death option. In round 2 the Scientist picks one Location option. The Scientist may pick any option but is on the Investigators' team.\n2. Announce. The hint is shown to everyone.\n3. Talk. Every seat 2..N writes one short message at the same time, without seeing the others. All messages are then shown together. The Scientist never speaks.\n4. Accusation vote (rounds 2 and 3 only; only if the pool is at least 1). Every seat 2..N votes at the same time, either 'pass' or one accusation 'Seat s: Cx + My'. s may be any seat 2..N, including the voter's own seat, and Cx and My must be cards held by seat s.\n5. Test. Among non-pass votes, find the accusation with the most votes. If it has at least 2 votes, it is tested and the pool falls by 1. If several accusations are tied for most votes, test the one voted for by the lowest-numbered seat among those tied. If the tested accusation equals the case file, set solved = 1.\n6. Reveal. Every seat's vote, and whether the tested accusation was correct, are shown to everyone.\n7. Witness hunt (private poll; only if solved = 1). The Murderer names seats that are neither themselves nor seat 1: 1 seat at N=5-6, 2 different seats at N=7-8. The named seats are recorded in the hunt list.\n8. End check. The game ends if solved = 1, or r = 3, or the pool is 0 after a test. Otherwise the next round begins.\n\nAt the end, the case file, all roles and the hunt list are revealed.",
    "objective": "It is a team win, decided by arithmetic. If solved = 1 and the Witness's seat is not in the hunt list, the Scientist, all Investigators and the Witness win. If solved = 1 and the Witness's seat is in the hunt list, the Murderer wins alone. If the game ends with solved = 0, the Murderer wins alone. There are no draws.",
    "expected_effect": "After the two exact hints, about 3-4 combos remain consistent at N=5 and about 5-6 at N=8. With only 1-2 tests, the Investigators win blind only about 30-40% of the time, so they need the Witness's knowledge of the seat.\n\nThe Witness faces a real trade-off. Steering hard almost guarantees a solve but leaves an early, confident trail in talk and votes. Staying silent leaves the team at blind odds.\n\nInvestigators can protect the Witness by floating candidates and joining the winning vote. The Murderer can pose as the Witness to split or hijack the vote, so following the loudest proposal can waste the only test.\n\nThe Murderer's hunt becomes evidence-based: who first argued for the correct seat, who changed vote after a failed test. The Murderer's initial pick and the Scientist's choice between two true options each reward working through the public tag table.\n\nTalk passes both tests. The Murderer and the team want opposite outcomes. The Witness and the Investigators agree on solving but disagree about who should take the risk of revealing knowledge. A player who just follows the first proposal can lose by spending the pool on the Murderer's decoy or by exposing the Witness."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 3
  }
}
```
````
