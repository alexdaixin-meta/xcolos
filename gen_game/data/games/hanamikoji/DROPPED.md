# Dropped: too complex

it could not be built to behave as designed: scenario `Active player draws 1 card from deck at turn start` failed: rule R7 is broken: At the start of each turn the active player draws 1 card from deck into hand.; the match crashed: CalcError: 'players[active_seat - 1].pending[0]': list index out of range (after 3 variation(s))

## The last variation tried

Hanamikoji: Five Geisha: Two players play 4 hands of 8 alternating turns. Each turn they draw an Item and use one of four one-shot actions to place Items beside 5 Geisha. After hands 2 and 4, Geisha markers move to whoever has strictly more Items of that Geisha. Reaching 11 Charm or 3 Geisha wins.

## What was tried

- round 1: design problem; triage said revise_rules: The game was built and behaves as specified, and its balance is acceptable (about 29-30 wins per seat against random play, no thoughtless policy dominates). The
- design 1: the critic found it not sound (playable)
- design 2: the critic found it not sound (balanced)
- round 2: behavior problem; triage said fix_game: The game deals 7 cards to each player instead of 6. After seat 1's draw and Secret, seat 1 holds 7 cards plus a secret, seat 2 holds 7 without drawing, and the 
- round 2: behavior problem; triage said fix_game: The deal is off by one. After seat 1 drew and played Secret in round 1, the trace shows 7 cards in each hand and 5 in the deck. That means the game dealt 7 card
- round 2: behavior problem; triage said fix_game: All four failing scenarios break the same way: the active seat in round 8 (Blaise in hand 1, Ada in hand 2) was scripted to play 'Trade-off', but the game never
- round 3: behavior problem; triage said fix_game: In every failing scenario the action is removed from unused_actions, but its cards never move. After Secret the hand still holds 4 cards and secret is empty, Tr
- round 3: build problem; triage said fix_game: Each attempt failed on a different coder mistake: `you` read in a step with no player, unfillable placeholders, bookkeeping fields shown to players, and an unus
- round 3: behavior problem; triage said fix_game: Three scenarios crash on 'players[active_seat - 1].pending[0]': list index out of range, so the file reads a pending card selection that was never filled. In th

To bring the game back, clear `dropped` in its inventory record.
