# Dropped: too complex

it is too large for the platform: the built game has 45 attributes, over the limit of 20 (after 3 variation(s))

## The last variation tried

Hanabi Duo: A two-player, 12-card Hanabi. Partners see each other's two cards but not their own. They spend scarce hints, discard to regain them, and try to build Red and Blue piles from 1 to 3. The team wins together if its score reaches 4.

## What was tried

- design 1: the critic found it not sound (playable)
- round 1: build problem; triage said fix_game: Each attempt failed on a different file-level problem: visible scratch fields, attributes that never change, an unused attribute. The coder has fixed the earlie
- round 1: behavior problem; triage said fix_tests: The game deals from a random shuffle, as the rules require, yet the failing tests assert specific card faces (#1=R1, #5=R3, #2=G1) that chance decides. The game
- round 1: behavior problem; triage said fix_game: The scenarios set each seat's hand through the game's own parallel lists hand_ids and hand_faces. The game instead looks up a revealed card's face in a separate
- round 2: design problem; triage said revise_rules: The game file follows the rules, but the design is too large and too hard. It needs 64 attributes against a limit of 20, with about 31 parameters alone. Random 
- round 3: design problem; triage said revise_rules: The game was built correctly, but the design needs 45 attributes against a limit of 20; the required parameter list alone has 21 entries. Random teams also win 

To bring the game back, clear `dropped` in its inventory record.
