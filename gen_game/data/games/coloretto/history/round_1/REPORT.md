# coloretto: needs review

Built from the variation **Coloretto: Secret Favourites** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Each engine round is ONE turn. The active player makes one choice: PLACE the revealed top card on row 1, 2 or 3, or TAKE row 1, 2 or 3. Whose turn it is comes from public flags (who has taken in the current cycle) and the last-taker rule. The game lasts exactly 36 turns. (fixes: P1): This turns Coloretto's variable rounds into a fixed sequence of single-choice engine rounds while keeping its exact turn logic.
- Each player is secretly dealt a distinct Favourite colour from the 5 colours. If the favourite is among a player's three scoring colours at the end, that player gains +6. (fixes: P2): This adds one strong hidden element. Rivals must infer favourites from take and placement behaviour, and a player may bluff or delay showing interest. All colours are equally common, so every favourite is worth the same and there is no lottery.
- The game uses 3 players, 5 colours of 7 cards each, and 3 +2 cards (38 cards). There are no jokers and no last-round card. The game ends after turn 36, and any cards left in rows are discarded. (fixes: P3): This makes one fixed configuration that is cheap to build. A known end date replaces the random last-round card and adds an endgame timing problem: whether to take before the clock runs out.
- The deck is shuffled once at setup. The top card is always face up and visible to everyone before the active player chooses. If the player takes, the card stays on top for the next player. (fixes: P4): No random draw is needed per turn. The choice becomes a reasoned one about where this specific card should go, or whom it should be left to.

Objective: The player with the highest final score wins. If two or three players tie for the highest score, those players draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Score table (triangular): 0=0, 1=1, 2=3, 3=6, 4=10, 5=15, 6=21, 7=28. Top three colour counts score positive, the other two negative, +2 per '+2' card, +6 if the Favourite is a scoring colour. The rules call this 'favourite' scoring, and the numbers agree. Concentration is rewarded convexly: a 4th c
- playable: pass. Every situation has a rule:
- legal PLACE/TAKE conditions;
- forced TAKE when all open rows are full;
- the last remaining player continues;
- cycle reset, with the last taker active;
- a default for illegal or missing choices;
- end after round 36, with leftover row cards discarded;
- tie handling 
- reasoning_over_luck: pass. Chance comes from the deck order (only one card ahead is visible) and the random Favourites. Every player gets a Favourite worth the same +6, and a top-3-of-5 condition is easy to reach, so the deal is near-symmetric and good play can overcome it.

The decisions are skill-based:
- placing the known 

## Complexity

- steps_per_round: designed 13, built 10, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 18, built 48, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: at setup no turn has been played, the turn counter is 1, all rows are empty and nobody has scored
- pass: R2: three different Favourites are dealt from the pool of 5, leaving 2, and none is revealed yet
- pass: R3: a full row cannot be placed on, and placing on an empty open row appends one card
- pass: R3: a closed row can be neither placed on nor taken
- pass: R4: taking row 2 (red, blue) on the last turn scores 1+1 plus the Favourite bonus (green count 0 >= third count 0), so 8
- pass: R5: when every open row is full, only take options are offered
- pass: R6: with only row 1 open and full, the single option is the take of the lowest open row with a card; the score is 1+1+1 with no bonus (yellow 0 < 1)
- pass: R7: a seat that has taken this cycle is skipped, so seat 3 acts after seat 1 and seat 2 is never asked
- pass: R8: after seat 1 places, seat 2 is the next active player
- FAIL: R8: when the other two seats have taken, the placing seat is active again | rule R8 is broken: When a place or a non-final take happens, then the next active player is the next seat in order 1,2,3,1 whose taken is false, which may be the same player.; Ada: the rule for 'take_1' was never matched (the game never put that option to this seat)
- pass: R9: the third take reopens all three rows empty and the last taker stays active
- pass: R10: taking two '+2' cards on the last turn gives 4 points plus the bonus (Favourite count 0 >= 0), so 10
- pass: R11: the game ends after round 36 and the placed card is discarded; every seat has no cards and scores only the bonus of 6
- pass: R12: counts 7, 4 and 3 are worth 28+10+6 = 44 with no bonus (yellow 0 < 3)
- pass: R13: counts 3,3,3 score +18 and the lowest two (2,2) score -3-3, so 12 with no bonus
- pass: R14: three '+2' cards add 6 to colour points 3+1+1, so 11 with no bonus (purple 0 < 1)
- pass: R15: a Favourite equal to the third count earns +6 (21); a Favourite below it does not (18)
- pass: R16: at the end each seat's Favourite is copied to favourite_revealed
- pass: R17: seats 1 and 2 tie on 12 at the top and share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seats 1 and 2': 1, 'seat 1': 5, 'seat 2': 7, 'seat 3': 6, 'seats 1 and 3': 1}, 30-34 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 36.0 decisions, prompts of 244 characters on average (longest 286)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 1 and 2': 4, 'seat 1': 16, 'seat 2': 19, 'seat 3': 17, 'seats 1 and 3': 1, 'seats 2 and 3': 3}
- always `first@seat1`: won 31, lost 25, drew 4
- always `first@seat2`: won 35, lost 23, drew 2
- always `last@seat1`: won 19, lost 38, drew 3
- always `last@seat2`: won 7, lost 48, drew 5

## Triage (whose problem each failure was)

- round 1: fix_tests: The game offered take_2 as a legal move, so row 2 was open in the game's own state. The test expected take_2 to be refused and row 2 to keep its card, which only makes sense if the test marked row 2 closed while it still held a card. Under the rules that state cannot happen: a row closes only when it is taken, and taking moves all its cards into the taker's collection, so a closed row is always empty until the cycle ends. The test also depends on an internal open/closed flag whose name the interface does not fix.
- round 1: fix_tests: The game offers only legal actions: place_1 on the full row is not in seat 1's offer, so the scripted illegal move could not be played. The move actually recorded was take_2, and the game scored it correctly (one red card plus the Favourite bonus is 7). The test's expected 12 assumes row 1 was taken, which the recorded move never asked for.
- round 1: fix_game: The rules state plainly that after a PLACE the next active player is the next seat in order that has not taken this cycle, and that this can be the same player again. The engine can express this. In the test, seat 1 placed while seats 2 and 3 had already taken, and the game never offered seat 1 the take of the row it was filling, so the next-active logic is wrong.

## Choices the rules did not make

- Exactly 3 players: The designer fixed the size at 3, and the rules are built around three rows and three takers per cycle. A fourth player has no row to take, and with two the cycle logic breaks.
- No talk step: The source rules include no discussion, and adding one would add a mechanic. The strategy lies in reading the other players' collections, guessing their Favourites from what they take, and deciding when to take a small row rather than wait.
- Points written as c*(c+1)/2: This matches the source table 0,1,3,6,10,15,21,28 exactly and is arithmetic.
- Favourite pool removes dealt colours: This makes every Favourite different, as the source requires.

## Simplifications

- One action per round; the active seat is tracked in active_seat and the asked seat is taken from it: The engine runs flat rounds, so the 'who' of the ask step comes from a table attribute.
- Top-3 versus bottom-2 scoring is computed by sorting the five colour counts in a calc step: There is no lookup operation; sorting counts gives the same result as sorting points because the points table is increasing.
- Favourites are revealed by copying them to a public attribute at the end: This is the engine's way to reveal hidden player state.
