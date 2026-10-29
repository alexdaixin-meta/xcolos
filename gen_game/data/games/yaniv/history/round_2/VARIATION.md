# Variation: Simultaneous Yaniv

Three to five players hold hidden hands and each round simultaneously either call or discard all cards of one value. They then claim a card another player discarded, or take a shared blind card. Calling when not strictly lowest costs +30. The lowest total wins when someone reaches 100 or after round 30.

Players: 3 to 5, best with 4

## Review of the original

Yaniv is a draw-and-discard card game for 2 to 8 players. Players shed cards to get a low hand total and may call 'Yaniv' when their hand is at or below a threshold. Calling when someone else is as low or lower (Asaf) costs a 30-point penalty, points accumulate across rounds, and players over 200 are eliminated.

- **non_degenerate**: good. No simple policy is safe. Always calling as soon as eligible loses to Asaf penalties against players who hold low hands. Never calling lets opponents end rounds while you hold high cards. Always discarding the highest card is reasonable but predictable, and opponents can exploit it by claiming or baiting. In the reviewed variation, seats are symmetric because choices are simultaneous.
- **skill_sensitive**: good. Timing the call, reading opponents' hand sums from public discards and claims, and avoiding contested claims all accumulate over up to 30 rounds. Deals are random, but many showdowns average the luck out.
- **headroom**: good. A weak player still scores by shedding high cards. A strong player keeps improving through card counting, bluffing in talk, baiting with low offers and calling just before others do.
- **reasoning_dependent**: good. Hands are hidden. Players must infer opponents' hand sums from public discard values, shed counts, claim results and blind draws, and must model who will call.
- **verifiable**: good. All scoring is arithmetic on hand sums and totals.
- **fits_platform**: weak. The reviewed variation fit the counts but had defects. Its ending was undefined after a call in round 30, its fallback broke on an empty hand, its option order was unspecified, its random-draw accounting was vague, and it was implicit which hand sum gates CALL.

## Problems

- P1: The ending is undefined if a call happens in round 30 and no total reaches 100: new hands are dealt but there is no round 31.
- P2: The fallback 'discard H, the highest value in hand' fails when the hand is empty.
- P3: Option order is unspecified, so listings and 'first/last option' policies are not fixed.
- P4: The random-draw accounting is vague: the redeal and setup deal are many cards, described loosely as 'the only random draw'.
- P5: It is implicit, not stated, that next round's CALL eligibility uses the hand_sum recomputed at the end of this round.
- P6 (minor): Hand sizes are not publicly trackable, which weakens inference about opponents' hand sums.

## Changes

- Every showdown in round 30, and any showdown that leaves a total at 100 or more, ends the game immediately after scoring; no new hands are dealt. (fixes: P1): This gives the game a defined end in every case.
- An invalid first-choice answer counts as CALL if the hand is empty, otherwise as 'discard H' with H the highest value in hand. (fixes: P2): The fallback is now always defined.
- First-choice options are listed as CALL first (if available), then 'discard V' by V ascending. Claim options are BLIND first, then 'value V' by V ascending. (fixes: P3): Option order is deterministic.
- The redeal is defined as a single deal operation (5 cards to every player at once) and is the round's one random operation. It happens only in showdown rounds that do not end the game. The blind draw B happens only in rounds with no call, so no round has both. The setup deal is a single operation before round 1. (fixes: P4): This keeps the game at one random draw per round.
- The rules explicitly state that the hand_sum recomputed in step 10 (or after a redeal) is what step 1 of the next round checks against call_limit. (fixes: P5): This removes the ambiguity about CALL eligibility.
- The number of cards each player shed and each player's hand size are announced publicly every round. Hand sizes are public from the start (5). (fixes: P6): This gives players more evidence for inferring opponents' hand sums.

## Kept from the original

- Yaniv card values (Joker 0, Ace 1, faces 10) and hidden hands.
- Shedding cards to get a low hand, with a call threshold of 7.
- The Asaf rule: a caller who is not strictly lowest scores hand sum + 30.
- Taking either a card from the discards or a blind draw, here as one offered card or the blind card.
- Cumulative scoring with the lowest total winning, ended by a total threshold.

## The variation's rules

