# Variation: Don't Cut Cthulhu: Counted Hands

There are 5-6 players: 2 known-to-each-other Cultists against 3-4 Investigators. Each player knows only the counts in their own hand. Players talk, then the active player names another player, and one of that player's face-down cards is revealed at random. Investigators need N Signs out of N+1 within 2N cuts. Cultists win on Cthulhu or the timer.

Players: 5 to 6, best with 5

## Review of the original

Don't Mess With Cthulhu is a hidden-team bluffing game. Investigators try to reveal enough Elder Signs from other players' face-down cards before Cthulhu is revealed or time runs out. Cultists win if Cthulhu is revealed or the rounds expire. Players know their own card counts but not the positions, and they may lie about them.

- **non_degenerate**: bad. In the reviewed variation the timer was dead. The limit of 4N cuts against N Signs needed left a slack of 3N, so Cultists effectively won only through a Cthulhu reveal. Owners knew their exact positions, so an Investigator holding Cthulhu simply never let it be cut. A thoughtless Investigator policy wins about 80% when an Investigator holds Cthulhu: tell the truth except about Cthulhu, and cut claimed Signs of anyone not yet caught lying. The 4-player deal also produced 1 or 2 Cultists at random.
- **skill_sensitive**: weak. Where Cthulhu was dealt largely decided the game. If an Investigator held it (50-75% of deals), Investigators won about 80% with near-mechanical play. Only Cultist-held Cthulhu deals turned on reading claims. Chance explained most of the outcome variance.
- **headroom**: weak. In most deals the Investigator line was close to solved: cut claimed Signs and pass control among trusted players. Cultists had little to do but blind stabs at about 1/13 per turn.
- **reasoning_dependent**: weak. Hidden roles and lying are present. However, exact position knowledge removed the risk from Investigators' own Cthulhu, and with N+2 Signs Investigators rarely had to probe suspected Cultist hands, so inference was optional in most deals.
- **verifiable**: good. The winner follows from counting: a Cthulhu reveal, Signs revealed reaching the target, or cuts reaching the limit. No judge is needed.
- **fits_platform**: good. The game is turn-based and text-only, with simultaneous talk, sequential cuts and arithmetic win checks. It has no board and is short.

## Problems

- P1 Dead timer: a cut limit of 4N against N Signs needed never threatens Investigators, so wasting cuts costs nothing and Cultists win only by revealing Cthulhu.
- P2 Cthulhu lottery: owners know exact positions, so an Investigator-held Cthulhu is never at risk. Whoever is dealt Cthulhu decides most games.
- P3 4-player role lottery: the set-aside token makes some games 3 Investigators against a lone, hopeless Cultist.
- P4 Cultists cannot coordinate: they don't know each other, so their only line is blind stabbing.
- P5 Too many Signs: with N+2 Signs, Investigators can usually win from their own hands and never need to judge whether to risk a suspected Cultist hand.
- P6 Telling Cultists who each other are (needed for P4) opens a ping-pong exploit. Two Cultists could cut each other forever, keeping control and stabbing at a Cultist-held Cthulhu every turn.

## Changes

- Set the cut limit to 2N: 10 cuts at 5 players, 12 at 6, against N Signs needed. (fixes: P1 Dead timer): Every cut now matters. Cultist time-wasting and Investigator 'safe' Futile passes are real costs, and Investigators need about a 50% Sign rate on their cuts.
- Owners are told only how many Signs, Futile cards and Cthulhu (0 or 1) they hold, never which card is where. A cut names a player, and one of that player's face-down cards is revealed at random. (fixes: P2 Cthulhu lottery): Cthulhu can be revealed from any hand that holds it, including an Investigator's. A known Cthulhu hand becomes a risky store of Signs that someone may have to dig into. Where Cthulhu is dealt changes what is safe, not who wins.
- Play only at 5 or 6 players, always with exactly 2 Cultists (3 v 2 or 4 v 2). (fixes: P3 4-player role lottery): This removes the random team size and the 1-v-3 deals.
- The Cultists learn each other's identity at setup. Each round they may exchange one private message each. (fixes: P4 Cultists cannot coordinate): Cultists can share counts, coordinate bait claims and false Cthulhu claims, and plan their stabs.
- Set the Elder Signs to N+1 (6 or 7), so the target is all Signs but one. (fixes: P5 Too many Signs): Any Sign held by a Cultist, or by the Cthulhu holder, quickly becomes necessary. Investigators must weigh claims and risk suspect hands.
- No-return rule: you may not cut the player who made the cut that made you active. (fixes: P6 Cultist ping-pong): This breaks Cultist ping-pong, so each Cultist possession gives one stab before control returns to an Investigator. Investigators can still rotate among themselves (I1, I2, I3, I1) unless one of their hands is unsafe.

