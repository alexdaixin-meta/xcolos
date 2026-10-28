# 17 design

- time: 2026-10-28T05:31:13+00:00 (29.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 498b4f820afad93c, reply sha256 257e96b2d9b1e14c

## Sent

````
Original game: Button Men
Players in the original: 2 to 2

Original rules:
Each player picks a Button that lists its dice, e.g. 3d6 2d10. A match is best of five rounds. To start a round both players roll all their dice at once; rolls are public. Players alternate turns. On your turn you must make a capture if able: a power attack uses one die whose value is at least the value of one opposing die to capture it; a skill attack uses any number of your dice whose values sum exactly to the value of one opposing die to capture it. Special skills on some dice modify this, but share the same structure. Captured dice are set aside and all dice used in the attack are rerolled immediately. If you cannot capture you must pass. When one player has no dice left, the round ends. The player who captured dice with higher total face-count (sum of sides, not rolled values) wins the round, and first to win three rounds wins the match.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Single-attack values, assuming the target is unguarded and the attacker does not know the target's value. A success scores the target's size. A failure gives the defender 2. Attacking a guarded die gives the defender 3. P(d12 >= d4) = (12+11+10+9)/48 = .875, so EV = .875*4 - .125*2 = +3.25. P(d12 >= d8) = 68/96 = .708, so EV = .708*8 - .292*2 = +5.08. P(d12 >= d12) = 78/144 = .542, so EV = .542*12 - .458*2 = +5.58. P(d8 >= d4) = (8+7+6+5)/32 = .8125, so EV = 3.25 - .375 = +2.875. P(d4 >= d4) = .625, so EV = 2.5 - .75 = +1.75. If the target is guarded with probability g, a d12 attack on the d12 is worth (1-g)*5.58 - 3g, which breaks even at g = .65. A player can guard only one die per exchange and earns nothing from the guard unless attacked, so neither guarding nor attacking dominates. Thoughtless policies under the winner rule: (a) Always option 1 or 3 (always guard one die). It scores only 3 when that die is attacked. The opponent attacks the other dice for +2.9 to +5.1 per exchange and also collects their survival bonuses, so the policy loses to sensible play. (b) Always option 12 (d12 attacks d12). An opponent who guards the d12 scores +3 per exchange while this player scores 0. Once the d12 is captured, the action does nothing for the rest of the leg. The policy loses to sensible play; it beats random play, which is acceptable. (c) Always attack with your highest die against their highest die. This is predictable and is countered the same way. No option is strictly better, and both players can realistically win. FAIL: a seat edge from information. Reroll step 5 sets B's rerolled die from D1. At a leg-start exchange, D1 is also the digit that set A's d8, since A's d8 = (D1 mod 8)+1. If B guards its d8 on exchange 1 of a leg, B's d8 rerolls to (D1 mod 8)+1, which is exactly A's hidden d8 value. Rerolling B's d4 or d12 reveals A's d8 mod 4 instead. A's reroll uses D0, which only repeats A's own d4, so A learns nothing about B. B can therefore guard its d8 at the start of every leg (at least 3 times a match) and learn an opponent value for free. A never gets this. The leak is systematic and favours seat B.
- change: Remove the reroll/leg-start digit overlap that lets B learn A's d8. For example, enlarge R to uniform 0 to 110,075,314,175 (24^8 - 1), keep D0-D5 for the six leg-start dice, and set A's rerolled die from D6 and B's from D7. Alternatively, state that at a leg-start exchange no die is rerolled at step 5 (guarded and successful dice keep their values).
The variation that was reviewed: Button Men: Guard and Strike: DICE. Each player owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.

RANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 191,102,975. Write R in base 24 as digits D0 to D5, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.

LEGS. The match is exactly 30 exchanges. These are grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2, and player B's from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each exchange of the leg.

EACH EXCHANGE:
1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.
2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.
3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions:
(1) Guard my d4
(2) Guard my d8
(3) Guard my d12
(4) My d4 attacks their d4
(5) My d4 attacks their d8
(6) My d4 attacks their d12
(7) My d8 attacks their d4
(8) My d8 attacks their d8
(9) My d8 attacks their d12
(10) My d12 attacks their d4
(11) My d12 attacks their d8
(12) My d12 attacks their d12
An action that names a die that is already captured (yours or theirs) does nothing.
4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.
- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.
- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed.
- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.
- A die may capture and be captured in the same exchange; both effects happen.
5. Rerolls. Player A's rerolled die is set from D0 and player B's from D1. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). New values are shown only to their owner.
6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.
7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores the bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.
8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over. Winner: After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "original_summary": "Button Men is a two-player dice duel. Both players roll public dice, then take turns capturing opposing dice with power attacks (one die whose value is at least the target's) or skill attacks (several dice summing exactly to the target). Rounds are scored by the total sides of the dice each player captured, and the match is best of five.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Original: rolls are public and a capture is compulsory whenever one is possible, so many turns are forced or nearly forced. The Button chosen gives a large built-in edge, and the first mover gains tempo. Previous variation: no simple policy dominated. Always-guard loses to attacks on the other dice; always d12-attacks-d12 loses to a guarded d12. But seat B had a systematic information edge: at every leg start B could guard its d8 and have it rerolled from digit D1, the same digit that set A's d8, so B learned A's d8 for free. Revised variation: reroll digits D6 and D7 are used only for rerolls and never for leg-start dice. B's reroll is now independent of every A value, so the two seats are symmetric."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Original: with public rolls and forced captures, the dice largely decide the round, and a best-of-five match is a small sample. Revised variation: 30 simultaneous exchanges average out individual rolls. Expected values per attack are known, for example d12 on d4 is +3.25, d12 on d8 is +5.08 and d12 on d12 is +5.58, while hitting a guard gives the defender 3. A player who mixes guarding and attacking well, and tracks revealed values, should beat a predictable or random player reliably."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Revised variation: guarding breaks even against a d12-on-d12 attack at a guard probability of about 0.65. Several things interact: memory of revealed values, which die to expose, leg timing (survival bonuses against 10-exchange legs) and score-state risk. That leaves room to keep improving, while simple sensible play (attack with the big die, guard occasionally) still scores."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Original: perfect information, so there is little to infer. Revised variation: die values are hidden and are revealed only by failed attacks. Values persist until a reroll, so each player must remember what was revealed and whether that die has since rerolled. Choices are simultaneous, so each player must predict the opponent's guard and attack choices."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every outcome is a comparison of numbers plus fixed point awards. The winner is the higher total, computed by arithmetic, with no judge."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Revised variation: one simultaneous poll per exchange, one random draw per exchange, no board, 30 exchanges and about 14 steps per exchange, all within the limits. The original's sequential multi-die skill attacks and special die powers would have needed long rule chains."
    },
    {
      "criterion": "balanced (from test)",
      "verdict": "good",
      "evidence": "The leak found in testing is gone. Leg-start dice use D0 to D5, A's reroll uses D6 and B's reroll uses D7. Each digit is uniform on 0 to 23, and 24 is divisible by 4, 8 and 12, so every die value is uniform and independent of the other player's dice."
    }
  ],
  "problems": [
    "Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures.",
    "Original: Button choice and turn order create seat and setup edges.",
    "Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits.",
    "Original: best of five rounds is a small sample, so luck weighs heavily.",
    "Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge."
  ],
  "changes": [
    {
      "what": "Enlarge the random draw to R uniform on 0 to 110,075,314,175 (24^8 - 1), giving eight base-24 digits D0 to D7. Leg-start dice still use D0 to D5. Player A's reroll uses D6 and player B's reroll uses D7.",
      "why": "No digit ever sets both a reroll and any leg-start die, so no reroll can reveal an opponent value. A and B are treated identically.",
      "fixes": "Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge."
    },
    {
      "what": "Keep hidden die values, revealed only by failed attacks.",
      "why": "This gives players something to infer and remember.",
      "fixes": "Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures."
    },
    {
      "what": "Keep identical fixed dice (d4, d8, d12) for both players and simultaneous choices.",
      "why": "This removes the setup and turn-order edges.",
      "fixes": "Original: Button choice and turn order create seat and setup edges."
    },
    {
      "what": "Keep single-die power attacks plus a guard action, and keep the 12-action menu.",
      "why": "This preserves the capture-by-value core within the build limits.",
      "fixes": "Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits."
    },
    {
      "what": "Keep 30 exchanges in legs of at most 10, with survival bonuses.",
      "why": "The larger sample lets skill dominate, and the legs keep the original's round structure.",
      "fixes": "Original: best of five rounds is a small sample, so luck weighs heavily."
    }
  ],
  "keeps": [
    "Dice of different sizes capture each other by comparing rolled values (the power attack).",
    "A capture is worth the captured die's size, not its rolled value.",
    "The attacking die rerolls after a successful capture.",
    "Play is in rounds (legs) that end when a player has lost all dice, and both players get all dice back each leg.",
    "It is a two-player duel."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation worked except for a seat-B information leak from a shared random digit. Separating the reroll digits fixes it without changing play."
  },
  "variation": {
    "name": "Button Men: Guard and Strike",
    "summary": "Two players each hold a d4, d8 and d12 with hidden values. Over 30 simultaneous exchanges, grouped into legs, each player either guards one die or attacks an opposing die with one of their own. A capture scores the target's size. Hitting a guard or failing an attack rewards the defender. Surviving dice score a bonus at the end of each leg.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DICE. Each player (A and B) owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.\n\nRANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 110,075,314,175. Write R in base 24 as digits D0 to D7, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.\n\nLEGS. The match is exactly 30 exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2. Player B's d4, d8 and d12 are set from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each further exchange of the leg.\n\nEACH EXCHANGE:\n1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.\n2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.\n3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions: (1) Guard my d4; (2) Guard my d8; (3) Guard my d12; (4) My d4 attacks their d4; (5) My d4 attacks their d8; (6) My d4 attacks their d12; (7) My d8 attacks their d4; (8) My d8 attacks their d8; (9) My d8 attacks their d12; (10) My d12 attacks their d4; (11) My d12 attacks their d8; (12) My d12 attacks their d12. An action that names a die that is already captured (yours or theirs) does nothing.\n4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.\n- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.\n- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed for the rest of the leg.\n- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.\n- A die may capture and be captured in the same exchange; both effects happen.\n5. Rerolls. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). Player A's rerolled die is set from digit D6. Player B's rerolled die is set from digit D7. New values are shown only to their owner.\n6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced to both players. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.\n7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores a bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.\n8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.",
    "objective": "After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.",
    "expected_effect": "Play is the same as the previous variation, but the seats are now symmetric. Neither player can learn an opponent value through their own reroll, so information comes only from failed attacks, which reveal values to both players equally. Players must balance aggressive d12 attacks (+3.25 to +5.58 expected per exchange against an unguarded target) against guarding, which breaks even near a 0.65 guard rate on the d12. They must remember revealed values until those dice reroll, and must time the end of each leg for survival bonuses. No simple policy wins against sensible play: always-guard loses to attacks on the other dice, and a fixed attack pattern loses to a matching guard."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 1,
    "attributes": 18,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```

Why it was refused: review needs exactly one entry per criterion, in this order: non_degenerate, skill_sensitive, headroom, reasoning_dependent, verifiable, fits_platform
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "original_summary": "Button Men is a two-player dice duel. Both players roll public dice, then take turns capturing opposing dice with power attacks (one die whose value is at least the target's) or skill attacks (several dice summing exactly to the target). Rounds are scored by the total sides of the dice each player captured, and the match is best of five.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Original: rolls are public and a capture is compulsory whenever one is possible, so many turns are forced or nearly forced. The Button chosen gives a large built-in edge, and the first mover gains tempo. Previous variation: no simple policy dominated. Always-guard scores only 3 when the guarded die is hit and loses to attacks on the other dice. Always d12-attacks-d12 loses to a guarded d12. Testing found a systematic seat-B edge: at every leg start B could guard its d8, and B's reroll used digit D1, the same digit that set A's d8. B therefore learned A's d8 for free at least 3 times a match. Revised variation: reroll digits D6 and D7 are used only for rerolls and never for leg-start dice. Each digit is uniform on 0 to 23, and 24 is divisible by 4, 8 and 12, so every die value is uniform and independent of the other player's dice. The two seats are now symmetric."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Original: with public rolls and forced captures, the dice largely decide the round, and best of five is a small sample. Revised variation: 30 simultaneous exchanges average out individual rolls. The expected value of an attack is known: d12 on d4 is +3.25, d12 on d8 is +5.08 and d12 on d12 is +5.58, while hitting a guard gives the defender 3. A player who mixes guarding and attacking well and tracks revealed values should reliably beat a predictable or random player."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Revised variation: guarding breaks even against a d12-on-d12 attack at a guard probability of about 0.65. Several factors interact: memory of revealed values, which die to expose, leg timing (survival bonuses against 10-exchange legs) and score-state risk. That leaves room to keep improving, while simple sensible play (attack with the big die, guard occasionally) still scores."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Original: perfect information, so there is little to infer. Revised variation: die values are hidden and are revealed only by failed attacks. A value persists until its die rerolls, so each player must remember what was revealed and whether that die has since rerolled. Choices are simultaneous, so each player must predict the opponent's guards and attacks."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every outcome is a comparison of numbers plus fixed point awards. The higher total wins, computed by arithmetic, with no judge."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Revised variation: one simultaneous poll per exchange, one random draw per exchange, no board, 30 exchanges and about 14 steps per exchange, all within the limits. The original's sequential multi-die skill attacks and special die powers would have needed long rule chains."
    }
  ],
  "problems": [
    "Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures.",
    "Original: Button choice and turn order create seat and setup edges.",
    "Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits.",
    "Original: best of five rounds is a small sample, so luck weighs heavily.",
    "Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge."
  ],
  "changes": [
    {
      "what": "Enlarge the random draw to R uniform on 0 to 110,075,314,175 (24^8 - 1), giving eight base-24 digits D0 to D7. Leg-start dice still use D0 to D5. Player A's reroll uses D6 and player B's reroll uses D7.",
      "why": "No digit ever sets both a reroll and a leg-start die, so no reroll can reveal an opponent value. A and B are treated identically.",
      "fixes": "Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge."
    },
    {
      "what": "Keep hidden die values, revealed only by failed attacks.",
      "why": "This gives players something to infer and remember.",
      "fixes": "Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures."
    },
    {
      "what": "Keep identical fixed dice (d4, d8, d12) for both players and simultaneous choices.",
      "why": "This removes the setup and turn-order edges.",
      "fixes": "Original: Button choice and turn order create seat and setup edges."
    },
    {
      "what": "Keep single-die power attacks plus a guard action, and keep the 12-action menu.",
      "why": "This preserves the capture-by-value core within the build limits.",
      "fixes": "Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits."
    },
    {
      "what": "Keep 30 exchanges in legs of at most 10, with survival bonuses.",
      "why": "The larger sample lets skill dominate, and the legs keep the original's round structure.",
      "fixes": "Original: best of five rounds is a small sample, so luck weighs heavily."
    }
  ],
  "keeps": [
    "Dice of different sizes capture each other by comparing rolled values (the power attack).",
    "A capture is worth the captured die's size, not its rolled value.",
    "The attacking die rerolls after a successful capture.",
    "Play is in rounds (legs) that end when a player has lost all dice, and both players get all dice back each leg.",
    "It is a two-player duel."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation worked except for a seat-B information leak from a shared random digit. Separating the reroll digits fixes the leak without changing play."
  },
  "variation": {
    "name": "Button Men: Guard and Strike",
    "summary": "Two players each hold a d4, d8 and d12 with hidden values. Over 30 simultaneous exchanges, grouped into legs, each player either guards one die or attacks an opposing die with one of their own. A capture scores the target's size. Hitting a guard or failing an attack rewards the defender. Surviving dice score a bonus at the end of each leg.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DICE. Each player (A and B) owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.\n\nRANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 110,075,314,175. Write R in base 24 as digits D0 to D7, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.\n\nLEGS. The match is exactly 30 exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2. Player B's d4, d8 and d12 are set from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each further exchange of the leg.\n\nEACH EXCHANGE:\n1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.\n2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.\n3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions: (1) Guard my d4; (2) Guard my d8; (3) Guard my d12; (4) My d4 attacks their d4; (5) My d4 attacks their d8; (6) My d4 attacks their d12; (7) My d8 attacks their d4; (8) My d8 attacks their d8; (9) My d8 attacks their d12; (10) My d12 attacks their d4; (11) My d12 attacks their d8; (12) My d12 attacks their d12. An action that names a die that is already captured (yours or theirs) does nothing.\n4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.\n- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.\n- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed for the rest of the leg.\n- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.\n- A die may capture and be captured in the same exchange; both effects happen.\n5. Rerolls. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). Player A's rerolled die is set from digit D6. Player B's rerolled die is set from digit D7. New values are shown only to their owner.\n6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced to both players. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.\n7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores a bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.\n8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.",
    "objective": "After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.",
    "expected_effect": "Play is the same as in the previous variation, but the seats are now symmetric. Neither player can learn an opponent value through their own reroll. Information comes only from failed attacks, which reveal values to both players equally. Players must balance aggressive d12 attacks (+3.25 to +5.58 expected per exchange against an unguarded target) against guarding, which breaks even near a 0.65 guard rate on the d12. They must remember revealed values until those dice reroll, and must time the end of each leg for survival bonuses. No simple policy wins against sensible play: always-guard loses to attacks on the other dice, and a fixed attack pattern loses to a matching guard."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 1,
    "attributes": 18,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
