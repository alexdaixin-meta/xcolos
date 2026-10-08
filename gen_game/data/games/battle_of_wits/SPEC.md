# Battle of Wits: High Affinity Duel

Two players with hidden Crimson/Azure types alternate as Poisoner and Chooser over 12 simultaneous Left/Right picks, scoring 3 on their High side and 1 on their Low side.

Players: 2 to 2

## Parameters

- `num_rounds` = 12
- `high_payoff` = 3
- `low_payoff` = 1
- `type_probability` = 0.5

## Round

1. **update** (all players): increment game round_number by 1
2. **tell** (all players): announce game round_number and who is Poisoner and who is Chooser this round (odd: seat 1 Poisoner / seat 2 Chooser, even: seat 2 Poisoner / seat 1 Chooser)
3. **poll** (all players): each player's current_choice set to chosen Left or Right simultaneously; Poisoner's choice is poisoned goblet, Chooser's choice is goblet to drink, hidden until reveal
4. **sync** (all players): reveal both players' current_choice to all players
5. **update** (all players): if game round_number is odd (seat 1 Poisoner) and seat 1 current_choice == seat 2 current_choice and seat 1 player_type == Crimson and seat 1 current_choice == Left then adjust seat 1 score by 3 (match on Poisoner's High)
6. **update** (all players): if game round_number is odd and seat 1 current_choice == seat 2 current_choice and seat 1 player_type == Azure and seat 1 current_choice == Right then adjust seat 1 score by 3 (match on Poisoner's High)
7. **update** (all players): if game round_number is odd and seat 1 current_choice == seat 2 current_choice and not High match then adjust seat 1 score by 1 (match on Poisoner's Low)
8. **update** (all players): if game round_number is even (seat 2 Poisoner) and seat 1 current_choice == seat 2 current_choice and seat 2 player_type == Crimson and seat 2 current_choice == Left then adjust seat 2 score by 3
9. **update** (all players): if game round_number is even and seat 1 current_choice == seat 2 current_choice and seat 2 player_type == Azure and seat 2 current_choice == Right then adjust seat 2 score by 3
10. **update** (all players): if game round_number is even and seat 1 current_choice == seat 2 current_choice and not High match then adjust seat 2 score by 1
11. **update** (all players): if game round_number is odd (seat 2 Chooser) and seat 1 current_choice != seat 2 current_choice and seat 2 player_type == Azure and seat 2 current_choice == Right then adjust seat 2 score by 3 (mismatch, Chooser High)
12. **update** (all players): if game round_number is odd and seat 1 current_choice != seat 2 current_choice and seat 2 player_type == Crimson and seat 2 current_choice == Left then adjust seat 2 score by 3
13. **update** (all players): if game round_number is odd and seat 1 current_choice != seat 2 current_choice and not Chooser High then adjust seat 2 score by 1 (mismatch, Chooser Low)
14. **update** (all players): if game round_number is even (seat 1 Chooser) and seat 1 current_choice != seat 2 current_choice and seat 1 player_type == Crimson and seat 1 current_choice == Left then adjust seat 1 score by 3
15. **update** (all players): if game round_number is even and seat 1 current_choice != seat 2 current_choice and seat 1 player_type == Azure and seat 1 current_choice == Right then adjust seat 1 score by 3
16. **update** (all players): if game round_number is even and seat 1 current_choice != seat 2 current_choice and not Chooser High then adjust seat 1 score by 1
17. **tell** (all players): announce both current_choice values, whether choices matched or mismatched, who scored and how many points (3 or 1), types stay hidden
18. **check** (all players): continue if game round_number < 12, otherwise end game

## Ending

- ends when: game.round_number >= 12
- results: seat 1, seat 2, draw
- decided by: highest total score wins; if seat 1 score > seat 2 score result is seat 1, if seat 2 score > seat 1 score result is seat 2, otherwise draw

## Choices the source did not make

- none

## Simplifications

- Payoff matrix implemented as 12 conditional single-step updates with when conditions instead of lookup operation: Engine has no payoff_matrix lookup; workaround requires arithmetic conditional updates (about 13 steps for 9 cells) - here 8 scoring cases split by parity
- Simultaneous hidden choices implemented via poll storing each player's current_choice and comparing equality to detect match/mismatch, rather than a Poisoner-only then Chooser-only step: Engine poll addresses all players at once; using poll guarantees simultaneity with no player hearing earlier answer, as required; match detection is equivalent to poisoner_choice == chooser_choice

## Unsupported (needs engine work)

- none
