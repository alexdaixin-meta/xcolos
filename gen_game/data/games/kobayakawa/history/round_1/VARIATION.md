# Variation: Kobayakawa: Held Cards

A 3-5 player bluffing game over 10 rounds. Players hold one secret card, which they keep while they pass. They may improve it or vote to swap the public Kobayakawa, then fight in turn order with a low or high stake. Among fighters, the lowest card adds the Kobayakawa value and the highest total takes the pot. Most kamons wins.

Players: 3 to 5, best with 4

## Review of the original

Kobayakawa is a short bluffing game of hidden single cards. Each round players may improve their card or swap the public Kobayakawa card, then decide in turn whether to pay a kamon to fight. Among the fighters, the lowest card gets the Kobayakawa value added, and the highest total takes the pot. The previous XColos variation made every choice simultaneous and dealt fresh cards every round.

- **non_degenerate**: good. In the previous variation, always-fight loses to players who fold hands that are weak for this Kobayakawa value. Always-pass stays at 4 kamons while 11 centre kamons and opponents' stakes flow to others, so it almost always loses. No seat has a fixed edge, because a tied total carries the pot.
- **skill_sensitive**: weak. The tested estimate puts the skill edge at about +0.1 to +0.3 kamons per round, against a standard deviation over 10 rounds of about 4 to 5 kamons. An estimated 60-70% of results came from the deal.
- **headroom**: weak. Once a player has learned to fold hands that are weak for this K and to draw sensibly, little remains to improve. Simultaneous fighting removes reading commitments, and the single fixed stake removes any signalling of confidence.
- **reasoning_dependent**: weak. Cards are hidden, but every round was a fresh deal with no carried state. The only evidence was drawers' discards, the choice labels and free talk. Bluffing was nearly powerless, because nobody saw a commitment before making their own.
- **verifiable**: good. Card totals, pot transfers, ties and the most-kamons winner are all arithmetic on tracked numbers.
- **fits_platform**: good. It is text-only and turn-based, with one deal per round, about 14 steps, 10 rounds, simultaneous and sequential polls, and no board.

## Problems

- P1: The fight decision is simultaneous, so nobody can read or exploit earlier commitments. The original game's core inference (who has already decided to fight) is lost.
- P2: There is a single fixed stake, so confidence cannot be expressed or bluffed, and strong and weak fights look identical.
- P3: Every round deals completely fresh cards. Nothing about hands carries over, so histories are worthless as evidence and the deal decides most results (lottery trap with equal sensible strategies).
- P4: Bluffing is weak. A sole fighter wins unrevealed, but there is no way to deter others except cheap talk.

## Changes

- FIGHT becomes a sequential choice in seat order. It starts with the player who won the last pot. If the last pot was not won, it starts with the seat after the previous start player. Everyone sees all earlier decisions and stakes before choosing. (fixes: P1): Later players can read commitments, and early players can try to deter others. Rotating the start and carrying tied pots keep any seat from having a built-in edge. The winner acting first next round is a small catch-up brake.
- Fighters choose LOW (the minimum stake: 1, or 2 in round 10) or HIGH (minimum + 1). Once anyone has fought HIGH, every later fighter in that round must also stake HIGH. Earlier LOW fighters do not top up. The pot winner takes everything. (fixes: P2, P4): A raise signals strength or bluffs it, and it raises the price for later callers. Reading stakes becomes part of opponent modelling.
- Cards carry between rounds. A player who passes keeps their hand card into the next round. Every fighter's card is discarded after the fight, and the fighter gets a fresh card next round. (fixes: P3): Holding a strong card until a favourable Kobayakawa appears becomes a multi-round plan. Opponents can infer a held card from a pass history, from discards and from draw behaviour. Fresh luck enters only after fights.
- Keep the simultaneous talk phase before the fight. Messages are short and shown all at once. (fixes: P4): Only one player takes each pot, so claims such as 'I'm holding a high card' are real bluffs or deterrents. Combined with the sequential fight, claims can now be tested against actions.

## Kept from the original

- One hidden card per player from a 1-15 deck and a public Kobayakawa card.
- The lowest-card fighter adds the Kobayakawa value; the highest total takes the pot.
- Draw-and-discard-face-up or replace-the-Kobayakawa as the improvement choice.
- A sole fighter wins without revealing.
- Fighting in turn order starting from the last winner.
- A centre pot that releases kamons, with a costlier final round.
- Elimination at 0 kamons; most kamons wins.

