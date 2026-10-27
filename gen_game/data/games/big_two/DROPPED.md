# Dropped: too complex

no design got past the critic in 3 rounds; still failing playable, reasoning_over_luck: The limits are met: steps 16 ≤ 20, choices 3 ≤ 4, rounds 39 ≤ 40, one shuffle per deal round, hidden elements 2 (hands and asides). About 18 attributes is plausible if each hand is stored as a list (3 hands, 4 asides, 3 penalties, play valu

## The last variation tried

Big Two: Balanced Climb: Three players play three hands of a suitless climbing game. Everyone holds one card of each value plus two random extras, which form their two pairs. Tricks are one pass of three turns and each trick won is worth a point. Players infer the hidden extras to decide when to spend their high cards.

## What was tried

- round 1: behavior problem; triage said fix_game: The game encodes multi-card combinations as concatenated numbers (the pair 13+14 is offered as 1314). That form is ambiguous (123 could be 1+23 or 12+3) and unr
- round 1: behavior problem; triage said fix_tests: After seat 2 played 22, seats 3 and 1 both passed, so by the clearing rule the pile was cleared and seat 2 had to lead. Its lead of 3 was legal and emptied its 
- round 1: behavior problem; triage said fix_game: In R1 seat 1 sent the move '13 14', which the game itself offered as a pair. The game recorded 'played 13', removed only one card and set the pile to single 13.
- round 1: behavior problem; triage said fix_game: In R1 the game offered '13 14' and seat 1 chose it, yet only card 13 left the hand and the pile became a single of 13. The file is resolving a multi-card answer
- round 2: design problem; triage said revise_rules: The game is built correctly, but a thoughtless policy (always take the last offered option, which is the biggest multi-card play or bomb) wins 77-90% of games. 
- design 1: the critic found it not sound (playable)
- design 2: the critic found it not sound (reasoning_over_luck)
- design 3: the critic found it not sound (playable, reasoning_over_luck)

To bring the game back, clear `dropped` in its inventory record.
