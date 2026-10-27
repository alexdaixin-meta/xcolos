# Variation: Air, Land and Sea: Four Battles

This is a two-player duel over four fixed 6-round battles. Players commit hidden hands to three theaters, read the opponent from what they reveal, and withdraw from bad battles to limit the VP they give up.

Players: 2 to 2, best with 2

## Review of the original

Air, Land and Sea is a two-player card duel fought over three theaters. Across several battles, players alternately deploy cards face-up to their matching theater or face-down anywhere at strength 2, and may withdraw early to give the opponent fewer victory points. Whoever controls more theaters wins a battle, and the first player to reach 12 VP wins the match.

- **non_degenerate**: good. Always withdrawing hands the opponent VP every battle and loses. Always improvising caps you at strength 2 per card and loses to sensible deploying. Always deploying your highest card spreads strength badly against a player who concentrates on two theaters. The first player wins ties within a battle, but first player alternates between battles, so neither seat has a built-in edge.
- **skill_sensitive**: good. The deal decides which hands are strong or weak. The real skill is choosing which two theaters to contest, when to spend face-down cards, and when to withdraw to save VP. A player who withdraws from losing battles cheaply and presses winning ones beats a player who plays every battle out.
- **headroom**: good. Card-counting the 6 unseen set-aside cards, reading the opponent's hand from what they deploy, and timing withdrawals give a strong player room to improve. A weak player still wins battles with good deals.
- **reasoning_dependent**: good. Hands are hidden, 6 of the 18 cards are out of play unseen, and face-down cards hide their identity. Whether to fight or withdraw depends on inferring what the opponent still holds.
- **verifiable**: good. Theater control is a comparison of strength sums, and VP awards come from a fixed table.
- **fits_platform**: weak. The original has 18 distinct card abilities (flip, move, adjacency, ongoing modifiers) and an open-ended first-to-12 length. Both are far beyond the step limits. The previous built variation also had loose battle-boundary rules: a withdrawal advanced the battle counter mid-battle, and it was unclear whether the other seat still acted in the withdrawal round.

## Problems

- P1: The 18 unique card abilities (flip, move, draw, adjacency, ongoing effects) need far more steps and state than the platform allows.
- P2: 'First to 12 VP' gives an open-ended length, and the battle count varies.
- P3: In the previous build, a withdrawal moved the battle counter and round_in_battle mid-battle (the final state showed battle 2, round_in_battle 1, battle_over true right after a round-1 withdrawal). Battle boundaries were therefore driven by events instead of by the round number, which broke the first-player rotation (R3) and the withdrawal-pass rule (R11).
- P4: The rules did not say clearly what happens to the second seat's action in the round where the first seat withdraws, or to the rounds left in a withdrawn battle.
- P5: The end-of-game tie rule was ambiguous ('draw' in the rules, 'shared win' in a test).
- P6: The withdrawal VP table differed by seat and hand size in ways that were hard to state and test.

## Changes

- Remove all card abilities. Cards are Air/Land/Sea 1–6 with strength equal to the number. Deploy (matching theater, full strength) and improvise (any theater, face-down, strength 2) remain. (fixes: P1): This keeps the core decisions (which theaters to fight for, what to hide, when to quit) inside the step budget.
- The match is exactly 4 battles of 6 rounds (24 rounds). Each player acts once per round. The higher VP total after round 24 wins; equal VP is a draw. (fixes: P2): A fixed length makes the game easy to build, and the tie rule is now unambiguous.
- Battle number, round-within-battle and first player are computed from the round number at the start of every round: battle = floor((round−1)/6)+1, round_in_battle = round − 6×(battle−1), first player = seat 1 in battles 1 and 3, seat 2 in battles 2 and 4. Nothing else ever changes them, and a withdrawal never does. (fixes: P3): This makes battle boundaries fixed and testable.
- A withdrawal sets battle_over to true immediately. The other seat is not asked to act that round. Every remaining round of that battle has no choices, and the battle gets no end-of-battle scoring. battle_over resets to false only at round_in_battle 1. (fixes: P4): This gives one precise reading of what a withdrawal does to the rest of the battle.
- Use a single withdrawal table for both seats, based on the withdrawer's hand size after withdrawing: 4 or more cards gives the opponent 2 VP; 2–3 cards gives 3 VP; 1 card gives 4 VP. Playing a battle out gives the winner 6 VP. (fixes: P6): It is simple and symmetric, and it keeps the original 'quit early, lose less' tension.
- State that equal VP after round 24 is a draw (no shared win). (fixes: P5): This removes the ambiguity in the end-of-game result.

