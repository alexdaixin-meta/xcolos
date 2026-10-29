# Dropped: too simple

no design got past the critic in 3 rounds; still failing balanced: WOLF NIGHT CARD (the only real card choice in the game). A wolf picks Maul or Salve and a target. Humans can only Salve, so a wolf's wounds can never rise except from its own partner. Night cards and targets are never revealed, and only net

## The last variation tried

Growl: Trial by Moonlight: 7 players, 2 secret wolves. Each day everyone talks at once and then votes. The top vote-getter is put on Trial and their true role is revealed. Wolves die, while innocent humans are cleared but wounded. Each silent night, wolves Maul and everyone Salves. Wolves win at parity, or if humans are fewer than twice the wolves after the Final Night (round 5). Humans win by killing both wolves or by keeping that 2:1 ratio.

## What was tried

- design 1: the critic found it not sound (balanced, reasoning_over_luck)
- round 1: build problem; triage said fix_game: The rules are sound and the engine can express them. Attempt 4 loaded and played, so the `game.` reference in rank_by can be written in a form the loader accept
- round 1: behavior problem; triage said fix_game: Every failing scenario crashed with the same engine error, FlowError: 'out' is not a declared status. The game file uses a player status named 'out' that it nev
- round 1: build problem; triage said fix_game: Each attempt fails for a different coder-side reason: a wrong reference in rank_by, bookkeeping fields left visible, attributes that are declared but never set,
- design 1: the critic found it not sound (balanced, playable, reasoning_over_luck)
- design 2: the critic found it not sound (balanced, playable, reasoning_over_luck)
- design 3: the critic found it not sound (balanced)

To bring the game back, clear `dropped` in its inventory record.
