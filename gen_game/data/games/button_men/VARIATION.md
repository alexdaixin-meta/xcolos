# Variation: Button Men: Guard and Strike

Two players each hold a d4, d8 and d12 with hidden values. Over 30 simultaneous exchanges, grouped into legs, each player either guards one die or attacks an opposing die with one of their own. A capture scores the target's size. Hitting a guard or failing an attack rewards the defender. Surviving dice score a bonus at the end of each leg.

Players: 2 to 2, best with 2

## Review of the original

Button Men is a two-player dice duel. Both players roll public dice, then take turns capturing opposing dice with power attacks (one die whose value is at least the target's) or skill attacks (several dice summing exactly to the target). Rounds are scored by the total sides of the dice each player captured, and the match is best of five.

- **non_degenerate**: weak. Original: rolls are public and a capture is compulsory whenever one is possible, so many turns are forced or nearly forced. The Button chosen gives a large built-in edge, and the first mover gains tempo. Previous variation: no simple policy dominated. Always-guard scores only 3 when the guarded die is hit and loses to attacks on the other dice. Always d12-attacks-d12 loses to a guarded d12. Testing found a systematic seat-B edge: at every leg start B could guard its d8, and B's reroll used digit D1, the same digit that set A's d8. B therefore learned A's d8 for free at least 3 times a match. Revised variation: reroll digits D6 and D7 are used only for rerolls and never for leg-start dice. Each digit is uniform on 0 to 23, and 24 is divisible by 4, 8 and 12, so every die value is uniform and independent of the other player's dice. The two seats are now symmetric.
- **skill_sensitive**: weak. Original: with public rolls and forced captures, the dice largely decide the round, and best of five is a small sample. Revised variation: 30 simultaneous exchanges average out individual rolls. The expected value of an attack is known: d12 on d4 is +3.25, d12 on d8 is +5.08 and d12 on d12 is +5.58, while hitting a guard gives the defender 3. A player who mixes guarding and attacking well and tracks revealed values should reliably beat a predictable or random player.
- **headroom**: good. Revised variation: guarding breaks even against a d12-on-d12 attack at a guard probability of about 0.65. Several factors interact: memory of revealed values, which die to expose, leg timing (survival bonuses against 10-exchange legs) and score-state risk. That leaves room to keep improving, while simple sensible play (attack with the big die, guard occasionally) still scores.
- **reasoning_dependent**: good. Original: perfect information, so there is little to infer. Revised variation: die values are hidden and are revealed only by failed attacks. A value persists until its die rerolls, so each player must remember what was revealed and whether that die has since rerolled. Choices are simultaneous, so each player must predict the opponent's guards and attacks.
- **verifiable**: good. Every outcome is a comparison of numbers plus fixed point awards. The higher total wins, computed by arithmetic, with no judge.
- **fits_platform**: good. Revised variation: one simultaneous poll per exchange, one random draw per exchange, no board, 30 exchanges and about 14 steps per exchange, all within the limits. The original's sequential multi-die skill attacks and special die powers would have needed long rule chains.

## Problems

- Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures.
- Original: Button choice and turn order create seat and setup edges.
- Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits.
- Original: best of five rounds is a small sample, so luck weighs heavily.
- Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge.

## Changes

- Enlarge the random draw to R uniform on 0 to 110,075,314,175 (24^8 - 1), giving eight base-24 digits D0 to D7. Leg-start dice still use D0 to D5. Player A's reroll uses D6 and player B's reroll uses D7. (fixes: Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge.): No digit ever sets both a reroll and a leg-start die, so no reroll can reveal an opponent value. A and B are treated identically.
- Keep hidden die values, revealed only by failed attacks. (fixes: Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures.): This gives players something to infer and remember.
- Keep identical fixed dice (d4, d8, d12) for both players and simultaneous choices. (fixes: Original: Button choice and turn order create seat and setup edges.): This removes the setup and turn-order edges.
- Keep single-die power attacks plus a guard action, and keep the 12-action menu. (fixes: Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits.): This preserves the capture-by-value core within the build limits.
- Keep 30 exchanges in legs of at most 10, with survival bonuses. (fixes: Original: best of five rounds is a small sample, so luck weighs heavily.): The larger sample lets skill dominate, and the legs keep the original's round structure.

## Kept from the original

- Dice of different sizes capture each other by comparing rolled values (the power attack).
- A capture is worth the captured die's size, not its rolled value.
- The attacking die rerolls after a successful capture.
- Play is in rounds (legs) that end when a player has lost all dice, and both players get all dice back each leg.
- It is a two-player duel.

## The variation's rules

DICE. Each player (A and B) owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.

RANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 110,075,314,175. Write R in base 24 as digits D0 to D7, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.

LEGS. The match is exactly 30 exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2. Player B's d4, d8 and d12 are set from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each further exchange of the leg.

EACH EXCHANGE:
1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.
2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.
3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions: (1) Guard my d4; (2) Guard my d8; (3) Guard my d12; (4) My d4 attacks their d4; (5) My d4 attacks their d8; (6) My d4 attacks their d12; (7) My d8 attacks their d4; (8) My d8 attacks their d8; (9) My d8 attacks their d12; (10) My d12 attacks their d4; (11) My d12 attacks their d8; (12) My d12 attacks their d12. An action that names a die that is already captured (yours or theirs) does nothing.
4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.
- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.
- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed for the rest of the leg.
- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.
- A die may capture and be captured in the same exchange; both effects happen.
5. Rerolls. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). Player A's rerolled die is set from digit D6. Player B's rerolled die is set from digit D7. New values are shown only to their owner.
6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced to both players. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.
7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores a bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.
8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.

Objective: After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.

Expected effect: Play is the same as in the previous variation, but the seats are now symmetric. Neither player can learn an opponent value through their own reroll. Information comes only from failed attacks, which reveal values to both players equally. Players must balance aggressive d12 attacks (+3.25 to +5.58 expected per exchange against an unguarded target) against guarding, which breaks even near a 0.65 guard rate on the d12. They must remember revealed values until those dice reroll, and must time the end of each leg for survival bonuses. No simple policy wins against sensible play: always-guard loses to attacks on the other dice, and a fixed attack pattern loses to a matching guard.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
