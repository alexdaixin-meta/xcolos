# 21 design

- time: 2026-10-28T06:11:15+00:00 (46.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 242d53015c108ca3, reply sha256 3001ac7f6e47560f

## Sent

````
Original game: Yaniv
Players in the original: 2 to 8

Original rules:
Each player is dealt 5 cards from a 54-card deck including jokers. Values: Ace=1, 2-10 face, J/Q/K=10, Joker=0. A draw pile and one upcard discard pile remain. On a turn you may discard: one card, two+ equal rank, or 3+ same-suit consecutive ranks with Ace low. After discarding you must draw one card: top of draw pile or only the first or last card of the previous set from discard. If draw pile empties, reshuffle discards except last play. At start of your turn if hand sum is below the Yaniv threshold (commonly 5-7) you may call Yaniv instead of playing. All hands are revealed. Lowest hand wins the round with 0. Others score their hand sum. If caller is not strictly lowest (Asaf), caller gets hand sum +30 penalty. Total score accumulates across rounds. A player exceeding 200 points is eliminated; last remaining or lowest total when first elimination occurs wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Complexity as stated: 17 steps (limit 20), 3 choice steps (limit 4), 18 attributes (limit 20), 2 hidden elements (limit 3), 30 rounds (limit 40). Talk is simultaneous and sensible: players disagree, and bluffing 'I will call' or 'I'm high' is meaningful given the bait/Asaf trap. Defects:
(1) Ending gap. If a CALL happens in round 30 and no total reaches 100, step 4 deals new hands and says 'the next round begins'. There is no round 31. Step 11 only covers round 30 without a call. The game ending is undefined.
(2) Invalid answer with an empty hand. A hand can become empty (step 5). The fallback 'discard H, the highest value in their hand' then has no H.
(3) Option order is unspecified ('one option for each distinct value'), so 'first option' or 'last option' fallbacks and listings are not fixed.
(4) Random draws. The reshuffle deal of 5 cards to each of up to 5 players (25 draws), plus the setup deal, is called 'the round's only random draw'. That is a stretch of the limit of 1 random draw per round. It needs to be stated as one deal operation, or restructured.
(5) It is unclear whether 'hand_sum is recomputed' in step 10 is also what gates CALL in the next round's step 1. This is implied but should be explicit.
The repeated-game betrayal test does not apply. There is no cooperation option, and late rounds are not dominated by a safe choice.
- change: Ending: state that if a showdown occurs in round 30 (or any showdown leaves a total >= 100), the game ends after scoring; no new hands are dealt after a round-30 call.
- change: Fallback for invalid first-choice answers: if the hand is empty (only CALL available), an invalid answer counts as CALL; otherwise it counts as 'discard H'.
- change: List first-choice options in a fixed order (e.g. CALL first if available, then discard values ascending) and claim options as BLIND then values ascending.
- change: Specify the reshuffle deal (and setup deal) as a single deal operation that is the round's one random draw, and confirm the engine counts it as one draw; otherwise reduce to one draw per round.
- change: State explicitly that the next round's CALL eligibility uses the hand_sum recomputed in step 10.
- change: Optional, to strengthen inference: announce publicly how many cards each player shed in step 5, so hand sizes become trackable.
The variation that was reviewed: Simultaneous Yaniv: CARDS
Card values are:
- Joker = 0
- Ace = 1
- 2 to 10 = face value
- J, Q, K = 10

Every random card is drawn from a 54-card shoe: two 0s, four each of 1 to 9, and sixteen 10s. The shoe is full for every draw, so drawing never runs out. A hand is a list of values. A player's hand_sum is the sum of their hand.

SETUP
Every total is 0. Each player is dealt 5 random cards, seen only by that player. Parameters:
- call_limit = 7
- asaf_penalty = 30
- end_total = 100
- max_rounds = 30

EACH ROUND (rounds 1 to 30)
1. Options. Each player's first-choice options are:
   - 'CALL', only if their hand_sum is 7 or less;
   - one option 'discard V' for each distinct value V in their hand.
2. Talk. Everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone.
3. First choice. Everyone answers at the same time with one of their options. An answer that is not one of their options counts as 'discard H', where H is the highest value in their hand.
4. If at least one player chose CALL, this is a showdown:
   - All hands are revealed. Let L be the lowest hand_sum among all players.
   - A caller scores 0 if every other player's hand_sum is strictly greater than theirs. Otherwise (Asaf) they score their hand_sum + 30.
   - A non-caller scores 0 if their hand_sum equals L, otherwise their hand_sum.
   - Each score is written as round_score and added to that player's total.
   - Discards chosen this round are ignored.
   - If any total is now 100 or more, the game ends.
   - Otherwise every player's hand is replaced with 5 new random cards, seen only by that player, and the next round begins. This deal is the round's only random draw.
5. If no one called:
   - Discard. Each player removes EVERY card of their chosen value V from their hand; the hand may become empty. These cards leave play.
   - Offers. Each player's discarded value is announced publicly as that player's offer: one card of value V, however many were shed.
6. Claim options. Each player's options are 'BLIND' plus 'value V' for every distinct value offered this round by at least one OTHER player.
7. Claim choice. Everyone answers at the same time. An answer not among their options counts as BLIND.
8. Resolve claims. A claim on value V succeeds if exactly one player claimed V this round. That player adds one card of value V to their hand. If two or more players claimed the same V, all of them fail.
9. Blind draw. One random card value B is drawn. Every player who chose BLIND or whose claim failed adds one card of value B to their hand, and is told B privately.
10. Announce. Everyone's hand_sum is recomputed. Each player's discarded value, claimed value, success or failure, and whether they took the blind card are announced publicly. B and hand contents stay private.
11. Final showdown. If this is round 30 and no call happened this round, all hands are revealed. Each player scores 0 if their hand_sum equals the lowest hand_sum, otherwise their hand_sum. This is added to total and the game ends. Winner: When the game ends (after a showdown leaves any total at 100 or more, or after the round-30 final showdown), the player with the LOWEST total wins. If two or more players share the lowest total, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Yaniv is a draw-and-discard card game for 2 to 8 players. Players shed cards to get a low hand total and may call 'Yaniv' when their hand is at or below a threshold. Calling when someone else is as low or lower (Asaf) costs a 30-point penalty, points accumulate across rounds, and players over 200 are eliminated.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. Always calling as soon as eligible loses to Asaf penalties against players who hold low hands. Never calling lets opponents end rounds while you hold high cards. Always discarding the highest card is reasonable but predictable, and opponents can exploit it by claiming or baiting. In the reviewed variation, seats are symmetric because choices are simultaneous."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Timing the call, reading opponents' hand sums from public discards and claims, and avoiding contested claims all accumulate over up to 30 rounds. Deals are random, but many showdowns average the luck out."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still scores by shedding high cards. A strong player keeps improving through card counting, bluffing in talk, baiting with low offers and calling just before others do."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer opponents' hand sums from public discard values, shed counts, claim results and blind draws, and must model who will call."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is arithmetic on hand sums and totals."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The reviewed variation fit the counts but had defects. Its ending was undefined after a call in round 30, its fallback broke on an empty hand, its option order was unspecified, its random-draw accounting was vague, and it was implicit which hand sum gates CALL."
    }
  ],
  "problems": [
    "P1: The ending is undefined if a call happens in round 30 and no total reaches 100: new hands are dealt but there is no round 31.",
    "P2: The fallback 'discard H, the highest value in hand' fails when the hand is empty.",
    "P3: Option order is unspecified, so listings and 'first/last option' policies are not fixed.",
    "P4: The random-draw accounting is vague: the redeal and setup deal are many cards, described loosely as 'the only random draw'.",
    "P5: It is implicit, not stated, that next round's CALL eligibility uses the hand_sum recomputed at the end of this round.",
    "P6 (minor): Hand sizes are not publicly trackable, which weakens inference about opponents' hand sums."
  ],
  "changes": [
    {
      "what": "Every showdown in round 30, and any showdown that leaves a total at 100 or more, ends the game immediately after scoring; no new hands are dealt.",
      "why": "This gives the game a defined end in every case.",
      "fixes": "P1"
    },
    {
      "what": "An invalid first-choice answer counts as CALL if the hand is empty, otherwise as 'discard H' with H the highest value in hand.",
      "why": "The fallback is now always defined.",
      "fixes": "P2"
    },
    {
      "what": "First-choice options are listed as CALL first (if available), then 'discard V' by V ascending. Claim options are BLIND first, then 'value V' by V ascending.",
      "why": "Option order is deterministic.",
      "fixes": "P3"
    },
    {
      "what": "The redeal is defined as a single deal operation (5 cards to every player at once) and is the round's one random operation. It happens only in showdown rounds that do not end the game. The blind draw B happens only in rounds with no call, so no round has both. The setup deal is a single operation before round 1.",
      "why": "This keeps the game at one random draw per round.",
      "fixes": "P4"
    },
    {
      "what": "The rules explicitly state that the hand_sum recomputed in step 10 (or after a redeal) is what step 1 of the next round checks against call_limit.",
      "why": "This removes the ambiguity about CALL eligibility.",
      "fixes": "P5"
    },
    {
      "what": "The number of cards each player shed and each player's hand size are announced publicly every round. Hand sizes are public from the start (5).",
      "why": "This gives players more evidence for inferring opponents' hand sums.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Yaniv card values (Joker 0, Ace 1, faces 10) and hidden hands.",
    "Shedding cards to get a low hand, with a call threshold of 7.",
    "The Asaf rule: a caller who is not strictly lowest scores hand sum + 30.",
    "Taking either a card from the discards or a blind draw, here as one offered card or the blind card.",
    "Cumulative scoring with the lowest total winning, ended by a total threshold."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation worked strategically; only rule-completeness defects needed fixing, and all fixes fit within the limits."
  },
  "variation": {
    "name": "Simultaneous Yaniv",
    "summary": "Three to five players hold hidden hands and each round simultaneously either call or discard all cards of one value. They then claim a card another player discarded, or take a shared blind card. Calling when not strictly lowest costs +30. The lowest total wins when someone reaches 100 or after round 30.",
    "players": {"min": 3, "max": 5, "suggested": 4},
    "rules": "CARDS\n- Card values: Joker = 0, Ace = 1, 2 to 10 = face value, J/Q/K = 10.\n- Every random card is drawn from a 54-card shoe: two 0s, four each of 1 to 9, and sixteen 10s.\n- The shoe is full for every draw, so it never runs out.\n- A hand is a list of values. hand_sum is the sum of the hand. hand_size is the number of cards in it.\n\nPARAMETERS\ncall_limit = 7; asaf_penalty = 30; end_total = 100; max_rounds = 30.\n\nSETUP\n- Every total is 0.\n- In one deal operation, each player is dealt 5 random cards, seen only by that player.\n- Each player's hand_sum is computed. Each hand_size (5) is public.\n\nEACH ROUND (rounds 1 to 30)\n1. Options. Each player's first-choice options are listed in this order:\n   - 'CALL', only if their current hand_sum is 7 or less;\n   - then 'discard V' for each distinct value V in their hand, V ascending.\n   The current hand_sum is the one computed at the end of the previous round (step 10, or after a redeal in step 4), or at setup in round 1.\n2. Talk. Everyone writes one short message at the same time without seeing the others; all messages are then shown to everyone.\n3. First choice. Everyone answers at the same time with one of their options. An invalid answer counts as follows:\n   - CALL if the player's hand is empty;\n   - otherwise 'discard H', where H is the highest value in their hand.\n4. Showdown, if at least one player chose CALL:\n   a. All hands are revealed. L = the lowest hand_sum among all players.\n   b. A caller scores 0 if every other player's hand_sum is strictly greater than theirs. Otherwise (Asaf) they score hand_sum + 30.\n   c. A non-caller scores 0 if their hand_sum equals L, otherwise their hand_sum.\n   d. Each score is added to that player's total. Discards chosen this round are ignored.\n   e. If any total is now 100 or more, or this is round 30, the game ends now.\n   f. Otherwise, in one deal operation (the round's only random draw), every player's hand is replaced by 5 new random cards, seen only by that player. hand_sums are recomputed, hand_sizes reset to 5 publicly, and the round ends (steps 5 to 11 are skipped).\n5. Discard, if no one called:\n   - Each player removes every card of their chosen value V from their hand; the hand may become empty. These cards leave play.\n   - Each player's V and the number of cards they shed are announced publicly. Each player's offer is one card of value V.\n6. Claim options. Each player's options are listed in this order:\n   - 'BLIND';\n   - then 'value V' for each distinct value offered this round by at least one OTHER player, V ascending.\n7. Claim choice. Everyone answers at the same time. An invalid answer counts as BLIND.\n8. Resolve claims.\n   - A claim on V succeeds if exactly one player claimed V; that player adds one card of value V to their hand.\n   - If two or more players claimed the same V, all of them fail.\n9. Blind draw. One random card value B is drawn (the round's only random draw).\n   - Every player who chose BLIND or whose claim failed adds one card of value B to their hand.\n   - Each such player is told B privately.\n10. Announce.\n   - Every hand_sum is recomputed; this is the value step 1 of the next round uses.\n   - Announced publicly for each player: discarded value, number shed, claimed value, success or failure, whether they took the blind card, and new hand_size.\n   - B and hand contents stay private.\n11. Final showdown, if this is round 30 and no one called this round:\n   - All hands are revealed.\n   - Each player scores 0 if their hand_sum equals the lowest hand_sum, otherwise their hand_sum. This is added to their total.\n   - The game ends.",
    "objective": "The game ends either after a showdown that leaves any total at 100 or more, or after a showdown in round 30 (from a call or the final showdown). The player with the lowest total wins. If two or more players share the lowest total, the game is a draw among them.",
    "expected_effect": "The game now always terminates cleanly and is fully deterministic apart from one random operation per round. Public shed counts and hand sizes sharpen inference about opponents' hand sums, so call timing and Asaf traps reward reading the table. Talk passes both tests. Players disagree about when the round should end: a player with a low hand wants a showdown, while others want time to shed. They also compete for offered low cards, since contested claims fail. So a player who follows 'I'm high, don't worry' and holds back can lose: the speaker may be baiting a call they will Asaf, or steering others away from a card they want. With one winner by lowest total and three or more players, no simple policy is safe. Always-call suffers Asaf penalties, never-call eats others' showdowns, and always-claim-the-lowest-offer collides with rivals."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 3,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
