# Dropped: too complex

it could not be built to behave as designed: attempt 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {offer} (in `prompt`: 'Your three cards, positions 1, 2 and 3: {offer}. Choose which card to keep face-down in yo'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {church_count} (in `prompt`: 'You played {church_count} Church card(s) this round. Choose one 

## The last variation tried

Biblios: The Scriptorium (revised): Three scribes take turns drawing 3 cards, secretly keeping one, auctioning one by sealed bid and giving one away. They collect Red, Green and Blue manuscripts, Gold and Church cards that shift what each colour is worth. The majority in each colour scores its die.

## What was tried

- round 1: behavior problem; triage said fix_game: The rules are clear and within the platform's abilities, but the game file draws from the wrong end of the deck and does not put the right bid amounts to the bi
- round 1: behavior problem; triage said fix_game: The tests follow the rules, but the game does not offer the moves the rules require. Bidding seats were never given the options 0 to their gold, so every bid fe
- round 1: behavior problem; triage said fix_game: In three bidding scenarios the scripted bids never reached the game. Seat 2 was never offered 4 or 0, seat 3 was never offered 2, and Blaise and Cleo were never
- design 1: the critic found it not sound (playable)
- design 2: the critic found it not sound (playable)
- round 2: behavior problem; triage said fix_game: The game file does not follow the drawing and auction rules. In the R4 trace it took 'blue-2' from the end of the deck first, not the first two cards in order. 
- round 2: behavior problem; triage said fix_game: The tests follow R4, R8, R10 and R11 correctly. The game's auction step does not offer the non-active seats the whole numbers from 0 to their current gold as op
- round 2: build problem; triage said fix_game: Both recurring failures are faults in the file, not in the rules. The empty `message` fields are a visibility mistake, and `vp_blue` is the only colour value th
- design 1: the critic found it not sound (playable)
- round 3: build problem; triage said fix_game: The rules are sound and expressible: hidden hands and private values are supported. The coder keeps alternating between two fixable mistakes. One is writing {of
- round 3: behavior problem; triage said fix_game: In all four failing scenarios the scripted bids never reached the game. The report says the bid options (0, 2, 3, 22) were never put to the seats, and every rec
- round 3: build problem; triage said fix_game: Both recurring failures are mistakes in the game file, not limits of the rules or the platform. Prompts interpolate names the step cannot fill ({offer}, {church

To bring the game back, clear `dropped` in its inventory record.
