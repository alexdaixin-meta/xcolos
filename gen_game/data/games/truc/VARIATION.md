# Variation: Truc Duel

Two players race to 12 points over repeated three-card rounds. One card is revealed per player, then a single secret raise poll lets each player bluff or value-bet. An unrefusable re-raise to Four is available, and a simultaneous card-ordering duel settles the last two tricks.

Players: 2 to 2, best with 2

## Review of the original

Truc is a two-player Occitan trick-taking and bluffing game. Each player holds three cards from a 32-card pack (7 highest, 9 lowest). A round is decided by best of three tricks, and either player can raise the stake with "Two more?" and force the other to accept or fold, racing to 12 points.

- **non_degenerate**: good. Every simple policy loses to a sensible opponent. Always folding gives away a point to every raise. Always raising is punished by accepting with strong hands. Never raising wins only the 1-point rounds that the cards decide. The seat effect is small: the non-dealer leads, but the follower sees the lead and the deal alternates.
- **skill_sensitive**: weak. A single round is close to a card lottery, since a three-card hand of 7s and 8s beats almost anything. Skill comes from raise and fold decisions and from bluffing over many rounds. The race to 12 is short, so a run of good hands can decide a game.
- **headroom**: good. Several skills can keep improving: judging when to bluff a raise, reading an opponent's raise frequency, folding at the right stake, and managing the score near 12 (Mon reste). A weak player still wins rounds on good cards.
- **reasoning_dependent**: good. Hands are hidden. A raise is a signal that may be a bluff. Played cards reveal part of the remaining hand and the 32-card composition limits what the opponent can hold. This is real inference about hidden state and opponent type.
- **verifiable**: good. Trick results, stakes and points all follow by comparing ranks and adding numbers.
- **fits_platform**: weak. It is text-only and turn-based. However, raises can happen before any lead and re-raise without limit. Lead and follow over three tricks plus repeats after spoils makes a variable-length chain of six or more choices per round, which needs conditional sub-sequences. The optional redeal adds a second random draw. Conceding at any time is not a fixed step.

## Problems

- P1: Open-ended raising (raise, re-raise, Mon reste, concede at any moment) cannot be built as a flat step list and exceeds 4 choice steps per round.
- P2: Lead-then-follow play of three tricks, with the leader repeating after a spoilt trick, needs 6 or more sequential choice steps and variable loops.
- P3: The optional redeal is a second random draw per round and a conditional block.
- P4: Raising happens before any information is revealed, so early raises are pure guesses. The interesting read of the opponent comes mid-round, which the flattened structure must preserve.
- P5: The round winner when tricks are spoilt is underspecified (e.g. all three spoilt, or the first trick spoilt), which an arithmetic engine cannot resolve.
- P6: A first-to-12 game has no length cap, so a run of void rounds could stall it.

## Changes

- Replace free raising with one fixed betting window after the first trick. Both players secretly and simultaneously choose Stay or "Two more". If exactly one raises, the other answers Accept, Fold or Four (a final re-raise the raiser cannot refuse). If both raise, the round is worth 4. (fixes: P1): This keeps raise, bluff, fold and re-raise in a fixed number of steps: one poll plus one conditional answer.
- Play the first trick with simultaneous card choice. After the betting window, each player secretly submits the order of their two remaining cards, which are compared in pairs as tricks 2 and 3. (fixes: P2): Two choice steps replace six or more. Simultaneous play removes the leader advantage and turns card order into a guessing duel. Revealing trick 1 before betting gives each raise real information to read.
- Place betting after trick 1 is revealed. (fixes: P4): Players bet knowing one card of the opponent's hand, and the trick-1 result matters for tie-breaks. A raise becomes a readable, bluffable signal rather than a coin flip.
- Remove the redeal. (fixes: P3): This keeps one random draw (the deal) per round and avoids a conditional block.
- Use an exact round-winner rule: most tricks won. If tied, the winner of the earliest non-spoilt trick takes the round. If all three are spoilt, the round is void. (fixes: P5): This makes every outcome arithmetic and keeps the original's 'spoilt tricks follow the first winner' spirit.
- Keep first to 12 points, but cap the game at 30 rounds. At the cap, the higher score wins and equal scores are a draw. (fixes: P6): This guarantees an end without changing the race in normal play, which lasts about 5 to 12 rounds.

