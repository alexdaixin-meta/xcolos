# 04 design

- time: 2026-10-28T01:35:54+00:00 (79.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 d5cafd17f53ed033, reply sha256 989b31ce86855c50

## Sent

````
Original game: Salem 1692
Players in the original: 4 to 12

Original rules:
Each player gets face-down Tryal cards; any Witch card makes you a Witch forever, even if later lost. One Town Hall power each. Deal 3 playing cards. Put Conspiracy in deck and Night at bottom; set Black Cat aside. At Dawn, Witches eyes-open secretly give Black Cat to any player. First player is Black Cat holder. On your turn you must either draw 2 cards (Black cards revealed and resolved instantly) or play any number of cards on others, never yourself. Green cards are one-shot, Blue stay, Red are accusations. At 7 accusations the accuser reveals one of that player's Tryal cards; if Witch revealed, that player dies. When Conspiracy is drawn, reveal one Tryal on Black Cat holder, then each player takes one unrevealed Tryal from left, becoming Witch if they gain a Witch card. When Night is drawn, all close eyes, Witches choose a kill, Constable chooses a save; if different player, victim dies. Witches win when all non-Witches dead; Town wins when all Witch Tryal cards are revealed.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: WITHIN LIMITS.
* steps_per_round 13 (≤20). Skipping dead seats for 'next living clockwise' adds up to about 4 conditional steps, giving about 17, still ≤20.
* choice_steps 3 (≤4).
* attributes 13 (≤20).
* hidden_elements 3 (roles, Gossip identity, Gossip result) (≤3).
* random_draws_per_round 1 (≤1).
* rounds 6 (≤40).
* Uses only supported features: hidden roles, simultaneous choice, elimination, free-text talk, fixed rounds. No board, judge or clock. Night choices are a simultaneous poll, correctly masking roles.

PROBLEMS.
1) Token rules are incomplete.
   * Step 6 only says tokens carry over on a tie. It does not say what happens when one player leads with fewer than 3 tokens. Is that a carry-over or a reset?
   * A player killed at night keeps their tokens, and tokens reset only on a hanging. It is ambiguous whether a dead player's tokens count in 'strictly more tokens than every other player'. A dead player holding 3 tokens could block or force a tie for every living player.
   These change whether trials happen, so neither the engine nor the players can resolve them from the text.
2) Talk is a single simultaneous message, then an immediate vote.
   * Talk is rightly present (Town and Witch disagree) and rightly simultaneous. But the game's core inference move is a Gossip claim against a Witch counter-claim, and neither can be answered before votes are cast.
   * A trial needs at least 3 votes on one strictly leading player. At 4 alive it needs all 3 Town votes on the Witch.
   * So the Town must coordinate a vote it cannot discuss after seeing the claims. Votes split, ties are frequent, and players are left guessing each other rather than reasoning from replies. This is the 'talk missing where players could then only guess each other' failure.
3) Minor: the rules do not say whether the Constable may protect the same player on consecutive nights. It is allowed by omission, but should be explicit.

Not applicable: the repeated-game check, because this is not a total-score game.
- reasoning_over_luck FAILED: INFORMATION SOURCE. One random check per round on one player: the Gossip's clockwise neighbour.

HIT PROBABILITY PER ROUND. Only the player counter-clockwise of the Witch can learn 'Witch': 1/L.
| N | R1 hit | R1 Gossip is the Witch (useless) | Hit by end of R2 |
|---|---|---|---|
| 5 | 1/5 | 1/5 | ≈ 1/5 + (4/5)(1/4) ≈ 0.40 |
| 6 | 1/6 | 1/6 | ≈ 0.37 |
By the trial arithmetic above, the Town effectively gets 1 trial in N=5 and about 2 in N=6. So about 60-80% of decisive trials happen with no positive information. 'Not the Witch' results clear one player, but they are unverifiable claims.

ALL PLAY WELL (Gossip always claims; the Witch fake-claims Gossip to collide).
* A hit gives two claimants, one of them the Witch. The Town's trial is then about a coin flip, 50%.
* No hit: the Town picks among 3-4 unconfirmed players, about 25-35%.
* The Constable's save is a guess among 2-3 players.

