# 28 design

- time: 2026-10-28T02:16:26+00:00 (239.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 96b5d8f977f80560, reply sha256 6ce7728681692237

## Sent

````
Original game: Growl
Players in the original: 4 to 10

Original rules:
Setup a shared face-up deck containing Night cards seeded at 1/3, 2/3 and bottom of deck, plus Bite, Wound, Charm, Salve and Gold cards. Deal each player one starter Bite or Gold to secretly set Wolf Zeros; then deal 3 cards for a 4-card hand, redrawing if 3 wounds. On your turn draw the top deck card aloud: if it is a Night card resolve its effect then start Night Phase, otherwise you must give it to another living player who adds it to hand. Players die instantly when wounds minus salves reach 3, and humans secretly become werewolves when bites minus charms reach 3. During Night Phase no talking is allowed and each living player must pass one chosen card left and one right face-down, but humans may not pass Bites. After receiving, check death/turn. Game ends after Final Night is resolved or only two alive remain; if at least one human lives humans win, otherwise wolves win.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: **Win thresholds (6 players: 2 wolves, 4 humans).** The wolves win as soon as living_humans <= living_wolves. That means the wolves need to remove only 2 humans (4 -> 2) before the humans find both wolves.

**Thoughtless wolf policy W:** both wolves always vote for the same human, and at night both play Maul on the same human (2 wounds = wound_limit, so the target dies).

**Day 1.** Humans have zero information: there has been no exposure and no Charm yet. A human picking blindly among 5 others has P(wolf) = 2/5 = 0.40. The wolves' 2 bloc votes also split or decide the human votes. Outcomes:
- Human lynched (about 0.45): 2v3. Night kill: 2v2, wolves win.
- Tie (about 0.15): 2v4, then the night kill makes 2v3.
- Wolf lynched (about 0.40).

**Can Salve stop the kill?** Each non-target human salves one of 4 others, so each hits the target with probability about 1/4. With 2 helpers in a 2v3 position, P(at least one save) = 1 - (3/4)^2 = 0.44. The target cannot salve itself.

**Exposure.** The random exposure reveals a mauling wolf with probability W/N, about 1/3, per night.

**Rough path sum, 6 players.** P(humans win) ≈ 0.40 x 0.6 (find the second wolf, helped by the 1/3 exposure) + 0.60 x [0.44 x 0.33 x 0.5 + tie branch about 0.05] ≈ 0.24 + 0.07 ≈ 0.31. So policy W, which never adapts, wins about 70% for the wolves.

**Bite is a stronger, still thoughtless policy.** Two wolves biting the same human X reach bites 2 on night 1. One more bite on night 2 gives bites 3, and X is infected. That is a swing of -1 human and +1 wolf with no public trace: no wound, no death, no revealed role. From 2v4 with no lynch, this alone gives 3v3 and the wolves win at step 17 of round 2. Only a Charm aimed at X by another human prevents it, and blind Charm hit rate is about 1/4 per human.

**Round-6 rule.** Any surviving wolf wins at round 6, which adds a further wolf-only tiebreak.

**Payoff table (team result).**
| Ending | wolf | human |
|---|---|---|
| wolves_won = 1 | 1 | 0 |
| wolves_won = 0 | 0 | 1 |

The wolves' bloc-vote plus focus-fire (or focus-bite) policy wins most games without any reasoning.

**7 players** (2v5, 3 human losses allowed) is closer, about 45/55. So the balance also swings strongly with player count. Seat order gives no edge, because all choices are simultaneous. The asymmetry lies entirely in information (wolves know everything relevant) and in the win conditions.
- playable FAILED: **Within limits:** 18 steps per round (<= 20). 4 choice steps (talk, vote, den, night) (<= 4). About 16-19 attributes (<= 20). 1 random draw per round (the exposure; the wolf choice is setup only). 6 rounds (<= 40).

**Talk is well placed:** it is simultaneous and placed where wolves and humans disagree.

**Hidden elements exceed the limit of 3.** The game actually hides five independent kinds of information:
1. Each player's is_wolf.
2. Each player's bites, private per owner.
3. Each player's night_card and night_target, except the exposed one.
4. The wolf-den private channel.
5. Per-player private Charm feedback.

The infection notice is also a private message to the new wolf and to all wolves. The stated 'hidden_elements: 3' undercounts.

**Minor ambiguities:**
- Whether a wolf may target another wolf with Maul is not stated (presumably yes).
- Whether a newly infected wolf joins the den in the same night is unclear. Step 15 comes after step 8, so it is presumably the next night.
- Whether a player at wounds 2 who is also at bites 3 dies as a human is resolved by step order (death before infection) but is not stated.

The rules are otherwise finite and arithmetic.
- reasoning_over_luck FAILED: **What humans can infer:**
- **Charm feedback** says 'had bites' only for bitten humans. A wolf can never have bites, so 'no bites' is consistent with both wolf and unbitten human. The positive signal only clears a human and never identifies a wolf.
- **Exposure** is the only hard evidence of a wolf. It fires with probability 2/N per night (1/3 at 6 players, 2/7 at 7). It is decided entirely by the random draw.
- **Day 1** lynch is a blind 2/5 guess.
- **Salve** saves are blind 1/4 guesses.

**Sensitivity to luck (6 players).** The human win rate is about 0.31 overall. Conditioned on luck, it is about 0.65 if a wolf is exposed on night 1 and about 0.15 if not. Most of the human outcome is set by the exposure draw and the day-1 coin flip, not by reasoning.

**Both sides playing well.** Wolves bloc-vote and focus-fire; humans vote blindly and act on exposures. The result is then mostly 'did the random exposure land on a wolf'.

**Wolf decisions** do carry real reasoning: Maul versus Bite versus a disguising Salve under exposure risk. But the human side, which needs to infer, has almost nothing reliable to infer from. Vote patterns help only marginally, because wolves can blend in with a bloc. A strong human reasoner is not clearly favoured over a random voter.
- change: Give humans an inference source that good play can exploit, not a random draw. For example: Charm reports 'your target is a Wolf / is not a Wolf' (or 'played Bite or Maul last night: yes/no'), or replace the random exposure with a vote-chosen inspection. Keep at most 1 random draw per round, but do not make it the main way wolves are found.
- change: Rebalance the kill and infection economy. Raise wound_limit to 3 or allow at most one Maul per night in total. Make infection need bites >= 3 from at least 2 different nights and reveal publicly that 'someone was infected', so Bite is not a hidden double swing that wins 6-player games by round 2.
- change: Remove the 'any wolf alive at round 6 = wolves win' timeout. Either make the game end only on a parity or elimination condition, or raise max_rounds and give humans the win if they reach the last round with living_humans >= 2 x living_wolves.
- change: Scale the wolf count with players (1 wolf at 6 players, 2 at 7, or a fixed 7 players), and show by path calculation that the always-bloc-vote, always-focus-Maul or focus-Bite wolf policy wins no more than about 55%.
- change: Cut hidden elements to 3. For example: drop the per-player bites counter and infection (or make bites public), and fold the Charm feedback into the inspection mechanic. Keep roles, night actions and the wolf den as the three.
- change: State explicitly: whether a wolf may Maul another wolf; that a newly infected wolf joins the den from the next night; and that death (step 14) is checked before infection (step 15).
The variation that was reviewed: Growl: Scent of Blood: PARAMETERS: max_rounds = 6; bite_limit = 3; wound_limit = 2. Starting wolves = 2.

TABLE STATE: round (public, starts 0); living_wolves and living_humans (hidden counts); exposed_player, exposed_card and exposed_target (announced each morning); wolves_won (starts -1).

PLAYER STATE:
- is_wolf (1 or 0): known to the player and to all other wolves.
- bites (starts 0): known only to its owner, who is told the value each morning.
- wounds (starts 0): public.
- alive (starts 1): public.
- revealed_role: public, blank until death, then 'Wolf' or 'Human'.
- vote_target and votes_received: public after each vote.
- night_card and night_target: private, except when exposed.

SETUP:
1. Choose 2 players uniformly at random as wolves (is_wolf = 1). All others are humans (is_wolf = 0).
2. Tell each player privately whether they are a Wolf or a Human. Each wolf is told who the other wolf is.
3. Set living_wolves = 2 and living_humans = players - 2.

EACH ROUND (only living players act; dead players are skipped):
1. Morning announcement: round increases by 1. Publicly show every player's wounds and alive status, and the revealed_role of the dead. From round 2 on, announce last night's exposure: 'exposed_player played exposed_card on exposed_target'. Privately tell each living player their current bites.
2. Talk: every living player writes one short message at the same time. All messages are then shown to everyone. Lying is allowed, and nothing is binding.
3. Vote: at the same time, each living player names one other living player (vote_target). Abstaining is not allowed.
4. Tally: votes_received = the number of votes each player got. Publicly show every player's vote_target and every votes_received.
5. Execution: if exactly one player has the most votes, that player dies. Set alive = 0 and reveal their role publicly. If the top count is tied, no one dies.
6. Count: living_wolves = living players with is_wolf = 1; living_humans = living players with is_wolf = 0.
7. Day end check: if living_wolves = 0 the game ends and the humans win. If living_wolves >= living_humans the game ends and the wolves win.
8. Wolf den: every living wolf writes one short message at the same time. Messages are shown only to living wolves. Humans see nothing and are not told what was said.
9. Night action: at the same time and in silence, each living player chooses one card and one other living player as its target. A human may choose Charm or Salve. A wolf may choose Bite, Maul, Charm or Salve. The card always goes to the chosen target; there is no pass.
10. Bites and Mauls: each Bite on a human adds 1 to the target's bites (a Bite on a wolf has no effect). Each Maul adds 1 to the target's wounds.
11. Charms: each player who played Charm is privately told 'your target had bites' or 'your target had no bites', judged after step 10 and before any Charm is applied. Then each Charm lowers the target's bites by 1, to a minimum of 0.
12. Salves: each Salve lowers the target's wounds by 1, to a minimum of 0.
13. Exposure: draw one living player uniformly at random. Record their name, card and target as exposed_player, exposed_card and exposed_target, to be announced next morning.
14. Death check: any living player with wounds >= 2 dies (alive = 0) and their role is revealed publicly.
15. Infection: any living human with bites >= 3 becomes a wolf. Set is_wolf = 1 and bites = 0. They are told privately, together with the names of all living wolves, and all wolves are told who the new wolf is. A new wolf acts as a wolf from the next round.
16. Count: recompute living_wolves and living_humans.
17. Night end check: if living_wolves = 0, the humans win. Otherwise, if living_wolves >= living_humans, the wolves win. Otherwise, if round = max_rounds, the wolves win, because a wolf survived.
18. If the game has not ended, start the next round.

WHAT IS NEVER REVEALED: the night cards and targets of anyone except the exposed player, other players' bites, wolf den messages, and any Charm feedback except to the player who played that Charm. Winner: Team game, decided by arithmetic. If the game ends with living_wolves = 0, wolves_won = 0. If it ends with living_wolves >= living_humans, or at the end of round 6 with any wolf alive, wolves_won = 1. Each player, alive or dead, scores result = 1 - |final is_wolf - wolves_won|. Players with result 1 win and players with result 0 lose, so the winning side is the whole team, and infected players count as wolves. There are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Growl is a 4-10 player hidden-team card game. Cards from a shared face-up deck are handed to other players, and on Night phases each player silently passes one card left and one right. Wounds kill a player, and bites secretly turn humans into werewolves. Humans win if at least one human survives the Final Night.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the original, whoever sits next to a wolf receives its bites, so seat adjacency decides much of who gets infected. In the previous variation, a thoughtless wolf policy won about 70% at 6 players: bloc-vote one human and focus both Mauls on one target (or focus Bites for a hidden infection swing). A round-6 timeout also handed the win to any surviving wolf. Balance swung from about 70/30 at 6 players to about 45/55 at 7."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The previous variation's human win rate moved from about 0.15 to about 0.65 depending on one random exposure draw. The day-1 lynch and Salve choices were blind guesses. A strong human reasoner was not clearly better than a random voter."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Wolves had real decisions (Maul, Bite or a disguising Salve). Humans had almost no reliable signal: Charm feedback could clear a human but never identify a wolf. So the human side had little room to improve."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hidden roles give plenty to infer, but the only hard evidence of a wolf was a random 2/N exposure each night. Vote patterns helped only a little."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Deaths, infections and team victory all follow from counters and comparisons."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original uses seat adjacency (pass left and right), a seeded deck and hands. The previous variation fit the step limits but hid five kinds of information: roles, bites, night actions, the den, and private Charm feedback. The limit is 3. Some edge cases were also unstated: Mauling a wolf, when a new wolf joins the den, and the order of death versus infection."
    }
  ],
  "problems": [
    "P1: The wolf bloc-vote plus focus-Maul or focus-Bite policy wins about 70% at 6 players without reasoning.",
    "P2: The hidden Bite infection is a double swing (one human fewer, one wolf more) with no public trace, and it can win by round 2.",
    "P3: The round-6 timeout gives the win to any surviving wolf, so wolves can stall.",
    "P4: Humans have no reliable inference source. A random exposure draw decides most games, which is the lottery trap.",
    "P5: Balance swings strongly with player count.",
    "P6: Five hidden elements exceed the limit of 3 (bites counters and private Charm feedback are extra).",
    "P7: Edge cases are unstated: Mauling a wolf, death versus infection order, self-targeting.",
    "P8: Day lynches of innocents are blind coin flips, so passive, blending wolves win about half the time against humans who cannot reason from anything."
  ],
  "changes": [
    {
      "what": "Replace the random exposure and the blind lynch with a Trial. The day's unique top vote-getter has their role revealed publicly and truthfully. A wolf is killed. A human is publicly cleared but takes 1 wound from the mob.",
      "why": "Humans get a deterministic, public inference source that good voting exploits. Mis-accusations still cost something: the cleared human becomes easy to kill. Vote records then become evidence, because whoever pushed a cleared human is suspect.",
      "fixes": "P4"
    },
    {
      "what": "Remove the random exposure draw entirely. There are no random draws after setup.",
      "why": "The outcome is no longer decided by whether a draw landed on a wolf.",
      "fixes": "P4"
    },
    {
      "what": "Make vote records public and run the Trial every day.",
      "why": "Two wolves who bloc-vote a human get exposed. That human is revealed as cleared, so their voters (2 of whom are wolves) become the obvious suspects next day, at about 2/3 accuracy. This punishes the thoughtless bloc policy and rewards reading votes.",
      "fixes": "P1"
    },
    {
      "what": "Drop Bite, bites counters and infection.",
      "why": "This removes the hidden double swing and one hidden element.",
      "fixes": "P2"
    },
    {
      "what": "Drop Charm and its private feedback; its inspection role moves into the public Trial.",
      "why": "This removes another hidden element.",
      "fixes": "P6"
    },
    {
      "what": "Replace the wolf timeout with a ratio rule. After the Final Night (round 5), humans win if living humans are at least 2 times living wolves; otherwise wolves win. Parity at any check still wins for wolves, and 0 wolves still wins for humans.",
      "why": "Passive wolves who never Maul lose: 5 humans is at least 2x2. Stalling is not a win. Wolves must make 2 kills by round 5, or 3 for an early parity win. If one wolf is found, humans need only keep 2 alive.",
      "fixes": "P3, P8"
    },
    {
      "what": "Fix the game at 7 players: 2 wolves and 5 humans.",
      "why": "Balance no longer swings with player count, and one size can be checked by path reasoning.",
      "fixes": "P5"
    },
    {
      "what": "Use one wound limit of 2 for everyone: each Maul adds 1 wound and each Salve removes 1, applied in a fixed order.",
      "why": "A kill needs both wolves on one fresh target, or one wolf on an already-wounded player. Salves are then a real guessing duel against the wolves rather than a blind lottery, because wounds are public.",
      "fixes": "P1"
    },
    {
      "what": "State the edge cases. A Maul may target a wolf, with normal effect. No one may target themselves. Mauls apply before Salves. The death check comes after Salves. Trial wounds can kill a player who was already wounded.",
      "why": "This makes the rules complete and unambiguous.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "Secret wolves among humans, with wolves knowing each other.",
    "Wound cards that kill at a threshold and Salve cards that heal them.",
    "A silent Night in which every player hands one face-down card to another player.",
    "A Final Night that ends the game, where human survival decides it.",
    "Table talk with lying allowed, and team victory in which dead players still share their team's result."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The hidden-team core is rich in inference and bluffing. It needed a public, skill-driven detection source, a fair end rule and fewer hidden elements, all of which fit within the limits."
  },
  "variation": {
    "name": "Growl: Trial by Moonlight",
    "summary": "7 players, 2 secret wolves. Each day everyone talks at once and then votes. The top vote-getter is put on Trial and their true role is revealed. Wolves die, while innocent humans are cleared but wounded. Each silent night, wolves Maul and everyone Salves. Wolves win at parity, or if humans are fewer than twice the wolves after the Final Night (round 5). Humans win by killing both wolves or by keeping that 2:1 ratio.",
    "players": {
      "min": 7,
      "max": 7,
      "suggested": 7
    },
    "rules": "PARAMETERS: 7 players, 2 wolves, wound limit 2, final round 5.\n\nTABLE STATE: round (public, starts 0); living_wolves and living_humans (computed, used only for end checks, never announced as counts); accused (public, blank or a name); winner (blank, 'Wolves' or 'Humans').\n\nPLAYER STATE:\n- is_wolf (1 or 0): known to the player and to the other wolf.\n- alive (starts 1): public.\n- wounds (starts 0): public.\n- cleared (starts 0): public. It becomes 1 when a Trial shows the player is human.\n- revealed_role: public. Blank until death or Trial, then 'Wolf' or 'Human'.\n- vote_target and votes_received: public after each vote.\n- night_card and night_target: private. Never revealed.\n- mauls_received and salves_received: private working counters, reset each night.\n\nSETUP:\n1. Choose 2 of the 7 players uniformly at random to be wolves; the other 5 are humans.\n2. Tell each player privately whether they are a Wolf or a Human. Tell each wolf who the other wolf is.\n\nEACH ROUND (only living players act; dead players are skipped but remain on their team):\n1. Morning: round increases by 1. Publicly show every player's alive, wounds, cleared and revealed_role, and name who died last night.\n2. Talk: every living player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Lying is allowed, and nothing is binding.\n3. Vote: at the same time, each living player names one other living player. Abstaining and self-votes are not allowed.\n4. Tally: votes_received = the number of votes each player got. Publicly show every vote_target and every votes_received.\n5. Trial: if exactly one player has the most votes, that player is the accused, and their role is revealed publicly. If the top count is tied, there is no Trial today.\n6. If the accused is a Wolf: they die (alive = 0, revealed_role = 'Wolf').\n7. If the accused is a Human: set cleared = 1 and revealed_role = 'Human', and add 1 to their wounds.\n8. Day death check: any living player with wounds >= 2 dies (alive = 0), and their role is revealed publicly.\n9. Count: living_wolves = living players with is_wolf = 1; living_humans = living players with is_wolf = 0.\n10. Day end check: if living_wolves = 0, the Humans win. Otherwise, if living_wolves >= living_humans, the Wolves win.\n11. Wolf den: every living wolf writes one short message at the same time. These messages are shown only to living wolves.\n12. Night (silent, no talk): at the same time, each living player chooses one card and one other living player as its target. A human must play Salve. A wolf plays either Maul or Salve. The card goes face-down to the target. Any player, including a wolf, may be targeted. No one may target themselves.\n13. Mauls: each living player's wounds += the number of Mauls they received.\n14. Salves: then each living player's wounds -= the number of Salves they received, to a minimum of 0.\n15. Night death check: any living player with wounds >= 2 dies (alive = 0), and their role is revealed publicly at the next Morning.\n16. Count: recompute living_wolves and living_humans.\n17. Night end check: if living_wolves = 0, the Humans win. Otherwise, if living_wolves >= living_humans, the Wolves win. Otherwise, if round = 5 (the Final Night), the Humans win if living_humans >= 2 x living_wolves, and the Wolves win otherwise. If no one has won, start the next round.\n\nNEVER REVEALED: anyone's night card or target, how many Mauls or Salves a player received (only resulting wounds and deaths are public), wolf den messages, and the role of a living player who has not been tried.",
    "objective": "This is a team game decided by arithmetic. The game ends at the first of these: living wolves = 0, which is a Humans win; living wolves >= living humans at a day or night check, which is a Wolves win; or the end of round 5, where Humans win if living humans >= 2 x living wolves and Wolves win otherwise. Every player, alive or dead, wins if their team wins and loses otherwise. There are no draws.",
    "expected_effect": "Thoughtless policies lose:\n- Passive wolves never Maul, so 5 humans stay at least 2x2 at round 5 and they lose.\n- Bloc-voting wolves get a human cleared. That human's voters then include both wolves, and reasoning humans try one of them next day at about 2/3 accuracy, which costs the wolves the game, since a lone wolf rarely makes the remaining kills. Estimate about 35% for the thoughtless bloc-and-focus wolf policy against reasoning humans.\n- Random-voting humans let the wolves steer Trials onto humans. Each cleared human becomes wounded and easy to kill. Estimate about 75% wolf wins against random humans.\n\nWith good play on both sides, the expected result is near 45/55, decided by reasoning:\n- Wolves split their votes and mimic human voting.\n- Wolves choose between killing cleared, trusted humans and uncleared ones (which thins the suspect pool).\n- Wolves sometimes Salve or wound a partner to fake innocence.\n- Humans read vote records and claims, and spread Salves to guess where the double Maul lands.\n\nTalk passes both tests. The players disagree because wolves need humans to try innocents. A human who simply follows the first confident proposal can be led by a wolf into a Trial on a human, which wounds a teammate and wastes the day.\n\nTalk is simultaneous, so no one can just echo the first speaker. There is no endgame unraveling, because the game ends on elimination, parity or a ratio, not on a highest total."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 3,
    "random_draws_per_round": 0,
    "rounds": 5
  }
}
```
````
