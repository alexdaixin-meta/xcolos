# 11 design

- time: 2026-10-28T03:53:43+00:00 (156.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 a7f0dfcb7db11e84, reply sha256 a57859ad84d36789

## Sent

````
Original game: Hogwash
Players in the original: 2 to 8

Original rules:
Deal the 13-rank deck evenly face down. The player left of dealer starts a central pile by playing 1-4 cards face down claiming them as 1s. Play goes clockwise, each turn the required rank increases by 1, wrapping from 13 to 1. The player must discard 1-4 cards face down claiming the required quantity and the required rank. If they lack that rank they must bluff with other cards. After any discard, any opponent may call Hogwash! to challenge the last play. Flip those cards: if they match the claim, the challenger takes the entire central pile into their hand; if they do not match, the bluffer takes the entire pile. First player to empty their hand wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Cut the choice steps per round to at most 4. Drop the separate free-text talk step, or fold talk into the play step, so each turn is one play choice plus one simultaneous challenge poll. If the 4-player count still exceeds the limit, count a round as one turn rather than a full cycle. Then rebalance so no fixed option ordering wins. As written, playing 1 card while never challenging, or a similar first-option default, is safe and strong: playing few cards rarely costs much, and challenging risks taking the whole pile. Options to try: (1) Require a minimum play that grows with pile size, or set the minimum at 2 when the player holds enough cards, so slow-dumping 1 card is not free. (2) Lessen the challenger's risk on a true claim, for example the challenger takes only the cards just played rather than the whole pile, so challenging bluffs is worthwhile and constant bluffing or constant passing is punished. (3) Make the challenge decision count for the player who challenges against a bluff, for example the challenger subtracts the revealed cards from their taken counter. Re-check that neither all-first nor all-last policies win clearly above the random baseline of about one third.
the game was built and behaves as specified, but evaluation found design flaws:
- the built game has 6 choice steps per round, over the limit of 4
- against random seats the results were {'seat 1': 20, 'seat 3': 17, 'seat 2': 23}
- a thoughtless policy `first@seat1`: won 46, lost 14, drew 0
- a thoughtless policy `first@seat2`: won 48, lost 12, drew 0
- a thoughtless policy `last@seat1`: won 14, lost 45, drew 1
- a thoughtless policy `last@seat2`: won 12, lost 48, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Hogwash (also known as Cheat or BS) is a shedding game. Players take turns discarding 1-4 cards face down, claiming they are the next rank in sequence. Any opponent may call a bluff: a wrong caller takes the pile, a caught bluffer takes it. The first player to empty their hand wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the original, the first player to empty their hand wins, and a player who gets out on a full cycle earlier is ahead, so there is a built-in seat edge. In the tested variation, 'play 1 card, never challenge' won 46-14 and 48-12 against random seats, while the opposite default lost 14-45 and 12-48. Slow, passive play was a safe, strong default because passing never cost anything and the challenger risked the whole pile."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Reading bluffs from the cards you hold, from claim sizes and from each player's history is a real skill, and good callers beat poor ones. The deal adds variance but does not decide the game, because a bad hand can be bluffed out of."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "There is room for constant improvement: when to bluff, how much to claim, when to trust, card counting and modelling each opponent's honesty. A weak player still sheds cards and can win on bluffs."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the pile are hidden. Every challenge decision is an inference from the copies you hold, the quantity claimed and the opponent's tendencies."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Claims are checked against the revealed cards and the winner is decided by card counts. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original lets anyone call at any time, which is real-time. It supports up to 8 players with no fixed length. The tested variation used 6 choice steps per round, above the limit of 4."
    }
  ],
  "problems": [
    "P1: Too many choice steps per round (6 in the tested build, the limit is 4), caused by a separate talk step and per-player challenge choices.",
    "P2: Passing is free. Never challenging costs nothing, so the passive default wins against random seats.",
    "P3: Slow-dumping one card is safe. A 1-card claim is almost always true and rarely punished, and with no time pressure it is not slower in any way that matters.",
    "P4: Challenging is too risky. A wrong challenger takes the whole pile, so challenging is rarely worth it and the reckless 'always challenge' default loses badly.",
    "P5: There is a seat edge. 'First to empty' rewards whoever's turn comes earlier in the cycle.",
    "P6: Calling at any moment is real-time and has no fixed length, which the turn-based engine cannot run.",
    "P7: A rank sequence that lines up with the seat order would give each seat the same ranks every time, so some seats could never play some ranks honestly."
  ],
  "changes": [
    {
      "what": "Fixed at 3 players. Each round is one turn: one play choice by the active player (with an optional statement attached), then one simultaneous Challenge/Trust poll of the other two. That is 2 choice steps per round.",
      "why": "This brings the game well under the 4-choice limit and removes the separate talk step.",
      "fixes": "P1"
    },
    {
      "what": "Calling becomes a simultaneous poll after every play, and the game lasts a fixed 24 rounds.",
      "why": "This makes the game turn-based and bounded in length.",
      "fixes": "P6"
    },
    {
      "what": "Trusting a bluff can cost you. If a play was a bluff and nobody challenged, each of the two other players takes 1 card from the top of the pile.",
      "why": "Never challenging now loses cards against bluffers. Challenging is still a gamble, so the decision becomes a real inference instead of a free pass.",
      "fixes": "P2"
    },
    {
      "what": "A wrong challenge costs only the size of the claim. The first wrong challenger (in seat order after the active player) takes the top k cards of the pile (k = cards just played); a second wrong challenger takes the next k.",
      "why": "Challenging becomes worthwhile when you suspect a bluff. Always-challenge is still punished by honest plays, especially honest 3s and 4s.",
      "fixes": "P4"
    },
    {
      "what": "A correct challenge pays the challenger. The bluffer takes the whole pile, and each correct challenger also removes one card from their own hand from the game.",
      "why": "Catching bluffs is a gain, not just avoiding a loss, so passive players fall behind active, accurate callers.",
      "fixes": "P2"
    },
    {
      "what": "A deck of 4 ranks with 6 copies each (8 cards per player). Claims are 1-4 cards. The game is capped at 24 rounds (8 turns each), and the player with the fewest cards wins.",
      "why": "Players usually hold 2 or more of a rank, so honest multi-card plays are common. Playing only 1 card per turn barely empties a hand within 8 turns, and any card picked up leaves it behind players who play honest 2s and 3s.",
      "fixes": "P3"
    },
    {
      "what": "The game may end only at the end of a full 3-round cycle (if someone has 0 cards), so every player always has had the same number of turns. Fewest cards wins; a tie for fewest is a draw.",
      "why": "This removes the 'got out first in the cycle' seat edge.",
      "fixes": "P5"
    },
    {
      "what": "4 ranks over 3 seats, so the required rank shifts relative to the seats. Over 24 rounds each seat faces each rank exactly twice.",
      "why": "Every seat gets equal honest opportunities.",
      "fixes": "P7"
    },
    {
      "what": "The engine picks the actual cards. Matching cards go first, then fillers from rank+1, then rank+2, then rank+3 (wrapping), which are the ranks you will need furthest in the future.",
      "why": "This keeps the play to one numeric choice while still letting the player decide how much to bluff.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Face-down discards claimed as a required rank that advances every turn and wraps around.",
    "Bluffing when you lack the rank, and claiming more than you have.",
    "Challenges that reveal the play: a caught bluffer takes the whole central pile.",
    "Shedding is the goal: fewest cards (ideally zero) wins.",
    "Table talk to sell a claim."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The bluff-and-call core is strongly reasoning-dependent. Its flaws (free passing, safe slow-dumping, an overly costly challenge, too many choice steps) are fixable with payoff and structure changes inside the limits."
  },
  "variation": {
    "name": "Hogwash: Three-Seat Call",
    "summary": "Three players shed cards by claiming the required rank. The two others decide at the same moment whether to challenge or trust. Trusting a bluff costs a card, a wrong challenge costs the claim size, and a caught bluffer takes the pile. After 24 rounds, fewest cards wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP. The deck has 24 cards: ranks 1, 2, 3, 4, six copies of each. Shuffle once and deal 8 cards to each of the 3 players (seats 1, 2, 3). Each hand is private; everyone always knows how many cards each player holds. The central pile starts empty. Cards in the pile are face down and unknown except when revealed by a challenge. Cards removed from the game are gone for good.\n\nROUNDS. There are at most 24 rounds. In round r the active player is seat ((r-1) mod 3) + 1 and the required rank is ((r-1) mod 4) + 1. So seat 1 plays rank 1 in round 1, seat 2 plays rank 2 in round 2, seat 3 plays rank 3 in round 3, seat 1 plays rank 4 in round 4, and so on. Over 24 rounds every seat is active 8 times and faces each rank exactly twice.\n\nEACH ROUND:\n1. Announce the round number, the active player and the required rank.\n2. If the active player has 0 cards, they skip the turn; go to step 9. Otherwise the active player privately chooses a number k from 1 to 4. If k is more than their hand size, k becomes their hand size. They may attach one short public statement (any text, which may be untrue).\n3. The engine moves k cards from the active player's hand to the top of the pile. It first takes cards of the required rank (as many as they hold, up to k). If more are needed, it takes cards of rank (required+1), then (required+2), then (required+3), counting 4 as followed by 1. The play is TRUE if all k cards are the required rank; otherwise it is a BLUFF. The engine records this privately.\n4. Announce: 'Seat X claims k cards of rank R', plus the statement.\n5. Simultaneous poll: each of the two other players secretly chooses Trust or Challenge. Both choices are revealed together.\n6. If at least one player chose Challenge, the k played cards are revealed to everyone.\n   (a) If the play was a BLUFF: the active player takes the entire pile into their hand, and the pile becomes empty. Then each player who chose Challenge removes from the game one card from their own hand: a card of the rank they hold the fewest of (counting only ranks they hold at least one of, lowest rank on a tie). If they have no cards, nothing is removed.\n   (b) If the play was TRUE: the challengers, in seat order starting after the active player, each take cards from the top of the pile. The first takes the top k cards (the cards just played). If there is a second challenger, they take the next k cards from the top, or all remaining cards if fewer than k.\n7. If both players chose Trust and the play was a BLUFF: announce that a bluff went unchallenged (without showing the cards). Each of the two other players, in seat order starting after the active player, takes 1 card from the top of the pile (if any remain).\n8. If both chose Trust and the play was TRUE, nothing happens. The cards stay face down in the pile.\n9. Announce every player's hand size.\n10. End check: if the round number is a multiple of 3 and at least one player has 0 cards, the game ends. If round 24 has been played, the game ends.\n\nThe pile is a stack. 'Top' means the most recently added cards.",
    "objective": "When the game ends, the player holding the fewest cards wins. If two or three players tie for the fewest, the game is a draw.",
    "expected_effect": "No fixed default is safe. 'Always 1, always Trust' sheds only 1 card per turn, absorbs a card whenever a bluff slips through, and gets caught more often as its hand shrinks. It loses to players who make honest 2s and 3s and challenge suspicious claims. 'Always 4, always Challenge' is nearly always caught (a 4-card claim is true under 10% of the time at the start) and pays k cards whenever it challenges an honest play. 'Always Challenge' bleeds cards against honest players; 'always Trust' bleeds cards against bluffers. Winning requires inference. Callers judge from their own copies of the rank (six exist), the claim size, the cards revealed so far and each opponent's honesty record. Players choose the largest claim they can get away with given how each opponent tends to call, and plan ahead, because fillers come from the ranks they need least soon. Talk is kept but folded into the play step as a single statement by the active player. It passes both tests. The players' interests conflict, since only the fewest-cards player wins. A bluffer wants trust, and each caller wants the other caller to take the risk (both Trusting a bluff costs both of them, but a lone correct challenger gains). A player who believes a confident statement like 'I hold three 2s, don't bother' can be burned by an unchallenged bluff."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 24
  }
}
```
````
