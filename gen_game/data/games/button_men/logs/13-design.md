# 13 design

- time: 2026-10-28T05:27:50+00:00 (72.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 aa387ea8e6ac96a0, reply sha256 bbbede013768b8d9

## Sent

````
Original game: Button Men
Players in the original: 2 to 2

Original rules:
Each player picks a Button that lists its dice, e.g. 3d6 2d10. A match is best of five rounds. To start a round both players roll all their dice at once; rolls are public. Players alternate turns. On your turn you must make a capture if able: a power attack uses one die whose value is at least the value of one opposing die to capture it; a skill attack uses any number of your dice whose values sum exactly to the value of one opposing die to capture it. Special skills on some dice modify this, but share the same structure. Captured dice are set aside and all dice used in the attack are rerolled immediately. If you cannot capture you must pass. When one player has no dice left, the round ends. The player who captured dice with higher total face-count (sum of sides, not rolled values) wins the round, and first to win three rounds wins the match.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: THE CORE PROBLEM: the opponent's choice never affects the outcome of your own choice that exchange. Resolution uses values from the start of the exchange. A die that is captured still delivers its own attack. Neither player has any defensive action. So your result depends only on your own die value and the target's hidden value.

EXPECTED VALUE OF AN ATTACK. Your attacking die shows v and the target has size s with an unknown uniform value. Success chance p = min(v,s)/s. EV = p*s - (1-p)*2 = min(v,s) - 2(1-p).

Table of my EV (rows: my d12 value; columns: target):
- v=12: their d12 +12.0 (certain); their d8 +8.0 (certain); their d4 +4.0 (certain)
- v=9: their d12 9 - 0.5 = +8.5; their d8 +8.0 (certain); their d4 +4.0
- v=6: their d12 6 - 1.0 = +5.0; their d8 6 - 0.5 = +5.5; their d4 +4.0
- v=2: their d12 2 - 1.67 = +0.33; their d8 2 - 1.5 = +0.5; their d4 2 - 1.0 = +1.0
Against these, a reroll is worth 0 now.
Every one of these numbers is the same in every column of the opponent's 12 possible actions. In each state, the EV-maximising action is therefore best whatever the opponent does. A certain capture, such as a d12 showing 12 against their d12, strictly dominates every alternative. The game is two parallel solitaire EV problems, so the opponent has nothing to answer with.

THOUGHTLESS POLICIES (winner rule):
- Always (1), reroll my d4: never scores from attacks, only collects +2 when the opponent fails. It loses to sensible play almost always. Against random play it often loses too, because random play captures it about half the time.
- Always (12), d12 attacks d12: succeeds on the first exchange with chance 78/144 = 54% for +12. On a failure its value is revealed and is not rerolled, so it fails forever while their d12 keeps its value, giving +2 per exchange. Against sensible play it loses or draws often, and against random play it usually wins.
- Always (10), d12 attacks d4: succeeds with chance 42/48 = 87.5% for +4, then does nothing for the rest of the match. It loses to sensible play.
So no fixed index never loses. However, a simple 'take the best EV attack' rule is optimal no matter what the opponent does.

SEATS: the game is symmetric and simultaneous, so there is no seat edge. Both players can win. The failure is the dominant per-state option and the absence of any interaction.
- playable FAILED: The rules are otherwise complete:
- dead-die actions are null;
- simultaneous capture is defined;
- reveals and the reroll set are specified;
- the match is finite (at most 12 exchanges, or earlier when a player runs out of dice);
- the end is scored arithmetically and ties are a draw.
Two players need no talk phase. The game does not rely on cooperation.

LIMIT VIOLATION: random_draws_per_round is declared as 1, but the rules need more than that.
- Setup rolls 6 dice.
- Each exchange can reroll up to 2 independent dice: one per player, from a successful attacker or a chosen reroll.
- So the design needs up to 2 random draws per round, which is over the limit of 1, and the setup roll comes on top of that.

DECLARED COUNTS ARE UNDERSTATED:
- Attributes: 6 die values + 6 alive flags + 2 scores = 14, not 10. This is still at most 20, but it is misstated.
- Steps: resolving 9 attack options per player needs an index-to-value mapping without a lookup operation (the payoff_matrix workaround). 14 steps is optimistic, though it is probably under 20.
- reasoning_over_luck FAILED: WHAT DECIDES THE WINNER:
- Your attacks do not depend on the opponent's simultaneous choice, so there is no opponent modelling within an exchange.
- You cannot defend, so whether your own dice get captured is pure luck: it depends on their values against the opponent's.
- Inference is mechanical. You know exactly which opposing dice are fresh uniform values (rerolled or successful attackers) and which are revealed. The only soft signal is that an unrerolled die is probably not low.

HOW LONG A MATCH LASTS: a typical match ends within 3-5 exchanges, because high-EV attacks capture roughly one die per player per exchange. If both players play the intended greedy-EV strategy, the result is fixed by the dice rolls: the initial 6 values and the few rerolls.

CHANCE SHARE: a careful reasoner beats a simple greedy player only slightly, mainly by not repeating revealed failing attacks and by rerolling low dice. I estimate chance decides 65-75% of results. A reasoning player is not clearly favoured.
- change: Make each player's outcome depend on the opponent's simultaneous choice. Example: replace 'Reroll my dX' with 'Guard my dX'. A guarded die cannot be captured this exchange. Any attack on it fails, the defender scores 3, and the attacker's value is revealed. The guarded die is then rerolled. Attacks and guards now form a guessing game: a sure capture can be blocked if predicted, and guarding the wrong die wastes the turn.
- change: Alternatively, or as well, resolve captures before counterattacks: a die captured this exchange does not deliver its attack. Removing the opponent's most dangerous die then matters, and choosing a target becomes a prediction about what they will attack with.
- change: Reduce the role of luck. Use a smaller value range or fewer rerolls, or add a scoring element tied to correct inference, so that greedy-EV play is clearly beaten by play that models the opponent's guard and attack tendencies.
- change: Stay within one random draw per round. Draw a single random integer R per exchange, for example 0..9999, and derive each rerolled die's value arithmetically: player A's die = (R mod size) + 1, player B's die = (floor(R/100) mod size) + 1. Do the initial 6-die roll in setup.
- change: Correct the declared complexity: attributes = 14. Recount steps_per_round, including the index-to-value mapping for both players' attacks, and confirm it stays at 20 or fewer.
The variation that was reviewed: Button Men: Blind Dice: SETUP. Each player has three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). At the start, each player's three dice are rolled. Each player sees their own values; neither sees the opponent's. Both players can always see which dice each player still has and their sizes. Both scores start at 0.

