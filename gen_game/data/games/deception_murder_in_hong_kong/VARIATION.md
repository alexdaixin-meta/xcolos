# Variation: Deception: Tagged Case File

A team hidden-role deduction game for 5-8 players. A silent Scientist gives two exact hints over a public tag table. The table votes on at most 1-2 accusations, so a secret Witness must steer the vote, and a caught Murderer can still win by reading the talk and vote record to find the Witness.

Players: 5 to 8, best with 7

## Review of the original

Deception: Murder in Hong Kong is a hidden-role deduction game. A silent Forensic Scientist knows which Clue and Means card the secret Murderer chose, and gives coded hints on scene tiles. Investigators discuss and spend badges to name the pair, while the Murderer misdirects, and an optional Witness, who knows the Murderer, must not be exposed or the Murderer wins anyway. The variation reviewed here is the previous XColos adaptation ('Case File'), with fixed tiles, 2 badges per seat and a single Witness hunt.

- **non_degenerate**: weak. Seats have no built-in edge: seat 1 is always the Scientist and all other roles are random. Each simple policy can lose. 'Always pass' hands the Murderer the win, and 'Witness names the murderer at once' gets hunted. But the best play for the Witness collapses to 'stay silent and look like an Investigator', because 2 badges per seat (up to 14 accusations at N=8) can brute-force the remaining candidates without the Witness. The Witness's private knowledge, the central choice of the original, then changes nothing.
- **skill_sensitive**: weak. The testers estimated 30-40% of outcomes are chance. Under good play the Murderer's hunt is a uniform guess among N-2 seats: 33% at N=5 and 17% at N=8. The free-form tiles also map unevenly onto some cards. For example, Location of Crime and Time of Death say little about a Receipt or a Map, so some case files are barely hintable whatever the Scientist does.
- **headroom**: weak. The Investigators' side is close to solved: hint plus blanket coverage. The Witness side has no headroom, since the right play is to do nothing. The Murderer's skill is capped by a hunt that has no evidence to work with.
- **reasoning_dependent**: weak. There is real inference: reading hints, pruning with the wrong accusations that get revealed, and spotting the Murderer's talk. But the information-rich parts (the Witness's knowledge and the Murderer's reading of who leaked) are made pointless by the badge budget. The hint reading itself depends on loose meanings rather than on a public structure that can be worked out.
- **verifiable**: good. The 'solved' flag compares an accusation string with the case file, the hunt compares seat numbers, and the team outcome follows by arithmetic. No judge is needed.
- **fits_platform**: good. It is turn-based text with simultaneous talk and polls, a flat step list, 4 rounds and no board. It fits the limits. The free-text accusation format is the only fragile point.

## Problems

- P1 Brute-force coverage: 2 badges per seat lets Investigators cover all plausible candidates without the Witness, so the Witness's private knowledge is unnecessary.
- P2 Lottery hunt: because the Witness plays best by staying invisible, the Murderer's hunt is an uninformed guess among N-2 seats, and in solved games the winner is decided by the role deal.
- P3 Deal luck in hints: the tiles have no defined link to the cards, so some dealt Clue/Means pairs can hardly be hinted, and solvability depends on the deal rather than on play.
- P4 Uncoordinated accusations: independent simultaneous accusations by every seat reward spreading guesses blindly rather than agreeing a case through talk. They also give the Murderer no vote to sway and the table no record of who backed what.

## Changes

- Replace per-seat badges with a small shared team pool: 1 test at N=5-6, 2 tests at N=7-8. At most one accusation is tested per round, chosen by a public vote. (fixes: P1 Brute-force coverage): After the two hints there are about 3-4 plausible candidates at N=5 and about 5-6 at N=8. With these pool sizes blind solving drops to roughly 30-40%, so the team usually needs the Witness's steer to win reliably.
- Accusations become a simultaneous vote. Each seat 2..N votes for one accusation or passes. The accusation with the most votes, needing at least 2, is tested and costs 1 from the pool. Ties go to the tied accusation backed by the lowest-numbered seat. Every vote is revealed afterwards. (fixes: P4 Uncoordinated accusations): The table has to converge through talk. The Murderer can try to split the vote. Who backed the correct accusation first, and when, becomes public evidence.
- The Witness hunt uses the public record: all talk messages and all revealed votes. The Murderer names 1 seat at N=5-6 and 2 seats at N=7-8. (fixes: P2 Lottery hunt): A Witness who wants the case solved must steer talk or votes, which leaves traces. Investigators can provide cover by backing candidates and voting with the table. The hunt becomes an inference about who knew too early, not a lottery.
- Every Means and Clue card carries a fixed public tag: exactly 2 of the 4 options on its tile. The tags are given in a lookup table, and each option appears on exactly 8 of the 16 cards. There are two hint tiles: Cause of Death for Means and Location for Clues. (fixes: P3 Deal luck in hints): Every case file can be hinted to the same degree. Pruning is exact arithmetic over a public table. The Scientist reasons about which of the two true options removes more decoys, and the Murderer reasons about which of their four combos is hardest to isolate.
- The game is cut to 3 rounds. Round 1 has the Means hint and talk. Round 2 has the Clue hint, talk and a vote. Round 3 has talk and a final vote. (fixes: P1 Brute-force coverage): With exact tags, 2 hints are enough to narrow the case without solving it. A third hint would let hints alone finish the job and push out the Witness again. The extra talk-and-vote round lets the Witness react to a failed test.

