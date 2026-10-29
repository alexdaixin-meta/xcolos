# 03 design

- time: 2026-10-28T03:58:18+00:00 (83.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b5121aa13e11c8c3, reply sha256 d61ddf9869cd8e9c

## Sent

````
Original game: Yaniv
Players in the original: 2 to 8

Original rules:
Each player is dealt 5 cards from a 54-card deck including jokers. Values: Ace=1, 2-10 face, J/Q/K=10, Joker=0. A draw pile and one upcard discard pile remain. On a turn you may discard: one card, two+ equal rank, or 3+ same-suit consecutive ranks with Ace low. After discarding you must draw one card: top of draw pile or only the first or last card of the previous set from discard. If draw pile empties, reshuffle discards except last play. At start of your turn if hand sum is below the Yaniv threshold (commonly 5-7) you may call Yaniv instead of playing. All hands are revealed. Lowest hand wins the round with 0. Others score their hand sum. If caller is not strictly lowest (Asaf), caller gets hand sum +30 penalty. Total score accumulates across rounds. A player exceeding 200 points is eliminated; last remaining or lowest total when first elimination occurs wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Random draws exceed the limit. The design says the deal 'counts as the single chance event of that round'. But in round 1, and in every round after a showdown, the deal happens at the start of the round. If no one calls in that round, step 5b then draws a blind card as well: 'one blind card is drawn (the round's chance event)'. That is two random draws in one round, and random_draws_per_round must be at most 1. Since 5-card hands rarely have a sum of 10 or less, the first round of every deal is almost always a no-call round, so this happens nearly every deal. Other points: steps 15 (limit 20), choice steps 2 (limit 4), attributes 12 (limit 20), hidden elements 2 (limit 3), rounds 40 (limit 40) are all within limits. Step 4 refers to 'this round's blind card' before 5b draws it; this is readable as 'the card to be drawn', but it should be worded so. Termination is defined: a showdown total of 100 or more, or round 40 with full hand sums added. Illegal answers have a default, and equal-value multiples (10/J/Q/K all count as 10) are clear. No talk is a defensible choice for 3-4 players, since they mainly guess each other's call timing. The pickup choice is not shared, so talk would add little. The game needs no board, judge or clock.
- reasoning_over_luck FAILED: The original game's skill was in contested pickups: taking the first or last card of the opponent's previous discard, and discarding with that in mind. The variation removes this. Discards are simply destroyed, and pickups are copies, so opponents never affect what you draw. Both non-call decisions then become solitaire with a fixed best policy and no reasoning about opponents: (1) discard your largest equal-value group, otherwise your highest card, keeping a card that pairs with the face-up; (2) take FACE-UP iff its value is about 6 or less (the blind expectation is 6.30), adjusted for pairing. When every player follows this policy, the only remaining decision is call timing. Its risk is driven by draw luck, because hand sizes shrink only through dealt or drawn pairs. Hands are 5 cards with SD 7.5 per deal. Each blind draw has SD 3.3, and roughly half of all pickups are blind. Non-callers score their hand sum (often 15-30), so a game lasts only about 4-6 showdowns before someone reaches 100. Estimate: in a field of good players, chance (deal, pair luck and blind draws) decides most games, perhaps around 70%. Inference does exist: all pickups and discards become public, so only the initial 5-card deal is hidden and it can be partly deduced. It acts on a single binary choice, and the gap between a good player and a mechanical threshold player is small.
- change: Keep one chance event per round. Deal the first hands at setup, before round 1. Move every later re-deal into the resolution of the showdown round (5a), where no blind card is drawn, so the re-deal is that round's only random draw. Word step 4 as 'the blind card to be drawn this round'.
- change: Make pickups contested so that opponent modelling matters. One option: let a non-caller choose BLIND or one specific card from the previous round's public discards, with only one copy of each discarded card. If two players claim the same card, neither gets it and both take BLIND (or the lower-total player gets it). Then discarding becomes a choice of what to offer opponents.
- change: Reduce luck in calling. Lower the call threshold to 7 as in standard Yaniv, or let a player call only when their hand has at least as many cards as some other player's hand. This rewards reading opponents' public discard and pickup history over pair luck.
- change: Lengthen games to average out deal variance, for example by ending at 150 total, so that several more showdowns decide the winner. Re-check that the game still finishes within 40 rounds.
The variation that was reviewed: Simultaneous Yaniv: CARDS. Card values: Ace = 1, 2 to 10 = face value, Jack/Queen/King = 10, Joker = 0. Suits do not matter. Every card is drawn from a shoe with the frequencies of a 54-card deck, which is reshuffled before every draw:
- each value from 1 to 9: 4 in 54;
- value 10 (10, J, Q, K): 16 in 54;
- value 0 (Joker): 2 in 54.

