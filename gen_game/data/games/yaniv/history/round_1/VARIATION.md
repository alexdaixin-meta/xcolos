# Variation: Simultaneous Yaniv: Claims

Players shed cards at the same moment, then secretly claim the edge card of an opponent's discard or take a shared blind card. A card claimed by two or more players goes to nobody. Players call Yaniv at 7 or less, risking Asaf, and race to keep their totals lowest over many deals.

Players: 3 to 5, best with 4

## Review of the original

Yaniv is a hand-shedding card game for 2 to 8 players. Each turn you discard singles, sets or same-suit runs and then draw from the deck or from the edge of the previous player's discard. You may call 'Yaniv' when your hand total is low; a caller who is not strictly lowest is caught ('Asaf') and takes a 30-point penalty. Points accumulate over deals until someone passes 200, and the lowest total wins.

- **non_degenerate**: good. No simple policy is safe in the original. 'Always call at the threshold' is punished by Asaf (+30). 'Never call' lets others go out and leaves you scoring your full hand. 'Always dump the highest card' ignores pairing and pickups. The previous simultaneous variation kept this, but it reduced the non-call choices to a fixed solitaire rule: dump the biggest group, and take the face-up card if it is 6 or less.
- **skill_sensitive**: weak. In the original, skill lies in contested pickups (taking the first or last card of the previous discard and shaping your discards around that) and in call timing. The deal and the deck draws are still large. The previous variation removed contested pickups, and the review estimated that chance decided about 70% of games among good players.
- **headroom**: weak. The original has headroom in tracking discards, denying pickups and timing calls. The previous variation collapsed to a threshold policy plus one binary call decision, and the gap between a good player and a mechanical one was small.
- **reasoning_dependent**: good. Hands are hidden. Opponents' totals must be inferred from what they discard and pick up, and calling well requires estimating whether anyone is lower (Asaf risk). The previous variation made every pickup public, so only the initial deal was hidden and inference shrank to one call decision.
- **verifiable**: good. Scores are hand sums, 0 for the lowest, and +30 for a caught caller. The winner is the lowest total. Everything is arithmetic.
- **fits_platform**: weak. The original uses sequential turns with a real reshuffled deck, same-suit runs and an elimination race to 200 that can run long. The previous variation fit within the step limits but drew two random events in the first round of most deals, which breaks the limit of one random draw per round.

## Problems

- P1: The previous variation drew two random events in one round: a deal at round start plus a blind card when no one called.
- P2: Pickups were uncontested copies, so opponents never affected what you drew and discarding offered nothing to anyone. Non-call play became solitaire with a fixed best policy.
- P3: Every pickup was public and the blind card was revealed, so after the deal nothing stayed hidden and inference about opponents was thin.
- P4: A call threshold of 10 with 5-card hands made call outcomes depend mostly on deal and pair luck rather than on reading opponents.
- P5: Games lasted only about 4 to 6 showdowns (end at 100), too few to average out deal variance.
- P6: Step 4 referred to the blind card before it was drawn (wording).

## Changes

- The first hands are dealt at setup, before round 1. Every later re-deal happens inside the showdown resolution of the round in which someone called. The blind card is drawn only in rounds with no call. Each round therefore has exactly one random draw (a blind card or a re-deal, never both), and round 1 has none. (fixes: P1): This keeps random_draws_per_round at 1.
- The face-up card is removed. After the simultaneous discards, each player's discard set is laid out publicly as that player's offer. In a single card or an equal-value set, one card is available. In a run, two cards are available: the lowest and the highest. Each non-caller then secretly claims one available card from another player's offer, or takes BLIND. If two or more players claim the same card, none of them gets it and all of them take BLIND. (fixes: P2): This restores Yaniv's core skill of taking the edge card of someone's discard, and adds contest and denial. You must predict who else wants a card. Your discard becomes a choice of what to offer rivals: a low single card helps them, while a high card or the middle of a run is safe.
- Runs are restored as 3 or more cards of consecutive values (suits ignored; Ace = 1 is low; Joker is not part of runs; a run cannot use two cards of value 10). (fixes: P2): Runs give a second way to shrink the hand and create two-ended offers, which makes claims richer. This keeps more of Yaniv's identity.
- The blind card is shown privately, and only to the players who took BLIND. Everyone sees who took BLIND and who claimed which card, but not the blind card's value. It is revealed only at a showdown. (fixes: P3): Each player's hand stays partly hidden throughout a deal, so estimating opponents' sums from their discards, claims and BLIND takes becomes real inference.
- The call threshold is lowered from 10 to 7, as in standard Yaniv. (fixes: P4): Reaching 7 or less needs several rounds of shedding and good pickups, so calls come later and depend on reading whether a rival is also low.
- The game ends when a total reaches 150 after a showdown, or after round 40 with a forced final showdown (no Asaf, lowest hand sum scores 0). (fixes: P5): This gives more deals to average out luck while still guaranteeing an end within 40 rounds.
- The rules are reworded so that the blind card is described only as drawn in the resolution step. (fixes: P6): This removes the ambiguity about when the blind card exists.

