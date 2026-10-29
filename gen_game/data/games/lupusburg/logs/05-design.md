# 05 design

- time: 2026-10-28T01:40:03+00:00 (60.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 1c8c68a8637201ba, reply sha256 8fd3221a052c1f0d

## Sent

````
Original game: Lupusburg
Players in the original: 4 to 8

Original rules:
Each player owns two houses, one hides his chest, and two facedown characters: 1 Werewolf, 1 Thief, rest Townsfolk dealt per player count. If one player gets Werewolf+Thief reshuffle. Characters are placed under houses, Werewolf/Thief cannot go under chest house. Night: all eyes closed tapping. Burgomaster calls Thief, who silently lifts any house to check for chest. Then Burgomaster calls Werewolf, who points central claw at a house to kill that character, may self-kill if he has two alive. Day: killed house and character are removed facedown. Burgomaster may privately look at one living character, then show one of his own to that owner. Then clockwise each player may bet: draw 3 coins from bag, choose 1, place facedown with his seal before a player suspected to be Werewolf. Then players debate and vote to lynch one living character, removing its house. Repeat nights/days until Werewolf character is lynched or all non-Werewolf characters are dead. If Werewolf slaughters all, he wins alone. Otherwise points: 2 per living character, 1 if your chest house survived, face value of correctly bet coin, 1 for unused seal. Highest points wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: The round-1 peek is a blind lottery whose prize equals a whole game's base score. Each non-Werewolf peeker hits the Werewolf house with chance 1/(2N-2).
- P(someone finds the Werewolf in round 1): N=4: 1-(5/6)^3 = 42%; N=5: 1-(7/8)^4 = 41%; N=6: 1-(9/10)^5 = 41%.
- P(a plain Townsfolk player finds the Thief in round 1): N=4: 1-(5/6)^2 = 31%; N=6: 1-(9/10)^4 = 34%.
So in roughly 60% of games at least one player gets a risk-free +6 in round 1, purely from an uninformed choice. That equals the maximum base score of 6.

The lucky finder also has every reason to hide it. Announcing the house reveals its owner, others co-accuse, and his payout drops by 1 each. He accuses silently and wins at about 12 against at most 6 to 7 for everyone else.

A careful reasoner can do little about this:
- Theft announcements and kills give weak signals: the kill shows owner and side, not the character.
- Systematic peeking only pays off from round 2 or 3, worth 5 or 4 and often shared, so k > 1.

When all players follow the intended good strategy (spread peeks, accuse only on a confirmed peek, lynch the confirmed Werewolf), the winner is whoever's round-1 or round-2 peek happened to land on the Werewolf or Thief house. That is decided by the random deal against blind choices. The Werewolf seat is also a deal lottery: whether he is found by round 2 (about 65%) decides between about 2 and about 9.

Estimated share of the result decided by chance: well over half.
- change: Remove the blind-peek lottery: allow no accusations in round 1, or have the round-1 peek reveal only 'Townsfolk' or 'not Townsfolk', which lumps the Werewolf and the Thief together. A finder must then use later evidence (theft announcements, kills, votes, talk) to tell the two roles apart before accusing.
- change: Shrink accusation rewards so they cannot exceed a game's base score. For example, correct = max(1, 4 - r - (k-1)) and wrong = -3, so house, chest and survival points still matter and one lucky hit cannot decide the game.
- change: Reward sharing true information so the finder's best play is not silent hoarding. For example, add +2 to every player who voted for the Werewolf house in the round it is lynched, so a confirmed finder gains by publicising it and the others must judge whether his claim is true.
- change: Cut the Werewolf's swing between found and unfound. For example, survival bonus +3 instead of +5, plus +1 per round he survives, so his result depends on deception through talk and kill choice across rounds rather than on whether a blind peek hits him early.
- change: Re-run the probability table after these changes. Target: in under 25% of games does a single blind round-1 choice decide the winner when everyone plays the intended strategy.
The variation that was reviewed: Lupusburg Nights: SETUP. Seats are numbered 1..N (N = 4 to 6). Each player owns two houses, Left and Right; a house is named by owner and side. The engine secretly deals characters. Exactly one house holds the Werewolf and exactly one holds the Thief; they belong to two different players, each in a random one of that player's houses. Every other house holds a Townsfolk. The Werewolf's owner and the Thief's owner have no chest. Every other player has one chest, hidden under a randomly chosen one of his two houses. Each player privately learns the characters under his own two houses and, if he has one, his chest side. Everyone knows these dealing rules. Each player has one unused accusation. The game lasts at most 5 rounds.

EACH ROUND, in order:

1. NIGHT (simultaneous). Every player secretly names one living house belonging to another player. The Werewolf's owner may instead name his own other house if it is alive; he may never name the Werewolf house. Players with no living houses still take part.

2. PEEKS. Every player except the Werewolf's owner privately learns the character (Werewolf, Thief or Townsfolk) of the house he named.

3. THEFT. This applies if the Thief house is alive, the Thief has not yet stolen, and the Thief has not been correctly accused. If the house the Thief's owner named is the chest house of its owner, the Thief steals that chest, and the Thief's owner privately learns this. If the house is not a chest house, he privately learns 'no chest'. A steal is announced publicly as 'a chest was stolen from player X'; the Thief is not named. The Thief can steal only once per game.

4. KILL. The house the Werewolf's owner named is removed. Its owner and side are announced publicly, but not its character. The Werewolf's owner privately learns the character. Removing a house never removes a chest.

5. SLAUGHTER CHECK. If no living Thief or Townsfolk house remains, the Werewolf's owner wins alone and the game ends.

6. TALK (simultaneous). Every player writes one short message without seeing the others. All messages are then shown to everyone. Messages may be true or false, and nothing said is binding.

7. VOTE AND ACCUSE (simultaneous). Every player, including those with no living houses, names one living house to lynch. A player who still holds his accusation may also, in the same step, name one other player and a role (Werewolf or Thief) as that player's character. This uses up his accusation.

8. ACCUSATION RESULTS. For each role, let k be the number of players who correctly named that role's owner this round. Each correct accuser scores max(1, 7 - r - (k - 1)), where r is the round number. Each wrong accuser scores -4. All accusations made this round (accuser, target, role) are announced publicly, but their correctness is not. If the Thief's owner is correctly accused, he loses any stolen chest, it returns to its victim, and he can no longer steal.

9. LYNCH. The house with the most votes is removed. If two or more houses tie for most votes, nothing is removed. It is announced only whether the lynched house was 'the Werewolf' or 'not the Werewolf'. If the Thief house is removed by kill or lynch, the Thief loses any stolen chest, it returns to its victim, and he can no longer steal.

10. END CHECK. If the Werewolf house was lynched, the game ends and is scored. Otherwise, if no living Thief or Townsfolk house remains, the Werewolf's owner wins alone. Otherwise, if this was round 5, the game ends and is scored. Otherwise a new round begins.

SCORING (when the game ends by lynch or after round 5). Each player adds:
(a) 2 points per living house he owns;
(b) 2 points if he has a chest and it is not currently held by the Thief;
(c) the sum of his accusation result, or 0 if he never accused;
(d) the Thief's owner: +2 if he still holds a stolen chest (he stole, his Thief house is alive, and he was not correctly accused as the Thief);
(e) the Werewolf's owner: +5 if the Werewolf house is still alive. Winner: If at a slaughter check or the end check no living Thief or Townsfolk house remains, the Werewolf's owner is the sole winner. Otherwise the player with the highest total wins. If totals tie, the tied player with the higher accusation points wins. If still tied, the one with more living houses wins. If still tied, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Lupusburg is a hidden-role social deduction game for 4 to 8 players. Each player hides characters (one Werewolf, one Thief, the rest Townsfolk) and a chest under two houses. Each night the Thief hunts chests and the Werewolf kills a house; each day players bet coins on who is the Werewolf and vote to lynch a house. Points come from surviving characters, an intact chest and correct bets.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The original's tapping, pointing and bag of coins do not translate to text, and bets drawn from a bag reward the draw. In the previous variation, silent hoarding of a lucky round-1 peek was the dominant policy. 'Never accuse' is never punished, and the Werewolf's result swings between about 2 and about 9 on whether a blind peek hits him early."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "In the previous variation, about 41-42% of games had someone find the Werewolf with a blind round-1 peek. A Townsfolk player found the Thief in 31-34% of games. Either find was worth +6, equal to the whole base score, so the luck of the deal outweighed reasoning."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading kill patterns, theft announcements, vote patterns and lies in talk gives a strong player room to improve. A weak player still keeps house and chest points."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "The hidden state is rich, but the previous variation let a single uninformed peek replace inference. Once found, the accuser had no further need to reason or persuade."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is arithmetic on houses, chests, accusations and lynch outcomes tracked by the engine."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Once the night actions are made simultaneous secret choices, the game is text-only and needs no board. Five rounds and about 11 steps per round fit the limits."
    }
  ],
  "problems": [
    "P1: A blind round-1 peek that lands on the Werewolf or Thief house gives a confirmed, risk-free accusation worth as much as a whole game's base score. This is the lottery trap.",
    "P2: Accusation rewards (up to 6) exceed the base score (6), so house and chest play barely matters next to one lucky hit.",
    "P3: A finder gains by hiding what he knows: publicising it raises k and cuts his payout, so talk carries no true information and the others have nothing to judge.",
    "P4: The Werewolf seat is itself a deal lottery. Found early he ends near 2; unfound he ends near 9. Whether he is found depends mostly on blind peeks, not on his deception.",
    "P5: Accusing is safe once a peek confirms the target, so accusation choices need no reasoning about evidence."
  ],
  "changes": [
    {
      "what": "Peeks never reveal the exact role. A peek reports only 'Townsfolk' or 'Special', where Special means Werewolf or Thief. The Thief's owner, knowing his own role, can of course deduce that a Special house that is not his own is the Werewolf.",
      "why": "Finding a Special house shows only that its owner is one of two roles. To tell Werewolf from Thief, players must use theft announcements, kill choices, lynch results, votes and talk.",
      "fixes": "P1"
    },
    {
      "what": "No accusations may be made in round 1.",
      "why": "A round-1 peek can never be cashed in at once. By round 2, more public evidence exists to tell the roles apart.",
      "fixes": "P1"
    },
    {
      "what": "A correct accusation scores max(1, 5 - r - (k - 1)), which is 3 at most, in round 2. A wrong accusation scores -3.",
      "why": "A coin-flip accusation between Werewolf and Thief has expected value 0. The best possible hit (3) is half the base score of 6, so houses and chests still matter.",
      "fixes": "P2, P5"
    },
    {
      "what": "In the round the Werewolf house is lynched, every player who voted for it scores +2.",
      "why": "A finder gains by persuading others to vote with him. Listeners must judge whether a claim of 'I found Special at X' is honest, and whether it points at the Werewolf or the Thief.",
      "fixes": "P3"
    },
    {
      "what": "The Werewolf's owner scores +1 for each round that ends without the Werewolf house being lynched, plus +2 if the Werewolf house is alive at the end. This replaces the flat +5.",
      "why": "His score grows steadily with every round he survives through deception. Being found early costs a few points rather than everything, and the growth is driven by inference, not blind peeks.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Two houses per player, with hidden characters and a hidden chest",
    "One Werewolf who kills a house each night and one Thief who hunts for chests",
    "Burgomaster-style private peeks at other players' houses",
    "Day discussion followed by a vote to lynch one house",
    "Bets (accusations) on who holds the Werewolf, rewarding early correct suspicion",
    "The Werewolf wins alone if he slaughters every other character",
    "Points for living characters, a surviving chest and correct bets"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation's structure works. Its failure was a lottery in how peeks were rewarded, which lumped peek results, a ban on round-1 accusations and smaller payoffs fix within the limits."
  },
  "variation": {
    "name": "Lupusburg Nights II",
    "summary": "A hidden-role deduction game for 4 to 6 players over at most 5 rounds. Peeks reveal only whether a house is 'Special' (Werewolf or Thief), so players must combine kills, thefts, lynch results and talk to tell the two apart before risking an accusation. The Werewolf scores for every round he survives.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP\n- Seats are numbered 1..N, where N is 4 to 6.\n- Each player owns two houses, Left and Right. A house is named by owner and side.\n- The engine secretly deals characters. Exactly one house holds the Werewolf and exactly one holds the Thief. They belong to two different players, each in a random one of that player's houses. Every other house holds a Townsfolk.\n- The Werewolf's owner and the Thief's owner have no chest. Every other player has one chest, hidden under a randomly chosen one of his two houses.\n- Each player privately learns the characters under his own two houses and, if he has one, his chest side.\n- Everyone knows these dealing rules.\n- Each player starts with one unused accusation.\n- The game lasts at most 5 rounds.\n\nEACH ROUND, in order (r is the round number):\n\n1. NIGHT (simultaneous). Every player secretly names one living house belonging to another player.\n   - The Werewolf's owner may instead name his own other house if it is alive. He may never name the Werewolf house.\n   - Players with no living houses still take part.\n\n2. PEEKS. Every player except the Werewolf's owner privately learns the result for the house he named.\n   - The result is 'Special' if it holds the Werewolf or the Thief, and 'Townsfolk' otherwise.\n\n3. THEFT. This applies only if the Thief house is alive, the Thief has not yet stolen, and the Thief's owner has not been correctly accused as the Thief.\n   - If the house the Thief's owner named is its owner's chest house, the Thief steals that chest and the Thief's owner privately learns 'chest stolen'. Otherwise he privately learns 'no chest'.\n   - A steal is announced publicly as 'a chest was stolen from player X', without naming the Thief.\n   - The Thief steals at most once per game.\n\n4. KILL. The house named by the Werewolf's owner is removed.\n   - Its owner and side are announced publicly, but its character is not.\n   - The Werewolf's owner privately learns its character.\n   - Removing a house never removes a chest. If the removed house is the Thief house, the Thief loses any stolen chest, it returns to its victim, and the Thief can no longer steal.\n\n5. SLAUGHTER CHECK. If no living Thief or Townsfolk house remains, the Werewolf's owner wins alone and the game ends.\n\n6. TALK (simultaneous). Every player writes one short message without seeing the others' messages. All messages are then shown to everyone. Messages may be true or false and nothing said is binding.\n\n7. VOTE AND ACCUSE (simultaneous). Every player, including those with no living houses, names one living house to lynch.\n   - From round 2 on, a player who still holds his accusation may also, in the same step, name one other player and one role (Werewolf or Thief) as that player's character. This uses up his accusation.\n   - No accusations may be made in round 1.\n\n8. ACCUSATION RESULTS.\n   - For each role, let k be the number of players who correctly named that role's owner this round. Each correct accuser scores max(1, 5 - r - (k - 1)). Each wrong accuser scores -3.\n   - All accusations made this round (accuser, target, role) are announced publicly, but whether they were correct is not.\n   - If the Thief's owner is correctly accused as the Thief, he loses any stolen chest, it returns to its victim, and he can no longer steal.\n\n9. LYNCH. The house with the most votes is removed. If two or more houses tie for most votes, nothing is removed.\n   - It is announced only whether the lynched house was 'the Werewolf' or 'not the Werewolf'.\n   - If the Thief house is removed, the Thief loses any stolen chest, it returns to its victim, and he can no longer steal.\n   - If the Werewolf house was lynched, every player who voted for it scores +2.\n\n10. WEREWOLF ROUND POINT. If the Werewolf house was not lynched this round, the Werewolf's owner scores +1.\n\n11. END CHECK.\n   - If the Werewolf house was lynched, the game ends and is scored.\n   - Otherwise, if no living Thief or Townsfolk house remains, the Werewolf's owner wins alone.\n   - Otherwise, if this was round 5, the game ends and is scored.\n   - Otherwise a new round begins.\n\nFINAL SCORING (when the game ends by lynch or after round 5). Each player adds the following to the points already earned in play (accusation results, lynch-vote bonuses, Werewolf round points):\n(a) 2 points per living house he owns;\n(b) 2 points if he has a chest and it is not currently held by the Thief;\n(c) the Thief's owner: +2 if he still holds a stolen chest;\n(d) the Werewolf's owner: +2 if the Werewolf house is alive.",
    "objective": "If at a slaughter check or the end check no living Thief or Townsfolk house remains, the Werewolf's owner is the sole winner. Otherwise the player with the highest total wins. If totals tie, the tied player with the higher accusation points wins. If still tied, the one with more living houses wins. If still tied, the game is a draw.",
    "expected_effect": "A blind round-1 hit now yields only 'this owner is Werewolf or Thief'. It cannot be cashed in round 1, and a guess between the two roles has expected value 0 (+3 or -3). Under intended play, an uninformed round-1 choice should decide the winner in well under 25% of games (estimated around 10%). Cashing in needs extra evidence: who reports no chest, which houses the Werewolf spares or kills, the timing of theft announcements, and lynch results.\n\nTalk passes both tests.\n- Reasoning: finders want to publicise a Special house to collect the +2 lynch-vote bonus.\n- Conflict: only one player can win, and the roles want different outcomes. The Werewolf and Thief want to redirect votes and misname each other. Correct accusers want few co-accusers, since k cuts their payout. Townsfolk want the Werewolf lynched but not at the cost of their own houses.\n- A player who simply follows a confident claim may be voting for the Thief's house, or accusing on a lie, and lose 3.\n\nThe Werewolf's score grows by 1 per round he survives, plus 2 if he is alive at the end. Being caught early costs a few points rather than everything, so his result rewards sustained deception over the deal."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 5
  }
}
```
````
