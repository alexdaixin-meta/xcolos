# Variation: Code 777: Ask and Guess

Each player sees everyone's tiles but their own. Each turn the active player chooses a question and a respondent, the engine answers it publicly from the respondent's view, and then everyone may risk a guess at their own three numbers. First to 3 points wins.

Players: 3 to 4, best with 3

## Review of the original

Code 777 is a deduction game for 2 to 5 players. Each player sees everyone's number tiles except their own three. Players take turns drawing a question card and answering it publicly from what they see. Anyone may interrupt at any moment to guess their own three numbers: a correct guess scores 1 point, and the first player to 3 points wins.

- **non_degenerate**: weak. Deduction drives results, but the free interrupt makes speed of shouting matter. A wrong guess costs nothing in points: it only resets your rack, which can even replace a hard rack with an easy one. A spam-guess policy is therefore cheap. Always-pass scores 0 and loses, which is fine.
- **skill_sensitive**: weak. Good deducers win more often. However, which question card comes up, and therefore who it helps, is pure luck. Freshly dealt racks vary a lot in how easy they are to deduce (a rack holding the single 1 is far easier). Real-time reflexes also decide close races.
- **headroom**: good. Weak players still deduce something from obvious answers. Strong players combine every public answer with tile-supply counting (one 1, two 2s, up to seven 7s) and discarded tiles, and they judge the right moment to risk a guess.
- **reasoning_dependent**: good. The core is inference about a hidden state, your own rack. You reason from other players' answers, which describe a view that includes your rack and excludes theirs.
- **verifiable**: good. Guesses are right or wrong and points are counted. The only soft spot is that players answer questions themselves and could err; an engine can compute the answers instead.
- **fits_platform**: bad. Interrupting at any time is real-time play, which the engine does not support. The random question deck plus random tile replacement is two chance events per turn. Colors double the tracked state (number plus color for every tile), which overflows the attribute limit with 4 players.

## Problems

- P1: Guessing by interrupt at any moment is real-time, which the engine does not support, and it rewards speed rather than reasoning.
- P2: A wrong guess costs no points, so blind or premature guessing is nearly free, and resetting your rack can even help.
- P3: A random question deck decides what information appears and whom it helps. That is luck, and a second chance event each turn, together with tile replacement.
- P4: Players have no strategic choice in what to ask, so there is little opponent modelling beyond the race to guess.
- P5: Tracking colors as well as numbers for every tile exceeds the attribute limit with 4 players and lengthens every question.
- P6: There is no length cap; a game where nobody reaches 3 could run indefinitely.

## Changes

- Replace interrupts with a simultaneous guess poll at the end of every round: each player either guesses their three numbers or passes. (fixes: P1): It is turn-based and removes the reflex advantage; every player gets the same chance to act on the same information.
- A wrong guess costs 1 point, and scores may go negative. Your rack is still replaced after any guess, right or wrong. (fixes: P2): Guessing becomes a calculated risk, so you guess only once your deduction is confident. The always-guess policy now sinks below zero.
- Drop the question deck. The active player picks a question from a fixed menu of six, and names which other player (the respondent) must have the engine answer it from that player's point of view. (fixes: P3): This removes the luck of the question draw and leaves only one chance event per round, the tile replacement. Choosing the question means steering the information toward your own rack. Choosing the respondent means denying information to the leader, because the respondent learns nothing about their own rack from their own answer. Both choices take planning and opponent modelling.
- The engine computes every answer exactly from the tiles. (fixes: P3): Answers are verifiable and cannot be lied about or miscounted.
- The asker's choice of question and respondent is a deliberate strategic act, as described above. (fixes: P4): Every turn becomes a decision about which information to release and to whom.
- Remove colors. Tiles are numbers only, and the menu uses number properties instead (even, high, specific number, rack sum, pairs, missing numbers). (fixes: P5): It keeps state within 20 attributes for 4 players and keeps every question a simple count.
- Cap the game at 10 rounds per player (30 rounds with 3 players, 40 with 4). The first player to 3 points wins. At the cap, the highest score wins. (fixes: P6): This bounds the length. Each seat asks equally often, so asking first is not an edge.

## Kept from the original

- You see every rack except your own and must deduce your own three numbers.
- The 28-tile pool of one 1, two 2s, through seven 7s, so supply counting is a deduction tool.
- Public questions answered from one player's view, which tell everyone else about their own racks.
- Guess your exact three numbers to score 1 point; your rack is then replaced from the pile.
- First to 3 points wins.

## The variation's rules

TILES. There are 28 tiles: one 1, two 2s, three 3s, four 4s, five 5s, six 6s and seven 7s.

SETUP. Shuffle the tiles into a face-down pile. Deal 3 tiles to each player's rack. Each player is told privately the numbers on every OTHER player's rack, but never their own. Each player starts with 0 points. The discard pile starts empty and is public: everyone always sees which tiles are in it. Seats are numbered 1 to N. Seat 1 is the active player in round 1, and the active player then rotates in seat order each round.

EACH ROUND:
1. The engine announces the round number and the active player.
2. The active player makes one choice: a question from the menu below, and a respondent, who must be one other player. For question 3, the active player also names a number k from 1 to 7.
3. The engine computes the answer exactly, counting only the tiles the respondent can see: every rack except the respondent's own. This includes the active player's rack. The engine announces the question, the respondent and the answer to everyone.
   Menu:
   (1) EVEN: how many even tiles (2, 4, 6) do you see?
   (2) HIGH: how many tiles numbered 5, 6 or 7 do you see?
   (3) NUMBER k: how many tiles numbered k do you see?
   (4) SUM15: how many of the racks you see total 15 or more?
   (5) PAIR: how many of the racks you see hold at least two tiles of the same number?
   (6) MISSING: how many of the numbers 1 to 7 appear on none of the racks you see?
4. GUESS POLL. All players answer at the same moment, without seeing each other's answers. Each either writes PASS or writes three numbers (order irrelevant) as a guess at their own rack.
5. SCORING. A guess that matches the player's rack exactly as a set of three numbers, duplicates included, scores +1 point. Any other guess scores -1 point. PASS scores 0. Scores may be negative.
6. REVEAL AND REPLACE. Every player who guessed, right or wrong, has their three tiles announced to all and moved to the discard pile. If the face-down pile then holds fewer tiles than are needed, the discard pile is shuffled into it. The engine then deals 3 new tiles to each player who guessed. This is the round's single random event.
7. Every player is privately told the current racks of all OTHER players.
8. END CHECK. If any player has 3 or more points, the game ends. Otherwise, if the final round has been played, the game ends. The final round is round 30 with 3 players and round 40 with 4 players.

There is no talk phase; the engine-answered questions are the only shared information.

Objective: When the game ends because someone reached 3 points, the player with the most points wins. If two or more players share that top score, the game is a draw. If the round limit is reached instead, the player with the highest score wins, and a tie for the highest score is a draw.

Expected effect: Players must combine public answers, tile-supply counting and the public discard pile to narrow their own rack, then judge when to guess. The -1 penalty punishes impatience, and always-guess goes deeply negative. Always-pass scores 0 and loses to anyone who scores. Every question informs all players except the respondent, so the asker must pick a question that pins down their own rack while naming as respondent the opponent who is closest to a guess, denying them that information. Simultaneous guessing removes reflexes. Rotating askers with 10 asks each balances the seats. Many rack replacements over a game average out easy and hard deals. Talk is omitted: the only thing players could usefully say is (possibly false) statements about other players' racks, which would replace deduction with kingmaking and noise rather than add a real decision.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
