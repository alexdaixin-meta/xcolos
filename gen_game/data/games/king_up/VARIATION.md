# Variation: King Up: Fair Throne

Each player secretly favours 3 characters that no one else favours. Players take turns raising characters toward height 5. Every character reaching height 5 faces a unanimous vote, and a single anonymous No eliminates it. Players score by the final heights of their favoured characters.

Players: 3 to 5, best with 4

## Review of the original

King Up is a 3-6 player game of hidden goals. Players secretly favour certain characters, take turns raising characters up castle floors, and vote on each character that reaches the throne. One secret No vote eliminates a candidate. Players score by how high their favoured characters finish.

- **non_degenerate**: weak. With 3 players nothing degenerate survives. Always Yes crowns rivals' characters and loses about 2 games in 3 even against random play. Always No burns cards, sometimes on the player's own characters, and leaves them unable to veto later. Always raising the same character reveals the goal and gets that character vetoed. The previous variation still gave seats an edge with 4-5 players. Seats 1-3 held disjoint triples, while seats 4-5 drew from a second shuffle. So the later seats' characters were always co-owned, which handed them built-in Yes allies, and about 3.6% of the time a late seat's triple duplicated another player's and could not win outright. First-raiser counts were also unequal (4,4,4,3 over 15 rounds with 4 players).
- **skill_sensitive**: good. The only randomness is the goal deal, and it changes what each player knows, not who is ahead. The result comes from raising decoys to hide one's goal, guessing rivals' goals from their raises, choosing when to spend a scarce No, and deciding when ending the game helps.
- **headroom**: good. A weak player still scores the heights of their own characters. A strong player can keep improving at bluffing with raises, reading the anonymous No counts, tracking how many No cards may remain, and timing the throne push. There is no simple solved line.
- **reasoning_dependent**: good. Three things are hidden: goals, No-card counts and who voted No. Every raise and vote has to be read as evidence about rivals' goals. Players must plan over rounds because raises to height 5 are eventually forced.
- **verifiable**: good. Scores are sums of fixed values per height. The winner is the highest total, a plain arithmetic comparison.
- **fits_platform**: weak. The original's floors are only numbers, so no spatial board is needed. But its free movement between floors, its three-round structure and the round-3 rule turning zero into 33 make it long and branchy. The earlier variation flattened this into one game of up to 15 rounds of numeric heights, which fits. Storing eliminated and crowned characters as separate state wasted attributes.

## Problems

- P1: Goals are not seat-symmetric with 4-5 players. Later seats draw from a second shuffle, so their characters are always co-owned (built-in voting allies), and they can be dealt a triple identical to another player's.
- P2: First-raiser turns are unequal when the round limit is not a multiple of the player count (15 rounds with 4 players gives 4,4,4,3).
- P3: The rotation direction and the raise order were not stated in the same terms, so seat order could be built inconsistently.
- P4: Eliminated and crowned status took extra attributes, pushing the attribute count toward the limit of 20 with more characters.
- P5: The No-card count differed by player count (1 each with 5 players), which would make vetoes too scarce once 15 characters are in play.

## Changes

- Use 3 characters per player (9 for 3 players, 12 for 4, 15 for 5) and deal each player a disjoint triple from one shuffle. Every character is favoured by exactly one player. (fixes: P1): Every seat gets the same goal structure. No seat has built-in allies or can be dealt a duplicate goal, and the sound 3-player logic (owner gains +5 if crowned, loses 5 if eliminated, non-owners only care about game length) carries over to every player count.
- Set the round limit by player count: 15 rounds for 3 players, 16 for 4 and 15 for 5. (fixes: P2): Each limit is a multiple of the player count, so every seat is first raiser equally often (5, 4 and 3 times). Raises still outnumber what heights 0-4 can absorb (45>36, 64>48, 75>60), so pushes to the throne are eventually forced.
- Define seat order once: ascending seat number, wrapping from the highest seat to seat 1. Both the raise sequence and the first-raiser rotation follow it. (fixes: P3): Removes the ambiguity between 'left' and seat order.
- Store status inside each character's height: -1 means eliminated, 6 means king, 0 to 5 means active. (fixes: P4): One attribute per character. That gives 15 heights plus goal, No cards, round number and first raiser = 19 attributes at 5 players.
- Give every player 2 secret No cards at every player count. (fixes: P5): With 3n characters and 2n No cards, vetoes stay scarce and strategic but meaningful at 5 players. The game still ends by a king or the round limit.

