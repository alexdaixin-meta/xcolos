# Variation: Hogwash: Six Ranks

This is a three-player bluffing shedding game. Each seat only ever faces two ranks, so most cards must be bluffed away. Opponents count cards to decide whether to call, and a wrong call costs the caller the whole pile.

Players: 3 to 3, best with 3

## Review of the original

Hogwash is a bluffing shedding game. Players take turns discarding 1 to 4 cards face down, claiming they are the required rank, which rises by one each turn. Any opponent may call 'Hogwash!': a caught bluffer takes the whole pile, a wrong challenger takes it instead, and the first player to empty their hand wins.

- **non_degenerate**: bad. In the reviewed 3-seat version (ranks 1-4, six copies, 8 cards each), every seat faces all four ranks within its first four turns. 'Play your true count, always Trust' therefore empties about 97% of hands with no bluffing at all. About 80% of games end in all-zero draws. Every end check falls right after seat 3's turn, which gives seat 3 an edge. The first challenger on a true play takes different cards from the second.
- **skill_sensitive**: bad. Under sensible play the result is a draw (about 80%) or a round-9 win decided by who was dealt no copies of their fourth rank. Better reading of claims is rarely needed, so it rarely shows up in results.
- **headroom**: weak. A near-optimal policy (play honestly, trust plausible claims) is trivially easy, so a strong player has little room to improve. The card-counting inference exists but is almost never needed.
- **reasoning_dependent**: weak. Hidden hands and a face-down pile allow real inference (copies left = total minus your own minus revealed). The rank rotation makes bluffing unnecessary, so that inference seldom decides anything.
- **verifiable**: good. Hand sizes, the truth of each play and the winner all follow by counting cards.
- **fits_platform**: good. The game is turn-based, text-only and has no board. It uses a private number choice, a simultaneous poll and stack operations, and fits in about 11 steps per round over 24 rounds.

## Problems

- P1: Rank rotation lets every seat meet every rank in four turns, so honest play empties hands and bluffing and challenge-reading become unnecessary.
- P2: About 80% of games are draws, because several players reach 0 and ties are not broken.
- P3: Seat edge: early-end checks only after rounds that are multiples of 3 always fall right after seat 3's turn.
- P4: The order of challengers matters on a true play (first takes the top k cards, second takes the next k).
- P5: Penalties are too soft and too mechanical. A wrong challenge costs only k cards, and an unchallenged bluff makes trusters take a card. This blunts the original's high-stakes challenge and punishes a correct Trust.
- P6: Under good play the winner is set by the deal (who lacked a rank), not by reasoning.

## Changes

- Use ranks 1-6 with 4 copies each (24 cards, 8 per player). The required rank in round r is ((r-1) mod 6)+1, so seat 1 always faces ranks 1 and 4, seat 2 faces 2 and 5, and seat 3 faces 3 and 6. (fixes: P1): Each player holds on average only about 2.7 cards of their two ranks. Roughly two-thirds of every hand can only leave through bluffs, which opponents must read by card counting (only 4 copies of each rank exist).
- Drop the early-end checks. The game always lasts exactly 24 rounds, so each seat is active 8 times and answers 16 claims. (fixes: P3): This removes the timing that favoured seat 3 and gives every seat the same number of turns and responses.
- Restore the original stakes. A caught bluffer takes the whole pile; a wrong lone challenger takes the whole pile. If two players wrongly challenge, the pile is shuffled and split evenly between them, with any odd card removed from the game. (fixes: P4, P5): Challenging becomes a real gamble whose cost grows with the pile. Seat order no longer decides who takes which cards.
- Remove the 'unchallenged bluff makes trusters take a card' rule. Trusting never adds cards; unchallenged bluff cards simply stay hidden in the pile. (fixes: P5): Trust and Challenge become a genuine read of the claimant, as in the original, and false information accumulates in the pile.
- Add a tiebreak for fewest cards: first, most correct challenges (bluffs caught); then, fewest times caught bluffing; draw only if still tied. (fixes: P2, P6): Players who reach 0 are separated by their reading skill, and a player at 0 still has a reason to keep making risky challenges.

## Kept from the original

- Face-down discards with a public claim of quantity and rank
- A required rank that advances each turn and wraps around
- Anyone may call a challenge; the loser of the challenge takes the whole pile
- Shedding objective: fewest cards wins
- Free bluffing talk attached to the claim

## The variation's rules

SETUP. The deck has 24 cards: ranks 1 to 6, four copies of each. Shuffle and deal 8 cards to each of seats 1, 2 and 3. Hands are private. Everyone always knows every hand size and the pile size. The central pile starts empty; its cards are face down. Each player has two public counters starting at 0: CATCHES (correct challenges) and CAUGHT (times caught bluffing).

ROUNDS. The game lasts exactly 24 rounds. In round r the active player is seat ((r-1) mod 3)+1 and the required rank is ((r-1) mod 6)+1. As a result, seat 1 always faces ranks 1 and 4, seat 2 faces ranks 2 and 5, and seat 3 faces ranks 3 and 6. Each seat is active 8 times.

EACH ROUND:
1. Announce the round, the active player and the required rank.
2. If the active player holds 0 cards, they skip; go to step 8. Otherwise the active player privately chooses k from 1 to 4. If k exceeds their hand size, k becomes their hand size. They may add one short public statement, which may be untrue.
3. The engine moves k cards from the active player's hand onto the top of the pile. It takes cards of the required rank first, up to k. If more are needed, it takes cards of the next rank up, then the next, counting 6 as followed by 1. The play is TRUE if all k cards are the required rank; otherwise it is a BLUFF. This is recorded privately.
4. Announce: 'Seat X claims k cards of rank R', plus the statement.
5. Simultaneous poll: each of the two other players secretly chooses Trust or Challenge. The choices are revealed together.
6. If anyone challenged, reveal the k played cards to all.
   (a) If the play was a BLUFF: the active player takes the entire pile into their hand, and the pile becomes empty. The active player's CAUGHT increases by 1. Each challenger's CATCHES increases by 1.
   (b) If the play was TRUE and there was one challenger: that challenger takes the entire pile into their hand.
   (c) If the play was TRUE and there were two challengers: shuffle the pile. Each challenger takes half of it, rounded down. If one card remains, it is removed from the game face down. The pile becomes empty.
7. If both players chose Trust, nothing happens. The cards stay face down in the pile, true or not.
8. Announce every player's hand size, the pile size and all CATCHES and CAUGHT counters.
9. If round 24 has been played, the game ends.

A player holding 0 cards still answers every poll. Trusting can never give them cards.

Objective: After round 24, the player holding the fewest cards wins. If several players tie for fewest, the one with the most CATCHES wins. If still tied, the one with the fewest CAUGHT wins. If still tied, the game is a draw among those players.

Expected effect: With only about 2.7 matching cards per hand, every player must bluff about 5 cards away in 8 turns. Each responder must weigh the claim size against the copies they can see (4 minus their own copies minus revealed copies) and against the growing pile. Calling a big pile is very costly if wrong, and so is letting a cheap bluff through. Simple policies lose. Always k=4 is almost always a bluff and swallows the pile. Always Challenge eats whole piles on true plays. Always Trust lets rivals shed freely while gaining nothing on the tiebreak. Always k=1 empties only if never caught, and cheap challenges punish it. Players disagree because only one can win: the active player's statement is a pure bluff tool, and each responder can hope the other challenges first. Ties at 0 are settled by challenge accuracy, so reading skill decides close games. The remaining seat effect (seat 1 moves first, onto an empty pile) should be checked in testing.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
