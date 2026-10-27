# Dropped: too simple

no design got past the critic in 3 rounds; still failing balanced: Thoughtless policies under the WINNER RULE (end-of-turn-40 shortfall, or an early win check). Always PASS: 0 points and shortfall 30 or 31. It loses to any opponent who plays even one point card and draws only an all-pass opponent, so it fa

## The last variation tried

Cuttle Lite: Grace Turn (rev. 3): A two-player race to a point threshold. Exact point ranks are hidden behind bands, each player holds one Jack and one King, and scuttles refund a card when they succeed, so reading the opponent and timing your answer decides the race.

## What was tried

- design 1: the critic found it not sound (balanced, reasoning_over_luck)
- round 1: behavior problem; triage said fix_game: The scuttle and Jack scenarios crash inside the game's own bookkeeping: it reads `pile_ranks[target_index - 1]` from a list that does not hold the targeted card
- round 1: behavior problem; triage said fix_game: The rules say an illegal or unparseable reply counts as PASS, so nothing should change. When the test sent an unusable reply, the game resolved it to 'draw' and
- round 1: behavior problem; triage said fix_game: In three end-of-game scenarios the file sets `won` = 1 for a player whose points (0) are below their threshold (30). So the start-of-turn win check, or an end-o
- design 1: the critic found it not sound (playable)
- design 2: the critic found it not sound (balanced, reasoning_over_luck)
- design 3: the critic found it not sound (balanced)

To bring the game back, clear `dropped` in its inventory record.
