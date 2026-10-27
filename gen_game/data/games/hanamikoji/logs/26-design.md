# 26 design

- time: 2026-10-27T10:31:53+00:00 (89.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e2f2e70c5170d271, reply sha256 334a05bde6e0cded

## Sent

````
Original game: Hanamikoji
Players in the original: 2 to 2

Original rules:
Two players compete for 7 Geisha cards. Each Geisha has a Charm value and a set of Item cards (total 21 Items across types). First to win 4 Geisha or 11+ Charm points from won Geisha wins; 11 Charm beats 4 Geisha if both achieved same scoring.
Each round: shuffle 21 Items, secretly remove 1 card from play, deal 6 cards each as hidden hands, remaining 8 form a deck. Players alternate turns for 4 turns each: draw 1 from deck, then use one unused Action marker. Secret: set aside 1 hand card face-down for final scoring. Trade-off: set aside 2 hand cards face-down discarded this round. Gift: reveal 3 hand cards, opponent takes 1 to his side, you keep 2. Competition: reveal 4 hand cards as two pairs of 2, opponent chooses one pair, you keep the other. All kept cards are placed by their Geisha. After 8 turns, reveal Secret cards and compare counts per Geisha: higher count wins that Geisha and moves its Victory Marker; ties leave marker. If winning goal met, game ends. Otherwise collect all Item cards, retain Victory Markers, flip Action markers up, swap starting player, and start new round.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: WIN CONDITIONS: Charm G1-G5 = 3,3,4,5,6 (total 21). The only two-Geisha set reaching 11 is G4+G5 = 11; G5+G3 = 10 falls short. Any three Geisha reach at least 3+3+4 = 10 Charm and win on count. Charm is checked first, so 'P1 holds G4+G5 while P2 holds G1,G2,G3' resolves to P1. The win rules are consistent.

GAME LENGTH: 20 cards are in play and 4 are traded off, leaving 16 counted cards. If all 5 Geisha are decided in hand 1, the split is 3-2 or 4-1, so someone has 3 Geisha and the game ends. With one tie, the 4 decided Geisha split 3-1 (ends) or 2-2 (ends only if one side has G4+G5). Ties are only likely on G1/G2, which have 3 cards with 1 removed. Rough estimate: about 70-80% of games end after hand 1.

SEAT EDGE: In every hand the non-starter is active in round 8. That player has seen everything before acting: all Gift and Competition reveals, every split, all draws, and both opponents' spent markers. They then take the last action, often Competition or Gift, with only one card left unseen to them in the opponent's region. The starter acts in round 1 with the least information and has their round-7 offer resolved by the non-starter. In the original game this edge is evened out by alternating starters over several rounds. Here the game is usually a single hand, so P2 has a structural information edge in most games. P1 also starts 3 of 5 hands, which is a further asymmetry if games run long. The design offers no compensation, such as a Charm tiebreak bonus or a mirrored second hand.

THOUGHTLESS POLICIES (winner rule):
(a) Always the first unused action (Secret, Trade-off, Gift, Competition) with the lowest cards: reveals intent and hands G1/G2 cards to Secret and Trade-off. Loses to sensible play, which takes G4/G5 majorities. Against random play it wins or loses depending on the deal.
(b) As chooser, always pick 1: the active player orders the offer worst-first ('1 5 5'), so this player always receives the worst card. Loses to sensible play.
(c) As chooser, always take the higher-Charm option: reasonable, but the offerer can split so that any pick leaves a region tied or lost. Not unbeatable.
(d) Always Secret a G5: no guarantee, since the opponent can still outcount G5 with 6 copies in the deck.
No option is strictly dominant and no policy is undefeated, so that part passes.

The fail rests on the uncompensated move-order and information advantage in a game that is usually decided in one hand.
- change: Remove the uncompensated seat edge. Recommended: check the winning conditions only after hands 2 and 4, play at most 4 hands (32 rounds) so each player starts equally often, and apply the hand-4 tiebreak (Charm, then Geisha count, then draw). Alternative: keep the per-hand win check, but if the game would end after a hand started by P1, play one more hand started by P2 and decide on the combined result.
- change: Optional, for clarity: state the card-legality check as 'for each Geisha number, the count named is at most the count in hand' so it is pure arithmetic.
The variation that was reviewed: Hanamikoji: Five Geisha: COMPONENTS
- 5 Geisha, G1 to G5, with Charm G1=3, G2=3, G3=4, G4=5, G5=6 (total 21).
- 21 Item cards. Each Geisha has as many Items as its Charm: three of G1, three of G2, four of G3, five of G4, six of G5. A card is identified by its Geisha number 1 to 5.
- 5 Victory Markers, one per Geisha, each on Player 1's side, on Player 2's side, or neutral. All start neutral.
- Each player has four action markers: Secret, Trade-off, Gift, Competition.
- Each player has a kept area, tracked as five counts (how many cards of G1 to G5 they have kept this hand).

STRUCTURE
- The game is played in hands of 8 rounds, at most 5 hands (40 rounds).
- Player 1 starts hands 1, 3 and 5. Player 2 starts hands 2 and 4.
- In each hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player in rounds 2, 4, 6 and 8. The non-active player is the opponent.

START OF EACH HAND (done before round 1 of the hand)
- Shuffle all 21 Items.
- Remove the top card face down. Nobody sees it; it plays no part this hand.
- Deal 6 cards to each player as a private hand. Each player sees only their own hand, shown as a sorted list of Geisha numbers.
- The remaining 8 cards form the face-down deck.
- Both players' action markers become unused, both kept areas are reset to 0 0 0 0 0, and both Secrets are emptied. Victory Markers stay where they are.

EACH ROUND (one turn)
1. The game announces: hand number, round number, the active player, each player's unused actions, both players' kept counts per Geisha, and the Victory Marker positions.
2. The active player draws the top deck card into their hand and is privately shown their new hand.
3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition.
4. Choice 2: the active player writes the cards the action uses as space-separated Geisha numbers, with repeats written out (example: '5 5 2'). Every card named must be in their hand, counting repeats.
   - Secret: exactly 1 number. That card is set face down as their Secret, hidden until scoring.
   - Trade-off: exactly 2 numbers. Those cards are discarded face down and do not count this hand.
   - Gift: exactly 3 numbers. The cards are revealed in the order written as offer 1, 2, 3.
   - Competition: exactly 4 numbers. The first two form pair A, the last two pair B. All four are revealed.
   The named cards leave the active player's hand.
5. Choice 3, only for Gift or Competition: the opponent writes a single digit.
   - Gift: 1, 2 or 3. The opponent adds that card to their kept area; the active player adds the other two to theirs.
   - Competition: 1 (pair A) or 2 (pair B). The opponent adds that pair to their kept area; the active player adds the other pair.
6. The used action becomes spent. The game publicly announces what was done: the action, and for Gift or Competition the revealed cards and the split. Secret and Trade-off cards are not revealed, only that the action was used.

DEFAULTS
- Illegal or missing action: use the first unused action in the order Secret, Trade-off, Gift, Competition.
- Illegal card answer (wrong count, unreadable, or a card not in hand): the engine uses the required number of lowest-numbered cards in hand, in ascending order. For Competition, the first two of these form pair A.
- Illegal or missing pick: counts as 1.
- Card counts always work out: each player holds 6 + 4 drawn = 10 cards and spends 1+2+3+4 = 10.

SCORING (after round 8 of each hand)
- Each player's Secret is revealed and added to their kept area.
- For each Geisha, compare the two kept counts. A strictly higher count moves that Geisha's marker to that player's side. A tie leaves the marker where it is, even if it is on a side from an earlier hand.
- Each player's Charm is the sum of Charm values of Geisha whose markers are on their side. Each player's Geisha count is the number of markers on their side.
- The game announces the revealed Secrets, all five marker positions, and both players' Charm and Geisha count.

WINNING (checked after each hand's scoring)
- If a player has 11 or more Charm, they win. Only one player can, since total Charm is 21.
- Otherwise, if a player has 3 or more Geisha, they win. Only one player can, since there are 5 Geisha.
- If nobody has won and fewer than 5 hands are complete, the next hand begins with the other player starting.
- After hand 5 with no winner: the higher Charm wins; if Charm is equal, the higher Geisha count wins; if that is also equal, the game is a draw. Winner: After each hand's scoring: a player with 11 or more Charm from Geisha markers on their side wins; otherwise a player with 3 or more markers on their side wins. If neither happens by the end of hand 5 (40 rounds), the higher Charm wins, then the higher Geisha count, otherwise a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Hanamikoji is a two-player card game. Over repeated hands of four alternating turns each, players use four one-shot actions (Secret, Trade-off, Gift, Competition) to commit Item cards to seven Geisha of different Charm values. Gift and Competition force the opponent to choose between offered splits. A player wins by holding the majority on enough Geisha, by count or by Charm.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The previous variation was tested. No thoughtless policy was undefeated: always the first action, always pick 1, always take the higher-Charm option and always Secret a G5 can all lose to sensible splitting. However, the win was checked after every hand and about 70-80% of games ended after hand 1. In every hand the non-starter acts in round 8 with almost full information and resolves the starter's round-7 offer. So in most games Player 2 had an uncompensated structural edge. That is a seat edge, which this criterion forbids."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Building Gift and Competition offers so that every pick still leaves you ahead in the Geisha that matter, and choosing well as the picker, are real skills. Timing the Secret and Trade-off actions is also a skill. Each player spends 10 cards over the hand, and the opponent's choices shape about 7 of them, so splitting skill dominates. The deal adds variance, especially when a game is decided by a single hand."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win Geisha by pushing majorities. Strong players plan the order of their four actions, bait with Gift offers, read hidden Secret and Trade-off cards from what has been revealed, and count the remaining copies. Play is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands, the removed card, the deck and the face-down Secret and Trade-off cards are hidden. Players must infer what the opponent holds and kept from their offers, picks and action order, and plan four actions in advance."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Majorities are counts per Geisha. Charm is a sum. The win checks are thresholds. Card legality is the check 'the count of each number named is at most the count in hand'."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is turn-based and text-only, with at most three choices per round and no board. Five Geisha keep the state small. The previous version could reach 40 rounds, which is right at the limit."
    }
  ],
  "problems": [
    "P1 Seat edge: most games were decided by a single hand, and in every hand the non-starter has a large last-mover information advantage that nothing compensated.",
    "P2 Starting turns were uneven: Player 1 started hands 1, 3 and 5 and Player 2 only hands 2 and 4.",
    "P3 Simply alternating the hands and checking only after even hands is not enough if markers carry over hand by hand. The second hand of a pair overwrites the first wherever it decides a Geisha, so one player's last-mover hand would count more than the other's.",
    "P4 Luck of a single deal decides too much when one hand decides the game.",
    "P5 The length was 40 rounds, right at the platform limit.",
    "P6 The card-legality check was worded loosely."
  ],
  "changes": [
    {
      "what": "Hands are played in pairs: hands 1 and 2 form pair 1, and hands 3 and 4 form pair 2. Within a pair, Player 1 starts the first hand and Player 2 starts the second. Kept counts add up across both hands of the pair, and Geisha markers move only after the second hand of a pair, by comparing these combined counts.",
      "why": "Each player gets the last-mover position exactly once in every scored contest, and both hands of a pair weigh the same. Both players play the second hand knowing the full first-hand result, so the extra information is shared.",
      "fixes": "P1"
    },
    {
      "what": "There are at most 2 pairs (4 hands, 32 rounds). Each player starts exactly 2 hands.",
      "why": "The number of starts is equal, and the game is shorter and well inside the limit.",
      "fixes": "P2"
    },
    {
      "what": "Markers are updated only from combined pair totals, never from a single hand. At the start of hand 3 the pair totals reset to zero, and markers already placed stay where they are when a later pair ties on that Geisha.",
      "why": "Neither hand of a pair can overwrite the other, so both last-mover hands count equally.",
      "fixes": "P3"
    },
    {
      "what": "At the end of the first hand of a pair, the Secrets are revealed and both players' running pair totals are announced.",
      "why": "Both players play the second hand with the same full knowledge of where they stand, and the deal's swing is averaged over 32 counted cards instead of 16.",
      "fixes": "P4"
    },
    {
      "what": "The win is checked after hands 2 and 4 only. After hand 4 the tiebreak is higher Charm, then more Geisha, otherwise a draw.",
      "why": "This gives a clean end, and the game always stops at a point where the seats are balanced.",
      "fixes": "P1"
    },
    {
      "what": "Legality is stated as 'for each Geisha number, how many times you name it must be at most how many of that number are in your hand'.",
      "why": "The check becomes pure arithmetic.",
      "fixes": "P6"
    },
    {
      "what": "The maximum length is 32 rounds instead of 40.",
      "why": "This gives margin under the 40-round limit.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "The four one-shot actions Secret, Trade-off, Gift and Competition, with the opponent choosing for Gift and Competition.",
    "Geisha with Charm values equal to their number of Item cards (five Geisha, 3, 3, 4, 5 and 6).",
    "One card removed unseen each hand, hidden hands of 6 cards, and a deck of 8.",
    "Majority per Geisha decides its Victory Marker, and ties leave the marker where it is.",
    "The dual win condition: Charm threshold first, then Geisha count.",
    "Starting turns alternate between hands."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is strong and fits the platform. Scoring hands in mirrored pairs removes the last-mover seat edge and halves the luck of the deal, while staying well within the limits."
  },
  "variation": {
    "name": "Hanamikoji: Paired Hands",
    "summary": "A two-player Hanamikoji on five Geisha. Hands are played in pairs, each player starts one hand of every pair, and Geisha are won by combined majorities over the pair. At most two pairs (32 rounds) are played.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS\n- 5 Geisha, G1 to G5, with Charm G1=3, G2=3, G3=4, G4=5, G5=6 (total 21).\n- 21 Item cards: three of G1, three of G2, four of G3, five of G4 and six of G5. A card is written as its Geisha number, 1 to 5.\n- 5 Victory Markers, one per Geisha. Each is on Player 1's side, on Player 2's side, or neutral. All start neutral.\n- Each player has four action markers: Secret, Trade-off, Gift and Competition.\n- Each player has pair totals: five counts, one per Geisha, of the cards they have kept during the current pair of hands.\n\nSTRUCTURE\n- There are at most 4 hands of 8 rounds each (32 rounds).\n- Hands 1 and 2 form pair 1. Hands 3 and 4 form pair 2.\n- Player 1 starts hands 1 and 3. Player 2 starts hands 2 and 4.\n- In each hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player is active in rounds 2, 4, 6 and 8. The player who is not active is the opponent.\n\nSTART OF EACH HAND (before its round 1)\n- Shuffle all 21 Items.\n- Remove the top card face down. Nobody sees it, and it plays no part this hand.\n- Deal 6 cards to each player as a private hand. Each player sees only their own hand, as a sorted list of numbers.\n- The other 8 cards form the face-down deck.\n- Both players' four actions become unused, and both Secrets are emptied.\n- At the start of hands 1 and 3 only, both players' pair totals are reset to 0 0 0 0 0.\n- Victory Markers always stay where they are.\n\nEACH ROUND\n1. The game announces the hand, the round, the active player, each player's unused actions, both players' pair totals and the marker positions.\n2. The active player draws the top deck card and is privately shown their hand.\n3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition.\n4. Choice 2: the active player writes the cards the action uses, as space-separated numbers with repeats written out (for example '5 5 2'). The cards are legal if, for each Geisha number, the number of times it is written is at most the number of that card in the player's hand.\n   - Secret: exactly 1 number. That card is set face down as their Secret.\n   - Trade-off: exactly 2 numbers. Those cards are discarded face down and do not count.\n   - Gift: exactly 3 numbers, revealed in the order written as offer 1, 2 and 3.\n   - Competition: exactly 4 numbers, all revealed. The first two form pair A and the last two form pair B.\n   The named cards leave the active player's hand.\n5. Choice 3, only for Gift or Competition: the opponent writes one digit.\n   - Gift: 1, 2 or 3. The opponent adds that card to their pair totals, and the active player adds the other two to theirs.\n   - Competition: 1 for pair A or 2 for pair B. The opponent adds the chosen pair to their pair totals, and the active player adds the other pair to theirs.\n6. The action becomes spent. The game publicly announces the action, and for Gift or Competition the revealed cards and the split. For Secret and Trade-off it announces only that the action was used.\n\nDEFAULTS\n- Illegal or missing action: the first unused action in the order Secret, Trade-off, Gift, Competition is used.\n- Illegal card answer (wrong count, unreadable or not in hand): the required number of lowest-numbered cards in hand are used, in ascending order. For Competition, the first two of them form pair A.\n- Illegal or missing pick: counts as 1.\n- Cards always work out: each player holds 6 + 4 = 10 cards and spends 1 + 2 + 3 + 4 = 10.\n\nEND OF EACH HAND (after round 8)\n- Each player's Secret is revealed and added to their pair totals.\n- The game announces both Secrets and both players' pair totals.\n\nEND OF EACH PAIR (after hands 2 and 4, following the end-of-hand step)\n- For each Geisha, compare the two players' pair totals. A strictly higher total moves that Geisha's marker to that player's side. A tie leaves the marker where it is (neutral, or on a side from pair 1).\n- Charm is the sum of the Charm values of the Geisha on a player's side. Geisha count is the number of markers on a player's side.\n- The game announces all markers, Charm and Geisha counts.\n- Win check:\n  - If a player has 11 or more Charm, they win.\n  - Otherwise, if a player has 3 or more Geisha, they win.\n  - Otherwise, after pair 1 the game continues with hand 3.\n  - After pair 2 with no winner, the higher Charm wins. If Charm is equal, the higher Geisha count wins. If both are equal, the game is a draw.",
    "objective": "After hand 2 and after hand 4: a player with 11 or more Charm from markers on their side wins. Otherwise a player with 3 or more markers on their side wins. Total Charm is 21 and there are 5 Geisha, so at most one player can meet each condition, and Charm is checked first. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count, and otherwise the game is a draw.",
    "expected_effect": "Every scored contest now contains one hand where each player is the starter and one where each is the last mover, so the move-order edge cancels. Both hands count equally, and the second is played with both players fully informed of the first, which turns the pair into a two-stage plan. In hand 1 players build a lead or a position. In hand 2 they defend or chase specific Geisha with known deficits, and offers can be targeted. The swing from the deal is spread over 32 counted cards, so splitting skill and reading hidden Secrets matter more. Most games should end after pair 1, and a stalemate goes to a second pair in which earlier markers hold on ties. Thoughtless policies still lose: a player who always picks 1 receives the worst offer, and fixed action orders reveal intent and waste high cards. No talk phase is used, since this is a two-player game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 3,
    "attributes": 15,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 32
  }
}
```
````