DEALING. At the start of the game and at the start of every new deal, every player is dealt 5 cards and one face-up card is turned over. This counts as the single chance event of that round. Each player sees only their own hand. Everyone sees the face-up card, every player's hand size, and every player's running total.

EACH ROUND:
(1) Public announcement: round number, face-up card, all hand sizes, all totals, and the previous round's discards and pickups.
(2) Each player is privately shown their hand and its sum.
(3) FIRST CHOICE, simultaneous. Each player secretly chooses one of:
- CALL, allowed only if their hand sum is 10 or less;
- DISCARD a single card from their hand;
- DISCARD two or more cards of equal value from their hand.
An illegal answer is replaced by discarding the single highest card.
(4) SECOND CHOICE, simultaneous. Every player who did not call secretly chooses FACE-UP (take a copy of the current face-up card) or BLIND (take a copy of this round's blind card, unseen). Callers make no second choice.
(5a) If at least one player called, there is a SHOWDOWN. Discards and pickups are cancelled and all hands are revealed as they stood. Let L be the lowest hand sum among all players.
- A caller whose sum is strictly lower than every other player's sum scores 0.
- Any other caller is caught (Asaf) and scores hand sum + 30.
- A non-caller whose sum equals L scores 0.
- Every other non-caller scores their hand sum.
Scores are added to totals. If no player has 100 or more, a new deal begins next round.
(5b) If no one called:
- the discarded cards are removed;
- one blind card is drawn (the round's chance event);
- each BLIND chooser receives that card and each FACE-UP chooser receives the face-up card;
- all discards are announced publicly, along with who took FACE-UP and who took BLIND;
- the blind card's value is then revealed and becomes the face-up card for the next round.
A player's hand cannot drop below 1 card, because a draw always follows a discard.
(6) End check:
- If any player's total is 100 or more after a showdown, the game ends.
- After round 40, if a deal is still in progress, all hands are revealed and every player adds their full hand sum, with no zeros. The game then ends. Winner: When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Yaniv is a hand-shedding card game for 2 to 8 players. Each turn you discard singles, sets or same-suit runs and then draw from the deck or from the edge of the previous player's discard. You may call 'Yaniv' when your hand total is low; a caller who is not strictly lowest is caught ('Asaf') and takes a 30-point penalty. Points accumulate over deals until someone passes 200, and the lowest total wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe in the original. 'Always call at the threshold' is punished by Asaf (+30). 'Never call' lets others go out and leaves you scoring your full hand. 'Always dump the highest card' ignores pairing and pickups. The previous simultaneous variation kept this, but it reduced the non-call choices to a fixed solitaire rule: dump the biggest group, and take the face-up card if it is 6 or less."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, skill lies in contested pickups (taking the first or last card of the previous discard and shaping your discards around that) and in call timing. The deal and the deck draws are still large. The previous variation removed contested pickups, and the review estimated that chance decided about 70% of games among good players."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "The original has headroom in tracking discards, denying pickups and timing calls. The previous variation collapsed to a threshold policy plus one binary call decision, and the gap between a good player and a mechanical one was small."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Opponents' totals must be inferred from what they discard and pick up, and calling well requires estimating whether anyone is lower (Asaf risk). The previous variation made every pickup public, so only the initial deal was hidden and inference shrank to one call decision."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scores are hand sums, 0 for the lowest, and +30 for a caught caller. The winner is the lowest total. Everything is arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original uses sequential turns with a real reshuffled deck, same-suit runs and an elimination race to 200 that can run long. The previous variation fit within the step limits but drew two random events in the first round of most deals, which breaks the limit of one random draw per round."
    }
  ],
  "problems": [
    "P1: The previous variation drew two random events in one round: a deal at round start plus a blind card when no one called.",
    "P2: Pickups were uncontested copies, so opponents never affected what you drew and discarding offered nothing to anyone. Non-call play became solitaire with a fixed best policy.",
    "P3: Every pickup was public and the blind card was revealed, so after the deal nothing stayed hidden and inference about opponents was thin.",
    "P4: A call threshold of 10 with 5-card hands made call outcomes depend mostly on deal and pair luck rather than on reading opponents.",
    "P5: Games lasted only about 4 to 6 showdowns (end at 100), too few to average out deal variance.",
    "P6: Step 4 referred to the blind card before it was drawn (wording)."
  ],
  "changes": [
    {
      "what": "The first hands are dealt at setup, before round 1. Every later re-deal happens inside the showdown resolution of the round in which someone called. The blind card is drawn only in rounds with no call. Each round therefore has exactly one random draw (a blind card or a re-deal, never both), and round 1 has none.",
      "why": "This keeps random_draws_per_round at 1.",
      "fixes": "P1"
    },
    {
      "what": "The face-up card is removed. After the simultaneous discards, each player's discard set is laid out publicly as that player's offer. In a single card or an equal-value set, one card is available. In a run, two cards are available: the lowest and the highest. Each non-caller then secretly claims one available card from another player's offer, or takes BLIND. If two or more players claim the same card, none of them gets it and all of them take BLIND.",
      "why": "This restores Yaniv's core skill of taking the edge card of someone's discard, and adds contest and denial. You must predict who else wants a card. Your discard becomes a choice of what to offer rivals: a low single card helps them, while a high card or the middle of a run is safe.",
      "fixes": "P2"
    },
    {
      "what": "Runs are restored as 3 or more cards of consecutive values (suits ignored; Ace = 1 is low; Joker is not part of runs; a run cannot use two cards of value 10).",
      "why": "Runs give a second way to shrink the hand and create two-ended offers, which makes claims richer. This keeps more of Yaniv's identity.",
      "fixes": "P2"
    },
    {
      "what": "The blind card is shown privately, and only to the players who took BLIND. Everyone sees who took BLIND and who claimed which card, but not the blind card's value. It is revealed only at a showdown.",
      "why": "Each player's hand stays partly hidden throughout a deal, so estimating opponents' sums from their discards, claims and BLIND takes becomes real inference.",
      "fixes": "P3"
    },
    {
      "what": "The call threshold is lowered from 10 to 7, as in standard Yaniv.",
      "why": "Reaching 7 or less needs several rounds of shedding and good pickups, so calls come later and depend on reading whether a rival is also low.",
      "fixes": "P4"
    },
    {
      "what": "The game ends when a total reaches 150 after a showdown, or after round 40 with a forced final showdown (no Asaf, lowest hand sum scores 0).",
      "why": "This gives more deals to average out luck while still guaranteeing an end within 40 rounds.",
      "fixes": "P5"
    },
    {
      "what": "The rules are reworded so that the blind card is described only as drawn in the resolution step.",
      "why": "This removes the ambiguity about when the blind card exists.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Yaniv card values: Ace 1, 2 to 10 face value, J/Q/K 10, Joker 0.",
    "Shedding by single card, equal-value set or run, then drawing exactly one card.",
    "Picking up the first or last card of an opponent's discard as an alternative to the blind draw.",
    "Calling Yaniv at a low threshold, the strictly-lowest test, and the Asaf penalty of +30.",
    "Non-callers scoring their hand sum, the lowest hand scoring 0, and the lowest cumulative total winning."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Contested pickups, partly hidden hands and a lower call threshold restore Yaniv's opponent-reading core within the limits, while keeping one random draw per round."
  },
  "variation": {
    "name": "Simultaneous Yaniv: Claims",
    "summary": "Players shed cards at the same moment, then secretly claim the edge card of an opponent's discard or take a shared blind card. A card claimed by two or more players goes to nobody. Players call Yaniv at 7 or less, risking Asaf, and race to keep their totals lowest over many deals.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "CARDS. Card values: Ace = 1, 2 to 10 = face value, Jack/Queen/King = 10, Joker = 0. Suits do not matter. Every card comes from a shoe with the frequencies of a 54-card deck, reshuffled before every draw:\n- each value from 1 to 9: 4 in 54;\n- value 10: 16 in 54;\n- value 0: 2 in 54.\n\nSETUP. Before round 1, each player is dealt 5 cards. Each player sees only their own hand. Everyone sees every player's hand size and running total, which starts at 0.\n\nEACH ROUND:\n(1) PUBLIC ANNOUNCEMENT. The round number, every player's hand size and total, and the previous round's public results (discards, claims, who took BLIND) are announced.\n(2) PRIVATE VIEW. Each player is privately shown their hand and its sum.\n(3) FIRST CHOICE, simultaneous. Each player secretly chooses exactly one of:\n- CALL, allowed only if their hand sum is 7 or less;\n- DISCARD one card;\n- DISCARD two or more cards of equal value;\n- DISCARD a RUN of three or more cards with consecutive values. Ace counts as 1. Jokers cannot be in a run. A run may contain at most one card of value 10, so 8-9-10 is allowed but 9-10-10 is not.\nA player must keep at least 1 card after discarding, so a player holding 1 card may not discard it and must CALL if allowed. If not allowed to call, that player discards nothing this round and still draws one card in step 9. Any illegal answer is replaced by discarding the single highest card (or by discarding nothing, for a player with 1 card).\n(4) SHOWDOWN, only if at least one player called. All discards are cancelled and all hands are revealed as they stood. Let L be the lowest hand sum.\n- A caller whose sum is strictly lower than every other player's sum scores 0.\n- Any other caller is caught (Asaf) and scores their hand sum + 30.\n- A non-caller whose sum equals L scores 0.\n- Every other non-caller scores their hand sum.\nScores are added to totals. If no total is 150 or more and this is not round 40, every player is dealt a fresh hand of 5 cards. This re-deal is this round's only random draw. Steps 5 to 10 are skipped this round.\n(5) OFFERS, only if no one called. Every player's discard is announced publicly: who discarded which values. The discarded cards leave play. Each player's discard creates an OFFER:\n- a single card or an equal-value set offers one card of that value;\n- a run offers two cards, its lowest and its highest value.\n(6) SECOND CHOICE, simultaneous, only if no one called. Each player secretly chooses either BLIND, or to CLAIM one specific offered card belonging to another player. A player may not claim from their own offer. A player who discarded nothing still makes this choice. An illegal answer becomes BLIND.\n(7) CONTESTS. If two or more players claim the same offered card, none of them receives it, and each of them is treated as having chosen BLIND. A card claimed by exactly one player goes to that player.\n(8) BLIND DRAW, only if no one called. One card is drawn from the shoe. This is this round's only random draw.\n(9) DELIVERY. Each successful claimant adds the claimed card to their hand. Each BLIND player adds a copy of the blind card to their hand and is privately told its value. The blind card's value is not told to anyone else until a showdown.\n(10) PUBLIC RESULT. It is announced who claimed which card, which claims failed through contest, and who took BLIND. The blind card's value is not announced.\n(11) FINAL SHOWDOWN. If this is round 40 and no showdown happened this round, all hands are revealed. Every player whose hand sum equals the lowest hand sum scores 0, and every other player scores their hand sum. There are no callers and no Asaf.\n(12) END CHECK. The game ends if any total is 150 or more after a showdown, or after round 40.",
    "objective": "When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw.",
    "expected_effect": "Non-call play becomes interactive. Players choose discards with an eye to what they offer: dumping a low single card or the end of a run hands rivals a gift. Claims become a prediction game. Claiming the obvious low card risks a contest that sends every claimant to BLIND, while claiming a less popular card or deliberately taking BLIND can be better. Each player's hand stays partly hidden because the blind card is not revealed, so call timing at 7 or less requires estimating rivals' sums from their discards, claims and BLIND takes; reading them well avoids Asaf and catches rash callers. Ending at 150, or at round 40, gives roughly 5 to 8 deals, so deal luck averages out more. Talk is left out. Its only use would be unverifiable announcements of intended claims, whose contest is better played as a silent prediction, and talk would cost steps while mostly leaking or faking hand information. The game is a race to stay lowest, not a cooperation game, so there is no endgame unravelling. The 150 threshold and the round-40 final showdown already define the end."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 2,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
