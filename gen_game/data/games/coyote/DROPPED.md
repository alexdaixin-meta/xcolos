# Dropped: too simple

no design got past the critic in 3 rounds; still failing reasoning_over_luck: The forced opening bid creates rounds decided by the deal alone. Declarations must be at least 1, but the true total can be as low as -4 (3 players: -2, -1, -1; 4 players: -2, -1, -1, 0), and Max→0 often pushes totals to 0 or below.

With 3

## The last variation tried

Coyote: Open Circle: Each player sees every card but their own and bids on the total of all cards. Bids strictly rise until someone calls Coyote. The loser of each round takes a token, three tokens eliminate a player, and the last player alive wins. Each round's turns run as a bounded loop of at most 16 turns that always ends in a call.

## What was tried

- round 1: behavior problem; triage said fix_game: Every failing scenario fails the same way: a responder was never offered the option 'raise'. The tests that only use 'call_coyote' and the opener's numeric decl
- round 1: behavior problem; triage said fix_tests: The game handled a declaration of 60 correctly. No raise is possible, so seat 2 was recorded as caller, the true total of 19 was below 60, and seat 1 (the decla
- round 1: behavior problem; triage said fix_tests: The game deals 1 card per player from the 33-card deck correctly: the trace shows the deck going from 33 to 30 during the hand. It then returns the cards after 
- design 1: the critic found it not sound (balanced, reasoning_over_luck)
- design 2: the critic found it not sound (balanced, reasoning_over_luck)
- round 2: behavior problem; triage said fix_game: The failures point to the game's own turn and hand bookkeeping, not to the tests or the rules. When a hand is already in progress, nobody acts, so Coyote and ra
- round 2: behavior problem; triage said fix_game: The game file has two rule bugs. It draws from the deck it already holds instead of rebuilding the full 20-card deck when a new hand begins (R3), so it crashes 
- round 2: behavior problem; triage said fix_game: In every scenario that starts with a hand already in progress (hand_active true, current_declaration set), the game played zero moves. It advanced the round wit
- design 1: the critic found it not sound (balanced, playable, reasoning_over_luck)
- design 2: the critic found it not sound (playable)
- design 3: the critic found it not sound (reasoning_over_luck)

To bring the game back, clear `dropped` in its inventory record.
