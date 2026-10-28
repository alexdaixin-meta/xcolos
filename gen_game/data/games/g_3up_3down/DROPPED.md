# Dropped: too complex

it could not be built to behave as designed: scenario `R1: after setup each seat holds 7 in hand and 3 face-up, and the stacks are empty` failed: rule R1 is broken: When setup ends, each seat has 7 cards in hand and 3 in up_pile, every hand began as 3 low (1-3), 3 mid (4-6), 3 high (7-9) and 1 'C', and all three stacks are empty.; seat 1 hand_count: expected 7, got 10; seat 1 up_count: expected 3, got 0; seat 2 hand_count: expected 7, got 10; (after 3 variation(s))

## The last variation tried

3Up Clear Race: Three players each hold a balanced private hand of 10 cards, lock 3 of them face-up, and race to shed everything. Each play must be equal to or higher than the top of the pile. Clear cards and runs of three equal ranks wipe the pile, and a player who cannot play takes it.

## What was tried

- design 1: the critic found it not sound (balanced)
- round 1: behavior problem; triage said fix_game: After the deal each seat's hand holds 10 cards, but hand_count, up_count and cards_left all stay at 0. The game never updates the public counts. It also never m
- round 1: behavior problem; triage said fix_game: The game crashes with a CalcError: `you.hand[0]` is read on an empty hand, a fault in the file and not in the rules. The setup also never finishes the simultane
- round 1: behavior problem; triage said fix_game: The rules put choosing the Up pile in SETUP (step 5), so after setup every seat must hold 7 Hand cards and 3 public Up cards. The game dealt the cards and built
- design 1: the critic found it not sound (balanced)
- round 2: behavior problem; triage said fix_game: Under rule S6, setup must end with hand_count = 7, up_count = 3 and cards_left = 10. With rounds = 0 the game dealt the hands and listed up_offer, but it never 
- round 2: behavior problem; triage said fix_game: After setup every seat still holds 10 cards in hand and 0 up. The engine built up_offer, but the simultaneous up-set pick (S4) and the move into up_pile (S5) we
- round 2: behavior problem; triage said fix_game: Two scenarios crash with "FlowError: 'out' is not a declared status". The game file treats the interface attribute `out` as an engine status, which is a coder e
- design 1: the critic found it not sound (playable)
- round 3: behavior problem; triage said fix_game: The rules put the three simultaneous face-up picks (S3) and the count reset (S4) in setup, before round 1, but the game file finished setup with 10 cards in han
- round 3: behavior problem; triage said fix_game: The deal works, but the three face-up picks (S3) never run during setup: hands stay at 10 with up_pile empty. The pick step instead fires later, inside the roun
- round 3: behavior problem; triage said fix_game: Rules S3 and S4 say three simultaneous face-up picks happen during setup, before round 1, leaving 7 in hand and 3 in up_pile. The game finished setup with every

To bring the game back, clear `dropped` in its inventory record.
