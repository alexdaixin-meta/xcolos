# 03 design

- time: 2026-10-28T01:35:54+00:00 (139.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 709a294887362731, reply sha256 b2c920f16cbd01ca

## Sent

````
Original game: Lupusburg
Players in the original: 4 to 8

Original rules:
Each player owns two houses, one hides his chest, and two facedown characters: 1 Werewolf, 1 Thief, rest Townsfolk dealt per player count. If one player gets Werewolf+Thief reshuffle. Characters are placed under houses, Werewolf/Thief cannot go under chest house. Night: all eyes closed tapping. Burgomaster calls Thief, who silently lifts any house to check for chest. Then Burgomaster calls Werewolf, who points central claw at a house to kill that character, may self-kill if he has two alive. Day: killed house and character are removed facedown. Burgomaster may privately look at one living character, then show one of his own to that owner. Then clockwise each player may bet: draw 3 coins from bag, choose 1, place facedown with his seal before a player suspected to be Werewolf. Then players debate and vote to lynch one living character, removing its house. Repeat nights/days until Werewolf character is lynched or all non-Werewolf characters are dead. If Werewolf slaughters all, he wins alone. Otherwise points: 2 per living character, 1 if your chest house survived, face value of correctly bet coin, 1 for unused seal. Highest points wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: SCORE TABLE (no thief or wolf extras unless stated). Townsfolk owner, untouched: 2+2 houses, 2 chest, accusation (1 if held; 4/3/2/1 if correct in round 1/2/3/4+; 0 if wrong). Range 6 to 10, typically 7. Thief owner, untouched, steal made: 4+2+2+acc = 9 to 12. Mechanical play gets him there: check an unchecked house each night, and each townsfolk house is a chest with p = 1/2, so P(no steal by night 3) = 1/8. His victim also drops 2. Werewolf owner, surviving to round 6: 4 houses + 2 chest + 1 held accusation + up to 6 kills + 2 bonus = 14 to 15, which beats every possible non-wolf total (max 12). So wolf survival is a guaranteed win. Wolf lynched in round r: 2+2+r+1 = 5+r (6 in round 1, 8 in round 3), still competitive with townsfolk. GOOD-PLAY CASE (wolf caught round 3, about 3 kills spread over 2N-2 houses): wolf 8; untouched townsfolk 7 if holding, 8 if accusing correctly in round 3, 9 in round 2; untouched Thief owner 9 to 11. The Thief role, a dealt seat, wins most non-wolf outcomes with no reasoning edge, because his own chest can never be stolen and the steal is an automatic +2. THOUGHTLESS POLICIES. (a) 'Always hold accusation': from round 4 on, correct = 1 = hold and wrong = 0, so holding weakly dominates. It never loses to accusing in rounds 4 to 6. (b) 'Blind accuse in round 1': EV = 4/(N-1) = 1.33 at N=4, above the 1.00 for holding, so a no-information guess is correct play at N=4. (c) Thief 'check the lowest unchecked house': as good as any reasoned Thief play. (d) Town 'vote randomly': ties then mean no lynch, so the wolf survives and wins with 15. SEAT EDGE: the Burgomaster order is fixed by seat. Seat 1 peeks in round 1, when an accusation is worth 4; seat 4 peeks in round 4, when it is worth 1. A wolf found by a peek therefore yields +3 for seat 1 versus +0 for seat 4 (the hold value of 1 equals the accusation value). DRAWS: untouched holders all score 7, and almost all components are even, so ties at the top are common when the wolf is caught early.
- playable FAILED: Limits are fine: 17 steps (≤20), 4 choice steps (night, peek, talk, vote+accuse; ≤4), 16 attributes (≤20), 2 hidden elements (≤3), 0 draws per round, 6 rounds (≤40). Night is a simultaneous poll with dummy choices for cover. Talk is simultaneous and justified, since town and wolf disagree and townsfolk are rivals. Scoring is pure arithmetic. No board, judge or clock is needed. AMBIGUITY: the Burgomaster is 'the r-th seat counting from seat 1, skipping players with no living house'. With N=4 there is no 5th or 6th seat, so rounds 5 and 6 are undefined (round 6 at N=5), and wrap-around is never stated. Skipping also has two readings. Example: seat 2 is dead in round 3. Under 'the r-th living seat' the Burgomaster is seat 4 and seat 3 is never Burgomaster; under 'rotate and skip' it is seat 3. A model cannot resolve this from the text. LATE-ROUND TEST: from round 4 the accusation pays 1 if correct and 1 if held, so the safe option (hold) weakly dominates in every late round. The accusation mechanic is dead for half the game.
- reasoning_over_luck FAILED: Under good play by all, the winner is mostly fixed by the deal and incidental chance. First, whoever is dealt the Thief gets a near-automatic +2 (steal by night 3 with p = 7/8, no skill involved) and is immune to being stolen from. That puts him at 9 to 11 against 7 to 9 for townsfolk. Second, the wolf, who does not know where the Thief is, decides which townsfolk lose 2 to 4 points. Third, who identifies the wolf in time for a 3- or 4-point accusation depends on the fixed Burgomaster order plus a peek that hits the wolf with p = 1/(2N-2) (1/6 at N=4, 1/10 at N=6). Inference does exist: kill patterns (the wolf rarely kills his own houses), peeks, lies in talk, public accusations, and 'chest stolen from X'. But the Thief role swing (about 4 points relative to a robbed rival) exceeds the typical skill swing from an early correct accusation (about 1 to 3 points). I estimate chance decides well over half of results when the wolf is caught, so a better reasoner is not clearly favoured.
- change: Remove the Thief's automatic edge. Make the steal transfer the victim's chest (Thief +2 only while his Thief house lives, victim -2), and add a counter: any player may name the Thief's owner instead of the Werewolf's owner with his accusation (correct = same round value, and the Thief loses the stolen +2). The Thief role then carries risk and requires concealment.
- change: Cap the wolf so survival is not an automatic win. Drop +1 per kill and give +3 for surviving to round 6. A surviving wolf then scores about 4+2+3 = 9 to 10, beatable by a townsfolk who accused correctly early (10).
- change: Fix the accusation values: unused = 0, wrong = -3, correct = 5/4/3/2/2/2 for rounds 1/2/3/4/5/6. A blind round-1 guess is then negative at N=4 ((5-6)/3 < 0), and late accusations still beat holding when informed.
- change: Remove the seat edge from peeking: every living player peeks at one other player's living house each round as a single simultaneous step, replacing the Burgomaster. If a Burgomaster is kept, define it exactly: round 1 = seat 1; each later round = the next seat clockwise with a living house after the previous Burgomaster, wrapping from N to 1.
- change: Add a tie-break before declaring a draw: first the earliest correct accusation, then the most living houses, then a shared win.
The variation that was reviewed: Lupusburg Ledger: SETUP. Seats are numbered 1..N (N = 4 to 6). Each player owns two houses, Left and Right. Each house hides one character.

The engine deals characters secretly. Exactly one house in the game holds the Werewolf and exactly one holds the Thief, owned by two different players, each in a random one of that player's houses. Every other house holds a Townsfolk.

Each player has a chest under exactly one of his houses. For the Werewolf's owner and the Thief's owner, the chest is under their other house, because the Werewolf and Thief can never be under a chest. For every other player, the chest side is random.

Each player privately learns the characters under both of his own houses and his own chest side. Everyone knows the dealing rules.

Each player also has one unused accusation.

ROUNDS. The game runs in rounds. The Burgomaster in round r is the r-th seat in turn order, counting from seat 1 and skipping players who have no living house.

Each round has these steps, in order:

1. NIGHT. Every player, at the same moment, secretly names one living house (owner and side). Only two choices take effect.
   a. If the Thief's house is alive and the Thief named another player's living house, the Thief privately learns whether that house hides a chest. If it does, and he has not stolen before, he steals that chest. It is then publicly announced that 'a chest was stolen from player X'; the Thief is not named.
   b. If the Werewolf's owner named a living house other than the Werewolf's own house, that house is killed and removed. It may be one of his own houses. Its character is not revealed. Only the owner and side are announced, and the Werewolf's kill count rises by 1.
   All other players' night choices are ignored.

2. SLAUGHTER CHECK. If no living non-Werewolf character remains, the Werewolf's owner wins alone and the game ends.

3. PEEK. The Burgomaster privately names one living house belonging to another player and privately sees its character.

4. TALK. Every player, at the same moment, writes one short message, which may be true or false. All messages are then shown to everyone. Nothing said is binding.

5. VOTE AND ACCUSE. Every player, at the same moment, names one living house to lynch. Players whose houses are all removed still vote.
   Any player who still holds his accusation may also, in the same step, name another player as the owner of the Werewolf. This uses up his accusation. Its value is fixed by the round in which it is made: 4 in round 1, 3 in round 2, 2 in round 3, 1 in round 4 or later.
   All accusations made this round are then announced publicly, with accuser and target.

6. LYNCH. The house with the most votes is removed. If two or more houses tie for most votes, nobody is lynched. It is announced only whether the lynched house was 'the Werewolf' or 'not the Werewolf'.

7. END CHECK.
   - If the Werewolf was lynched, the game ends and is scored.
   - Otherwise, if no living non-Werewolf character remains, the Werewolf's owner wins alone.
   - Otherwise, a new round begins.
   - If round 6 ends with the game unfinished, the game ends and is scored, and the Werewolf's owner adds 2 bonus points.

REMOVED CHESTS. A chest is lost if the house above it is removed or if it is stolen.

SCORING (when the game ends by lynch or after round 6). Each player adds up:
- 2 points per living house he owns.
- 2 points if his chest's house is alive and his chest was not stolen.
- His accusation: its value if correct, 0 if wrong, 1 if never used.
- The Thief's owner: +2 if he stole a chest and his Thief house is alive.
- The Werewolf's owner: +1 per successful night kill. Winner: If, at a slaughter check or the end check, no living non-Werewolf character remains, the Werewolf's owner is the sole winner. Otherwise the player with the highest point total wins. If two or more players share the highest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Lupusburg is a 4-8 player hidden-role deduction game. Each player hides two characters (one Werewolf and one Thief in play, the rest Townsfolk) and a chest under two houses. Night kills and thefts alternate with day peeks, coin bets on who the Werewolf is, and lynch votes, and points go to surviving houses, chests and correct bets, unless the Werewolf slaughters everyone and wins alone.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the previous variation a surviving Werewolf scored 14-15, above any possible non-wolf total (12 maximum), so wolf survival was a guaranteed win. From round 4, holding the accusation (1) equalled a correct accusation (1) and beat a wrong one (0), so 'always hold' weakly dominated. A blind round-1 accusation had positive expected value at N=4 (4/3 against 1 for holding). The fixed Burgomaster order gave seat 1 a 4-point peek window and seat 4 a 1-point one."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The Thief seat collected a near-automatic +2 (a steal by night 3 with probability 7/8 from mechanically checking houses) and could never be robbed itself. That swing of about 4 points against a robbed rival exceeded the typical 1-3 point gain from good deduction."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Kill patterns, peeks, lies in talk and theft announcements all reward reasoning. But the accusation was dead for half the game, and Thief play was solved by 'check the lowest unchecked house'."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Characters and chests are hidden. The wolf must be inferred from kills, peeks and talk, and claims can be bluffs. The core is strongly inference-based."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every score component (houses, chests, accusation values, bonuses) is arithmetic on tracked state."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It fits the limits (17 steps, 4 choice steps). However, the Burgomaster rule ('r-th seat, skipping dead players') is undefined for rounds 5-6 at N=4 and has two readings when a player is dead. The original's tapping and pointing must be replaced by simultaneous polls."
    }
  ],
  "problems": [
    "P1: Werewolf survival scored above every possible non-wolf total, so survival was an automatic win.",
    "P2: The Thief role was a dealt edge: a near-automatic +2 steal, immunity to theft, and no risk.",
    "P3: Late accusations were worth the same as holding, so holding weakly dominated from round 4.",
    "P4: A blind round-1 accusation had positive expected value, rewarding a no-information guess.",
    "P5: The Burgomaster peek gave fixed seats unequal information windows, and the rule was ambiguous for later rounds and dead seats.",
    "P6: Totals were mostly even numbers with similar components, so draws at the top were common.",
    "P7: Which townsfolk lost points to kills, theft and chest loss was largely luck, swamping deduction (lottery trap)."
  ],
  "changes": [
    {
      "what": "Remove the Burgomaster. The night becomes one simultaneous poll in which every player names a house. A non-wolf player privately sees the character of the house he names (his peek). The Thief also checks that house for a chest. The Werewolf's owner kills the named house and privately learns its character.",
      "why": "Every player gets one equal peek per round, with no seat order to define or argue about. The night choice itself becomes a reasoning decision.",
      "fixes": "P5"
    },
    {
      "what": "The Werewolf's owner and the Thief's owner have no chest. Townsfolk chests are lost only by theft, never by a house being killed or lynched.",
      "why": "Removes the Thief's theft immunity and the double loss (house plus chest) from random kills, so kills cost a flat 2 per house.",
      "fixes": "P2, P7"
    },
    {
      "what": "A steal moves 2 points from the victim to the Thief's owner. The Thief keeps it only if his Thief house survives and nobody correctly accuses him as the Thief; otherwise the chest returns to the victim.",
      "why": "A Thief who steals but is exposed ends at 4 + accusation, below a townsfolk's 6 + accusation. Stealing becomes a concealment problem. The publicly announced victim has a motive and a route to recover his loss through deduction.",
      "fixes": "P2, P7"
    },
    {
      "what": "Accusations name a player and a role (Werewolf or Thief). Correct pays max(1, 7 - round - (k - 1)), where k is the number of players who correctly named the same role in the same round. Wrong pays -4. Unused pays 0.",
      "why": "Blind round-1 guesses have negative expected value: at N=4, (6 - 2*4)/3 < 0. An informed late accusation (at least 1) still beats holding (0). Splitting the value with co-accusers makes sharing a discovery a real trade-off. Varied values break ties.",
      "fixes": "P3, P4, P6"
    },
    {
      "what": "The Werewolf earns a flat +5 for surviving to the end of round 5 and nothing per kill. The game lasts 5 rounds.",
      "why": "A surviving wolf scores 9 at most. That beats townsfolk who hold, guessed wrong, or were hit, but it ties or loses to a townsfolk who accused correctly in time. Survival alone no longer wins.",
      "fixes": "P1"
    },
    {
      "what": "Tie-breaks in order: higher accusation points, then more living houses, then a draw.",
      "why": "Makes draws rare and rewards the deduction component.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Two houses per player, each hiding a character, with one Werewolf, one Thief and the rest Townsfolk.",
    "Chests that the Thief steals at night, with the werewolf and thief never under a chest.",
    "The night kill, including the wolf's option to kill his own other house for cover.",
    "Private peeks, open debate and plurality lynch votes, with a tie meaning no lynch.",
    "Bets on the Werewolf's identity whose value falls the later you bet.",
    "The Werewolf wins alone if he slaughters every other character.",
    "Points for surviving houses, chests and correct bets."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The hidden-role deduction core is strong. The flaws are payoff and seat-order problems, fixable within the limits."
  },
  "variation": {
    "name": "Lupusburg Nights",
    "summary": "A 4-6 player hidden-role game. Each night every player secretly names a house: townsfolk peek, the Thief peeks and tries to steal a chest, and the Werewolf kills. Each day players talk simultaneously, vote to lynch a house, and may stake one accusation naming the Werewolf or the Thief. That accusation is worth more the earlier it is made and less when shared, and costs points when wrong.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP. Seats are numbered 1..N (N = 4 to 6). Each player owns two houses, Left and Right; a house is named by owner and side. The engine secretly deals characters. Exactly one house holds the Werewolf and exactly one holds the Thief; they belong to two different players, each in a random one of that player's houses. Every other house holds a Townsfolk. The Werewolf's owner and the Thief's owner have no chest. Every other player has one chest, hidden under a randomly chosen one of his two houses. Each player privately learns the characters under his own two houses and, if he has one, his chest side. Everyone knows these dealing rules. Each player has one unused accusation. The game lasts at most 5 rounds.\n\nEACH ROUND, in order:\n\n1. NIGHT (simultaneous). Every player secretly names one living house belonging to another player. The Werewolf's owner may instead name his own other house if it is alive; he may never name the Werewolf house. Players with no living houses still take part.\n\n2. PEEKS. Every player except the Werewolf's owner privately learns the character (Werewolf, Thief or Townsfolk) of the house he named.\n\n3. THEFT. This applies if the Thief house is alive, the Thief has not yet stolen, and the Thief has not been correctly accused. If the house the Thief's owner named is the chest house of its owner, the Thief steals that chest, and the Thief's owner privately learns this. If the house is not a chest house, he privately learns 'no chest'. A steal is announced publicly as 'a chest was stolen from player X'; the Thief is not named. The Thief can steal only once per game.\n\n4. KILL. The house the Werewolf's owner named is removed. Its owner and side are announced publicly, but not its character. The Werewolf's owner privately learns the character. Removing a house never removes a chest.\n\n5. SLAUGHTER CHECK. If no living Thief or Townsfolk house remains, the Werewolf's owner wins alone and the game ends.\n\n6. TALK (simultaneous). Every player writes one short message without seeing the others. All messages are then shown to everyone. Messages may be true or false, and nothing said is binding.\n\n7. VOTE AND ACCUSE (simultaneous). Every player, including those with no living houses, names one living house to lynch. A player who still holds his accusation may also, in the same step, name one other player and a role (Werewolf or Thief) as that player's character. This uses up his accusation.\n\n8. ACCUSATION RESULTS. For each role, let k be the number of players who correctly named that role's owner this round. Each correct accuser scores max(1, 7 - r - (k - 1)), where r is the round number. Each wrong accuser scores -4. All accusations made this round (accuser, target, role) are announced publicly, but their correctness is not. If the Thief's owner is correctly accused, he loses any stolen chest, it returns to its victim, and he can no longer steal.\n\n9. LYNCH. The house with the most votes is removed. If two or more houses tie for most votes, nothing is removed. It is announced only whether the lynched house was 'the Werewolf' or 'not the Werewolf'. If the Thief house is removed by kill or lynch, the Thief loses any stolen chest, it returns to its victim, and he can no longer steal.\n\n10. END CHECK. If the Werewolf house was lynched, the game ends and is scored. Otherwise, if no living Thief or Townsfolk house remains, the Werewolf's owner wins alone. Otherwise, if this was round 5, the game ends and is scored. Otherwise a new round begins.\n\nSCORING (when the game ends by lynch or after round 5). Each player adds:\n(a) 2 points per living house he owns;\n(b) 2 points if he has a chest and it is not currently held by the Thief;\n(c) the sum of his accusation result, or 0 if he never accused;\n(d) the Thief's owner: +2 if he still holds a stolen chest (he stole, his Thief house is alive, and he was not correctly accused as the Thief);\n(e) the Werewolf's owner: +5 if the Werewolf house is still alive.",
    "objective": "If at a slaughter check or the end check no living Thief or Townsfolk house remains, the Werewolf's owner is the sole winner. Otherwise the player with the highest total wins. If totals tie, the tied player with the higher accusation points wins. If still tied, the one with more living houses wins. If still tied, the game is a draw.",
    "expected_effect": "SIMPLE POLICIES. 'Always hold and vote randomly': lynches split, the wolf survives with 9, and the holder's 6 loses. A blind round-1 accusation loses on average (-4 if wrong). 'Accuse whoever a message names' is exploited by lying wolves and thieves. A Thief who checks houses mechanically and is careless gets accused, falling to 4 + accusation. A wolf who survives but lets an accuser keep his houses loses to that accuser's 10-12. Every simple policy can lose. GOOD PLAY. Typical totals are a townsfolk accusing correctly and alone in round 2 at 11, a shared round-3 accusation at 9, a surviving wolf at 9, and a hidden Thief who stole at 6 + accusation. The finish is decided by when and whether players act on information and protect themselves, not by the deal. LUCK. Who peeks the wolf first is partly luck, but the edge is 1-3 points. It can be erased by sharing, by the wolf's retaliatory kills, and by others' later correct accusations. A robbed player can recover his chest by exposing the Thief. TALK earns its place. The wolf and Thief want to mislead. A townsfolk who found the wolf faces a dilemma: revealing it in talk lets everyone accuse in the same round and cuts his reward (k rises), while hiding it risks a failed lynch and wolf survival. Accusers are announced, so the wolf will kill their houses. A player who simply follows a claim can lose 4 points to a bluff, or dilute his payoff by joining a crowd."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 5
  }
}
```
````
