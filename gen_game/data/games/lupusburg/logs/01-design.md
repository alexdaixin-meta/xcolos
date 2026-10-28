# 01 design

- time: 2026-10-28T01:31:46+00:00 (136.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 260f4738db22b7fb, reply sha256 bd233bbe339ac7b1

## Sent

````
Original game: Lupusburg
Players in the original: 4 to 8

Original rules:
Each player owns two houses, one hides his chest, and two facedown characters: 1 Werewolf, 1 Thief, rest Townsfolk dealt per player count. If one player gets Werewolf+Thief reshuffle. Characters are placed under houses, Werewolf/Thief cannot go under chest house. Night: all eyes closed tapping. Burgomaster calls Thief, who silently lifts any house to check for chest. Then Burgomaster calls Werewolf, who points central claw at a house to kill that character, may self-kill if he has two alive. Day: killed house and character are removed facedown. Burgomaster may privately look at one living character, then show one of his own to that owner. Then clockwise each player may bet: draw 3 coins from bag, choose 1, place facedown with his seal before a player suspected to be Werewolf. Then players debate and vote to lynch one living character, removing its house. Repeat nights/days until Werewolf character is lynched or all non-Werewolf characters are dead. If Werewolf slaughters all, he wins alone. Otherwise points: 2 per living character, 1 if your chest house survived, face value of correctly bet coin, 1 for unused seal. Highest points wins.
````

## Reply

````
```json
{
  "original_summary": "Lupusburg is a 4-8 player hidden-role deduction game. Each player hides two face-down characters under two houses and a chest under one of them. A secret Werewolf kills one character each night and a secret Thief peeks for chests. By day a rotating Burgomaster peeks at a character, players bet coins drawn at random on who owns the Werewolf, and the table lynches one character. The game ends when the Werewolf is lynched or has killed every other character, and is scored on surviving characters, chests, correct bets and unused seals.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No single simple policy wins outright, because lynch votes and kills depend on what the others do. But the betting coin is drawn blindly from a bag, so the timing of a bet barely matters. The Thief's peek has no stated payoff, so the role is information with nothing to spend it on. The Werewolf player can only win by slaughtering everyone, because once his Werewolf is lynched he scores like a crippled townsperson. That makes the seat feel all-or-nothing."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Deduction and persuasion matter in lynching and accusing. However, the coin value comes from a random 3-coin draw, so two equally correct accusers can score very differently. The random deal of Werewolf and Thief also strongly shapes what a player can score."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading kill patterns, cross-checking claims about the Burgomaster's peek, timing a bet, and the Werewolf's option to kill his own second house to look innocent all leave room to improve. A weak town player still scores points for surviving characters and an unused seal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Characters and chests are hidden. Private peeks give partial information. The rule that a Werewolf or Thief can never sit under the chest house is an inference hook: knowing where a chest is tells you which house could hide the Werewolf. Lynching requires reading lies."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The end condition and the point totals are pure arithmetic: 2 per living character, 1 per surviving chest, coin face value, 1 per unused seal. The debate needs no judge."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The physical mechanics (eyes closed, tapping, a pointed claw, a coin bag) must become private simultaneous choices. The Burgomaster's look-then-show exchange, separate clockwise betting, debate and vote exceed the 4-choice-step budget. The random coin draw each round is an extra source of chance that adds nothing. The play length is fine."
    }
  ],
  "problems": [
    "P1: Physical secrecy mechanics (eyes closed, tapping, pointing) do not exist on a text platform. The acting roles would be exposed if only they were asked to act.",
    "P2: The bet coin is a random draw of 3 coins from a bag. That is luck, not judgement, and the value is not tied to how early or how risky the accusation was.",
    "P3: The Thief's chest peek has no scoring consequence, so the Thief role is pure information with no conflict of interest.",
    "P4: The Werewolf player's score collapses once the Werewolf is lynched, so the seat is win-alone-or-last. A random deal decides which players get this lopsided seat (lottery trap).",
    "P5: Too many separate choice steps per round (night actions, Burgomaster peek, Burgomaster show-back, clockwise betting, debate, vote) for the engine's limit of 4.",
    "P6: Sequential clockwise betting and open-ended debate let later players copy earlier ones, and debate has no defined length or form.",
    "P7: Facedown removal of lynched characters leaves unclear how the table learns that the game has ended. The Burgomaster's role as host or player is ambiguous."
  ],
  "changes": [
    {
      "what": "Every player submits a secret 'night choice' (a house) at the same moment each round. Only the Thief's and the Werewolf's choices take effect; everyone else's are ignored.",
      "why": "This reproduces eyes-closed secrecy as a simultaneous poll. Nobody can tell who acted.",
      "fixes": "P1: Physical secrecy mechanics (eyes closed, tapping, pointing) do not exist on a text platform."
    },
    {
      "what": "The random coin bag is replaced by one public, once-per-game accusation whose value falls with time: 4 points in round 1, 3 in round 2, 2 in round 3, 1 from round 4 on. A wrong accusation scores 0. An unused accusation scores 1.",
      "why": "Accusation timing becomes a real risk/reward judgement. Accusing early pays only with good inference, since a blind round-1 guess among 4 rivals averages 1, the same as holding. Making accusations public adds a signal that others can follow only at a lower value.",
      "fixes": "P2: The bet coin is a random draw of 3 coins from a bag."
    },
    {
      "what": "The first time the Thief's night check finds a chest, he steals it. The owner loses his chest points, and the Thief gains 2 if his Thief house is alive at the end. The theft is announced publicly with the victim's name, not the Thief's.",
      "why": "This gives the Thief a stake and creates conflict. Victims want the Thief lynched, but lynching a non-Werewolf character helps the Werewolf. The announcement also feeds deduction, because it reveals which of the victim's houses is the non-chest house.",
      "fixes": "P3: The Thief's chest peek has no scoring consequence."
    },
    {
      "what": "If the Werewolf is lynched, the Werewolf player still scores normally plus 1 point per successful night kill. Killing every non-Werewolf character remains an outright win.",
      "why": "The Werewolf seat gets a graded points path. A Werewolf who survives long and hides well can still top the table, so the seat is a different job rather than a jackpot or a dud.",
      "fixes": "P4: The Werewolf player's score collapses once the Werewolf is lynched."
    },
    {
      "what": "The Burgomaster's show-back is dropped, and the bet is folded into the lynch vote as one optional field. Each round has exactly 4 choice steps: night choice, Burgomaster peek, message, vote plus optional accusation.",
      "why": "This brings the round within the engine's limit of 4 choice steps while keeping the peek, the bet and the lynch.",
      "fixes": "P5: Too many separate choice steps per round."
    },
    {
      "what": "Debate becomes one short message per player, written at the same moment and then shown to all. Votes and accusations are simultaneous.",
      "why": "This removes copying from turn order. Bluffs, peek claims and trust must be judged from one round of statements.",
      "fixes": "P6: Sequential clockwise betting and open-ended debate let later players copy earlier ones."
    },
    {
      "what": "A lynched house is announced as 'Werewolf' or 'not the Werewolf' only. The Burgomaster is a seated player, rotating by seat.",
      "why": "The end trigger becomes explicit while the Thief's identity stays hidden. The Burgomaster's status is clarified.",
      "fixes": "P7: Facedown removal of lynched characters leaves unclear how the table learns that the game has ended."
    }
  ],
  "keeps": [
    "Two houses per player, each hiding one character, with a chest under one house.",
    "Exactly one Werewolf and one Thief, never owned by the same player and never under the chest house.",
    "The Werewolf kills one character per night and may kill his own second house to look innocent.",
    "The Thief checks houses for chests at night.",
    "A rotating Burgomaster privately looks at one living character.",
    "A sealed-style bet on who owns the Werewolf, with an unused seal worth 1.",
    "A day lynch of one character.",
    "The end comes when the Werewolf is lynched or has killed all other characters (outright Werewolf win).",
    "Scoring of 2 per living character, a chest bonus, bet value and unused seal."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The hidden-character and chest-location deduction is a strong reasoning core. The physical mechanics, luck-based coins, payoff-less Thief and all-or-nothing Werewolf seat can all be fixed within the limits."
  },
  "variation": {
    "name": "Lupusburg Ledger",
    "summary": "A text-only Lupusburg for 4-6 players. Secret night choices hide who the Werewolf and Thief are. The Thief steals the first chest he finds. A rotating Burgomaster peeks at one character each day. Players exchange one simultaneous message, then lynch a house and may make one public, time-decaying accusation of who owns the Werewolf. The Werewolf wins outright by killing every other character; otherwise the highest point total wins.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP. Seats are numbered 1..N (N = 4 to 6). Each player owns two houses, Left and Right. Each house hides one character.\n\nThe engine deals characters secretly. Exactly one house in the game holds the Werewolf and exactly one holds the Thief, owned by two different players, each in a random one of that player's houses. Every other house holds a Townsfolk.\n\nEach player has a chest under exactly one of his houses. For the Werewolf's owner and the Thief's owner, the chest is under their other house, because the Werewolf and Thief can never be under a chest. For every other player, the chest side is random.\n\nEach player privately learns the characters under both of his own houses and his own chest side. Everyone knows the dealing rules.\n\nEach player also has one unused accusation.\n\nROUNDS. The game runs in rounds. The Burgomaster in round r is the r-th seat in turn order, counting from seat 1 and skipping players who have no living house.\n\nEach round has these steps, in order:\n\n1. NIGHT. Every player, at the same moment, secretly names one living house (owner and side). Only two choices take effect.\n   a. If the Thief's house is alive and the Thief named another player's living house, the Thief privately learns whether that house hides a chest. If it does, and he has not stolen before, he steals that chest. It is then publicly announced that 'a chest was stolen from player X'; the Thief is not named.\n   b. If the Werewolf's owner named a living house other than the Werewolf's own house, that house is killed and removed. It may be one of his own houses. Its character is not revealed. Only the owner and side are announced, and the Werewolf's kill count rises by 1.\n   All other players' night choices are ignored.\n\n2. SLAUGHTER CHECK. If no living non-Werewolf character remains, the Werewolf's owner wins alone and the game ends.\n\n3. PEEK. The Burgomaster privately names one living house belonging to another player and privately sees its character.\n\n4. TALK. Every player, at the same moment, writes one short message, which may be true or false. All messages are then shown to everyone. Nothing said is binding.\n\n5. VOTE AND ACCUSE. Every player, at the same moment, names one living house to lynch. Players whose houses are all removed still vote.\n   Any player who still holds his accusation may also, in the same step, name another player as the owner of the Werewolf. This uses up his accusation. Its value is fixed by the round in which it is made: 4 in round 1, 3 in round 2, 2 in round 3, 1 in round 4 or later.\n   All accusations made this round are then announced publicly, with accuser and target.\n\n6. LYNCH. The house with the most votes is removed. If two or more houses tie for most votes, nobody is lynched. It is announced only whether the lynched house was 'the Werewolf' or 'not the Werewolf'.\n\n7. END CHECK.\n   - If the Werewolf was lynched, the game ends and is scored.\n   - Otherwise, if no living non-Werewolf character remains, the Werewolf's owner wins alone.\n   - Otherwise, a new round begins.\n   - If round 6 ends with the game unfinished, the game ends and is scored, and the Werewolf's owner adds 2 bonus points.\n\nREMOVED CHESTS. A chest is lost if the house above it is removed or if it is stolen.\n\nSCORING (when the game ends by lynch or after round 6). Each player adds up:\n- 2 points per living house he owns.\n- 2 points if his chest's house is alive and his chest was not stolen.\n- His accusation: its value if correct, 0 if wrong, 1 if never used.\n- The Thief's owner: +2 if he stole a chest and his Thief house is alive.\n- The Werewolf's owner: +1 per successful night kill.",
    "objective": "If, at a slaughter check or the end check, no living non-Werewolf character remains, the Werewolf's owner is the sole winner. Otherwise the player with the highest point total wins. If two or more players share the highest total, the game is a draw.",
    "expected_effect": "Simultaneous night choices hide the acting roles, so deduction rests on kill patterns, the theft announcement, peek claims and votes.\n\nThe chest rule makes information valuable. Learning where a player's chest is (by theft, a peek or a claim) narrows that player's Werewolf candidate to one house.\n\nThe decaying accusation forces a real timing decision: guess early for 4 points, or wait for evidence at a lower value. A never-accuse policy (1 point) loses to anyone who accuses correctly by round 3. A blind round-1 accuser averages about 1 point with high variance. Neither policy is safe.\n\nAs a rough estimate, random lynching gives the Werewolf about 40% outright wins at 5 players. Informed towns should cut that toward roughly 20%, and a Werewolf who survives several rounds also has a points path. This keeps the seat competitive without making it a jackpot; the pipeline should measure whether this balance holds.\n\nTalk passes both tests.\n- Reasoning: the Burgomaster can report or invent a peek, the Werewolf bluffs, and theft victims hunt the Thief.\n- Conflict: the Werewolf wants innocents lynched. Townsfolk compete with each other on points: whose houses survive, who accused first. A theft victim wants the Thief lynched, but lynching any non-Werewolf character brings the slaughter closer.\n- How a follower loses: a player who blindly follows a confident proposal can lynch his own interests away, or copy an accusation a round later at lower value. He can also be led by a lying Werewolf posing as the Burgomaster."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 6
  }
}
```
````
