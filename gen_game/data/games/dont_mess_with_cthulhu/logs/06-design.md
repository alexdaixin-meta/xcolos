# 06 design

- time: 2026-10-28T01:37:56+00:00 (84.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2fd3a893403b9608, reply sha256 f394a89353c6af85

## Sent

````
Original game: Dont Mess With Cthulhu
Players in the original: 3 to 6

Original rules:
Setup: for 4-6 players use 3-4 Investigators vs 2 Cultists, plus extra hidden tokens, shuffle and deal one role face down to each player. Build Investigation deck per player count with Futile cards, Elder Signs equal to player count, and one Cthulhu, shuffle and deal five to each player face down. Each player looks at own cards, notes counts but shuffles so positions unknown, then may lie about contents. Play is four rounds. Each round has actions equal to player count. Active player chooses one face-down Investigation card belonging to another player and reveals it. If Cthulhu is revealed Cultists win instantly. If all Elder Signs revealed Investigators win instantly. Otherwise the owner of the revealed card becomes next Active player. After actions equal to player count, collect remaining face-down cards, reshuffle and redeal evenly, one fewer per player each round. After four rounds without all Signs, Cultists win.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: BASELINE (random cutting). The N+2 Signs and 1 Cthulhu form N+3 key cards. Investigators win only if Cthulhu falls after the N-th Sign, so P = 3/(N+3): 0.43, 0.375 and 0.33 for N = 4, 5, 6. TIMER. Investigators need N Signs, but the limit is 4N cuts, a slack of 3N (12, 15, 18 cuts). Even uniform random cuts nearly always reach N Signs before cut 4N. At N = 4, 16 of 20 cards are revealed, leaving 4 unseen. Wasting cuts therefore never threatens Investigators, so the stated timer win condition is vestigial. In effect Cultists win only by a Cthulhu reveal. WHO CAN REVEAL CTHULHU. Positions are fixed and fully known to their owners, so Investigators never knowingly cut it. Cthulhu comes up only through (a) a Cultist's blind stab while active, or (b) a Cultist holding it and claiming that position is a Sign as bait. CASE A, an Investigator holds Cthulhu. P = (N-2)/N: 1/2, 3/5 and 2/3. In the 4-player deals with one Cultist it is 3/4. The holder claims it is Futile. Cultists only stab among the remaining claimed-Futile cards of others, about 13 at N = 5, which is about 7% per Cultist active turn. Cultists are active only when an Investigator cuts a Cultist's card, or when seat 1 is a Cultist. Over an estimated 2-3 such turns, Cultists win about 15-20%, so Investigators win about 80%. CASE B, a Cultist holds Cthulhu. The bait claim makes it close to a coin flip. Weighted together, Investigators win about 65-75% under sensible play, against a random baseline of 33-43%. The information change swings the game well past even. 4-PLAYER SUBCASE. The set-aside token is a Cultist with probability 2/5. So 2/5 of deals are 3 Investigators v 1 Cultist and 3/5 are 2 v 2. A lone Cultist with no known partner and 5 of 20 cards is badly outmatched. THOUGHTLESS POLICIES. Investigator policy: 'always state my hand truthfully except Cthulhu, always cut a claimed Sign of someone not yet caught lying'. It wins about 80% in Case A. Cultist policy: 'always cut a random claimed-Futile card'. It wins about 7% per turn. Seat order and move order are not the problem. The deal of Cthulhu and the dead timer are.
- reasoning_over_luck FAILED: Assume both teams play well: Investigators truthful except about Cthulhu, Cultists lying. The decisive variable is then a setup deal: which hand Cthulhu lands in. In Case A, an Investigator holds it (50-75% of deals) and there is little to infer. The Investigators' best line is near-mechanical: cut claimed Signs and pass control among verified players. The Cultists can only make blind stabs at about 1/13. Investigators win about 80% almost regardless of reasoning quality. Only in Case B, bait Cthulhu held by a Cultist, does inference decide the game: claims, consistency of Sign totals and lying patterns. A second deal factor: Investigators' own hands hold on average (N-2)(N+2)/N Signs, which is 3, 4.2 and 5.3 for N = 4, 5, 6, against N needed. So the deal largely sets whether they must risk Cultist hands. The 4-player role deal (1 v 2 Cultists) is a further unreasoned swing. Chance accounts for well over half the outcome variance.
- change: Make the timer bite. Set the cut limit to about N+3 cuts (7, 8, 9) instead of 4N, so wasted Cultist cuts and safe Investigator Futile 'passes' carry a real cost. Re-check that sensible play gives each team 40-60%.
- change: Remove the 4-player role lottery. Either always deal exactly 2 Cultists, or always 1 Cultist with compensation, for example a cut limit of N+2.
- change: Restore uncertainty about Cthulhu's location so it is not decided by the deal. Either (a) at the end of every N cuts, reshuffle each player's own face-down cards into new positions without telling the owner the order (the original's 'know counts, not positions'), or (b) tell owners only their counts, never their positions. Every Cthulhu reveal then depends on inference and risk, not on who was dealt it.
- change: Tell the two Cultists who each other are, using a private channel (supported). They can then pass control to each other and coordinate bait claims, giving Cultists a strategic line beyond blind stabs.
- change: Consider Signs = N+1 rather than N+2. Investigators must then sometimes probe suspected Cultist hands, so the bait and opponent-modelling decision arises in most deals.
The variation that was reviewed: Don't Cut Cthulhu: Named Cards: SETUP.
1. Roles. With 4 players, shuffle 3 Investigator and 2 Cultist tokens, deal 1 face down to each player and set the 5th aside unseen, so there are 1 or 2 Cultists. With 5 players, deal 3 Investigators and 2 Cultists. With 6 players, deal 4 Investigators and 2 Cultists. Each player privately learns only their own role. Cultists are not told who the other Cultist is.
2. Deck. There are 5 cards per player. The deck holds Elder Signs equal to the number of players plus 2, exactly 1 Cthulhu, and Futile cards for the rest. With 4 players: 6 Signs, 1 Cthulhu, 13 Futile (20 cards). With 5 players: 7 Signs, 1 Cthulhu, 17 Futile (25 cards). With 6 players: 8 Signs, 1 Cthulhu, 21 Futile (30 cards). Shuffle and deal 5 cards face down to each player, placed in positions numbered 1 to 5. Positions never move or renumber.
3. Private knowledge. Each player is told privately exactly what card is in each of their own 5 positions.
4. Public information, always visible to everyone: which positions of each player are still face down; every card revealed so far, with its owner and position; Signs revealed; cuts made; the target (Signs needed = number of players); the cut limit (4 times the number of players: 16, 20 or 24); and who is active.
5. Player 1 is the first active player. Roles are random, so this gives no team an edge.

EACH ROUND (one cut).
1. Talk. Every player writes one short message at the same time, without seeing the others. Messages may claim anything: the contents of any of your positions, guesses about others' roles, or requests about whom to cut. Lying is allowed. All messages are then shown to everyone.
2. Cut. The active player names one other player and one of that player's face-down positions. You may not name yourself or an already revealed position.
3. Reveal. That exact card is turned face up for everyone. It stays revealed and is out of play.
4. If it is Cthulhu, the Cultists win immediately.
5. If it is an Elder Sign, add 1 to Signs revealed. If Signs revealed equals the number of players (4, 5 or 6), the Investigators win immediately.
6. The named player becomes the active player for the next round.
7. Add 1 to cuts made. If cuts made equals 4 times the number of players, the game ends and the Cultists win.

NOTES. Talk is never binding. Nothing may be exchanged except through the public messages. Players can never look at another player's cards. With 4 players, the unused role token is not a player and wins nothing. Winner: This is a team victory decided by counting. If Cthulhu is revealed, every Cultist wins and every Investigator loses. If Signs revealed reaches the number of players before that, every Investigator wins and every Cultist loses. If cuts made reaches 4 times the number of players first, every Cultist wins and every Investigator loses. Exactly one of these happens, so there are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Don't Mess With Cthulhu is a hidden-team bluffing game. Investigators try to reveal enough Elder Signs from other players' face-down cards before Cthulhu is revealed or time runs out. Cultists win if Cthulhu is revealed or the rounds expire. Players know their own card counts but not the positions, and they may lie about them.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed variation the timer was dead. The limit of 4N cuts against N Signs needed left a slack of 3N, so Cultists effectively won only through a Cthulhu reveal. Owners knew their exact positions, so an Investigator holding Cthulhu simply never let it be cut. A thoughtless Investigator policy wins about 80% when an Investigator holds Cthulhu: tell the truth except about Cthulhu, and cut claimed Signs of anyone not yet caught lying. The 4-player deal also produced 1 or 2 Cultists at random."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Where Cthulhu was dealt largely decided the game. If an Investigator held it (50-75% of deals), Investigators won about 80% with near-mechanical play. Only Cultist-held Cthulhu deals turned on reading claims. Chance explained most of the outcome variance."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "In most deals the Investigator line was close to solved: cut claimed Signs and pass control among trusted players. Cultists had little to do but blind stabs at about 1/13 per turn."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hidden roles and lying are present. However, exact position knowledge removed the risk from Investigators' own Cthulhu, and with N+2 Signs Investigators rarely had to probe suspected Cultist hands, so inference was optional in most deals."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner follows from counting: a Cthulhu reveal, Signs revealed reaching the target, or cuts reaching the limit. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is turn-based and text-only, with simultaneous talk, sequential cuts and arithmetic win checks. It has no board and is short."
    }
  ],
  "problems": [
    "P1 Dead timer: a cut limit of 4N against N Signs needed never threatens Investigators, so wasting cuts costs nothing and Cultists win only by revealing Cthulhu.",
    "P2 Cthulhu lottery: owners know exact positions, so an Investigator-held Cthulhu is never at risk. Whoever is dealt Cthulhu decides most games.",
    "P3 4-player role lottery: the set-aside token makes some games 3 Investigators against a lone, hopeless Cultist.",
    "P4 Cultists cannot coordinate: they don't know each other, so their only line is blind stabbing.",
    "P5 Too many Signs: with N+2 Signs, Investigators can usually win from their own hands and never need to judge whether to risk a suspected Cultist hand.",
    "P6 Telling Cultists who each other are (needed for P4) opens a ping-pong exploit. Two Cultists could cut each other forever, keeping control and stabbing at a Cultist-held Cthulhu every turn."
  ],
  "changes": [
    {
      "what": "Set the cut limit to 2N: 10 cuts at 5 players, 12 at 6, against N Signs needed.",
      "why": "Every cut now matters. Cultist time-wasting and Investigator 'safe' Futile passes are real costs, and Investigators need about a 50% Sign rate on their cuts.",
      "fixes": "P1 Dead timer"
    },
    {
      "what": "Owners are told only how many Signs, Futile cards and Cthulhu (0 or 1) they hold, never which card is where. A cut names a player, and one of that player's face-down cards is revealed at random.",
      "why": "Cthulhu can be revealed from any hand that holds it, including an Investigator's. A known Cthulhu hand becomes a risky store of Signs that someone may have to dig into. Where Cthulhu is dealt changes what is safe, not who wins.",
      "fixes": "P2 Cthulhu lottery"
    },
    {
      "what": "Play only at 5 or 6 players, always with exactly 2 Cultists (3 v 2 or 4 v 2).",
      "why": "This removes the random team size and the 1-v-3 deals.",
      "fixes": "P3 4-player role lottery"
    },
    {
      "what": "The Cultists learn each other's identity at setup. Each round they may exchange one private message each.",
      "why": "Cultists can share counts, coordinate bait claims and false Cthulhu claims, and plan their stabs.",
      "fixes": "P4 Cultists cannot coordinate"
    },
    {
      "what": "Set the Elder Signs to N+1 (6 or 7), so the target is all Signs but one.",
      "why": "Any Sign held by a Cultist, or by the Cthulhu holder, quickly becomes necessary. Investigators must weigh claims and risk suspect hands.",
      "fixes": "P5 Too many Signs"
    },
    {
      "what": "No-return rule: you may not cut the player who made the cut that made you active.",
      "why": "This breaks Cultist ping-pong, so each Cultist possession gives one stab before control returns to an Investigator. Investigators can still rotate among themselves (I1, I2, I3, I1) unless one of their hands is unsafe.",
      "fixes": "P6 Cultist ping-pong"
    }
  ],
  "keeps": [
    "Hidden Investigator and Cultist teams, dealt face down.",
    "Elder Signs, Futile cards and a single Cthulhu dealt face down. Owners know counts but not positions.",
    "Lying about your own cards is allowed and expected.",
    "The player whose card was revealed becomes the next active player.",
    "Cthulhu wins instantly for the Cultists, enough Signs win instantly for the Investigators, and Cultists win if time runs out."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of hidden teams, bluffed hand claims and a passing cutter is sound. The failures come from parameters and information rules, and they can be fixed inside the limits."
  },
  "variation": {
    "name": "Don't Cut Cthulhu: Counted Hands",
    "summary": "There are 5-6 players: 2 known-to-each-other Cultists against 3-4 Investigators. Each player knows only the counts in their own hand. Players talk, then the active player names another player, and one of that player's face-down cards is revealed at random. Investigators need N Signs out of N+1 within 2N cuts. Cultists win on Cthulhu or the timer.",
    "players": {
      "min": 5,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP.\n1. Roles. With 5 players deal 3 Investigator and 2 Cultist roles at random; with 6 players deal 4 Investigators and 2 Cultists. Each player privately learns their own role. Each Cultist is also told privately who the other Cultist is.\n2. Deck. Each player gets 5 cards. The deck holds Elder Signs equal to players + 1, exactly 1 Cthulhu, and Futile cards for the rest. At 5 players that is 6 Signs, 1 Cthulhu and 18 Futile (25 cards). At 6 players it is 7 Signs, 1 Cthulhu and 22 Futile (30 cards). Shuffle and deal 5 face down to each player.\n3. Private knowledge. Each player is told privately only HOW MANY Signs, Futile cards and Cthulhu (0 or 1) they hold. Nobody, including the owner, knows which face-down card is which.\n4. Public information, always visible: each player's number of face-down cards; every revealed card and its owner; Signs revealed; cuts made; the target (Signs needed = number of players: 5 or 6); the cut limit (2 x players: 10 or 12); the active player; and the 'last cutter' (the player who made the previous cut, none at the start).\n5. Player 1 starts as the active player. Roles are random, so this favours no team.\n\nEACH ROUND (one cut).\n1. Talk. Every player writes one short public message at the same time, without seeing the others. Messages may claim anything (your counts, others' roles, whom to cut), and lying is allowed. At the same time, each Cultist may write one private message seen only by the other Cultist. All public messages are then shown to everyone.\n2. Cut. The active player names one other player who has at least one face-down card. They may not name themselves, and they may not name the last cutter (the player whose cut made them active). If every eligible player has no face-down cards, the active player may name the last cutter.\n3. Reveal. One of the named player's face-down cards is chosen at random and turned face up for everyone. It stays revealed. The owner's private counts are reduced to match.\n4. If it is Cthulhu, the Cultists win immediately.\n5. If it is an Elder Sign, add 1 to Signs revealed. If Signs revealed equals the number of players, the Investigators win immediately.\n6. The active player becomes the last cutter, and the named player becomes the active player.\n7. Add 1 to cuts made. If cuts made equals 2 x the number of players (10 or 12), the game ends and the Cultists win.\n\nNOTES. Talk is never binding. Nothing can be traded. No one may look at another player's cards.",
    "objective": "This is a team win decided by counting, and exactly one outcome happens, so there are no draws. If Cthulhu is revealed, both Cultists win and all Investigators lose. If Signs revealed reaches the number of players (5 or 6) first, all Investigators win and both Cultists lose. If cuts made reaches 2 x players (10 or 12) first, both Cultists win.",
    "expected_effect": "With only N+1 Signs and 2N cuts, Investigators need roughly half their cuts to hit Signs. They must chase hands that truthfully claim many Signs, and sooner or later they must decide whether to dig into a hand that may hold Cthulhu or belong to a Cultist.\n\nAn Investigator holding Cthulhu can warn others away. But that hand's Signs are then hard to reach, and a Cultist can copy the claim to fence off their own Signs or bait Investigators. Two Cthulhu claims force a judgement on who is lying.\n\nSum checks matter: claimed Sign totals must fit N+1 Signs. The no-return rule means passing control through a suspect player hands Cultists exactly one stab, which tests who is trusted.\n\nTalk passes both tests. The teams disagree outright, and only one can win. An Investigator who follows a Cultist's 'cut me, I have 3 Signs' advice wastes cuts, or passes control to a stabber. A Cultist who follows the table's consensus helps reveal Signs.\n\nThoughtless policies all lose regularly. Investigators who cut a random eligible player hit Signs only about 24-28% of the time and mostly lose to the timer. Cultists who always stab the claimed-Cthulhu hand can be fed bait or kept out of control. Investigators who never touch a Cthulhu-claimed or suspect hand fall short whenever 2+ Signs sit there.\n\nThe numbers are estimates. Simulation should check that sensible play gives each team 40-60%. If not, tune the cut limit by plus or minus 1 (for example 11 at 5 players)."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 3,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