ESTIMATED OUTCOME SPLIT.
| Factor | Share of outcome |
|---|---|
| Chance (whether the Gossip lands on the Witch's neighbour in R1-R2, coin-flip claim collisions, Constable guess, Witch's guess of the Constable at 3 alive) | ~55-65% |
| Reasoning (vote reading, kill-pattern reading, consistency of claims) | the remainder |

VERDICT. There is something to infer, but too little of it arrives in time. A strong Town is not clearly favoured over a random-voting Town: about 0.43 against about 0.36. Chance often decides the winner.
- change: Define tokens fully: dead players' tokens are removed and never count in the trial check; a sole leader with fewer than the threshold keeps tokens (carry-over), the same as a tie.
- change: Replace the fixed threshold of 3 with a living-majority threshold: a player is tried if they have strictly the most tokens AND at least floor(L/2)+1 tokens, where L is the number of living players. At 3 alive this needs 2 votes, so the Town keeps a real final trial.
- change: Make talk two simultaneous rounds before the accusation. In round A all write and all are shown; in round B all write and all are shown; then everyone votes. This makes 4 choice steps, still ≤4, and lets claims and counter-claims be answered and votes coordinated.
- change: Increase information so reasoning outweighs the draw, without new hidden elements: tell the Gossip whether the Witch is among its two living neighbours (either side). Alternatively, publicly reveal each round whether the Witch voted for the round's top-token player, as a computed aggregate. The aim is that a well-reasoning Town reaches about 50% wins against about 25-30% for random voting.
- change: State explicitly whether the Constable may protect the same player on consecutive nights.
The variation that was reviewed: Salem 1692: Gossip and Gallows: SETUP. Seat players in a circle, numbered 1..N (N = 5 or 6). Deal hidden roles at random: exactly 1 Witch, 1 Constable, and the rest Townsfolk. Each player sees only their own role. Every player starts alive with 0 accusation tokens. The game lasts at most 6 rounds.

EACH ROUND, in this order:
1. GOSSIP DRAW. The engine draws one living player uniformly at random as the Gossip. Only that player is told they were drawn.
2. GOSSIP RESULT. The Gossip is privately told whether the next living player clockwise from them is the Witch ("Witch" or "not the Witch"). Nobody else learns who the Gossip was or what they heard. A Witch may be drawn and will simply learn that their neighbour is not the Witch.
3. TALK. Every living player writes one short message at the same time, without seeing the others. Then all messages are shown to everyone. Players may claim, accuse, lie or stay vague. Nothing said is binding.
4. ACCUSATION. All living players simultaneously name one other living player (never themselves). Each named player gains 1 accusation token per vote.
5. ANNOUNCE. All votes and every player's token total are made public.
6. TRIAL CHECK. If one player has strictly more tokens than every other player AND has at least 3 tokens, that player is tried. If two or more players tie for the most tokens, nobody is tried this round and tokens carry over.
7. TRIAL. The tried player's role is revealed to all.
   - If they are the Witch, the game ends immediately and the Town wins.
   - Otherwise they are hanged (eliminated). All players' tokens then reset to 0.
8. PARITY CHECK. If the number of living Witches (1) is at least the number of living non-Witches, the game ends and the Witch wins.
9. NIGHT. Every living player privately names one living player as their night target. Only two choices count:
   - The Witch's choice is the kill. It must be a living non-Witch.
   - The Constable's choice is the protection. It must be a living player other than the Constable.
   Everyone else's choice is ignored. This hides who the active roles are. If the Constable is dead, there is no protection.
10. NIGHT RESOLUTION. If the kill target differs from the protection target, the kill target dies and their role is revealed. If they are the same, nobody dies, and it is announced only that the night passed peacefully.
11. PARITY CHECK. Repeat the check in step 8.
12. ROUND END. If this was round 6 and the Witch is still alive, the game ends and the Witch wins. Otherwise start the next round.

