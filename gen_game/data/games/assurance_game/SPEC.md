# Assurance Threshold - Three Hunters

Three hunters with hidden sheltered/exposed types simultaneously choose to invest (C) or not (D) for ten rounds, scoring by threshold participation payoffs toward a 38-point target.

Players: 3 to 3

## Parameters

- `rounds` = 10
- `payoff_c_all_cooperate` = 5
- `payoff_c_sheltered_partial` = 1
- `payoff_c_exposed_partial` = 0
- `payoff_d_lone_defector` = 4
- `payoff_d_other` = 2
- `win_threshold` = 38
- `type_probability_sheltered` = 0.5

## Round

1. **poll** (all players): each player simultaneously chooses C (hunt stag / invest) or D (hunt hare / do not invest), stored in player.choice
2. **update** (all players): set game.n_c to count of players with choice==C (0-3) and increment game.round_number by 1
3. **update** (all players): adjust player.total_score and set player.round_payoff: if player.choice==C and game.n_c==3 add payoff_c_all_cooperate (5); else if player.choice==C and game.n_c!=3 and player.type==Sheltered add payoff_c_sheltered_partial (1); else if player.choice==C and game.n_c!=3 and player.type==Exposed add payoff_c_exposed_partial (0); else if player.choice==D and game.n_c==2 add payoff_d_lone_defector (4); else if player.choice==D and game.n_c!=2 add payoff_d_other (2)
4. **tell** (all players): tell each player game.n_c and their own player.round_payoff and player.total_score; do not reveal other players' choices or types
5. **check** (all players): continue if game.round_number < rounds (10), otherwise end game

## Ending

- ends when: game.round_number >= 10
- results: seat 1, seat 2, seat 3, shared win, draw
- decided by: after 10 rounds count players with player.total_score >= win_threshold (38): if count==1 sole winner is that seat; if count>1 shared win among those seats (draw among qualifiers); if count==0 draw; higher total without reaching 38 does not win

## Choices the source did not make

- 3 to 3 players: Coordination with threshold 3 and lone-defector bonus at n_C==2 only meaningful with exactly 3; with 2 there is no threshold tension, with >3 payoff thresholds 3 and 2 become arbitrary and one player's deviation matters less. Minimum 3 makes agreement hard and a single holdout breaks full cooperation.
- No pre-round communication poll: Source rules have simultaneous choice with no talk; adding free-text talk would change assurance dilemma into bargaining and is not in source. With 3 players payoff conflict already gives disagreement without talk.
- Use poll for simultaneous C/D choice: Source says simultaneously every player chooses; poll is required so later players do not see earlier answers, per engine capability
- Parameter values 5,4,2,1,0 and threshold 38: Source fixes 5>4>=2>1 and 5>4>=2>0 and example satisfies with 5 for C if n_C==3, 1 if Sheltered else 0 if Exposed when C and n_C!=3, 4 if D and n_C==2 else 2; threshold 38 explicitly given for winner determination
- Win condition as shared win / draw, not ranking: Source says higher total alone does not win unless it reaches 38; multiple qualifiers draw among themselves, zero qualifiers is draw. Implemented as arithmetic count of qualifiers, not highest-score ranking.

## Simplifications

- Payoff matrix implemented as conditional arithmetic updates instead of lookup table: Engine has no payoff-matrix lookup; same arithmetic effect achieved with conditional adds per player using n_c and type (supported with workaround: ~5 conditional branches)
- n_C and private payoff revealed via tell/sync rather than separate private channels: Engine's tell/sync delivers private state; matches source 'each player is told n_C and their own payoff, but not who chose what'
- Type draw implemented as independent 50% via initial hidden attribute: Engine initialize with hidden_hands/private_values; no deck needed

## Unsupported (needs engine work)

- none