## Kept from the original

- The 32-card pack and Truc's odd ranking: 7 8 A K Q J 10 9.
- Three-card hands and best-of-three tricks, with equal ranks spoiling a trick.
- The "Two more?" raise, the choice to accept or fold conceding the lower value, and a re-raise.
- Bluffing with hidden hands as the core skill.
- The race to 12 points.

## The variation's rules

CARDS. Use a 32-card pack with four cards of each of eight ranks. Suits do not matter. Rank strength from highest to lowest: 7 (strength 8), 8 (7), A (6), K (5), Q (4), J (3), 10 (2), 9 (1).

SCORES. Both players start at 0 points.

EACH ROUND:
1. Deal. Shuffle the full 32-card pack and deal 3 cards privately to each player. Each player sees only their own hand.
2. First trick. Both players secretly and simultaneously choose one card from their hand to play. If a player names a card not in their hand, their first-listed card is played. Both cards are revealed. The higher strength wins trick 1. Equal strength means trick 1 is spoilt and belongs to no one.
3. Raise poll. Both players secretly and simultaneously choose STAY or TWO MORE. The choices are then revealed.
   - Both STAY: the round is worth 1 point.
   - Both TWO MORE: the round is worth 4 points, and no one may fold.
   - Exactly one TWO MORE: that player is the raiser. The other player, the responder, now answers once with ACCEPT, FOLD or FOUR.
     - ACCEPT: the round is worth 2 points.
     - FOLD: the raiser immediately scores 1 point, and the round ends (skip steps 4 to 6).
     - FOUR: the round is worth 4 points, and the raiser may not fold.
4. Last two tricks. Each player secretly and simultaneously writes the order in which they will play their two remaining cards (first, then second). If a player's answer is invalid, their two cards are played in the order they were dealt.
   - Trick 2 compares each player's first card.
   - Trick 3 compares each player's second card.
   - In each trick, higher strength wins and equal strength is spoilt.
5. Round winner.
   - The player who won more of the three tricks wins the round.
   - If both won the same number (1-1 with one spoilt, or 0-0 with three... see below), the winner of the earliest trick that was not spoilt wins the round.
   - If all three tricks were spoilt, the round is void and no one scores.
6. Scoring. The round winner adds the round's value (1, 2 or 4) to their score.
7. End check. If a player has 12 or more points, the game ends.

ROUND CAP. If 30 rounds have been played and no one has reached 12, the game ends.

There is no talk phase. All information comes from revealed cards and choices.

Objective: The first player whose score reaches 12 or more wins. Only one player scores in any round, so two players cannot reach 12 at once. If the game ends at the 30-round cap, the player with the higher score wins, and equal scores are a draw.

Expected effect: Revealing trick 1 before betting makes the raise poll a real inference problem. Players must weigh their two remaining cards against what the opponent's revealed card and the pack composition imply, and guess whether a TWO MORE is strength or bluff.

Simple policies are each beatable:
- Always TWO MORE is beaten by a responder who answers FOUR with strong hands and accepts or folds otherwise.
- Always FOLD concedes a point to every raise.
- Always STAY wins only half the 1-point rounds while ceding big rounds.
- Always FOUR is exploited by raising only with strong hands.

The simultaneous card-order duel adds a mixed-strategy guessing layer: lead strong or save strong, informed by trick 1. Card luck still decides single rounds. Over a race to 12, the stake decisions (folding cheaply, winning big rounds) let the better reasoner win reliably. Both seats are fully symmetric.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