Dead players take no further part, receive no tokens and are skipped when finding the next living player clockwise. Winner: Team game. The Town (Constable and all Townsfolk, alive or dead) wins together if the Witch is tried and revealed. The Witch wins if, after a trial or a night, living non-Witches are no more numerous than the living Witch (1 versus 1), or if the Witch is still alive at the end of round 6. There are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Salem 1692 is a social-deduction card game for 4 to 12 players. Hidden Witches, whose number can grow when Tryal cards pass between players, kill at Night while the Town plays accusation cards to force Tryal reveals, and Witch status spreads through a Conspiracy card. The Town wins by revealing every Witch Tryal card; the Witches win when all non-Witches are dead.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. If the Town always accuses the same player, the Witch hides and kills. If the Witches kill at random, the Constable's saves and accusations catch them. There is no fixed seat advantage beyond a small first-turn effect. In the previous adaptation, a random-voting Town rarely reached the trial threshold, so it lost to stalling. The choices clearly change the outcome."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, card draws decide much: who draws accusation cards, when Conspiracy and Night appear, and which Tryal card the 7th accusation reveals. In the previous adaptation, one random neighbour check gave only a 1/L chance of positive information per round. Testing estimated about 55-65% of outcomes were decided by chance, with a strong Town at about 0.43 against a random Town at about 0.36."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading votes, judging whether claims are consistent, interpreting kill patterns, and the Witch choosing a lie and a victim all reward deeper play without limit. A weak Town still wins sometimes, and a weak Witch can still survive."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Roles are hidden, so every decision rests on inferring who is lying. In the previous adaptation too little information arrived in time to infer from. The fix is a two-neighbour check given only to non-Witches, which makes every round's private result informative."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Win conditions are factual: a Witch is revealed, or parity is reached, or the round limit passes. In the previous adaptation, though, the token rules (sole leader below the threshold, dead players' tokens) were undefined, so whether a trial happens could not be computed from the text. This revision defines them."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original has dozens of distinct card effects, multiple Tryal cards per player, Tryal passing that changes roles, a variable number of Witches and up to 12 players. This far exceeds 3 hidden elements and 20 steps. A cut-down version with 1 Witch, 1 Constable, a Gossip draw, talk, votes and a night poll fits inside the limits, as the previous test confirmed (13 to 17 steps)."
    }
  ],
  "problems": [
    "Original: the card engine is too large for the platform: many card types, multiple Tryal cards, Tryal passing at Conspiracy, a growing Witch team and up to 12 players.",
    "Original: luck in draws (accusation cards, the timing of Night and Conspiracy, which Tryal is revealed) swamps reasoning.",
    "Previous variation: the token rules were incomplete. It did not say whether a sole leader below the threshold carries tokens over or resets, or whether a dead player's tokens count in the 'strictly most' check. So whether a trial happens could not be decided.",
    "Previous variation: the fixed threshold of 3 tokens made late trials nearly impossible to coordinate and did not scale with the living count.",
    "Previous variation: one simultaneous message followed at once by the vote meant claims and counter-claims could never be answered. The Town had to coordinate a near-unanimous vote blind, so it guessed rather than reasoned.",
    "Previous variation: too little information. The Gossip checked one neighbour and could be the Witch, so it had only about a 1/L chance per round of positive information. About 60-80% of decisive trials happened with no evidence, and chance decided about 55-65% of outcomes.",
    "Previous variation: it did not say whether the Constable may protect the same player on consecutive nights."
  ],
  "changes": [
    {
      "what": "Keep the cut-down cast from the previous variation: 5 or 6 players, 1 Witch, 1 Constable, the rest Townsfolk. Replace the card engine with a Gossip draw, talk, an accusation vote and a night poll.",
      "why": "This keeps hidden Witches, accusation pressure, night kills and the Constable's save, inside the step and hidden-element limits.",
      "fixes": "Original: the card engine is too large for the platform: many card types, multiple Tryal cards, Tryal passing at Conspiracy, a growing Witch team and up to 12 players."
    },
    {
      "what": "Define tokens fully. A sole leader below the threshold keeps all tokens, as does every other player, the same as a tie. A night victim's tokens are removed and never count. After a hanging, every living player's tokens reset to 0. Only living players' tokens are compared in the trial check.",
      "why": "The trial check now follows from the rules by arithmetic.",
      "fixes": "Previous variation: the token rules were incomplete. It did not say whether a sole leader below the threshold carries tokens over or resets, or whether a dead player's tokens count in the 'strictly most' check. So whether a trial happens could not be decided."
    },
    {
      "what": "Use a living-majority threshold. A player is tried if they alone hold the most tokens and hold at least floor(L/2)+1 tokens, where L is the number of living players. That is 4 at 6 alive, 3 at 5 or 4 alive, and 2 at 3 alive.",
      "why": "Trials then need real Town coordination but stay reachable, including a final 2-vote trial at 3 alive. Carried-over tokens let pressure build across rounds.",
      "fixes": "Previous variation: the fixed threshold of 3 tokens made late trials nearly impossible to coordinate and did not scale with the living count."
    },
    {
      "what": "Hold two simultaneous talk rounds before the vote. In round A everyone writes and all messages are shown. In round B everyone writes and all messages are shown. Then everyone votes.",
      "why": "Gossip claims can now be challenged, counter-claims answered and a vote target agreed in the open. The Witch must also keep its lie consistent under questioning.",
      "fixes": "Previous variation: one simultaneous message followed at once by the vote meant claims and counter-claims could never be answered. The Town had to coordinate a near-unanimous vote blind, so it guessed rather than reasoned."
    },
    {
      "what": "Draw the Gossip only from living non-Witches. The Gossip learns whether the Witch is among its two nearest living neighbours, one on each side.",
      "why": "Every round now produces true information that narrows the suspects. At 5 alive, either answer cuts the Gossip's suspects from 4 to 2. The Witch can still pose as the Gossip, so the Town must judge which claim is true. The information also builds up over rounds and against the revealed roles of the dead.",
      "fixes": "Previous variation: too little information. The Gossip checked one neighbour and could be the Witch, so it had only about a 1/L chance per round of positive information. About 60-80% of decisive trials happened with no evidence, and chance decided about 55-65% of outcomes."
    },
    {
      "what": "The Constable may not protect the same player on two consecutive nights, and may never protect themself.",
      "why": "This makes the rule explicit. It stops a lock on the confirmed Gossip and makes the Witch's kill choice a real read of the Constable.",
      "fixes": "Previous variation: it did not say whether the Constable may protect the same player on consecutive nights."
    },
    {
      "what": "Reveal the role of every player who dies at night.",
      "why": "If the Witch kills a true Gossip claimant, that player's revealed role exposes the rival claimant. This links the kill choice to the information war and replaces luck with inference.",
      "fixes": "Original: luck in draws (accusation cards, the timing of Night and Conspiracy, which Tryal is revealed) swamps reasoning."
    }
  ],
  "keeps": [
    "A hidden Witch hiding among the Town and killing at night.",
    "The Constable's secret night protection, which cancels the kill if it matches.",
    "Accusations that build up as tokens until they force a trial.",
    "A trial that reveals the accused: a Witch ends the game for the Town; an innocent is hanged and the cost is paid in lives.",
    "Team victory: the Town wins by exposing the Witch, the Witch wins by thinning the Town.",
    "Open talk with bluffing, false claims and reading accusers."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The adaptation already fits the limits. Defining the token rules, using a majority threshold, adding two talk rounds and giving the Gossip a richer check fix the playability and luck failures without adding hidden elements or random draws."
  },
  "variation": {
    "name": "Salem 1692: Gossip and Gallows (revised)",
    "summary": "One hidden Witch, one Constable and Townsfolk play up to 6 rounds. Each round a random innocent Gossip privately learns whether the Witch sits beside them. Then come two rounds of open talk, a public accusation vote that builds tokens toward a majority trial, and a night in which the Witch kills and the Constable protects.",
    "players": {
      "min": 5,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP. Seat the players in a circle, numbered 1 to N (N = 5 or 6). Deal hidden roles at random: exactly 1 Witch, 1 Constable, and the rest Townsfolk. Each player sees only their own role. Every player starts alive with 0 accusation tokens. The game lasts at most 6 rounds.\n\nTERMS. L is the number of living players at the moment of checking. A player's 'living neighbours' are the nearest living player clockwise and the nearest living player counter-clockwise, skipping dead players. When L = 3, these are simply the other two living players. Dead players take no further part, cannot vote, cannot be voted for and hold no tokens.\n\nEACH ROUND, in this order:\n1. GOSSIP DRAW. The engine draws one living player uniformly at random from the living players who are NOT the Witch. That player is the Gossip and is told so privately. Nobody else learns who the Gossip is.\n2. GOSSIP RESULT. The Gossip is privately told either 'The Witch IS one of your two living neighbours' or 'The Witch is NOT one of your two living neighbours'. Nobody else learns the result.\n3. TALK A. Every living player writes one short message at the same time, without seeing the others. Then all messages are shown to everyone. Players may claim to be the Gossip, claim any role, accuse, lie or stay silent. Nothing said is binding.\n4. TALK B. Every living player again writes one short message at the same time, having seen all the Talk A messages but not each other's Talk B messages. Then all are shown to everyone.\n5. ACCUSATION. All living players simultaneously name one other living player, never themselves. Each named player gains 1 accusation token per vote received. Tokens from earlier rounds are kept.\n6. ANNOUNCE. Every vote and every living player's token total are made public.\n7. TRIAL CHECK. Let T = floor(L/2) + 1: T is 4 when 6 are alive, 3 when 5 or 4 are alive, and 2 when 3 are alive. If exactly one living player holds strictly more tokens than every other living player, AND that player holds at least T tokens, that player is tried. Otherwise nobody is tried this round, and every player keeps their tokens. This applies both to a tie for the most tokens and to a sole leader with fewer than T tokens.\n8. TRIAL. The tried player's role is revealed to all. If they are the Witch, the game ends immediately and the Town wins. Otherwise they are hanged (eliminated), and every living player's tokens reset to 0.\n9. PARITY CHECK. If the Witch is alive and there is at most 1 living non-Witch, the game ends and the Witch wins.\n10. NIGHT. Every living player privately names one living player as their night target. Only two choices count:\n    - The Witch's choice is the kill. It must be a living player other than the Witch.\n    - The Constable's choice is the protection. It must be a living player other than the Constable, and it may NOT be the same player the Constable protected on the previous night.\n    Everyone else's choice is ignored; everyone names a target so that nobody can tell who holds an active role. If the Constable is dead, there is no protection.\n11. NIGHT RESOLUTION. If the kill target is different from the protection target, the kill target dies, their role is revealed to all, and their tokens are removed. The other players' tokens are unchanged. If the two targets are the same, nobody dies, and it is announced only that the night passed peacefully. The engine records the Constable's protection target for the next night's restriction.\n12. PARITY CHECK. Repeat the check in step 9.\n13. ROUND END. If this was round 6 and the game has not ended, the Witch wins. Otherwise begin the next round.",
    "objective": "Team game, no draws. The Town (the Constable and all Townsfolk, alive or dead) wins together the moment the Witch is tried and revealed. The Witch wins if, after a trial or a night, the Witch is alive and at most 1 non-Witch is alive, or if the Witch is still alive at the end of round 6.",
    "expected_effect": "The Gossip is always innocent and checks two neighbours, so every round adds real evidence. Over 2-3 rounds a Town that tracks claims against seating and against the roles revealed at death can narrow the Witch down. The Witch's counter-play takes thought:\n- choosing a fake Gossip claim that frames innocents but stays consistent across rounds;\n- deciding whether to kill a rival claimant, which exposes the Witch if that claimant is revealed as Townsfolk;\n- guessing the Constable's protection, now limited by the no-repeat rule.\n\nThe two talk rounds let claims be challenged and votes coordinated. The majority threshold with carry-over tokens rewards building a case, while a Town that votes at random rarely reaches the threshold and loses to the round limit or to kills. Expected results: a strong Town wins about 50-55% against a strong Witch, and a random-voting Town about 20-30%.\n\nTalk passes both tests:\n- Reasoning: claims, challenges, consistency checks and coordinating votes all happen in talk.\n- Conflict: the Witch and the Town want opposite outcomes, and the Witch's whole game is a proposal that sounds safe. A Townsperson who simply follows the loudest Gossip claim may be following the Witch's fake claim. That hangs an innocent, costs the Town a life and moves the Witch toward parity, so blind following loses."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 6
  }
}
```
````
