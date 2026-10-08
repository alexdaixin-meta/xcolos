# Battle of Wits: High Affinity Duel

Alternating Poisoner/Chooser duel over 12 rounds where matching or mismatching Left/Right choices scores 3 on your High side or 1 on your Low side.

Players: 2 to 2

## Parameters

- `num_rounds` = 12
- `high_payoff` = 3
- `low_payoff` = 1
- `low_payoff_value` = 1
- `high_payoff_value` = 3
- `initial_score` = 0
- `type_probability_crimson` = 0.5
- `type_probability_azure` = 0.5

## Round

1. **tell** (all players): announce round_number and that poisoner_seat is Poisoner and chooser_seat is Chooser (odd rounds seat 1 Poisoner, even rounds seat 2 Poisoner)
2. **poll** (all players): simultaneously collect each player's current_choice as Left or Right: Poisoner secretly chooses poisoned goblet, Chooser secretly chooses goblet to drink; choices hidden until reveal
3. **update** (all players): copy current_choice of poisoner_seat to game last_poisoner_choice and to last_poisoner_choice_code (Left=0 Right=1); copy current_choice of chooser_seat to game last_chooser_choice and to last_chooser_choice_code
4. **update** (all players): set game last_match = 1 if last_poisoner_choice_code == last_chooser_choice_code else 0 using arithmetic 1 - abs(last_poisoner_choice_code - last_chooser_choice_code)
5. **update** (all players): compute game last_poisoner_points = last_match * (1 + 2*(1 - abs(last_poisoner_choice_code - type_code of poisoner_seat))) ; 3 if match and poisoned side equals Poisoner's High side (type_code), else 1 if match on Low side, else 0
6. **update** (all players): compute game last_chooser_points = (1 - last_match) * (1 + 2*(1 - abs(last_chooser_choice_code - type_code of chooser_seat))) ; 3 if mismatch and Chooser's chosen side equals Chooser's High side, else 1 if mismatch on Low side, else 0
7. **update** (all players): adjust total_score of player in poisoner_seat by last_poisoner_points and total_score of player in chooser_seat by last_chooser_points
8. **tell** (all players): reveal last_poisoner_choice and last_chooser_choice, announce whether match (Poisoner scores) or mismatch (Chooser scores) and how many points (3 High or 1 Low) were added; types remain hidden
9. **update** (all players): increment game round_number by 1; set poisoner_seat = 2 if now even else 1, chooser_seat = 3 - poisoner_seat for next round
10. **check** (all players): continue if round_number <= 12, else end game after 12 rounds have been scored

## Ending

- ends when: round_number > 12
- results: seat 1, seat 2, draw
- decided by: compare player total_score by arithmetic: highest total_score wins; if total_score seat 1 == total_score seat 2 then draw; winner decided solely by sum of round points (payoff_matrix resolved arithmetically)

## Choices the source did not make

- Encoded affinity_type as numeric type_code 0/1 and choices as 0/1: Source gives types as Crimson/Azure and Left/Right text; numeric encoding needed for arithmetic payoff without lookup, mapping High side = type_code
- Set parameters high_payoff=3 low_payoff=1 num_rounds=12 type_probability=0.5: Values are explicit in rules but must be listed as concrete numbers in parameters
- Mirrored player current_choice and type_code to game last_poisoner_choice_code/last_chooser_choice_code and computed match/points as game attributes: Engine has no player-attribute operand for arithmetic; workaround keeps table attribute beside score for comparison
- Visibility of affinity_type and type_code = none, total_score = public, current_choice = none until reveal via tell: Source says types stay hidden always, scores and revealed choices are announced publicly after each round

## Simplifications

- Replaced conditional branching for scoring with pure arithmetic formulas using abs and multiplication: Engine step list is flat (conditional_subsequence not supported); payoff_matrix workaround requires ~13 arithmetic steps - implemented as last_match*(1+2*matchHigh) and (1-last_match)*(1+2*matchHigh)
- Simultaneous secret choice implemented as single poll of all players instead of separate Poisoner/Chooser actions: Engine supports simultaneous_choice via poll where nobody sees answer until all are in; poll with Left/Right satisfies source's simultaneous hidden choice
- Alternating roles derived arithmetically from round_number parity and stored in game poisoner_seat/chooser_seat: Source defines odd/even role swap; flat round list can compute seat each round without conditional subsequence
- No board/grid representation: Engine is text-only with no board, grid, map or movement; game is purely choice-reveal scoring so fits naturally

## Unsupported (needs engine work)

- none
