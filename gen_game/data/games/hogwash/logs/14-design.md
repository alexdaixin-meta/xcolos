# 14 design

- time: 2026-10-28T03:58:29+00:00 (94.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2e6e59c513fd7301, reply sha256 3c9dcec46dffa7ed

## Sent

````
Original game: Hogwash
Players in the original: 2 to 8

Original rules:
Deal the 13-rank deck evenly face down. The player left of dealer starts a central pile by playing 1-4 cards face down claiming them as 1s. Play goes clockwise, each turn the required rank increases by 1, wrapping from 13 to 1. The player must discard 1-4 cards face down claiming the required quantity and the required rank. If they lack that rank they must bluff with other cards. After any discard, any opponent may call Hogwash! to challenge the last play. Flip those cards: if they match the claim, the challenger takes the entire central pile into their hand; if they do not match, the bluffer takes the entire pile. First player to empty their hand wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Deck: 24 cards, ranks 1-4, six copies of each; 8 cards per hand. Hypergeometric odds for one hand: P(no copies of a given rank) = C(18,8)/C(24,8) = 43758/735471 = 0.059. P(at least 4 of a rank) = 0.0624 + 0.0067 + 0.0002 = 0.069. P(5 or more of a rank) is about 0.007 per rank, about 0.027 per hand.

Responder decision for one claim (cards gained by the responder; negative is good):
- k=1 claim (true about 94%): Trust = 0.94x0 + 0.06x(+1) = +0.06. Challenge = 0.94x(+1) + 0.06x(-1) = +0.88. Trust is better.
- k=4 claim (true about 7% unless the responder's own count rules it out): Trust = about 0.93x(+1) = +0.93. Challenge = 0.07x(+4) + 0.93x(-1) = about -0.65. Challenge is better.
So neither response is strictly better.

Thoughtless policies:
- Always k=4: about 93% bluffs, and any sensible responder challenges, so the bluffer swallows the pile. It loses.
- Always k=1: removes at most 1 card per turn and cannot empty before round 22. It loses.
- Always Challenge: takes k cards on every true play. It loses.
- 'Play k = my count of the required rank (true every time), always Trust': this is the real problem. The ranks rotate, so seat 1 faces 1,4,3,2 in rounds 1,4,7,10. Seat 2 faces 2,1,4,3 in rounds 2,5,8,11. Seat 3 faces 3,2,1,4 in rounds 3,6,9,12. A player with at most 4 of every rank (about 97%) can therefore dump the whole hand honestly within four turns, and nobody can profitably challenge.

Under this policy for all three players:
- Round-9 check: it fires only if a seat was dealt no copies of its fourth rank. That chance is about 1-(0.94)^3, roughly 17%, and it is a sole win only if exactly one seat lacks that rank.
- Round-12 check: otherwise all three hold 0 cards, or two hold 0 if someone was dealt 5+ of a rank. Under the WINNER RULE that is a draw.
Roughly 80% of games end as draws, and the honest-plus-trust policy essentially never loses against sensible opponents. Bluffing gains little because the honest route already empties you.

Seat edge: every end check (rounds 3,6,9,...) comes immediately after seat 3's turn. Seats 1 and 2, if they empty in rounds 10 and 11, must still answer seat 3's and each other's claims while at 0, where a wrong guess costs cards (Trust on a bluff gives +1, Challenge on a true play gives +k). Seat 3 never faces that exposure before a check. A second, smaller asymmetry: on a true play the first challenger in seat order takes exactly the k played cards, while the second takes the next k from deeper in the pile.
- reasoning_over_luck FAILED: There is real inference available. A responder can cap the opponent's possible count using 6 minus their own copies minus revealed copies; a k=4 claim when you hold 3 of the rank is a certain bluff. Hand-size tracking also helps.

Under the intended good strategy (play your true count, trust plausible claims, challenge impossible ones), no one needs to bluff, because each seat meets every rank within its first four turns. The result is then:
- about 80% draws at round 12, or
- a win at round 9 decided purely by which player happened to be dealt no copies of their fourth-faced rank.
The winner is therefore set by the deal or not at all, and a good reasoner is not clearly favoured over a merely honest one. I estimate chance and draws decide well over half of the results.
- change: Force bluffing so that inference matters. Use ranks 1-6 with 4 copies each (still 24 cards) and keep the required rank at ((r-1) mod 6)+1, with the engine's wraparound counting 6 as followed by 1. Each seat then always faces the same two ranks (seat 1: 1 and 4, seat 2: 2 and 5, seat 3: 3 and 6), so roughly two-thirds of every hand can only leave through bluffs, which opponents must read using card counting.
- change: Remove the seat-3 edge from check timing. Replace the 'multiple of 3' early end with a single fixed end after round 24. Alternatively, run the end check after every round and end the game when any player reaches 0, with the winner being the player who emptied first.
- change: Cut the draw rate. Add an arithmetic tiebreak for tied fewest cards: first, more successful challenges (bluffs caught); then, fewer times caught bluffing; draw only if still tied.
- change: Remove the first/second challenger asymmetry on true plays: each challenger takes ceil(k/2) cards from the top, or both take k, so seat order does not matter.
The variation that was reviewed: Hogwash: Three-Seat Call: SETUP. The deck has 24 cards: ranks 1, 2, 3, 4, six copies of each. Shuffle once and deal 8 cards to each of the 3 players (seats 1, 2, 3). Each hand is private; everyone always knows how many cards each player holds. The central pile starts empty. Cards in the pile are face down and unknown except when revealed by a challenge. Cards removed from the game are gone for good.

ROUNDS. There are at most 24 rounds. In round r the active player is seat ((r-1) mod 3) + 1 and the required rank is ((r-1) mod 4) + 1. So seat 1 plays rank 1 in round 1, seat 2 plays rank 2 in round 2, seat 3 plays rank 3 in round 3, seat 1 plays rank 4 in round 4, and so on. Over 24 rounds every seat is active 8 times and faces each rank exactly twice.

EACH ROUND:
1. Announce the round number, the active player and the required rank.
2. If the active player has 0 cards, they skip the turn; go to step 9. Otherwise the active player privately chooses a number k from 1 to 4. If k is more than their hand size, k becomes their hand size. They may attach one short public statement (any text, which may be untrue).
3. The engine moves k cards from the active player's hand to the top of the pile. It first takes cards of the required rank (as many as they hold, up to k). If more are needed, it takes cards of rank (required+1), then (required+2), then (required+3), counting 4 as followed by 1. The play is TRUE if all k cards are the required rank; otherwise it is a BLUFF. The engine records this privately.
4. Announce: 'Seat X claims k cards of rank R', plus the statement.
5. Simultaneous poll: each of the two other players secretly chooses Trust or Challenge. Both choices are revealed together.
6. If at least one player chose Challenge, the k played cards are revealed to everyone.
   (a) If the play was a BLUFF: the active player takes the entire pile into their hand, and the pile becomes empty. Then each player who chose Challenge removes from the game one card from their own hand: a card of the rank they hold the fewest of (counting only ranks they hold at least one of, lowest rank on a tie). If they have no cards, nothing is removed.
   (b) If the play was TRUE: the challengers, in seat order starting after the active player, each take cards from the top of the pile. The first takes the top k cards (the cards just played). If there is a second challenger, they take the next k cards from the top, or all remaining cards if fewer than k.
7. If both players chose Trust and the play was a BLUFF: announce that a bluff went unchallenged (without showing the cards). Each of the two other players, in seat order starting after the active player, takes 1 card from the top of the pile (if any remain).
8. If both chose Trust and the play was TRUE, nothing happens. The cards stay face down in the pile.
9. Announce every player's hand size.
10. End check: if the round number is a multiple of 3 and at least one player has 0 cards, the game ends. If round 24 has been played, the game ends.

The pile is a stack. 'Top' means the most recently added cards. Winner: When the game ends, the player holding the fewest cards wins. If two or three players tie for the fewest, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Hogwash is a bluffing shedding game. Players take turns discarding 1 to 4 cards face down, claiming they are the required rank, which rises by one each turn. Any opponent may call 'Hogwash!': a caught bluffer takes the whole pile, a wrong challenger takes it instead, and the first player to empty their hand wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed 3-seat version (ranks 1-4, six copies, 8 cards each), every seat faces all four ranks within its first four turns. 'Play your true count, always Trust' therefore empties about 97% of hands with no bluffing at all. About 80% of games end in all-zero draws. Every end check falls right after seat 3's turn, which gives seat 3 an edge. The first challenger on a true play takes different cards from the second."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Under sensible play the result is a draw (about 80%) or a round-9 win decided by who was dealt no copies of their fourth rank. Better reading of claims is rarely needed, so it rarely shows up in results."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "A near-optimal policy (play honestly, trust plausible claims) is trivially easy, so a strong player has little room to improve. The card-counting inference exists but is almost never needed."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hidden hands and a face-down pile allow real inference (copies left = total minus your own minus revealed). The rank rotation makes bluffing unnecessary, so that inference seldom decides anything."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Hand sizes, the truth of each play and the winner all follow by counting cards."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is turn-based, text-only and has no board. It uses a private number choice, a simultaneous poll and stack operations, and fits in about 11 steps per round over 24 rounds."
    }
  ],
  "problems": [
    "P1: Rank rotation lets every seat meet every rank in four turns, so honest play empties hands and bluffing and challenge-reading become unnecessary.",
    "P2: About 80% of games are draws, because several players reach 0 and ties are not broken.",
    "P3: Seat edge: early-end checks only after rounds that are multiples of 3 always fall right after seat 3's turn.",
    "P4: The order of challengers matters on a true play (first takes the top k cards, second takes the next k).",
    "P5: Penalties are too soft and too mechanical. A wrong challenge costs only k cards, and an unchallenged bluff makes trusters take a card. This blunts the original's high-stakes challenge and punishes a correct Trust.",
    "P6: Under good play the winner is set by the deal (who lacked a rank), not by reasoning."
  ],
  "changes": [
    {
      "what": "Use ranks 1-6 with 4 copies each (24 cards, 8 per player). The required rank in round r is ((r-1) mod 6)+1, so seat 1 always faces ranks 1 and 4, seat 2 faces 2 and 5, and seat 3 faces 3 and 6.",
      "why": "Each player holds on average only about 2.7 cards of their two ranks. Roughly two-thirds of every hand can only leave through bluffs, which opponents must read by card counting (only 4 copies of each rank exist).",
      "fixes": "P1"
    },
    {
      "what": "Drop the early-end checks. The game always lasts exactly 24 rounds, so each seat is active 8 times and answers 16 claims.",
      "why": "This removes the timing that favoured seat 3 and gives every seat the same number of turns and responses.",
      "fixes": "P3"
    },
    {
      "what": "Restore the original stakes. A caught bluffer takes the whole pile; a wrong lone challenger takes the whole pile. If two players wrongly challenge, the pile is shuffled and split evenly between them, with any odd card removed from the game.",
      "why": "Challenging becomes a real gamble whose cost grows with the pile. Seat order no longer decides who takes which cards.",
      "fixes": "P4, P5"
    },
    {
      "what": "Remove the 'unchallenged bluff makes trusters take a card' rule. Trusting never adds cards; unchallenged bluff cards simply stay hidden in the pile.",
      "why": "Trust and Challenge become a genuine read of the claimant, as in the original, and false information accumulates in the pile.",
      "fixes": "P5"
    },
    {
      "what": "Add a tiebreak for fewest cards: first, most correct challenges (bluffs caught); then, fewest times caught bluffing; draw only if still tied.",
      "why": "Players who reach 0 are separated by their reading skill, and a player at 0 still has a reason to keep making risky challenges.",
      "fixes": "P2, P6"
    }
  ],
  "keeps": [
    "Face-down discards with a public claim of quantity and rank",
    "A required rank that advances each turn and wraps around",
    "Anyone may call a challenge; the loser of the challenge takes the whole pile",
    "Shedding objective: fewest cards wins",
    "Free bluffing talk attached to the claim"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core bluff-and-call loop is a strong inference game. The problems were the rank rotation, end timing and soft penalties, and all of these can be fixed within the limits."
  },
  "variation": {
    "name": "Hogwash: Six Ranks",
    "summary": "This is a three-player bluffing shedding game. Each seat only ever faces two ranks, so most cards must be bluffed away. Opponents count cards to decide whether to call, and a wrong call costs the caller the whole pile.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP. The deck has 24 cards: ranks 1 to 6, four copies of each. Shuffle and deal 8 cards to each of seats 1, 2 and 3. Hands are private. Everyone always knows every hand size and the pile size. The central pile starts empty; its cards are face down. Each player has two public counters starting at 0: CATCHES (correct challenges) and CAUGHT (times caught bluffing).\n\nROUNDS. The game lasts exactly 24 rounds. In round r the active player is seat ((r-1) mod 3)+1 and the required rank is ((r-1) mod 6)+1. As a result, seat 1 always faces ranks 1 and 4, seat 2 faces ranks 2 and 5, and seat 3 faces ranks 3 and 6. Each seat is active 8 times.\n\nEACH ROUND:\n1. Announce the round, the active player and the required rank.\n2. If the active player holds 0 cards, they skip; go to step 8. Otherwise the active player privately chooses k from 1 to 4. If k exceeds their hand size, k becomes their hand size. They may add one short public statement, which may be untrue.\n3. The engine moves k cards from the active player's hand onto the top of the pile. It takes cards of the required rank first, up to k. If more are needed, it takes cards of the next rank up, then the next, counting 6 as followed by 1. The play is TRUE if all k cards are the required rank; otherwise it is a BLUFF. This is recorded privately.\n4. Announce: 'Seat X claims k cards of rank R', plus the statement.\n5. Simultaneous poll: each of the two other players secretly chooses Trust or Challenge. The choices are revealed together.\n6. If anyone challenged, reveal the k played cards to all.\n   (a) If the play was a BLUFF: the active player takes the entire pile into their hand, and the pile becomes empty. The active player's CAUGHT increases by 1. Each challenger's CATCHES increases by 1.\n   (b) If the play was TRUE and there was one challenger: that challenger takes the entire pile into their hand.\n   (c) If the play was TRUE and there were two challengers: shuffle the pile. Each challenger takes half of it, rounded down. If one card remains, it is removed from the game face down. The pile becomes empty.\n7. If both players chose Trust, nothing happens. The cards stay face down in the pile, true or not.\n8. Announce every player's hand size, the pile size and all CATCHES and CAUGHT counters.\n9. If round 24 has been played, the game ends.\n\nA player holding 0 cards still answers every poll. Trusting can never give them cards.",
    "objective": "After round 24, the player holding the fewest cards wins. If several players tie for fewest, the one with the most CATCHES wins. If still tied, the one with the fewest CAUGHT wins. If still tied, the game is a draw among those players.",
    "expected_effect": "With only about 2.7 matching cards per hand, every player must bluff about 5 cards away in 8 turns. Each responder must weigh the claim size against the copies they can see (4 minus their own copies minus revealed copies) and against the growing pile. Calling a big pile is very costly if wrong, and so is letting a cheap bluff through. Simple policies lose. Always k=4 is almost always a bluff and swallows the pile. Always Challenge eats whole piles on true plays. Always Trust lets rivals shed freely while gaining nothing on the tiebreak. Always k=1 empties only if never caught, and cheap challenges punish it. Players disagree because only one can win: the active player's statement is a pure bluff tool, and each responder can hope the other challenges first. Ties at 0 are settled by challenge accuracy, so reading skill decides close games. The remaining seat effect (seat 1 moves first, onto an empty pile) should be checked in testing."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 2,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 24
  }
}
```
````