## The variation's rules

SETUP: Each player starts with 4 kamons and sits in a numbered seat (1 to N). The centre holds 11 kamons and the pot starts at 0. Nobody holds a card. The start player for round 1 is seat 1. The game lasts 10 rounds, or ends sooner if only one player remains.

EACH ROUND:
1. DEAL (the round's only random event). Shuffle all cards numbered 1 to 15 except the hand cards currently held by players. Each active player without a hand card receives one, seen only by that player. Every active player then receives one RESERVE card, face down and unseen. Then deal the KOBAYAKAWA face up and the ALTERNATE face down.
2. ANNOUNCE. The engine announces:
   - the round number;
   - the Kobayakawa value and the current pot;
   - each player's kamons;
   - which players are holding a card kept from an earlier round, and for how many rounds;
   - the start player;
   - the minimum stake: 1 in rounds 1-9, 2 in round 10.
3. DRAW CHOICE (simultaneous). Each active player secretly chooses one option:
   - KEEP: keep your hand card.
   - DRAW: look at your reserve card.
   - SHIFT: vote to replace the Kobayakawa.
4. Each player who chose DRAW privately sees their reserve card.
5. KEEP CHOICE (simultaneous, drawers only). Each drawer keeps OLD (the hand card) or NEW (the reserve card) as their hand card. The other card is discarded face up. All undrawn reserve cards are discarded face down, unseen.
6. REVEAL. The engine announces each player's draw choice and all face-up discards.
7. SHIFT. If at least one player chose SHIFT, the Alternate replaces the Kobayakawa and its value is announced.
8. TALK (simultaneous). Every active player writes one short message without seeing the others; all messages are then shown. Talk is not binding and may be false.
9. FIGHT (sequential). Players act once each in seat order, beginning with the start player and wrapping around. Each player sees all earlier choices.
   - The REQUIRED STAKE is the minimum stake, or the minimum + 1 if any earlier player this round fought HIGH.
   - A player chooses PASS, FIGHT LOW (stake = minimum, allowed only while nobody has fought HIGH) or FIGHT HIGH (stake = minimum + 1).
   - A player must PASS if they have fewer kamons than every stake they are allowed to choose.
10. STAKE. Each fighter pays their stake into the pot. The engine moves centre kamons into the pot: 1 in rounds 1-9, and all remaining centre kamons in round 10.
11. SCORE.
   - Nobody fought: the pot carries to the next round.
   - Exactly one fighter: that player takes the whole pot, and their card is not revealed.
   - Two or more fighters: all fighters' cards are revealed. Each fighter's total is their card value. The fighter with the lowest card adds the Kobayakawa value to their total. The highest total takes the whole pot.
12. TIES. If fighters share the highest total, nobody takes the pot and it carries to the next round. In round 10, the pot is instead split equally among the tied fighters, rounding down, and any remainder is removed from the game.
13. CLEANUP.
   - Every fighter's hand card is discarded; that player will receive a fresh card next round.
   - Every player who passed keeps their hand card, still secret.
   - The next start player is the pot winner. If nobody won the pot, it is the next active seat after this round's start player.
14. ELIMINATION. Any player with 0 kamons is eliminated, and their card is discarded unseen.
15. END CHECK. The game ends after round 10, or as soon as only one active player remains.

Objective: When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one active player remains before round 10, that player wins.

Expected effect: Results should depend far more on decisions than on the deal.

Planning: players will hold strong cards across rounds, waiting for a Kobayakawa value that does not reward a low card. Their opponents read long pass streaks as a strong held card (or a bluff setup).

Commitment and stakes: fighting HIGH early deters callers and taxes them, so late seats must decide whether a raise is real. Sole-fighter bluffs become viable when the raise comes from an early seat. Carried cards, discards and pass histories make each opponent's hand partly inferable, which reduces the share decided by fresh cards.

Talk: players disagree because only one fighter takes each pot. A claim like 'I hold 14, stay out' is meant to make others pass. A player who believes it and passes hands the bluffer the pot. A player who ignores it pays a stake against a real strong card.

Simple policies:
- Always-pass ends near 4 kamons while the 11 centre kamons go to others, so it loses.
- Always-fight-LOW loses stakes to selective fighters.
- Always-fight-HIGH is called by strong hands and pays the extra kamon each time.
- Each can lose.

With equal sensible play, the hold-or-fight timing, raise reading and seat rotation still separate players. Honest residual luck is moderate, not dominant.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