## Kept from the original

- Hidden Investigator and Cultist teams, dealt face down.
- Elder Signs, Futile cards and a single Cthulhu dealt face down. Owners know counts but not positions.
- Lying about your own cards is allowed and expected.
- The player whose card was revealed becomes the next active player.
- Cthulhu wins instantly for the Cultists, enough Signs win instantly for the Investigators, and Cultists win if time runs out.

## The variation's rules

SETUP.
1. Roles. With 5 players deal 3 Investigator and 2 Cultist roles at random; with 6 players deal 4 Investigators and 2 Cultists. Each player privately learns their own role. Each Cultist is also told privately who the other Cultist is.
2. Deck. Each player gets 5 cards. The deck holds Elder Signs equal to players + 1, exactly 1 Cthulhu, and Futile cards for the rest. At 5 players that is 6 Signs, 1 Cthulhu and 18 Futile (25 cards). At 6 players it is 7 Signs, 1 Cthulhu and 22 Futile (30 cards). Shuffle and deal 5 face down to each player.
3. Private knowledge. Each player is told privately only HOW MANY Signs, Futile cards and Cthulhu (0 or 1) they hold. Nobody, including the owner, knows which face-down card is which.
4. Public information, always visible: each player's number of face-down cards; every revealed card and its owner; Signs revealed; cuts made; the target (Signs needed = number of players: 5 or 6); the cut limit (2 x players: 10 or 12); the active player; and the 'last cutter' (the player who made the previous cut, none at the start).
5. Player 1 starts as the active player. Roles are random, so this favours no team.

EACH ROUND (one cut).
1. Talk. Every player writes one short public message at the same time, without seeing the others. Messages may claim anything (your counts, others' roles, whom to cut), and lying is allowed. At the same time, each Cultist may write one private message seen only by the other Cultist. All public messages are then shown to everyone.
2. Cut. The active player names one other player who has at least one face-down card. They may not name themselves, and they may not name the last cutter (the player whose cut made them active). If every eligible player has no face-down cards, the active player may name the last cutter.
3. Reveal. One of the named player's face-down cards is chosen at random and turned face up for everyone. It stays revealed. The owner's private counts are reduced to match.
4. If it is Cthulhu, the Cultists win immediately.
5. If it is an Elder Sign, add 1 to Signs revealed. If Signs revealed equals the number of players, the Investigators win immediately.
6. The active player becomes the last cutter, and the named player becomes the active player.
7. Add 1 to cuts made. If cuts made equals 2 x the number of players (10 or 12), the game ends and the Cultists win.

NOTES. Talk is never binding. Nothing can be traded. No one may look at another player's cards.

Objective: This is a team win decided by counting, and exactly one outcome happens, so there are no draws. If Cthulhu is revealed, both Cultists win and all Investigators lose. If Signs revealed reaches the number of players (5 or 6) first, all Investigators win and both Cultists lose. If cuts made reaches 2 x players (10 or 12) first, both Cultists win.

Expected effect: With only N+1 Signs and 2N cuts, Investigators need roughly half their cuts to hit Signs. They must chase hands that truthfully claim many Signs, and sooner or later they must decide whether to dig into a hand that may hold Cthulhu or belong to a Cultist.

An Investigator holding Cthulhu can warn others away. But that hand's Signs are then hard to reach, and a Cultist can copy the claim to fence off their own Signs or bait Investigators. Two Cthulhu claims force a judgement on who is lying.

Sum checks matter: claimed Sign totals must fit N+1 Signs. The no-return rule means passing control through a suspect player hands Cultists exactly one stab, which tests who is trusted.

Talk passes both tests. The teams disagree outright, and only one can win. An Investigator who follows a Cultist's 'cut me, I have 3 Signs' advice wastes cuts, or passes control to a stabber. A Cultist who follows the table's consensus helps reveal Signs.

Thoughtless policies all lose regularly. Investigators who cut a random eligible player hit Signs only about 24-28% of the time and mostly lose to the timer. Cultists who always stab the claimed-Cthulhu hand can be fed bait or kept out of control. Investigators who never touch a Cthulhu-claimed or suspect hand fall short whenever 2+ Signs sit there.

The numbers are estimates. Simulation should check that sensible play gives each team 40-60%. If not, tune the cut limit by plus or minus 1 (for example 11 at 5 players).

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
