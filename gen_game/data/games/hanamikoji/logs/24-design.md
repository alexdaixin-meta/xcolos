# 24 design

- time: 2026-10-27T10:29:46+00:00 (65.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 907d9647b122d964, reply sha256 376af5fae8609983

## Sent

````
Original game: Hanamikoji
Players in the original: 2 to 2

Original rules:
Two players compete for 7 Geisha cards. Each Geisha has a Charm value and a set of Item cards (total 21 Items across types). First to win 4 Geisha or 11+ Charm points from won Geisha wins; 11 Charm beats 4 Geisha if both achieved same scoring.
Each round: shuffle 21 Items, secretly remove 1 card from play, deal 6 cards each as hidden hands, remaining 8 form a deck. Players alternate turns for 4 turns each: draw 1 from deck, then use one unused Action marker. Secret: set aside 1 hand card face-down for final scoring. Trade-off: set aside 2 hand cards face-down discarded this round. Gift: reveal 3 hand cards, opponent takes 1 to his side, you keep 2. Competition: reveal 4 hand cards as two pairs of 2, opponent chooses one pair, you keep the other. All kept cards are placed by their Geisha. After 8 turns, reveal Secret cards and compare counts per Geisha: higher count wins that Geisha and moves its Victory Marker; ties leave marker. If winning goal met, game ends. Otherwise collect all Item cards, retain Victory Markers, flip Action markers up, swap starting player, and start new round.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Rules content is complete: deal, draw, the four actions, picks, defaults for an illegal action, illegal cards and an illegal pick, scoring, winning and the hand-5 tiebreak are all specified. The game is finite (at most 40 rounds) and decided by arithmetic. It is two-player with no talk, which is fine. It is not a repeated cooperation game, so the late-round betrayal test does not apply. The failure is that the complexity claim is not credible. The step list is flat, so hand-start, per-round and scoring steps all sit in one list gated by `when`. Minimal count: (1) Hand start: shuffle, remove 1, deal P1, deal P2, reset action markers and kept areas = 5 steps. (2) Per round: announce, draw, choice 1, default and validate the action, choice 2, validate and default the cards, apply Secret/Trade-off/reveal, choice 3 when Gift or Competition, apply the pick to both kept areas, spend the marker, public announce = 10 to 11 steps. (3) Scoring: reveal Secrets into the kept areas, then compare 7 Geisha and move markers. There is no lookup or per-attribute compare operand, so this is a workaround costing several steps. Then 2 Charm sums, 2 Geisha counts, the threshold win check and the hand-5 tiebreak, about 6 to 11 steps. Total is about 21 to 27, which exceeds the 20 limit; the stated 15 is understated. The attribute figure of 14 is also doubtful. Seven Victory Markers plus per-Geisha kept counts for 2 players is already 7 + 14 = 21 if kept counts are numbers. Add 8 action-marker flags, 2 hands, 2 Secrets, the deck, the removed card, and the hand and round counters. Only aggressive packing into lists could fit 20, and then every scoring comparison needs calc counting, which adds steps. Minor: the card-answer format (separators, whether duplicates are written as '7 7') is unstated. The default rule covers bad input, but legal intent may be misparsed.
- change: Playable: give an explicit step-by-step budget showing steps_per_round <= 20 and attributes <= 20 in the flat list, merging steps as needed. Do all of hand-start in at most 3 steps (one shuffle-and-deal step with multiple operations, one reset step). Store the 7 Victory Markers as a single list attribute, and each player's kept area and used actions as one list each. Do all 7 Geisha comparisons, marker moves, Charm sums and Geisha counts in at most 2 calc steps with per-operation `if` conditions. Fold the threshold check and the hand-5 tiebreak into one gated step.
- change: Playable: if that consolidation cannot reach 20 steps, cut scope, for example to 5 Geisha with 15 Items, so the scoring comparison fits.
- change: Playable: state the exact card-answer format, for example 'space-separated Geisha numbers, repeats written out, e.g. 7 7 3'.
The variation that was reviewed: Hanamikoji: One Turn per Round: COMPONENTS
- There are 7 Geisha, G1 to G7, with Charm values G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5.
- There are 21 Item cards. Each Geisha has as many Items as its Charm: two each of G1 to G3, three each of G4 and G5, four of G6 and five of G7.
- Each Geisha has a Victory Marker that is neutral at the start. A marker is on Player 1's side, on Player 2's side, or neutral.
- Each player has four action markers: Secret, Trade-off, Gift and Competition.

STRUCTURE
- The game is played in hands of 8 rounds each, at most 5 hands (40 rounds).
- Player 1 starts hands 1, 3 and 5. Player 2 starts hands 2 and 4.
- Within a hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player in rounds 2, 4, 6 and 8.
- The other player in a round is called the opponent.

START OF EACH HAND (first round of the hand)
- Shuffle all 21 Items.
- Remove 1 card face down. Nobody sees it, and it plays no part this hand.
- Deal 6 cards to each player as a private hand. Each player sees only their own hand, shown as a sorted list of Geisha numbers.
- The remaining 8 cards form a face-down deck.
- Both players' four action markers become unused.
- Both players' kept-card areas are emptied. Victory markers stay where they are.

EACH ROUND (one turn)
1. The game announces the hand number, the round number, the active player, which actions each player still has unused, and both players' kept cards per Geisha.
2. The active player draws the top card of the deck into their hand.
3. Choice 1: the active player chooses one of their unused actions.
4. Choice 2: the active player writes the Geisha numbers of the cards the action uses. Every named card must be in their hand.
   - Secret: 1 card. It is placed face down as their Secret and stays hidden until scoring.
   - Trade-off: 2 cards. They are discarded face down and do not count this hand.
   - Gift: 3 cards, which are revealed in the order written.
   - Competition: 4 cards, written as pair A (the first two) and pair B (the last two), and revealed.
5. Choice 3, only if the action is Gift or Competition: the opponent picks.
   - For Gift, the opponent writes 1, 2 or 3. They take that revealed card into their own kept area, and the active player keeps the other two.
   - For Competition, the opponent writes 1 (pair A) or 2 (pair B). They keep that pair, and the active player keeps the other.
   - An illegal pick counts as 1.
6. The used action becomes spent. The game announces publicly what happened, without revealing Secret or Trade-off cards.

DEFAULTS
- An illegal or missing action counts as the first unused action in the order Secret, Trade-off, Gift, Competition.
- If the card answer is illegal (wrong count, or a card not in hand), the engine uses the required number of lowest-numbered cards in the hand, in ascending order.
- The card counts always work out: each player draws 4 cards and spends 1+2+3+4 = 10 cards from 6+4.

SCORING (after round 8 of each hand)
- Each player's Secret card is revealed and added to their kept area.
- For each Geisha, compare the two players' kept counts. A strictly higher count moves that Geisha's marker to that player's side. A tie leaves the marker where it is.
- Each player's Charm is the sum of Charm of the Geisha whose markers are on their side. Each player's Geisha count is the number of those markers.

WINNING
- If a player has 11 or more Charm, they win.
- Otherwise, if a player has 4 or more Geisha, they win.
- Two players cannot both reach either threshold, because the totals are 21 Charm and 7 Geisha.
- If nobody has won, the next hand starts with the other starting player.
- If 5 hands are completed without a winner: the higher Charm wins; if Charm is equal, the higher Geisha count wins; if that is also equal, the game is a draw. Winner: The game is checked after each hand's scoring. A player with 11 or more Charm from Geisha markers on their side wins immediately. Otherwise a player with 4 or more Geisha markers wins. If no one has won after 5 hands (40 rounds), the higher Charm total wins, then the higher Geisha count, otherwise the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Hanamikoji is a two-player hidden-hand majority game. Over repeated hands, players use four one-shot actions (Secret, Trade-off, Gift, Competition) to commit Item cards to 7 Geisha of differing Charm. The first player to control 11 Charm or 4 Geisha wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy is safe. 'Always take the first unused action with the lowest cards' telegraphs its hand and is exploited at every Gift and Competition. 'Always pick option 1' lets the offerer place the bait card first. Starting player alternates per hand, which limits seat edge; with an odd hand cap, Player 1 starts one more hand."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The deal adds variance, but a player who sequences actions well beats one who does not, because a single round is many small decisions. Good sequencing means Secret and Trade-off timing, building Gift and Competition offers the opponent cannot split profitably, and tracking the cards seen."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card counting against the removed card, inferring the opponent's Secret, and holding back Competition to the last turn are deep, unsolved skills. A naive player still wins Geisha from favourable deals."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "There are private hands, a hidden Secret, hidden Trade-off discards and one unseen removed card. Every Gift and Competition pick requires inferring what the offerer holds and what they want you to take."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Geisha go to the strictly higher kept count, Charm is summed and thresholds are checked. All of it is pure arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only with no board. However, 7 per-Geisha comparisons for two players, plus Victory Markers, action flags, hands and Secrets, push the flat step list to about 21 to 27 steps and the attributes past 20. The previous variation understated both. The card-answer format was also unstated."
    }
  ],
  "problems": [
    "Step budget: with 7 Geisha, the scoring comparison has no lookup operand. Together with hand start, turn handling and win checks, the flat step list goes past 20 steps.",
    "Attribute budget: 7 Victory Markers plus 14 per-Geisha kept counts already exceed 20 attributes before hands, Secrets, deck and action flags are counted.",
    "Card answers had no stated format (separators, how repeated Geisha are written, how Competition pairs are delimited), so legal intent could be misparsed into a default.",
    "The hand-start setup and the end-of-hand scoring were described as many separate operations rather than merged, gated steps. This inflated the count and left the build ambiguous."
  ],
  "changes": [
    {
      "what": "Reduce to 5 Geisha with Charm 3, 3, 4, 5, 6 (total 21). Each Geisha has as many Items as its Charm, so there are still 21 Items. The thresholds become 11 Charm or 3 Geisha.",
      "why": "Keeping 21 Items preserves the exact card economy: remove 1, deal 6 each, an 8-card deck, 10 cards spent per player. Five Geisha cut the scoring comparison and the stored counts by almost a third. 11 of 21 Charm and 3 of 5 Geisha are still majority thresholds, as in the original.",
      "fixes": "Step budget: with 7 Geisha, the scoring comparison has no lookup operand. Together with hand start, turn handling and win checks, the flat step list goes past 20 steps."
    },
    {
      "what": "Store all Victory Markers as one 5-entry list, each player's kept area as one 5-entry count list, and each player's used actions as one list.",
      "why": "This brings the attribute count to 18, with every quantity explicit.",
      "fixes": "Attribute budget: 7 Victory Markers plus 14 per-Geisha kept counts already exceed 20 attributes before hands, Secrets, deck and action flags are counted."
    },
    {
      "what": "Merge the hand start into 2 gated steps (shuffle, remove and deal; then reset). Do scoring as: one step to add the Secrets, one calc step for all 5 marker updates using per-operation 'if', one calc step for Charm and Geisha counts, one gated win check and one gated final tiebreak.",
      "why": "This gives an explicit 18-step flat list, within the 20-step limit.",
      "fixes": "The hand-start setup and the end-of-hand scoring were described as many separate operations rather than merged, gated steps. This inflated the count and left the build ambiguous."
    },
    {
      "what": "Specify the card-answer format: space-separated Geisha numbers 1 to 5, repeats written out (e.g. '5 5 2'). Competition is exactly four numbers, the first two being pair A. Picks are a single digit.",
      "why": "This removes parsing ambiguity, so defaults only trigger on genuinely illegal answers.",
      "fixes": "Card answers had no stated format (separators, how repeated Geisha are written, how Competition pairs are delimited), so legal intent could be misparsed into a default."
    }
  ],
  "keeps": [
    "Two players, majority control of Geisha with differing Charm, Victory Markers that persist between hands and only move on a strict majority.",
    "The four one-shot actions with their exact card costs (1, 2, 3, 4) and the offer-and-split mechanics of Gift and Competition.",
    "The card economy: shuffle, one card secretly removed, 6-card hands, an 8-card deck, one draw per turn.",
    "Dual win condition with Charm checked before Geisha count, alternating starting player each hand."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of hidden hands, a secret commitment and offers the opponent splits is strong strategic reasoning. Reducing to 5 Geisha with the same 21-card economy fits the step and attribute limits without changing the game's identity."
  },
  "variation": {
    "name": "Hanamikoji: Five Geisha",
    "summary": "Hanamikoji compressed to 5 Geisha but with the same 21-Item economy. Two players alternate single turns, each using one of four one-shot actions, to win majorities of hidden and offered Items. The first to control 11 Charm or 3 Geisha after a hand's scoring wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS\n- 5 Geisha, G1 to G5, with Charm G1=3, G2=3, G3=4, G4=5, G5=6 (total 21).\n- 21 Item cards. Each Geisha has as many Items as its Charm: three of G1, three of G2, four of G3, five of G4, six of G5. A card is identified by its Geisha number 1 to 5.\n- 5 Victory Markers, one per Geisha, each on Player 1's side, on Player 2's side, or neutral. All start neutral.\n- Each player has four action markers: Secret, Trade-off, Gift, Competition.\n- Each player has a kept area, tracked as five counts (how many cards of G1 to G5 they have kept this hand).\n\nSTRUCTURE\n- The game is played in hands of 8 rounds, at most 5 hands (40 rounds).\n- Player 1 starts hands 1, 3 and 5. Player 2 starts hands 2 and 4.\n- In each hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player in rounds 2, 4, 6 and 8. The non-active player is the opponent.\n\nSTART OF EACH HAND (done before round 1 of the hand)\n- Shuffle all 21 Items.\n- Remove the top card face down. Nobody sees it; it plays no part this hand.\n- Deal 6 cards to each player as a private hand. Each player sees only their own hand, shown as a sorted list of Geisha numbers.\n- The remaining 8 cards form the face-down deck.\n- Both players' action markers become unused, both kept areas are reset to 0 0 0 0 0, and both Secrets are emptied. Victory Markers stay where they are.\n\nEACH ROUND (one turn)\n1. The game announces: hand number, round number, the active player, each player's unused actions, both players' kept counts per Geisha, and the Victory Marker positions.\n2. The active player draws the top deck card into their hand and is privately shown their new hand.\n3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition.\n4. Choice 2: the active player writes the cards the action uses as space-separated Geisha numbers, with repeats written out (example: '5 5 2'). Every card named must be in their hand, counting repeats.\n   - Secret: exactly 1 number. That card is set face down as their Secret, hidden until scoring.\n   - Trade-off: exactly 2 numbers. Those cards are discarded face down and do not count this hand.\n   - Gift: exactly 3 numbers. The cards are revealed in the order written as offer 1, 2, 3.\n   - Competition: exactly 4 numbers. The first two form pair A, the last two pair B. All four are revealed.\n   The named cards leave the active player's hand.\n5. Choice 3, only for Gift or Competition: the opponent writes a single digit.\n   - Gift: 1, 2 or 3. The opponent adds that card to their kept area; the active player adds the other two to theirs.\n   - Competition: 1 (pair A) or 2 (pair B). The opponent adds that pair to their kept area; the active player adds the other pair.\n6. The used action becomes spent. The game publicly announces what was done: the action, and for Gift or Competition the revealed cards and the split. Secret and Trade-off cards are not revealed, only that the action was used.\n\nDEFAULTS\n- Illegal or missing action: use the first unused action in the order Secret, Trade-off, Gift, Competition.\n- Illegal card answer (wrong count, unreadable, or a card not in hand): the engine uses the required number of lowest-numbered cards in hand, in ascending order. For Competition, the first two of these form pair A.\n- Illegal or missing pick: counts as 1.\n- Card counts always work out: each player holds 6 + 4 drawn = 10 cards and spends 1+2+3+4 = 10.\n\nSCORING (after round 8 of each hand)\n- Each player's Secret is revealed and added to their kept area.\n- For each Geisha, compare the two kept counts. A strictly higher count moves that Geisha's marker to that player's side. A tie leaves the marker where it is, even if it is on a side from an earlier hand.\n- Each player's Charm is the sum of Charm values of Geisha whose markers are on their side. Each player's Geisha count is the number of markers on their side.\n- The game announces the revealed Secrets, all five marker positions, and both players' Charm and Geisha count.\n\nWINNING (checked after each hand's scoring)\n- If a player has 11 or more Charm, they win. Only one player can, since total Charm is 21.\n- Otherwise, if a player has 3 or more Geisha, they win. Only one player can, since there are 5 Geisha.\n- If nobody has won and fewer than 5 hands are complete, the next hand begins with the other player starting.\n- After hand 5 with no winner: the higher Charm wins; if Charm is equal, the higher Geisha count wins; if that is also equal, the game is a draw.",
    "objective": "After each hand's scoring: a player with 11 or more Charm from Geisha markers on their side wins; otherwise a player with 3 or more markers on their side wins. If neither happens by the end of hand 5 (40 rounds), the higher Charm wins, then the higher Geisha count, otherwise a draw.",
    "expected_effect": "Play is the same as Hanamikoji at a buildable size. Players time Secret and Trade-off, build Gift and Competition offers whose split costs the opponent, and read the opponent's offers as evidence of their hand and Secret. Fewer, more valuable Geisha make each contested majority sharper. The G5 (6 Charm) plus G4 (5 Charm) pair is a direct route to 11 Charm that competes with the 3-Geisha route, so players must judge which threat the opponent is chasing. Persistent markers keep multi-hand planning relevant when a hand ends with ties. No talk is used: it is a two-player zero-sum game with nothing to bargain over."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 3,
    "attributes": 18,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