## Kept from the original

- Secret goals of favoured characters
- Characters climbing numbered levels toward a throne
- Unanimous election: one anonymous No eliminates the candidate
- Unlimited Yes and scarce, secret No cards
- Scoring by final height, with the king worth 10 and an eliminated character worth 0
- Bluffing through which characters you raise

## The variation's rules

SEAT ORDER. Seats are numbered 1 to N (N = 3, 4 or 5). 'Seat order' always means ascending seat number, wrapping from seat N back to seat 1.

SETUP.
- Use 3N characters, labelled with letters: A-I for 3 players, A-L for 4, A-O for 5.
- Each character has a public height, starting at 0. Height also records status: -1 means eliminated, 6 means king, and 0 to 5 means active.
- Shuffle all labels once. Deal 3 to seat 1, the next 3 to seat 2, and so on. Every character is favoured by exactly one player, and no two players share a character.
- Each player's 3 characters are their secret goal.
- Each player receives 2 secret No cards. Yes votes are unlimited. The number of No cards a player holds is secret.
- The round limit is 15 rounds with 3 players, 16 with 4 and 15 with 5.
- Seat 1 is the first raiser in round 1.

EACH ROUND:
1. Announce. Show everyone all heights and the round number.
2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.
3. Raise. Starting with this round's first raiser and going in seat order, each player in turn raises one active character's height by 1. A character may go from 4 to 5 only if no character is currently at height 5. No height may exceed 5. A player with no legal raise passes.
4. Election. If a character is at height 5, it is the candidate, and every player votes Yes or No at the same time. A player with no No cards left must vote Yes. If no character is at height 5, skip steps 4 and 5.
5. Resolve.
   - If all votes are Yes, the candidate's height becomes 6 (king) and the game ends after this round.
   - If any vote is No, each No voter loses one No card and the candidate's height becomes -1 (eliminated for the rest of the game). Only the number of No votes is announced, not who cast them.
6. Rotate. The first raiser for the next round is the next seat in seat order.
7. End check. The game ends if a king was crowned or the round limit has been played.

SCORING. Each player reveals their goal. For each of their 3 characters they score:
- 10 if its height is 6 (king);
- 0 if its height is -1 (eliminated);
- otherwise its height (0 to 5).
A player's score is the sum of these three values.

Objective: The player with the highest score wins. If two or more players tie for the highest score, the game is a draw among them.

Expected effect: Every seat now has the same goal structure and the same number of first-raiser turns, so the seat edge is gone.

Play centres on four things:
- raising decoys to hide one's goal;
- inferring rivals' goals from their raises and from anonymous No counts;
- spending the two No cards on threatening candidates rather than wasting them;
- choosing whether to let a candidate through to end the game while ahead.

Talk passes both tests.
- What players disagree about: each candidate has exactly one owner who wants it crowned. The others want it vetoed unless they lead and want the game over.
- Why reasoning is needed: players propose vetoes, claim false goals and try to bait rivals into spending No cards.
- How a follower loses: a player who obeys the call 'everyone veto C' may be spending a scarce No for the caller's benefit, or may be fooled into crowning the caller's own character.

The thoughtless policies all lose. Always Yes crowns rivals' characters. Always No exhausts both cards and may hit the player's own characters. Always raising one character exposes it to a veto. When everyone plays well, the deal only fixes who owns what. Every goal is equally placed, so reading and timing decide the winner.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