## Kept from the original

- Yaniv card values: Ace 1, 2 to 10 face value, J/Q/K 10, Joker 0.
- Shedding by single card, equal-value set or run, then drawing exactly one card.
- Picking up the first or last card of an opponent's discard as an alternative to the blind draw.
- Calling Yaniv at a low threshold, the strictly-lowest test, and the Asaf penalty of +30.
- Non-callers scoring their hand sum, the lowest hand scoring 0, and the lowest cumulative total winning.

## The variation's rules

CARDS. Card values: Ace = 1, 2 to 10 = face value, Jack/Queen/King = 10, Joker = 0. Suits do not matter. Every card comes from a shoe with the frequencies of a 54-card deck, reshuffled before every draw:
- each value from 1 to 9: 4 in 54;
- value 10: 16 in 54;
- value 0: 2 in 54.

SETUP. Before round 1, each player is dealt 5 cards. Each player sees only their own hand. Everyone sees every player's hand size and running total, which starts at 0.

EACH ROUND:
(1) PUBLIC ANNOUNCEMENT. The round number, every player's hand size and total, and the previous round's public results (discards, claims, who took BLIND) are announced.
(2) PRIVATE VIEW. Each player is privately shown their hand and its sum.
(3) FIRST CHOICE, simultaneous. Each player secretly chooses exactly one of:
- CALL, allowed only if their hand sum is 7 or less;
- DISCARD one card;
- DISCARD two or more cards of equal value;
- DISCARD a RUN of three or more cards with consecutive values. Ace counts as 1. Jokers cannot be in a run. A run may contain at most one card of value 10, so 8-9-10 is allowed but 9-10-10 is not.
A player must keep at least 1 card after discarding, so a player holding 1 card may not discard it and must CALL if allowed. If not allowed to call, that player discards nothing this round and still draws one card in step 9. Any illegal answer is replaced by discarding the single highest card (or by discarding nothing, for a player with 1 card).
(4) SHOWDOWN, only if at least one player called. All discards are cancelled and all hands are revealed as they stood. Let L be the lowest hand sum.
- A caller whose sum is strictly lower than every other player's sum scores 0.
- Any other caller is caught (Asaf) and scores their hand sum + 30.
- A non-caller whose sum equals L scores 0.
- Every other non-caller scores their hand sum.
Scores are added to totals. If no total is 150 or more and this is not round 40, every player is dealt a fresh hand of 5 cards. This re-deal is this round's only random draw. Steps 5 to 10 are skipped this round.
(5) OFFERS, only if no one called. Every player's discard is announced publicly: who discarded which values. The discarded cards leave play. Each player's discard creates an OFFER:
- a single card or an equal-value set offers one card of that value;
- a run offers two cards, its lowest and its highest value.
(6) SECOND CHOICE, simultaneous, only if no one called. Each player secretly chooses either BLIND, or to CLAIM one specific offered card belonging to another player. A player may not claim from their own offer. A player who discarded nothing still makes this choice. An illegal answer becomes BLIND.
(7) CONTESTS. If two or more players claim the same offered card, none of them receives it, and each of them is treated as having chosen BLIND. A card claimed by exactly one player goes to that player.
(8) BLIND DRAW, only if no one called. One card is drawn from the shoe. This is this round's only random draw.
(9) DELIVERY. Each successful claimant adds the claimed card to their hand. Each BLIND player adds a copy of the blind card to their hand and is privately told its value. The blind card's value is not told to anyone else until a showdown.
(10) PUBLIC RESULT. It is announced who claimed which card, which claims failed through contest, and who took BLIND. The blind card's value is not announced.
(11) FINAL SHOWDOWN. If this is round 40 and no showdown happened this round, all hands are revealed. Every player whose hand sum equals the lowest hand sum scores 0, and every other player scores their hand sum. There are no callers and no Asaf.
(12) END CHECK. The game ends if any total is 150 or more after a showdown, or after round 40.

Objective: When the game ends, the player with the strictly lowest total wins. If two or more players tie for the lowest total, the game is a draw.

Expected effect: Non-call play becomes interactive. Players choose discards with an eye to what they offer: dumping a low single card or the end of a run hands rivals a gift. Claims become a prediction game. Claiming the obvious low card risks a contest that sends every claimant to BLIND, while claiming a less popular card or deliberately taking BLIND can be better. Each player's hand stays partly hidden because the blind card is not revealed, so call timing at 7 or less requires estimating rivals' sums from their discards, claims and BLIND takes; reading them well avoids Asaf and catches rash callers. Ending at 150, or at round 40, gives roughly 5 to 8 deals, so deal luck averages out more. Talk is left out. Its only use would be unverifiable announcements of intended claims, whose contest is better played as a silent prediction, and talk would cost steps while mostly leaking or faking hand information. The game is a race to stay lowest, not a cooperation game, so there is no endgame unravelling. The 150 threshold and the round-40 final showdown already define the end.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