EXCHANGES. The match has up to 12 exchanges. Each exchange runs as follows.

1. Announcement. The exchange number, both scores, and the dice each player still holds are announced to both players. Each player is privately reminded of the current values of their own remaining dice.

2. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one action from this list:
(1) Reroll my d4
(2) Reroll my d8
(3) Reroll my d12
(4) My d4 attacks their d4
(5) My d4 attacks their d8
(6) My d4 attacks their d12
(7) My d8 attacks their d4
(8) My d8 attacks their d8
(9) My d8 attacks their d12
(10) My d12 attacks their d4
(11) My d12 attacks their d8
(12) My d12 attacks their d12
An action that names a die that has already been captured, whether your own or the opponent's, does nothing that exchange.

3. Resolution. Both attacks are resolved using the values the dice showed at the start of the exchange, so the order does not matter.
- An attack succeeds if the attacking die's value is greater than or equal to the target die's value. The attacker scores points equal to the target's size, and the target is captured and removed.
- An attack fails if the attacking die's value is lower than the target's. The defender scores 2 points, and the current values of both dice are announced to both players.
- A die may capture and be captured in the same exchange; both effects happen. If both attacks fail, both pairs of values are announced.

4. Rerolls. After resolution, these dice are rerolled together, with new values shown only to their owner:
- every attacking die whose attack succeeded and that was not itself captured this exchange;
- every die its owner chose to reroll, if it was not captured this exchange.
A die that was not rerolled keeps its value, including any value already announced.

