# Variation: Three Up: Even Rounds

A three-player shedding game in which every player plays a card equal to or higher than the top of a shared Pile or else takes the Pile. Clears and runs of three wipe the Pile. All three players get equal turns, the win is checked at the end of each round, and players who finish together are separated by who picked up fewer cards.

Players: 3 to 3, best with 3

## Review of the original

3Up 3Down is a shedding card game for 2 to 6 players. Each player has hidden blind cards, face-up cards and a hand, and on each turn plays a card equal to or higher than the top of the discard pile, or else picks the whole pile up. Clear cards and runs of three wipe the pile, and the first player to get rid of every card wins.

- **non_degenerate**: weak. In the original, the blind 3DOWN flips and the random refills from the draw pile are pure chance. In the previous variation, no simple policy dominated. Always picking up never sheds a card. Always playing the highest card strands low cards. Playing the lowest legal rank is competent but loses to timed forcing plays. However, First wins every race in which the players need the same number of plays, because the END CHECK ends the game immediately and First moves first. The '1' handicap costs First an extra play in only about 24% of deals (expected cost about 0.24 plays). That is a built-in seat edge.
- **skill_sensitive**: weak. The original is dominated by the draws: blind flips and refills. The previous variation removed the draw pile and stratified the deal, which made skill matter: choosing the Up pile, saving the Clear, and forcing a pickup with a 9 or a triple at the right moment. But the seat edge decides close races regardless of skill.
- **headroom**: good. A player needs about 7.9 plays with no pickups. The quality of play shows in when you dump low groups, when you block the next seat, and when you spend the Clear, so strong players keep finding improvements. Weak but legal play still sheds cards and can win when an opponent is forced into a big pickup.
- **reasoning_dependent**: good. Each hand is private, but the history of plays and the known 30-card deck let players infer what an opponent can still play. Up piles are public commitments. Timing a block or a Clear needs a plan over several turns and a prediction of the next seat's reply.
- **verifiable**: good. Legality, run counts, clears, card counts and the winner all follow by arithmetic from the recorded plays.
- **fits_platform**: weak. The original has 2 to 6 players, a draw pile, blind flips and multi-play Clear+1 and Clear+2 cards. These are heavy, but the previous variation trimmed them to fit. That variation's claim of 15 steps per round was not broken down, and its immediate mid-round win check costs a check after every turn.

## Problems

- Seat edge: the game ends the instant a player empties, so First wins every race in which players need equal numbers of plays, and with 7 to 9 plays needed such ties are common.
- The compensation for First (an extra '1') is nearly free: it costs a play in only about 24% of deals, and it can even complete a run of three 1s and clear the Pile, so it does not offset the tempo edge.
- When several players finish level, nothing decided by skill separates them; the result falls to seat order alone.
- The step budget was asserted rather than shown, and an end check after every individual turn inflates the step count.

## Changes

- Every player always gets the same number of turns. The win check happens once, at the end of each round, after all three players have acted. A player who empties mid-round simply passes on their remaining turns that round, and the others still take their turns. (fixes: Seat edge: the game ends the instant a player empties, so First wins every race in which players need equal numbers of plays, and with 7 to 9 plays needed such ties are common.): Moving first no longer lets a player finish a turn ahead of an equally fast opponent. A player who needs the same number of plays as First now finishes in the same round.
- Remove the extra '1' handicap card. Each player gets exactly 3 Low, 3 Mid, 3 High and 1 Clear, which uses all 30 cards. (fixes: The compensation for First (an extra '1') is nearly free: it costs a play in only about 24% of deals, and it can even complete a run of three 1s and clear the Pile, so it does not offset the tempo edge.): Once turns are equalised, no compensation is needed, and the handicap only created a new asymmetry of its own.
- If two or three players empty in the same round, the one who picked up the fewest cards over the whole game wins. If they are still tied, the game is a draw. The engine keeps a public 'cards picked up' count for each player. (fixes: When several players finish level, nothing decided by skill separates them; the result falls to seat order alone.): Ties in the race are settled by play quality, since avoiding pickups and forcing them on others is the core skill, not by seat.
- The step budget is laid out explicitly. Per round: 1 talk poll and 1 reveal. Per player: 1 choice, 1 apply step (play or pickup, using if-conditions) and 1 run/clear step. Then 1 end check and 1 cap check. That is 13 steps and 4 choice steps per round. (fixes: The step budget was asserted rather than shown, and an end check after every individual turn inflates the step count.): This makes the build verifiable within the 20-step and 4-choice limits.

## Kept from the original

