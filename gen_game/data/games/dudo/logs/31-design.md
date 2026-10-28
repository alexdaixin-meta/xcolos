# 31 design

- time: 2026-10-28T05:57:54+00:00 (46.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 5583bcfafb026339, reply sha256 058ddbc9b181a4f5

## Sent

````
Original game: Dudo
Players in the original: 2 to 10

Original rules:
Each player starts with 5 dice and a cup. Each round all players shake and conceal their dice, then look at only their own. In clockwise order starting from the loser of last round, players bid: a number and a face, claiming at least that many dice among all players show that face. Ones are wild and count as any face. A bid must increase either the quantity, the face value, or both. Bidding aces is special: to switch to aces you may halve the current quantity rounded up; to switch from aces you must more than double the quantity. Instead of raising, a player may call Dudo. All cups are lifted. If the bid is true (at least as many dice as claimed), the caller loses one die; otherwise the bidder loses one die. Losing your last die eliminates you. Last player with dice wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: **Limits.** The stated complexity is 16 steps (≤ 20), 4 choice steps (≤ 4), 13 attributes (≤ 20), 1 hidden element (≤ 3), 1 random draw per round (≤ 1) and 9 rounds (≤ 40). All are within limits.
- Steps 4 and 5 and the resolution can be done with per-step `when` conditions on a stored 'challenger' and 'bid maker'. That is arithmetic conditional scoring, not block selection.
- Exactly one die is lost per round, so the game ends within 9 rounds.
- The game uses no board, judge, clock, trading or binding agreements.
- With 2 players and no need for talk, omitting talk is correct.
- Ones being wild, the bid order (quantity first, then face) and the Q ≤ T cap are unambiguous.

**Gap.** The opening may legally be 'T sixes' because Q ≤ T is allowed. Step 4 can also produce T sixes. The rule 'if the current bid already has quantity T and face 6, the responder must call Dudo' covers only step 5.
- At step 3 (responder) or step 4 (opener), facing T sixes, no raise exists.
- An attempted raise is 'replaced by the lowest higher bid', which does not exist, so the outcome is undefined.

This matters in practice. At T = 2, opening '2 sixes' while holding a 1 or 6 is a real tactic: it is true with probability 1/3 and leaves the responder no legal raise. A model with only these words cannot resolve that case.
- change: Extend the forced-Dudo rule to every answer step: 'At step 3, 4 or 5, if the current bid has quantity T and face 6, the player to act must call Dudo; any other response is treated as Dudo.' Alternatively, forbid opening or raising to T sixes.
- change: Optional: also state that an unreadable response at steps 3–5 is treated as the lowest legal raise only when one exists, and otherwise as Dudo.
The variation that was reviewed: Four-Bid Dudo: SETUP: Two players, each with 5 six-sided dice. Seat 1 is the opener in round 1. After that the opener role alternates every round. The other player is the responder.

TERMS: A bid is two whole numbers, a quantity Q and a face F, where F is 2, 3, 4, 5 or 6. It claims that at least Q dice on the whole table show F, counting every die showing 1 as also showing F (ones are wild; 1 cannot be bid as a face). Bid B is higher than bid A if B's quantity is larger, or the quantities are equal and B's face is larger. A raise must be higher than the current bid. Quantity can never exceed T, the total dice in play. If a player submits an illegal or unreadable bid, it is replaced by the lowest legal bid: the lowest higher bid, or Q0 twos for an opening. This replacement is announced.

EACH ROUND:
1. Roll. All dice in play are rolled. Each player privately sees only their own dice. T is the total dice in play, and Q0 = ceil(T/3) (for example, T=10 gives Q0=4, T=9 gives 3, T=2 gives 1). Both players are told T, Q0 and each player's dice count.
2. Opening (opener). The opener makes a bid with quantity at least Q0, and it is announced. It becomes the current bid.
3. Answer (responder). The responder either calls Dudo on the current bid, or raises; the raise is announced and becomes the current bid. If Dudo is called, go to Resolution.
4. Answer (opener; only if no Dudo yet). The opener either calls Dudo on the current bid, or raises; the raise is announced and becomes the current bid. If Dudo is called, go to Resolution.
5. Final answer (responder; only if no Dudo yet). The responder either calls Dudo on the current bid, or makes a final raise. A final raise is announced and is then resolved immediately as if the opener had called Dudo on it. If the current bid already has quantity T and face 6, the responder must call Dudo.

RESOLUTION: All dice are revealed. Count the dice showing the bid face plus all dice showing 1. If the count is at least the bid quantity, the bid is true and the challenger loses one die (for a final raise, the challenger is the opener). Otherwise the bid is false and the player who made the bid loses one die. The result and both dice counts are announced.

END OF ROUND: If a player has 0 dice, they are eliminated and the other player wins. Otherwise the opener role passes to the other player and a new round begins. Exactly one die is lost every round, so the game ends within 9 rounds. Winner: The last player with dice wins: as soon as a player's dice count reaches 0, the opponent wins. Draws cannot occur.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Dudo (Perudo) is a bluffing dice game for 2 to 10 players. Each player hides a cup of dice, players make rising claims about how many dice of a face exist across all cups (ones are wild), and anyone may call 'Dudo' to challenge the standing claim. The loser of each challenge loses a die, and the last player holding dice wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies all lose. 'Always call Dudo' loses to an opener who bids near the expected count. 'Always raise by the minimum' walks into a challenge on an impossible bid. 'Always bid high' is caught. Seat advantage from bidding first is balanced by rotating who starts. Every choice moves the probability of losing a die."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Each roll is random, but losing a die needs a misjudged bid or call. A player who conditions on their own dice and reads the opponent's bids as evidence beats one who does not, over many challenges. In the 2-player cut, the game ends only after 5 lost dice, which averages out the luck of single rolls."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Basic play is easy to learn: bid about a third of the table plus your own matches. Strong play is not solved within a few rounds. It needs Bayesian updating on bids, bluffing about which face you hold, adjusting as dice counts shrink, and exploiting the opponent's calling tendencies. A weak player still wins some challenges."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Every die is hidden from the opponent. Each bid is a signal that may be honest or a bluff. Deciding to raise or challenge requires inferring the opponent's dice from their bids and modelling whether they bluff."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "A challenge is settled by counting the dice showing the bid face plus ones against the bid quantity. Elimination follows from dice counts. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original has up to 10 players and 50 dice. Its bidding chain is unbounded within a round, so the round has no fixed step count. Ace-switching (halve, or more than double) adds rule branches. A long multi-player elimination can exceed the step and round limits. The previous 2-player, four-bid cut fits the limits, but it left the 'T sixes' dead end undefined at steps 3 and 4."
    }
  ],
  "problems": [
    "The unbounded bidding chain gives a round no fixed number of steps, which the engine needs (at most 20 steps and 4 choices per round).",
    "With up to 10 players the game is long and has a large hidden state, and players knocked out early sit idle.",
    "Ace-switching rules (halve rounded up, or more than double) add branches that models misapply and that cost steps.",
    "Gap in the previous variation: the highest possible bid, T sixes, can be the current bid at step 3 (after an opening of T sixes) or at step 4 (after the responder raises to T sixes). No raise exists there, so the rule 'an illegal raise is replaced by the lowest higher bid' is undefined. Forced Dudo was stated only for step 5.",
    "Gap in the previous variation: the rule for an unreadable response did not say what happens when no legal raise exists, and did not say whether an unreadable response could be read as Dudo."
  ],
  "changes": [
    {
      "what": "Two players only, 5 dice each, with the opener role alternating every round.",
      "why": "This keeps the hidden state small and the game short (at most 9 rounds, since exactly one die is lost per round). Alternation removes any seat edge.",
      "fixes": "With up to 10 players the game is long and has a large hidden state, and players knocked out early sit idle."
    },
    {
      "what": "Each round is capped at four bidding actions: opening, answer, answer, and a final answer. A final raise is resolved immediately as if the opener had challenged it.",
      "why": "Every round then has a bounded, flat step list within 4 choice steps, using per-step 'when' conditions only.",
      "fixes": "The unbounded bidding chain gives a round no fixed number of steps, which the engine needs (at most 20 steps and 4 choices per round)."
    },
    {
      "what": "Ones are wild but can never be bid as a face. Bid order is quantity first, then face. The opening quantity floor is Q0 = ceil(T/3) and the cap is T.",
      "why": "This removes ace-switching while keeping the wild ones that make Dudo recognisable. The floor stops trivially safe openings.",
      "fixes": "Ace-switching rules (halve rounded up, or more than double) add branches that models misapply and that cost steps."
    },
    {
      "what": "Forced Dudo at every answer step. At steps 3, 4 and 5, if the current bid is quantity T and face 6, the player to act must call Dudo, and any other response counts as Dudo. Opening or raising to T sixes stays legal.",
      "why": "This defines the only dead end in the bid order. It keeps the real tactic of a 'T sixes' bid that forces the opponent to challenge, which is true with probability 1/3 at T=2 when you hold a 1 or a 6.",
      "fixes": "Gap in the previous variation: the highest possible bid, T sixes, can be the current bid at step 3 (after an opening of T sixes) or at step 4 (after the responder raises to T sixes). No raise exists there, so the rule 'an illegal raise is replaced by the lowest higher bid' is undefined. Forced Dudo was stated only for step 5."
    },
    {
      "what": "Explicit default rule. An unreadable or illegal opening becomes Q0 twos, which always exists. An unreadable or illegal answer becomes the lowest legal raise if one exists, and otherwise Dudo. The response is counted as Dudo only if it clearly says Dudo, or if no raise exists. Every replacement is announced.",
      "why": "Every response then has exactly one defined outcome.",
      "fixes": "Gap in the previous variation: the rule for an unreadable response did not say what happens when no legal raise exists, and did not say whether an unreadable response could be read as Dudo."
    }
  ],
  "keeps": [
    "Concealed dice: each player sees only their own.",
    "Rising bids of 'at least Q dice show face F' across the whole table.",
    "Ones are wild.",
    "Calling Dudo to challenge. A true bid costs the caller a die and a false bid costs the bidder a die.",
    "Losing dice shrinks your information and the table total.",
    "The last player with dice wins (elimination)."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game is a strong hidden-information bluffing game. The capped two-player form fits the limits, and the only defect found (the undefined T-sixes dead end) is closed by extending forced Dudo to every answer step."
  },
  "variation": {
    "name": "Four-Bid Dudo",
    "summary": "Two-player Dudo with wild ones, a four-action cap on bidding each round, an alternating opener and elimination at 0 dice. When the current bid is the maximum (T sixes), the player to act must call Dudo.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "SETUP: There are two players, each starting with 5 six-sided dice. Seat 1 is the opener in round 1. After that the opener role alternates every round. The other player in a round is the responder.\n\nTERMS: A bid is two whole numbers: a quantity Q and a face F, where F is 2, 3, 4, 5 or 6. It claims that at least Q dice on the whole table show F. Every die showing 1 also counts as showing F (ones are wild). 1 can never be bid as a face. T is the total number of dice in play this round. Q must be between 1 and T. Bid B is higher than bid A if B's quantity is larger, or if the quantities are equal and B's face is larger. A raise must be higher than the current bid. The highest possible bid is 'T sixes'.\n\nDEFAULTS: If the opening is illegal or unreadable, it is replaced by 'Q0 twos'. If an answer is illegal or unreadable, it is replaced by the lowest legal raise: the current quantity with the next higher face, or, if the face is 6, quantity plus 1 with face 2. If no legal raise exists, the answer is replaced by Dudo. Every replacement is announced.\n\nFORCED DUDO: At steps 3, 4 and 5, if the current bid is quantity T and face 6, the player to act must call Dudo. Any other response from them counts as Dudo.\n\nEACH ROUND:\n1. Roll. All dice in play are rolled. Each player privately sees only their own dice. Both players are told T, Q0 = ceil(T/3) and each player's dice count. Examples: T=10 gives Q0=4, T=9 gives 3, T=4 gives 2, T=2 gives 1.\n2. Opening (opener). The opener bids with quantity at least Q0 and at most T, with face 2 to 6. The bid is announced and becomes the current bid.\n3. Answer (responder). The responder either calls Dudo or raises. A raise is announced and becomes the current bid. If Dudo is called, the opener is the bidder and the responder is the challenger; go to Resolution.\n4. Answer (opener; only if no Dudo yet). The opener either calls Dudo or raises. A raise is announced and becomes the current bid. If Dudo is called, the responder is the bidder and the opener is the challenger; go to Resolution.\n5. Final answer (responder; only if no Dudo yet). The responder either calls Dudo or makes a final raise. If Dudo is called, the opener is the bidder and the responder is the challenger. A final raise is announced and resolved immediately, with the responder as bidder and the opener as challenger. The opener makes no further choice.\n\nRESOLUTION: All dice are revealed. Count the dice showing the bid face plus all dice showing 1. If the count is at least the bid quantity, the bid is true and the challenger loses one die. Otherwise the bid is false and the bidder loses one die. The count, the result and both dice counts are announced.\n\nEND OF ROUND: If a player has 0 dice, they are eliminated and the other player wins. Otherwise the opener role passes to the other player and a new round begins. Exactly one die is lost each round, so the game ends after at most 9 rounds.",
    "objective": "Elimination. As soon as a player's dice count reaches 0, the other player wins. Exactly one die is lost per round, so the game always ends within 9 rounds and draws cannot occur.",
    "expected_effect": "Play centres on judging the bid against the expected count: a third of the opponent's dice plus your own matches, including ones. Players read the opponent's bids as evidence about their dice and bluff about which face they hold. Because a bid of T sixes forces Dudo at any answer step, a player can push the opponent into a challenge at the maximum, which matters most late in the game when T is small and every bid is a sharp probability call. The responder's last word (the final raise, resolved as a challenge by the opener) is offset by the opener's control of the opening and by alternating roles. Simple policies lose: always calling Dudo, always raising minimally, and always bidding the maximum are each beaten by a player who bids near the expected count. No talk is used, since with two players talk would only be cheap bluffing already captured by the bids."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 9
  }
}
```
````