## Kept from the original

- Three theaters (Air, Land, Sea) and 18 cards, each numbered 1–6 within its theater.
- Hidden 6-card hands, with 6 cards set aside unseen each battle.
- Deploy face-up to the matching theater, or improvise face-down anywhere at strength 2.
- Withdrawal as damage control, conceding fewer VP the earlier you quit.
- Winning a battle means controlling 2 of 3 theaters, and ties go to the battle's first player.
- First player alternates between battles.

## The variation's rules

CARDS. There are 18 cards: Air 1–6, Land 1–6 and Sea 1–6. A card's strength is its number.

MATCH. The match has 24 rounds, grouped into 4 battles of 6 rounds:
- Battle 1 is rounds 1–6.
- Battle 2 is rounds 7–12.
- Battle 3 is rounds 13–18.
- Battle 4 is rounds 19–24.

START OF EVERY ROUND (bookkeeping, no choices).
- Set battle = floor((round−1)/6)+1.
- Set round_in_battle = round − 6×(battle−1).
- Set first player = seat 1 if battle is 1 or 3, seat 2 if battle is 2 or 4.
- These values come only from the round number. Nothing else changes them.

BATTLE START (only when round_in_battle = 1).
- Set battle_over to false.
- Reset every player's Air, Land and Sea strength to 0 and clear all played cards.
- Shuffle all 18 cards.
- Deal 6 privately to each player's hand.
- Put the remaining 6 aside unseen. They are out of play for this battle.
- This is the only random event in a round.

ACTIONS. If battle_over is false, the first player takes one action. Then, if battle_over is still false, the second player takes one action. An action is exactly one of:
(a) DEPLOY: play a card from your hand face-up to the theater named on it. Add its number to your strength there.
(b) IMPROVISE: play a card from your hand face-down to any theater. Add 2 to your strength there. The opponent sees only the theater and the +2, not the card.
(c) WITHDRAW: concede the battle.

All theater strengths and face-up cards are public. Hands, the set-aside cards and the identity of face-down cards are hidden.

WITHDRAWAL.
- When a player withdraws, count the cards left in their hand.
- The opponent immediately gains VP as follows: 4 or more cards gives 2 VP; 2 or 3 cards gives 3 VP; 1 card gives 4 VP.
- battle_over becomes true at once.
- If the first player withdrew, the second player does not act that round.
- Every remaining round of the battle passes with no actions and no scoring.
- The next battle starts at its fixed round as usual.

BATTLE END (only when round_in_battle = 6 and battle_over is false, after both actions).
- Both hands are now empty.
- In each theater, the player with the higher strength controls it. A tie goes to that battle's first player.
- The player who controls 2 or more theaters wins the battle and gains 6 VP.
- Set battle_over to true.

END.
- After round 24 the game ends.

Objective: After round 24, the player with more VP wins. Equal VP is a draw.

Expected effect: Without abilities, each battle becomes a hidden-allocation duel. You choose two theaters to win, decide which low cards to spend face-down, and use what the opponent deploys (and the 6 unseen cards) to estimate their hand. The 2-versus-6 VP gap makes early withdrawal from a weak deal the key judgement, and bluffing strength can push an opponent into withdrawing. The fixed, round-driven boundaries make first-player rotation, withdrawal passing and the final tie result deterministic and testable. Simple policies lose: always-withdraw concedes 8 VP, always-improvise is capped at 12 strength, and always-play-out gives away 6-VP battles that could have cost only 2.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
