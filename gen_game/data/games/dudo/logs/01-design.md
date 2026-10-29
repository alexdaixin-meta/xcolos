# 01 design

- time: 2026-10-28T05:23:00+00:00 (59.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 36f10697a4907ef0, reply sha256 6cd73bbf7dfd2088

## Sent

````
Original game: Dudo
Players in the original: 2 to 10

Original rules:
Each player starts with 5 dice and a cup. Each round all players shake and conceal their dice, then look at only their own. In clockwise order starting from the loser of last round, players bid: a number and a face, claiming at least that many dice among all players show that face. Ones are wild and count as any face. A bid must increase either the quantity, the face value, or both. Bidding aces is special: to switch to aces you may halve the current quantity rounded up; to switch from aces you must more than double the quantity. Instead of raising, a player may call Dudo. All cups are lifted. If the bid is true (at least as many dice as claimed), the caller loses one die; otherwise the bidder loses one die. Losing your last die eliminates you. Last player with dice wins.
````

## Reply

````
```json
{
  "original_summary": "Dudo (Perudo, or Liar's Dice) is a bluffing game for 2 to 10 players. Each player rolls hidden dice. Players then take turns raising a claim about how many dice on the whole table show a face, with ones wild. A player may instead call 'Dudo' to challenge the last claim, and whoever is wrong loses a die. The last player with dice wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every simple policy can lose. 'Always call Dudo' loses to openers who bid only what their own dice guarantee. 'Always raise minimally' eventually makes a false claim and gets challenged. 'Always bid high' gets challenged at once. Seat order rotates, because the loser of a hand opens the next one, so no seat keeps a lasting edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Each hand is noisy, but a game lasts many hands (up to 14 with 3 players). Over that span, estimating the expected count from your own dice plus the unseen dice, and reading what opponents' bids reveal about their dice, reliably beats naive bidding."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win challenges against obviously inflated bids. Strong players gain by inferring hidden dice from bid sequences, bluffing on faces they lack, and timing challenges as dice counts shrink. The game has never been solved at the table."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Every player's dice are hidden. Each bid is a noisy signal of the bidder's hand, so play is probabilistic inference combined with opponent modelling."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "A challenge is settled by counting matching dice plus ones, which is pure arithmetic. Elimination and the last survivor follow directly from that."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Turn-based and text-only, but bidding within a hand has no length limit, which a flat step list with at most 4 choices per round cannot express. The rule for switching to and from aces (halve the quantity, or more than double it) is fiddly to validate. With 10 players a game would run far too long."
    }
  ],
  "problems": [
    "Bidding within a hand can go round the table any number of times, but the engine allows at most 4 choice steps per round and cannot repeat a block of steps conditionally.",
    "The rule for switching to and from bids on aces (halve the quantity rounded up, or more than double it) adds validation complexity with little strategic payoff.",
    "With up to 10 players of 5 dice each, a game could need far more than 40 hands, and a model has to track too much.",
    "The rules do not say what happens after an invalid bid, or who opens the first hand."
  ],
  "changes": [
    {
      "what": "Each round is one hand with at most 4 bidding turns, taken clockwise from the opener and wrapping around. If the 4th turn is a raise rather than a Dudo call, the player who made the previous bid is deemed to call Dudo on that raise.",
      "why": "This bounds a hand at 4 choice steps while keeping the raise-or-challenge tension. The last speaker still decides between challenging and pushing a claim that will be tested.",
      "fixes": "Bidding within a hand can go round the table any number of times, but the engine allows at most 4 choice steps per round and cannot repeat a block of steps conditionally."
    },
    {
      "what": "Ones stay wild but can no longer be bid as a face. Bids name faces 2 to 6 only, and a raise means a higher quantity, or the same quantity with a higher face.",
      "why": "This keeps the defining wild-ones counting and removes the halving and doubling exceptions.",
      "fixes": "The rule for switching to and from bids on aces (halve the quantity rounded up, or more than double it) adds validation complexity with little strategic payoff."
    },
    {
      "what": "The game takes 3 or 4 players with 5 dice each.",
      "why": "The game then needs at most 14 hands (3 players) or 19 hands (4 players), well inside 40 rounds, and keeps the hidden information manageable.",
      "fixes": "With up to 10 players of 5 dice each, a game could need far more than 40 hands, and a model has to track too much."
    },
    {
      "what": "Seating is shuffled at setup and seat 1 opens the first hand. An invalid raise counts as a Dudo call on the standing bid. An opening bid must be valid or its player loses a die.",
      "why": "This closes the gaps in the rules so the engine can resolve every action.",
      "fixes": "The rules do not say what happens after an invalid bid, or who opens the first hand."
    }
  ],
  "keeps": [
    "Hidden dice rolled each hand, seen only by their owner",
    "Escalating claims about how many dice on the whole table show a face",
    "Ones wild",
    "Calling Dudo to challenge, with the wrong party losing a die",
    "The loser of a hand opens the next one",
    "Elimination, with the last player holding dice winning"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Liar's Dice is already a strong game of inference and bluffing. It needs only a bounded bidding structure and a smaller table to fit the engine."
  },
  "variation": {
    "name": "Four-Call Dudo",
    "summary": "Liar's Dice for 3 to 4 players in which each hand allows at most four bids or calls. Ones are wild. Losing a challenge costs a die, and the last player with dice wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "SETUP: Seat the players in a random order (seats 1 to 3 or 1 to 4). Each player starts with 5 dice.\n\nEACH ROUND (one hand):\n1. Every player still in the game rolls all their dice. Each player is privately shown their own faces and no one else's. Everyone is told how many dice each player holds and the total number of dice in play.\n2. The opener is the player who lost a die in the previous hand. If that player was eliminated, the opener is the next surviving player clockwise. Seat 1 opens the first hand.\n3. A bid is a quantity and a face from 2 to 6, for example 'four 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face. Ones cannot be bid as a face.\n4. A raise must name a higher quantity (with any face), or the same quantity with a higher face. The quantity must be at least 1 and at most the total dice in play.\n5. BIDDING: up to four turns are taken in clockwise order starting with the opener, skipping eliminated players and wrapping around if needed. With 3 players the order is opener, next, next, opener. With 2 survivors the two alternate.\n   Turn 1: the opener must make a bid. If it is invalid, the opener loses one die, the hand ends, and no dice are counted.\n   Turns 2, 3 and 4: the player either raises or calls 'Dudo' on the current bid. An invalid raise counts as a Dudo call.\n   As soon as anyone calls Dudo, bidding stops.\n   If turn 4 is a valid raise, the player who made the bid before it is automatically deemed to call Dudo on that raise.\n6. RESOLUTION: All dice are revealed. Count the dice showing the bid face plus all ones.\n   If the count is at least the bid quantity, the bid is true and the challenger loses one die.\n   Otherwise the bid is false and the bidder loses one die.\n7. A player with 0 dice is eliminated.\n8. The loser of the die opens the next hand (see step 2).\n\nEND: The game ends when only one player has dice left. It cannot last more than 19 hands. A limit of 40 rounds exists only as a technical safeguard; if it were ever reached, the player with the most dice would win, and players tied on most dice would share a draw.",
    "objective": "The last player with at least one die wins. Every other player loses. If the 40-round safeguard were reached, the player holding the most dice wins, and a tie for most dice is a draw among those tied.",
    "expected_effect": "Play centres on estimating the likely count: roughly one third of the unseen dice show any given face, since ones count too, plus your own matches. Players also read what earlier bids say about other hands and decide when to bluff. The 4-turn cap gives the last speaker a sharp choice: challenge now, or raise and face an automatic challenge. This makes the timing of raises and the position in the turn order strategic. As dice counts shrink, the estimates must be updated, which rewards careful players. Free talk is deliberately left out: the bids themselves are the signalling and bluffing channel, and chat would add only noise."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