- Shedding by playing a rank equal to or higher than the top of the Pile, or else taking the whole Pile.
- Playing several copies of one rank together, and runs of three of the same rank clearing the Pile.
- Clear cards that wipe the Pile whatever is on it.
- A chosen face-up Up pile, played only after the Hand is empty.
- The goal: be the first to get rid of all your cards.

## The variation's rules

CARDS. There are 30 cards: three copies each of ranks 1 to 9 (27 cards) and three Clear cards.

SETUP.
1. Seat the three players in a random order called First, Second and Third. Turn order is First, Second, Third in every round.
2. Make three separately shuffled stacks: Low (all 1s, 2s and 3s; 9 cards), Mid (all 4s, 5s and 6s; 9 cards) and High (all 7s, 8s and 9s; 9 cards).
3. Deal each player 3 cards from Low, 3 from Mid, 3 from High and 1 Clear, so each player has 10 cards. Every card is dealt.
4. Each player privately looks at their cards.
5. At the same moment, each player chooses exactly 3 of their cards to be their Up pile. All Up piles are then revealed.
6. A player's remaining 7 cards are their Hand, which only that player sees.
7. The discard Pile starts empty, with a run count of 0. Each player's 'picked up' count starts at 0.

PUBLIC INFORMATION. At all times everyone can see:
- every card on the Pile, its top rank and its run count (how many cards of the top rank lie on top of the Pile in a row);
- every Up pile;
- each player's number of Hand cards;
- each player's picked-up count;
- the full history of plays and pickups.

EACH ROUND (at most 40 rounds).
(a) TALK. Every player writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Messages bind no one.
(b) TURNS. First, then Second, then Third each take one turn as described below. A player who already has no cards in Hand or Up pile skips their turn.
(c) END CHECK. After Third's turn, look at every player who now has no cards in Hand or Up pile.
- If exactly one player is out of cards, that player wins.
- If two or three players are out of cards, the one among them with the lowest picked-up count wins. If they are tied on that count, the game is a draw.
- If nobody is out of cards, play continues.
(d) ROUND CAP. If round 40 ends with nobody out of cards, the player with the fewest cards (Hand plus Up pile) wins. A tie for fewest cards is broken by the lowest picked-up count. If players are still tied, the game is a draw.

A TURN. The player chooses one of two actions.
- PLAY: choose one rank and play one or more cards of that rank together, all from the same source.
  - The source must be your Hand while your Hand has any cards. You play from your Up pile only once your Hand is empty.
  - A numbered play is legal only if the Pile is empty or the rank is equal to or higher than the Pile's top rank.
  - A Clear is always legal and is played on its own.
- PICK UP: take every card on the Pile into your Hand, and add the number of cards taken to your picked-up count. The Pile becomes empty with a run count of 0. You may pick up even when you have a legal play. Picking up an empty Pile does nothing.
- An illegal or unreadable choice counts as PICK UP.

RESOLVING A PLAY.
- Numbered cards go on top of the Pile. If their rank equals the previous top rank, the run count rises by the number of cards played; otherwise the run count becomes the number of cards played.
- If the run count reaches 3 or more, the Pile is cleared: its cards are removed from the game, it becomes empty, and the run count is 0.
- A played Clear and the whole Pile are removed from the game, leaving the Pile empty.
- The turn then ends, and the next player acts on whatever Pile remains. An empty Pile accepts any card.

Objective: At the end of each round, if exactly one player has no cards left in Hand or Up pile, that player wins. If several players emptied by the end of the same round, the one with the lowest total of cards picked up during the game wins; if they are tied on that total, the game is a draw. If round 40 ends with nobody out of cards, the player with the fewest remaining cards wins, ties are broken by the lowest picked-up total, and a remaining tie is a draw.

Expected effect: Equal turns per round remove First's tempo win: two players who need 8 plays each now finish in the same round, and the one who absorbed fewer pickups wins. This makes forcing pickups on others, and avoiding them yourself, decisive in close races, instead of seat order. Always picking up loses to everything. Always playing the highest card strands low cards. The lowest-legal-rank heuristic loses to timed blocks with a 9 or a triple and to a well-saved Clear. Talk earns its place because only one player can win. The two trailing players can propose to gang up on the leader (for example, 'both play high so the leader must pick up'), but each also wants the other to absorb the cost of blocking. A player who follows a proposal can therefore spend their own high cards or their Clear while the proposer sheds freely, and lose. Players must judge which proposals serve the speaker. Remaining asymmetries, such as First's opening on an empty Pile and Third seeing the round's earlier plays, recur cyclically and are small. Seat win rates should still be confirmed by simulation.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 11 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
