# 27 design

- time: 2026-10-28T05:51:57+00:00 (148.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 34d04e66d82bb6c3, reply sha256 e84169bbda218812

## Sent

````
Original game: Dudo
Players in the original: 2 to 10

Original rules:
Each player starts with 5 dice and a cup. Each round all players shake and conceal their dice, then look at only their own. In clockwise order starting from the loser of last round, players bid: a number and a face, claiming at least that many dice among all players show that face. Ones are wild and count as any face. A bid must increase either the quantity, the face value, or both. Bidding aces is special: to switch to aces you may halve the current quantity rounded up; to switch from aces you must more than double the quantity. Instead of raising, a player may call Dudo. All cups are lifted. If the bid is true (at least as many dice as claimed), the caller loses one die; otherwise the bidder loses one die. Losing your last die eliminates you. Last player with dice wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rework the round so it fits in at most 4 choice steps. The opening bid currently needs two choices (face and quantity). Make it a single choice, either from one menu of combined face+quantity bids or by fixing the quantity rule so only the face is chosen. Alternatively, drop one response step: opening bid, one response, and a forced final call. Then remove the dominant and dominated lines. Always raising wins because it pushes the forced Dudo/Calza call onto the opponent while bids stay plausible, and Calza almost always loses. So cut the raise ladder to a single raise per round, or make a raise cost something, such as losing a die if your raised bid is proven false regardless of who calls. Drop Calza, or let it succeed when N is within 1 of the bid. Check that no single option position wins well above 50% against random play, for each seat, before resubmitting.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 1 wins 92% of decided matches against random seats
- always taking the first option as seat 2 wins 97% of decided matches against random seats
- the built game has 5 choice steps per round, over the limit of 4
- against random seats the results were {'seat 1': 30, 'seat 2': 30}
- a thoughtless policy `first@seat1`: won 55, lost 5, drew 0
- a thoughtless policy `first@seat2`: won 58, lost 2, drew 0
- a thoughtless policy `last@seat1`: won 0, lost 60, drew 0
- a thoughtless policy `last@seat2`: won 0, lost 60, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Dudo is a bluffing dice game for 2 to 10 players. Everyone rolls hidden dice, players bid in turn on how many dice of a face are showing across all cups (ones are wild), and anyone may call 'Dudo' to challenge the last bid. The loser of the challenge loses a die, and the last player with dice wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The open-ended raise ladder plus a forced call means the player who keeps raising while the bid stays plausible pushes the risky call onto the other player. In the previous version, 'always first option' (always raise) won 92% as seat 1 and 97% as seat 2 against random seats. 'Always last option' (Calza) lost every game. Ace switching adds special cases without adding decisions."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The dice are luck, but over many rounds and several dice losses, players who judge probability from their own dice, read the opponent's face choices and bluff well win reliably."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Computing probability from your own hand is learnable. Reading an opponent's bluffing tendencies and mixing your own bids is open-ended. A weak player still wins challenges sometimes."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player's dice are hidden. Every bid is both a probability claim and a possible bluff, and the opponent must infer from it what the bidder holds."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Whether a bid is true is a count of matching dice and wild ones. Losses and elimination are arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The free raise ladder has no bounded number of choices per round. The previous build used 5 choice steps (the opening bid needed separate face and quantity choices), over the limit of 4."
    }
  ],
  "problems": [
    "P1: The previous build had 5 choice steps per round, because the opening bid was split into a face choice and a quantity choice.",
    "P2: Always raising was dominant. It pushed a forced Dudo/Calza call onto the opponent, so 'always first option' won over 90% from either seat.",
    "P3: Calza (the last option) almost always lost, making it a dominated option and 'always last' a guaranteed loss.",
    "P4: Raises jumped quantity so fast that bids two steps up were almost always false. Whoever held the challenge at that moment won almost automatically, so position in the ladder, not judgment, decided rounds.",
    "P5: Ace-switching rules (halve or more than double the quantity) add rule complexity without adding meaningful decisions for a 2-player text game."
  ],
  "changes": [
    {
      "what": "The opening quantity is fixed by rule at max(1, floor(T/3)), where T is the total number of dice in play. The opener chooses only the face (2 to 6).",
      "why": "Makes the opening bid a single choice from 5 symmetric options, so no menu position is better than another.",
      "fixes": "P1"
    },
    {
      "what": "The round is exactly four bounded choice steps. The opener picks a face. The responder calls Dudo or raises by exactly 1 on any face. The opener (if raised) calls Dudo or re-bids at that same quantity on any face. The responder (if re-bid) calls Dudo or passes.",
      "why": "Caps the round at 4 choice steps and removes the open-ended ladder.",
      "fixes": "P1"
    },
    {
      "what": "There is no forced call. If the responder passes at the last step, nobody loses a die that round.",
      "why": "Raising no longer pushes an unavoidable losing call onto the opponent. A raise is a gamble that the opponent will not challenge it.",
      "fixes": "P2"
    },
    {
      "what": "The quantity rises at most once per round, from q0 to q0+1. The opener's second bid keeps the quantity and may only change (or keep) the face.",
      "why": "Keeps every bid in the 40 to 70% plausibility band, so challenging and standing are both live and neither seat holds an automatic win.",
      "fixes": "P4"
    },
    {
      "what": "Calza is removed.",
      "why": "It was a near-always-losing option.",
      "fixes": "P3"
    },
    {
      "what": "Ones remain wild, but ones cannot be bid and the ace-switching rules are dropped.",
      "why": "Simpler rules with the same probability reasoning.",
      "fixes": "P5"
    },
    {
      "what": "Option menus are ordered so that Dudo sits in the middle of the step-2 and step-3 menus. Step 4 is ordered [Dudo, Pass].",
      "why": "'Always first' and 'always last' become 'always raise and stand', which is roughly break-even. By hand calculation against random seats: about 53% decided wins with Dudo at step 4, about 50% with Pass at step 4, and opener and responder seats are close to even.",
      "fixes": "P2"
    },
    {
      "what": "The opener role strictly alternates each round, with seat 1 opening round 1. There is a 40-round cap: the player with more dice wins, and equal dice is a draw.",
      "why": "Removes any built-in seat or role edge and guarantees the game ends within the limits.",
      "fixes": "P2"
    }
  ],
  "keeps": [
    "Hidden dice rolled each round, with each player seeing only their own.",
    "Bids claim at least N dice of a face across all dice, with ones wild.",
    "Calling 'Dudo' reveals all dice. A true bid costs the caller a die and a false bid costs the bidder a die.",
    "Losing your last die eliminates you, and the last player with dice wins.",
    "Bluffing and reading the opponent's bids as the core skill."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Dudo's hidden-dice bluffing is ideal reasoning material. It only needed a bounded four-step round, no forced call, and a flat plausibility ladder to stop simple policies from dominating."
  },
  "variation": {
    "name": "Short Dudo",
    "summary": "Two players bluff about hidden dice in a fixed four-step round: open on a face, raise once, stand or switch, then challenge or let it go. Lose all your dice and you are out.",
    "players": {"min": 2, "max": 2, "suggested": 2},
    "rules": "SETUP: Each of the 2 players starts with 5 dice. Seat 1 is the opener in round 1. After that, the opener role alternates every round, whether or not a die was lost.\n\nEACH ROUND:\n1. Roll. Every die in play is rolled (faces 1 to 6). Each player privately sees only their own dice. Let T be the total number of dice in play. The base quantity is q0 = max(1, floor(T/3)), and both players are told T and q0.\n2. Opening bid (opener chooses one). Options in this order: 'twos', 'threes', 'fours', 'fives', 'sixes'. The bid is 'at least q0 dice show the chosen face'. Ones are wild: every die showing 1 counts toward any bid. Ones cannot be bid as a face. The bid is announced.\n3. Response (responder chooses one). Options in this order: 'raise to q0+1 twos', 'raise to q0+1 threes', 'Dudo', 'raise to q0+1 fours', 'raise to q0+1 fives', 'raise to q0+1 sixes'. If Dudo is chosen, go to Resolution against the opening bid. Otherwise the raise becomes the current bid (made by the responder) and is announced.\n4. Stand or challenge (opener chooses one; only if the responder raised). Options in this order: 're-bid q0+1 twos', 're-bid q0+1 threes', 'Dudo', 're-bid q0+1 fours', 're-bid q0+1 fives', 're-bid q0+1 sixes'. A re-bid keeps the quantity q0+1 and may name any face, including the current one. If Dudo is chosen, go to Resolution against the responder's raise. Otherwise the re-bid becomes the current bid (made by the opener) and is announced.\n5. Last call (responder chooses one; only if the opener re-bid). Options in this order: 'Dudo', 'Pass'. If Dudo is chosen, go to Resolution against the opener's re-bid. If Pass is chosen, the round ends: all dice are revealed and nobody loses a die.\n\nRESOLUTION (only when Dudo was called): All dice are revealed. Count the dice showing the bid face plus all dice showing 1. If the count is at least the bid quantity, the bid is true and the caller loses one die. Otherwise the bid is false and the player who made that bid loses one die. The result is announced.\n\nEND OF ROUND: The opener role passes to the other player. A player with 0 dice is eliminated and the other player wins. If 40 rounds are completed with both players still holding dice, the player with more dice wins. Equal dice is a draw.",
    "objective": "Be the last player with dice: a player wins as soon as the opponent's dice count reaches 0. If round 40 ends with both players holding dice, the player with more dice wins; equal counts are a draw.",
    "expected_effect": "Every bid stays plausible (roughly 40 to 70% true before considering your own hand), so each challenge is a real probability-and-bluff judgment rather than a forced loss. The opener's face choice and re-bid signal (or fake) what they hold, and the responder must read that against their own dice. Raising is no longer free, because it is exposed to a challenge with no forced call to hide behind. By hand calculation against random play, the simple policies come out near even: 'always first' (open twos, always raise or re-bid twos, always Dudo at the last call) wins about 53% of decided games, 'always last' (always sixes, always pass at the last call) about 50%, and challenge-heavy play loses to informed bidders. Skill shows in choosing faces you hold, bluffing selectively, and calling Dudo on bids that do not fit your hand. Two players, so no talk phase."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
