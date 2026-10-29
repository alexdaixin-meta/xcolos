# 04 design

- time: 2026-10-27T08:39:14+00:00 (68.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c2eb28a58ef56477, reply sha256 1b64d3cfa5675a9b

## Sent

````
Original game: Kobayakawa
Players in the original: 3 to 6

Original rules:
Each player gets 4 kamons and one hidden card from a 1-15 deck; one card is revealed as Kobayakawa. Place 8 kamons in the center pot. Each round has a Draw phase: in turn order each player either draws from deck to keep one of the two cards discarding the other face-up, or blindly replaces the Kobayakawa card. Then Fight phase: in order each player chooses to bet 1 kamon to fight or pass. Only fighters reveal. The fighter with the lowest card adds the Kobayakawa value to his total; highest total wins. Winner takes all bet kamons plus 1 from center. Ties broken by earlier turn order. If sole fighter, wins without revealing. Winner becomes start player. Players with 0 kamons are eliminated. Continue until 2 kamons remain in center; last round costs 2 kamons to fight and winner takes both remaining. Most kamons at end wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: Every round is a fresh deal of one card per player, and nothing carries between rounds except kamons. Information available before the fight: the public K, discards from drawers only, the KEEP/DRAW/SHIFT labels and cheap talk. The fight choice is simultaneous, which removes the original game's main inference: later players can no longer see who has already committed.

A good reasoner's edge comes mainly from folding hands that are weak for this K and choosing DRAW or SHIFT well. That is worth roughly +0.1 to +0.3 kamons per round over always-fight. Per-round outcome swings are about ±1 to 3 kamons, so the standard deviation over 10 rounds is about 4 to 5 kamons, against a skill edge of about 1 to 3. The good reasoner is therefore not clearly favoured. I estimate that 60-70% of results are decided by the deal.

With all players using the same sensible strategy (draw, fold weak-for-K hands, fight otherwise), the winner is set by who was dealt K-favourable cards in contested rounds, i.e. by the deal alone. Bluffing is weak: a sole fighter wins unrevealed, but with simultaneous choice only talk can deter anyone, and talk is free and non-binding.
- change: Make the FIGHT step a sequential choice in seat order, starting with the previous pot winner and otherwise rotating each round. Each player sees earlier FIGHT/PASS decisions before choosing, which restores reading of opponents' commitments. Keep total ties carrying the pot (as now) rather than breaking them by seat, so order gives no automatic edge.
- change: Add a bet size: a fighter stakes 1 or 2 kamons (2 or 3 in round 10). A fighter may stake more than the minimum only if every earlier fighter staked the same or less. The pot winner takes all stakes. This lets confidence and bluffs be expressed and punished, increasing the reward for opponent modelling.
- change: Carry information across rounds: a player who passes keeps their hand card into the next round, while fighters and drawers receive a fresh card. Repeated KEEP/PASS histories and discards then become evidence to infer from, and the share of results set by each round's fresh deal falls well below half.
The variation that was reviewed: Kobayakawa: Simultaneous Duel: SETUP: Each player starts with 4 kamons. The centre holds 11 kamons. The pot starts at 0. The game lasts 10 rounds, or ends sooner if only one player remains.

EACH ROUND:
1. DEAL (the round's only random event). Shuffle a deck of cards numbered 1 to 15. Each active player receives one HAND card, seen only by that player, and one RESERVE card, face down and unseen by anyone. Two more cards are dealt: the KOBAYAKAWA, face up for all to see, and the ALTERNATE, face down.
2. ANNOUNCE. The engine announces the round number, the Kobayakawa value, the current pot, every player's kamon count, and the fight cost: 1 in rounds 1-9, 2 in round 10.
3. DRAW CHOICE (simultaneous). Each active player secretly chooses one of three options:
   - KEEP: keep your hand card.
   - DRAW: look at your reserve card.
   - SHIFT: vote to replace the Kobayakawa.
4. Each player who chose DRAW privately sees their reserve card.
5. KEEP CHOICE (simultaneous, drawers only). Each drawer chooses to keep either OLD (the hand card) or NEW (the reserve card). The kept card becomes the hand card. The other card is discarded face up for everyone to see.
6. REVEAL. The engine announces each player's draw choice and all face-up discards.
7. SHIFT. If at least one player chose SHIFT, the alternate card replaces the Kobayakawa and its value is announced. Otherwise the original Kobayakawa stays.
8. TALK (simultaneous). Every active player writes one short message without seeing the others. All messages are then shown to everyone. Talk is not binding, and claims may be false.
9. FIGHT CHOICE (simultaneous). Each active player chooses FIGHT or PASS. A player with fewer kamons than the fight cost must PASS.
10. STAKE. Each fighter pays the fight cost into the pot. The engine then moves centre kamons into the pot: 1 in rounds 1-9, and all remaining centre kamons in round 10.
11. SCORE.
   - If nobody fights, the pot stays where it is and carries into the next round.
   - If exactly one player fights, that player takes the whole pot and their card is not revealed.
   - If two or more fight, all fighters' cards are revealed. Each fighter's total equals their card value, except that the fighter with the lowest card adds the Kobayakawa value to their card. The fighter with the highest total takes the whole pot.
12. TIES. If two or more fighters share the highest total, nobody takes the pot and it carries into the next round. In round 10, the pot is instead divided equally among the tied fighters, rounding down, and any remainder is removed from the game.
13. ELIMINATION. Any player with 0 kamons is eliminated.
14. END CHECK. The game ends after round 10, or as soon as only one active player remains. Winner: When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one player is left before round 10, that player wins.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Kobayakawa is a short bluffing game of hidden single cards. Each round players may improve their card or swap the public Kobayakawa card, then decide in turn whether to pay a kamon to fight. Among the fighters, the lowest card gets the Kobayakawa value added, and the highest total takes the pot. The previous XColos variation made every choice simultaneous and dealt fresh cards every round.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "In the previous variation, always-fight loses to players who fold hands that are weak for this Kobayakawa value. Always-pass stays at 4 kamons while 11 centre kamons and opponents' stakes flow to others, so it almost always loses. No seat has a fixed edge, because a tied total carries the pot."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The tested estimate puts the skill edge at about +0.1 to +0.3 kamons per round, against a standard deviation over 10 rounds of about 4 to 5 kamons. An estimated 60-70% of results came from the deal."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Once a player has learned to fold hands that are weak for this K and to draw sensibly, little remains to improve. Simultaneous fighting removes reading commitments, and the single fixed stake removes any signalling of confidence."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Cards are hidden, but every round was a fresh deal with no carried state. The only evidence was drawers' discards, the choice labels and free talk. Bluffing was nearly powerless, because nobody saw a commitment before making their own."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card totals, pot transfers, ties and the most-kamons winner are all arithmetic on tracked numbers."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is text-only and turn-based, with one deal per round, about 14 steps, 10 rounds, simultaneous and sequential polls, and no board."
    }
  ],
  "problems": [
    "P1: The fight decision is simultaneous, so nobody can read or exploit earlier commitments. The original game's core inference (who has already decided to fight) is lost.",
    "P2: There is a single fixed stake, so confidence cannot be expressed or bluffed, and strong and weak fights look identical.",
    "P3: Every round deals completely fresh cards. Nothing about hands carries over, so histories are worthless as evidence and the deal decides most results (lottery trap with equal sensible strategies).",
    "P4: Bluffing is weak. A sole fighter wins unrevealed, but there is no way to deter others except cheap talk."
  ],
  "changes": [
    {
      "what": "FIGHT becomes a sequential choice in seat order. It starts with the player who won the last pot. If the last pot was not won, it starts with the seat after the previous start player. Everyone sees all earlier decisions and stakes before choosing.",
      "why": "Later players can read commitments, and early players can try to deter others. Rotating the start and carrying tied pots keep any seat from having a built-in edge. The winner acting first next round is a small catch-up brake.",
      "fixes": "P1"
    },
    {
      "what": "Fighters choose LOW (the minimum stake: 1, or 2 in round 10) or HIGH (minimum + 1). Once anyone has fought HIGH, every later fighter in that round must also stake HIGH. Earlier LOW fighters do not top up. The pot winner takes everything.",
      "why": "A raise signals strength or bluffs it, and it raises the price for later callers. Reading stakes becomes part of opponent modelling.",
      "fixes": "P2, P4"
    },
    {
      "what": "Cards carry between rounds. A player who passes keeps their hand card into the next round. Every fighter's card is discarded after the fight, and the fighter gets a fresh card next round.",
      "why": "Holding a strong card until a favourable Kobayakawa appears becomes a multi-round plan. Opponents can infer a held card from a pass history, from discards and from draw behaviour. Fresh luck enters only after fights.",
      "fixes": "P3"
    },
    {
      "what": "Keep the simultaneous talk phase before the fight. Messages are short and shown all at once.",
      "why": "Only one player takes each pot, so claims such as 'I'm holding a high card' are real bluffs or deterrents. Combined with the sequential fight, claims can now be tested against actions.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "One hidden card per player from a 1-15 deck and a public Kobayakawa card.",
    "The lowest-card fighter adds the Kobayakawa value; the highest total takes the pot.",
    "Draw-and-discard-face-up or replace-the-Kobayakawa as the improvement choice.",
    "A sole fighter wins without revealing.",
    "Fighting in turn order starting from the last winner.",
    "A centre pot that releases kamons, with a costlier final round.",
    "Elimination at 0 kamons; most kamons wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Sequential fighting, stake sizes and carried hand cards restore commitment-reading and multi-round planning within the limits."
  },
  "variation": {
    "name": "Kobayakawa: Held Cards",
    "summary": "A 3-5 player bluffing game over 10 rounds. Players hold one secret card, which they keep while they pass. They may improve it or vote to swap the public Kobayakawa, then fight in turn order with a low or high stake. Among fighters, the lowest card adds the Kobayakawa value and the highest total takes the pot. Most kamons wins.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP: Each player starts with 4 kamons and sits in a numbered seat (1 to N). The centre holds 11 kamons and the pot starts at 0. Nobody holds a card. The start player for round 1 is seat 1. The game lasts 10 rounds, or ends sooner if only one player remains.\n\nEACH ROUND:\n1. DEAL (the round's only random event). Shuffle all cards numbered 1 to 15 except the hand cards currently held by players. Each active player without a hand card receives one, seen only by that player. Every active player then receives one RESERVE card, face down and unseen. Then deal the KOBAYAKAWA face up and the ALTERNATE face down.\n2. ANNOUNCE. The engine announces:\n   - the round number;\n   - the Kobayakawa value and the current pot;\n   - each player's kamons;\n   - which players are holding a card kept from an earlier round, and for how many rounds;\n   - the start player;\n   - the minimum stake: 1 in rounds 1-9, 2 in round 10.\n3. DRAW CHOICE (simultaneous). Each active player secretly chooses one option:\n   - KEEP: keep your hand card.\n   - DRAW: look at your reserve card.\n   - SHIFT: vote to replace the Kobayakawa.\n4. Each player who chose DRAW privately sees their reserve card.\n5. KEEP CHOICE (simultaneous, drawers only). Each drawer keeps OLD (the hand card) or NEW (the reserve card) as their hand card. The other card is discarded face up. All undrawn reserve cards are discarded face down, unseen.\n6. REVEAL. The engine announces each player's draw choice and all face-up discards.\n7. SHIFT. If at least one player chose SHIFT, the Alternate replaces the Kobayakawa and its value is announced.\n8. TALK (simultaneous). Every active player writes one short message without seeing the others; all messages are then shown. Talk is not binding and may be false.\n9. FIGHT (sequential). Players act once each in seat order, beginning with the start player and wrapping around. Each player sees all earlier choices.\n   - The REQUIRED STAKE is the minimum stake, or the minimum + 1 if any earlier player this round fought HIGH.\n   - A player chooses PASS, FIGHT LOW (stake = minimum, allowed only while nobody has fought HIGH) or FIGHT HIGH (stake = minimum + 1).\n   - A player must PASS if they have fewer kamons than every stake they are allowed to choose.\n10. STAKE. Each fighter pays their stake into the pot. The engine moves centre kamons into the pot: 1 in rounds 1-9, and all remaining centre kamons in round 10.\n11. SCORE.\n   - Nobody fought: the pot carries to the next round.\n   - Exactly one fighter: that player takes the whole pot, and their card is not revealed.\n   - Two or more fighters: all fighters' cards are revealed. Each fighter's total is their card value. The fighter with the lowest card adds the Kobayakawa value to their total. The highest total takes the whole pot.\n12. TIES. If fighters share the highest total, nobody takes the pot and it carries to the next round. In round 10, the pot is instead split equally among the tied fighters, rounding down, and any remainder is removed from the game.\n13. CLEANUP.\n   - Every fighter's hand card is discarded; that player will receive a fresh card next round.\n   - Every player who passed keeps their hand card, still secret.\n   - The next start player is the pot winner. If nobody won the pot, it is the next active seat after this round's start player.\n14. ELIMINATION. Any player with 0 kamons is eliminated, and their card is discarded unseen.\n15. END CHECK. The game ends after round 10, or as soon as only one active player remains.",
    "objective": "When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one active player remains before round 10, that player wins.",
    "expected_effect": "Results should depend far more on decisions than on the deal.\n\nPlanning: players will hold strong cards across rounds, waiting for a Kobayakawa value that does not reward a low card. Their opponents read long pass streaks as a strong held card (or a bluff setup).\n\nCommitment and stakes: fighting HIGH early deters callers and taxes them, so late seats must decide whether a raise is real. Sole-fighter bluffs become viable when the raise comes from an early seat. Carried cards, discards and pass histories make each opponent's hand partly inferable, which reduces the share decided by fresh cards.\n\nTalk: players disagree because only one fighter takes each pot. A claim like 'I hold 14, stay out' is meant to make others pass. A player who believes it and passes hands the bluffer the pot. A player who ignores it pays a stake against a real strong card.\n\nSimple policies:\n- Always-pass ends near 4 kamons while the 11 centre kamons go to others, so it loses.\n- Always-fight-LOW loses stakes to selective fighters.\n- Always-fight-HIGH is called by strong hands and pays the extra kamon each time.\n- Each can lose.\n\nWith equal sensible play, the hold-or-fight timing, raise reading and seat rotation still separate players. Honest residual luck is moderate, not dominant."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 17,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