CARDS
- Card values: Joker = 0, Ace = 1, 2 to 10 = face value, J/Q/K = 10.
- Every random card is drawn from a 54-card shoe: two 0s, four each of 1 to 9, and sixteen 10s.
- The shoe is full for every draw, so it never runs out.
- A hand is a list of values. hand_sum is the sum of the hand. hand_size is the number of cards in it.

PARAMETERS
call_limit = 7; asaf_penalty = 30; end_total = 100; max_rounds = 30.

SETUP
- Every total is 0.
- In one deal operation, each player is dealt 5 random cards, seen only by that player.
- Each player's hand_sum is computed. Each hand_size (5) is public.

EACH ROUND (rounds 1 to 30)
1. Options. Each player's first-choice options are listed in this order:
   - 'CALL', only if their current hand_sum is 7 or less;
   - then 'discard V' for each distinct value V in their hand, V ascending.
   The current hand_sum is the one computed at the end of the previous round (step 10, or after a redeal in step 4), or at setup in round 1.
2. Talk. Everyone writes one short message at the same time without seeing the others; all messages are then shown to everyone.
3. First choice. Everyone answers at the same time with one of their options. An invalid answer counts as follows:
   - CALL if the player's hand is empty;
   - otherwise 'discard H', where H is the highest value in their hand.
4. Showdown, if at least one player chose CALL:
   a. All hands are revealed. L = the lowest hand_sum among all players.
   b. A caller scores 0 if every other player's hand_sum is strictly greater than theirs. Otherwise (Asaf) they score hand_sum + 30.
   c. A non-caller scores 0 if their hand_sum equals L, otherwise their hand_sum.
   d. Each score is added to that player's total. Discards chosen this round are ignored.
   e. If any total is now 100 or more, or this is round 30, the game ends now.
   f. Otherwise, in one deal operation (the round's only random draw), every player's hand is replaced by 5 new random cards, seen only by that player. hand_sums are recomputed, hand_sizes reset to 5 publicly, and the round ends (steps 5 to 11 are skipped).
5. Discard, if no one called:
   - Each player removes every card of their chosen value V from their hand; the hand may become empty. These cards leave play.
   - Each player's V and the number of cards they shed are announced publicly. Each player's offer is one card of value V.
6. Claim options. Each player's options are listed in this order:
   - 'BLIND';
   - then 'value V' for each distinct value offered this round by at least one OTHER player, V ascending.
7. Claim choice. Everyone answers at the same time. An invalid answer counts as BLIND.
8. Resolve claims.
   - A claim on V succeeds if exactly one player claimed V; that player adds one card of value V to their hand.
   - If two or more players claimed the same V, all of them fail.
9. Blind draw. One random card value B is drawn (the round's only random draw).
   - Every player who chose BLIND or whose claim failed adds one card of value B to their hand.
   - Each such player is told B privately.
10. Announce.
   - Every hand_sum is recomputed; this is the value step 1 of the next round uses.
   - Announced publicly for each player: discarded value, number shed, claimed value, success or failure, whether they took the blind card, and new hand_size.
   - B and hand contents stay private.
11. Final showdown, if this is round 30 and no one called this round:
   - All hands are revealed.
   - Each player scores 0 if their hand_sum equals the lowest hand_sum, otherwise their hand_sum. This is added to their total.
   - The game ends.

Objective: The game ends either after a showdown that leaves any total at 100 or more, or after a showdown in round 30 (from a call or the final showdown). The player with the lowest total wins. If two or more players share the lowest total, the game is a draw among them.

Expected effect: The game now always terminates cleanly and is fully deterministic apart from one random operation per round. Public shed counts and hand sizes sharpen inference about opponents' hand sums, so call timing and Asaf traps reward reading the table. Talk passes both tests. Players disagree about when the round should end: a player with a low hand wants a showdown, while others want time to shed. They also compete for offered low cards, since contested claims fail. So a player who follows 'I'm high, don't worry' and holds back can lose: the speaker may be baiting a call they will Asaf, or steering others away from a card they want. With one winner by lowest total and three or more players, no simple policy is safe. Always-call suffers Asaf penalties, never-call eats others' showdowns, and always-claim-the-lowest-offer collides with rivals.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