5. Results. Every attack and reroll action is announced, along with whether each attack succeeded or failed, any revealed values, which dice were captured, and the new scores. New rolled values are not announced.

6. End check. The match ends immediately if either player has no dice left. Otherwise it ends after exchange 12.

END OF MATCH. Each player adds half the size of each of their own surviving dice to their score: d4 adds 2, d8 adds 4, d12 adds 6. Winner: After surviving-dice points are added, the player with the higher score wins. Equal scores are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Button Men is a two-player dice duel. Each player rolls a set of dice of different sizes, and players take turns capturing opposing dice, either with one die whose value is at least the target's (a power attack) or with several dice whose values sum exactly to it (a skill attack). Captured sizes are scored, and the match is best of five rounds.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the previous variation no fixed index policy was safe. Even so, 'take the highest-EV attack' was optimal whatever the opponent chose, because the opponent's simultaneous choice never changed the result of your own action. Captured dice still struck, and nobody could defend. A certain capture, such as a d12 showing 12 against a d12, strictly dominated every other option. There was no seat edge, but each state had a dominant option."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Chance decided an estimated 65-75% of results. A careful player beat a greedy-EV player only by small margins, such as not repeating a revealed failing attack and rerolling low dice. A match lasted 3-5 exchanges, so a single leg of six die rolls dominated the result."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Once the EV table is known the game is solved: compute min(v,s) - 2(1-p) and pick the maximum. A weak player still scores, but a strong player has nothing further to learn."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Opposing die values were hidden, but inference was mechanical: a fresh die is uniform and a revealed die is known. There was no opponent modelling, because the opponent's move never mattered to your own outcome."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Captures, scores and surviving-dice bonuses are all arithmetic on tracked values. Ties are a draw."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It was turn-based and text-only, but it needed up to 2 independent rerolls per exchange plus a 6-die setup, against a limit of 1 random draw per round. Its declared attributes (10) and steps (14) were understated."
    }
  ],
  "problems": [
    "P1: There is no interaction. The opponent's simultaneous choice never affects the outcome of your action, so the greedy-EV attack is dominant in every state and a certain capture cannot be answered.",
    "P2: Luck swamps skill. A single short leg of 3-5 exchanges means the opening roll largely decides the match.",
    "P3: Inference is only mechanical. There is nothing to read about the opponent's intentions or likely move.",
    "P4: Up to 2 rerolls per exchange plus the setup roll exceed the limit of 1 random draw per round.",
    "P5: Declared complexity was understated: attributes were 14, not 10, and steps were under-counted for the index-to-value mapping."
  ],
  "changes": [
    {
      "what": "Replace the three 'Reroll my dX' actions with 'Guard my dX'. A guarded die cannot be captured this exchange. An attack on it fails, its owner scores 3, and only the attacker's value is revealed. The guarded die is then rerolled, whether or not it was attacked.",
      "why": "Every attack now becomes a guess about which die the opponent will guard, and every guard becomes a guess about which die they will attack. A certain capture can be blocked if it is predicted, so no action is best regardless of the opponent. Guarding the wrong die wastes the exchange.",
      "fixes": "P1"
    },
    {
      "what": "Use failed attacks and guards as information. An unguarded failed attack reveals both values. A guarded failed attack reveals only the attacker's value, and the guarded die then becomes fresh and hidden again.",
      "why": "Players must track what the opponent has learned about their dice and what the opponent's guards and attacks suggest about hidden values. A guard hints at a low or valuable die; an attack hints at a high attacker.",
      "fixes": "P3"
    },
    {
      "what": "Play a fixed 30 exchanges grouped into legs. A leg ends when a player has no dice left or after 10 exchanges in that leg. Surviving dice score their bonus, then all dice are restored and rerolled. Scores accumulate over the whole match.",
      "why": "Several legs average out the opening rolls, so the steadier guesser and reader of tendencies wins more reliably. Opponent tendencies also persist across legs, which gives players something to model.",
      "fixes": "P2"
    },
    {
      "what": "Draw exactly one random integer R per exchange, uniform from 0 to 191,102,975 (24^6 - 1). Read it as six base-24 digits D0..D5. A rerolled die of size s takes (digit mod s) + 1. Player A uses D0 and player B uses D1. A fresh leg uses D0-D2 for A's dice and D3-D5 for B's. Each player rerolls at most one die per exchange.",
      "why": "Because 24 is divisible by 4, 8 and 12, every die is uniform. All randomness, including restarting a leg, comes from one draw per round.",
      "fixes": "P4"
    },
    {
      "what": "Recount complexity honestly: 16 attributes and 18 steps, including the action-to-die mapping for both players.",
      "why": "The declared numbers must match what the builder will need.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Dice of different sizes (d4, d8, d12), where a capture is worth the target's size.",
    "A capture succeeds when the attacking value is at least the target's value, as in the original power attack.",
    "A die that captures is rerolled.",
    "Several legs make up a match, echoing the original's several rounds.",
    "Hidden rolled values and the tension between using a high die and risking a big die."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Adding a guard creates a real simultaneous guessing game layered on hidden values, and multiple legs cut the weight of the opening roll. All of this fits within one draw and one choice step per round."
  },
  "variation": {
    "name": "Button Men: Guard and Strike",
    "summary": "Two players each hold a hidden d4, d8 and d12 and simultaneously either attack an opposing die or guard one of their own, over 30 exchanges grouped into legs of up to 10. Captures score the target's size, blocked attacks reward the guard, and surviving dice score at the end of each leg.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DICE. Each player owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.\n\nRANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 191,102,975. Write R in base 24 as digits D0 to D5, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.\n\nLEGS. The match is exactly 30 exchanges. These are grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2, and player B's from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each exchange of the leg.\n\nEACH EXCHANGE:\n1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.\n2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.\n3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions:\n(1) Guard my d4\n(2) Guard my d8\n(3) Guard my d12\n(4) My d4 attacks their d4\n(5) My d4 attacks their d8\n(6) My d4 attacks their d12\n(7) My d8 attacks their d4\n(8) My d8 attacks their d8\n(9) My d8 attacks their d12\n(10) My d12 attacks their d4\n(11) My d12 attacks their d8\n(12) My d12 attacks their d12\nAn action that names a die that is already captured (yours or theirs) does nothing.\n4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.\n- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.\n- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed.\n- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.\n- A die may capture and be captured in the same exchange; both effects happen.\n5. Rerolls. Player A's rerolled die is set from D0 and player B's from D1. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). New values are shown only to their owner.\n6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.\n7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores the bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.\n8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.",
    "objective": "After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.",
    "expected_effect": "Every exchange becomes a simultaneous guessing game. A high die aimed at the big target is the obvious threat, so the opponent may guard it. That makes a cheaper attack on an unguarded d4 or d8 attractive, which in turn makes guarding the d12 a wasted turn. Guards also refresh dice that have been revealed or rolled low, so players must judge when the opponent's information about their dice is worth erasing. Repeated policies lose: 'always attack their d12' is shut down by 'always guard d12', which scores 3 per exchange; 'always guard' scores nothing against attacks on other dice; and greedy-EV play becomes predictable and can be blocked. Thirty exchanges across about four legs average out the opening rolls and give players time to learn the opponent's habits. The dice still matter, but mixing well, reading revealed values and exploiting a predictable opponent should decide most matches. There are two players, so there is no talk phase."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 1,
    "attributes": 16,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
