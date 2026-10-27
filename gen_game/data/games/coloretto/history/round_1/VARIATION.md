# Variation: Coloretto: Secret Favourites

This is three-player Coloretto played one turn per round. Each turn the active player places the face-up top card on a row or takes a row. Every player secretly favours one colour worth a bonus, so rivals must read each other's interests from their play.

Players: 3 to 3, best with 3

## Review of the original

Coloretto is a card game for 2 to 5 players. On each turn a player either draws a coloured card and places it on one of several shared rows (each holding up to 3 cards), or takes a row and sits out the rest of the round. At the end each player scores their best three colours positively on a rising table and all other colours negatively.

- **non_degenerate**: good. Simple policies lose. 'Always take at once' collects 1-card rows and ends with few cards. 'Always place' is forced into full 3-card rows of colours it did not choose, which spreads it across many colours that score negatively. Where you place a card (poisoning a row a rival wants, or building one you want) and when you take both change the result. The rule that a round starts with whoever took last softens the advantage of moving first.
- **skill_sensitive**: good. The draw order is random, but each player makes many small decisions: where to place, when to stop and take, and which colours to commit to. Their effects add up, so a careful player usually beats a careless one over a game of about 30 to 40 turns.
- **headroom**: good. A weak player still scores something with three colours. A strong player keeps gaining by reading rivals' colours, timing takes against the size of the rows, and denying cards to others. The game is not solved.
- **reasoning_dependent**: weak. The only hidden thing is the order of the deck. Every tableau is public, so 'what does the opponent want' can be read straight off the table. Inference is shallow: it amounts to counting public colours plus estimating probabilities. Planning over turns and opponent modelling are present.
- **verifiable**: good. Scoring is a lookup table on colour counts, with the best three positive, the rest negative, and +2 per bonus card. One discretionary step, assigning jokers at the end, is still arithmetic.
- **fits_platform**: weak. The game is turn-based and text-only, and the rows are just piles, not a board. However, a 'round' contains a variable number of turns, so it cannot be one engine round with a few choice steps. Ending on a 'last-round card', joker assignment, rules that differ by player count, and 2 to 5 players all add steps and attributes.

## Problems

- P1: A Coloretto round has a variable number of turns, which does not fit the engine's flat, fixed-length step list of at most 4 choice steps per round.
- P2: Very little is hidden. All collections are public, so modelling an opponent is mere counting and there is no private information to infer.
- P3: Variable length (the last-round card), jokers with free assignment, and different card sets per player count add complexity and building risk with little strategic return.
- P4: Drawing a card face down and only then deciding where it goes needs a draw on every turn, and it makes the place-or-take decision partly blind.

## Changes

- Each engine round is ONE turn. The active player makes one choice: PLACE the revealed top card on row 1, 2 or 3, or TAKE row 1, 2 or 3. Whose turn it is comes from public flags (who has taken in the current cycle) and the last-taker rule. The game lasts exactly 36 turns. (fixes: P1): This turns Coloretto's variable rounds into a fixed sequence of single-choice engine rounds while keeping its exact turn logic.
- Each player is secretly dealt a distinct Favourite colour from the 5 colours. If the favourite is among a player's three scoring colours at the end, that player gains +6. (fixes: P2): This adds one strong hidden element. Rivals must infer favourites from take and placement behaviour, and a player may bluff or delay showing interest. All colours are equally common, so every favourite is worth the same and there is no lottery.
- The game uses 3 players, 5 colours of 7 cards each, and 3 +2 cards (38 cards). There are no jokers and no last-round card. The game ends after turn 36, and any cards left in rows are discarded. (fixes: P3): This makes one fixed configuration that is cheap to build. A known end date replaces the random last-round card and adds an endgame timing problem: whether to take before the clock runs out.
- The deck is shuffled once at setup. The top card is always face up and visible to everyone before the active player chooses. If the player takes, the card stays on top for the next player. (fixes: P4): No random draw is needed per turn. The choice becomes a reasoned one about where this specific card should go, or whom it should be left to.

## Kept from the original

- Shared rows of up to 3 cards, and the core choice between placing a card and taking a row and sitting out.
- Taken rows leave play for the cycle, and the last player left may keep placing on the remaining row.
- The next cycle starts with the player who took last.
- The triangular colour scoring (1, 3, 6, 10, 15, 21, 28), with the best three colours positive and all others negative.
- +2 bonus cards.
- Poisoning rows that rivals want, and judging when a row is good enough to take.

## The variation's rules

COMPONENTS. 38 cards: 7 each of Red, Blue, Green, Yellow and Purple, plus 3 '+2' cards. There are three rows, numbered 1, 2 and 3, and each holds at most 3 cards.

SETUP. Shuffle the 38 cards into a face-down deck. The top card is always shown face up to everyone. Deal each player a different secret Favourite colour, chosen at random from the 5 colours. Only that player knows it. All rows start empty and open. No player has taken. Player 1 is active.

CYCLE. A cycle runs until all three players have taken a row.
- A player who has taken a row in the current cycle sits out until the cycle ends.
- A row that has been taken is closed for the rest of the cycle.
- When the third player takes, the cycle ends immediately. All three rows reopen empty, all players become eligible again, and the player who took last is active.

TURN (one per round, 36 rounds). The game shows everyone: the face-up top card, the contents of every row and whether it is open, every player's collected cards, who has taken this cycle, and the turn number. The active player chooses one action:
(a) PLACE on row k. This is legal only if row k is open and has fewer than 3 cards. Move the top card onto row k; the next card becomes the face-up top card.
(b) TAKE row k. This is legal only if row k is open and has at least 1 card. Add all its cards to your collection, close the row, and mark yourself as taken.
If every open row is full, the player must TAKE. An illegal or missing choice becomes TAKE of the lowest-numbered open row that has a card. If there is none, it becomes PLACE on the lowest-numbered open row that has room.

NEXT ACTIVE PLAYER. After a PLACE, or after a TAKE that does not end the cycle, the next active player is the next player in seat order (1, 2, 3, 1, ...) who has not taken this cycle. This may be the same player again if they are the only one left; that player may keep placing on the remaining row until it is full, then must take it.

END. The game ends after round 36. Cards still lying in rows are discarded.

SCORING. For each colour, count the cards of that colour you hold and convert the count to points: 0 = 0, 1 = 1, 2 = 3, 3 = 6, 4 = 10, 5 = 15, 6 = 21, 7 = 28.
- Your three colours with the highest counts score positive. If counts tie for third place, either tied colour can be counted; the points are the same.
- Your other two colours score negative.
- Add 2 for each '+2' card you hold.
- Add 6 if your Favourite colour's count is at least your third-highest colour count, that is, if it can be one of your scoring colours.
All favourites are revealed at the end.

Objective: The player with the highest final score wins. If two or three players tie for the highest score, those players draw.

Expected effect: Players weigh placing a card to build a row they want, or to poison a row a rival wants, against taking early before rows are spoiled or the game clock runs out. The secret favourite turns tableau-reading into real inference. Was that take a commitment, or a bluff to make rivals poison the wrong colour? Hiding your favourite costs tempo, while revealing it invites denial. The known 36-turn end creates late-game timing problems about who will be left holding the last row. Discussion is left out: there is no shared goal, and talk would mostly be cheap claims that add steps. Thoughtless policies such as 'always take at once' or 'always place' lose to a timing-aware player.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