## Kept from the original

- A silent Forensic Scientist who knows the solution and can only hint through scene tiles.
- A hidden Murderer who chooses their own Clue+Means combination and misdirects in open discussion.
- A Witness who knows the Murderer and must help without being exposed; the Murderer still wins by naming the Witness after being caught.
- Accusations naming one Clue and one Means, a limited budget for them, and the Murderer winning if the case goes unsolved.
- The same Clue and Means card lists and the Cause of Death and Location of Crime tiles.

## The variation's rules

SETUP (once, before round 1)
S1. Roles. Seat 1 is always the Forensic Scientist, and everyone knows this. Among seats 2..N, roles are dealt at random and in secret: 1 Murderer, 1 Witness, and the rest Investigators. Each player sees only their own role. The Witness is privately told the Murderer's seat number. The Scientist is not told any roles.

S2. Cards. Shuffle the 16 Clues and the 16 Means. Deal each seat 2..N two Clues (labelled C1, C2) and two Means (labelled M1, M2). All dealt cards are public.

S3. Public tag table. Each card has exactly two tags on its tile.
Cause of Death options are Breathing, Blunt, Bleeding and Chemical. Means tags:
- Breathing+Blunt: Rope, Bare Hands, Pillow.
- Breathing+Bleeding: Knife, Axe, Strangling Scarf.
- Breathing+Chemical: Drowning, Fire.
- Blunt+Bleeding: Brick, Push from Height.
- Blunt+Chemical: Electric Shock, Car Crash, Sleeping Pills.
- Bleeding+Chemical: Poison, Injection, Pistol.
Location options are Home, Outdoors, Public Venue and Workplace. Clue tags:
- Home+Outdoors: Muddy Boots, Glove, Key.
- Home+Public Venue: Lipstick, Wine Bottle, Necklace.
- Home+Workplace: Diary, Photograph.
- Outdoors+Public Venue: Train Ticket, Map.
- Outdoors+Workplace: Cigarette Butt, Fingerprint, Hair Strand.
- Public Venue+Workplace: Receipt, Letter, Wedding Ring.
A card is consistent with a hint if the hinted option is one of its two tags.

S4. Counters. The team pool is 1 at N=5-6 and 2 at N=7-8, and it is public. solved = 0. The hunt list is empty.

S5. Murderer's pick (private poll, once). The Murderer chooses one of C1+M1, C1+M2, C2+M1 or C2+M2 from their own cards. It is recorded as the case file 'Seat s: Cx + My'. Only the Scientist sees the case file.

EACH ROUND r = 1..3, in this order:
1. Scientist's hint (private poll; rounds 1 and 2 only). In round 1 the Scientist picks one Cause of Death option. In round 2 the Scientist picks one Location option. The Scientist may pick any option but is on the Investigators' team.
2. Announce. The hint is shown to everyone.
3. Talk. Every seat 2..N writes one short message at the same time, without seeing the others. All messages are then shown together. The Scientist never speaks.
4. Accusation vote (rounds 2 and 3 only; only if the pool is at least 1). Every seat 2..N votes at the same time, either 'pass' or one accusation 'Seat s: Cx + My'. s may be any seat 2..N, including the voter's own seat, and Cx and My must be cards held by seat s.
5. Test. Among non-pass votes, find the accusation with the most votes. If it has at least 2 votes, it is tested and the pool falls by 1. If several accusations are tied for most votes, test the one voted for by the lowest-numbered seat among those tied. If the tested accusation equals the case file, set solved = 1.
6. Reveal. Every seat's vote, and whether the tested accusation was correct, are shown to everyone.
7. Witness hunt (private poll; only if solved = 1). The Murderer names seats that are neither themselves nor seat 1: 1 seat at N=5-6, 2 different seats at N=7-8. The named seats are recorded in the hunt list.
8. End check. The game ends if solved = 1, or r = 3, or the pool is 0 after a test. Otherwise the next round begins.

At the end, the case file, all roles and the hunt list are revealed.

Objective: It is a team win, decided by arithmetic. If solved = 1 and the Witness's seat is not in the hunt list, the Scientist, all Investigators and the Witness win. If solved = 1 and the Witness's seat is in the hunt list, the Murderer wins alone. If the game ends with solved = 0, the Murderer wins alone. There are no draws.

Expected effect: After the two exact hints, about 3-4 combos remain consistent at N=5 and about 5-6 at N=8. With only 1-2 tests, the Investigators win blind only about 30-40% of the time, so they need the Witness's knowledge of the seat.

The Witness faces a real trade-off. Steering hard almost guarantees a solve but leaves an early, confident trail in talk and votes. Staying silent leaves the team at blind odds.

Investigators can protect the Witness by floating candidates and joining the winning vote. The Murderer can pose as the Witness to split or hijack the vote, so following the loudest proposal can waste the only test.

The Murderer's hunt becomes evidence-based: who first argued for the correct seat, who changed vote after a failed test. The Murderer's initial pick and the Scientist's choice between two true options each reward working through the public tag table.

Talk passes both tests. The Murderer and the team want opposite outcomes. The Witness and the Investigators agree on solving but disagree about who should take the risk of revealing knowledge. A player who just follows the first proposal can lose by spending the pool on the Murderer's decoy or by exposing the Witness.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 3 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
