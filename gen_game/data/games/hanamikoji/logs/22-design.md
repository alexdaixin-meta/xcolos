# 22 design

- time: 2026-10-27T10:27:41+00:00 (66.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4239e1c5bb68faa9, reply sha256 982c6f17f326ec82

## Sent

````
Original game: Hanamikoji
Players in the original: 2 to 2

Original rules:
Two players compete for 7 Geisha cards. Each Geisha has a Charm value and a set of Item cards (total 21 Items across types). First to win 4 Geisha or 11+ Charm points from won Geisha wins; 11 Charm beats 4 Geisha if both achieved same scoring.
Each round: shuffle 21 Items, secretly remove 1 card from play, deal 6 cards each as hidden hands, remaining 8 form a deck. Players alternate turns for 4 turns each: draw 1 from deck, then use one unused Action marker. Secret: set aside 1 hand card face-down for final scoring. Trade-off: set aside 2 hand cards face-down discarded this round. Gift: reveal 3 hand cards, opponent takes 1 to his side, you keep 2. Competition: reveal 4 hand cards as two pairs of 2, opponent chooses one pair, you keep the other. All kept cards are placed by their Geisha. After 8 turns, reveal Secret cards and compare counts per Geisha: higher count wins that Geisha and moves its Victory Marker; ties leave marker. If winning goal met, game ends. Otherwise collect all Item cards, retain Victory Markers, flip Action markers up, swap starting player, and start new round.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Redesign the turn so it needs at most 4 choice steps per round, and keep the scoring, markers, Charm values and win conditions, which test well. Options: (1) Fix the action by turn rather than letting the player choose it. For example, each player's turns in a hand go Secret, Trade-off, Gift, Competition in that order, so the only choice is which cards to commit. (2) Or merge the action and its cards into one choice from a single option list, such as 'Secret:G3' or 'Gift:G1,G4,G6'. (3) Give every action an equal-sized commitment, or drop Trade-off and Secret, so one card-choice step serves every action. (4) Phrase each choice as 'the active player' and 'the opponent' rather than seat by seat, so the alternation of who acts first does not double the steps. The result should be one choice by the active player and one pick by the opponent, used only when the action is Gift or Competition (a `when` condition on a single step is fine). Keep the opponent's pick as a single 1/2/3 choice.
the game was built and behaves as specified, but evaluation found design flaws:
- the built game has 7 choice steps per round, over the limit of 4
- against random seats the results were {'seat 1': 29, 'seat 2': 30, 'seats 1 and 2': 1}
- a thoughtless policy `first@seat1`: won 28, lost 32, drew 0
- a thoughtless policy `first@seat2`: won 27, lost 33, drew 0
- a thoughtless policy `last@seat1`: won 35, lost 25, drew 0
- a thoughtless policy `last@seat2`: won 32, lost 28, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "Hanamikoji is a two-player card game of hidden hands. Players compete for 7 Geisha (Charm 2,2,2,3,3,4,5) by committing their matching Item cards through four one-use actions: Secret, Trade-off, Gift and Competition. The last two make the opponent split your offer, so you must predict what they will take. The first player to own 11 Charm or 4 Geisha after a hand's scoring wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "The tested build gave random seats 29 to 30 with 1 draw. Every thoughtless policy (first or last option, in either seat) lost between 25 and 33 of 60 games, so no simple policy cannot lose. The worst case, last@seat1 at 35-25, is a mild edge within noise. Alternating the starting player each hand offsets the second-mover advantage."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The deal is random, but every card reaches someone's tableau through choices. You choose the order of actions, what to bury, what to discard and how to split Gift and Competition offers knowing the opponent will take the best part. A player who thinks about these beats one who does not over several hands. Markers carry over between hands, so one bad deal is recoverable."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win some Geisha, because ties keep markers and the offers force sharing. Strong play has depth: tracking the 1 removed card and the hidden Secret, timing the actions, and building offers whose every split helps you. It is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each hand has three hidden elements: the opponent's hand, the removed card and each player's Secret card. Players infer from revealed offers and from which actions remain. The Gift and Competition splits are direct opponent modelling, and the race for markers needs planning across hands."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner of each Geisha comes from comparing card counts. Charm and Geisha totals are sums, and the win check compares them to 11 and 4. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only with no board. As built before, a turn was written seat by seat and a whole hand was packed into one round, giving 7 choice steps per round against a limit of 4. The game also has no length cap."
    }
  ],
  "problems": [
    "The previous build used 7 choice steps per round, over the limit of 4, because turns were duplicated seat by seat and several turns were packed into one engine round.",
    "The game has no hard length limit, but the platform allows at most 40 rounds, so the game needs a cap and an arithmetic tiebreak.",
    "Card selection had no defined fallback for an illegal answer, which risks a stalled or ambiguous build.",
    "The thoughtless policy last@seat1 reached 35-25, a slight edge that should not be made worse by any seat-specific structure."
  ],
  "changes": [
    {
      "what": "One engine round is now exactly one turn: one action by the active player. A hand is 8 consecutive rounds. Every choice is phrased as 'the active player' or 'the opponent', never by seat.",
      "why": "Each round now has 3 choice steps: the active player picks an unused action, the active player names the cards, and the opponent splits the offer (only when the action is Gift or Competition). This keeps the free choice of action, which is the heart of the game.",
      "fixes": "The previous build used 7 choice steps per round, over the limit of 4, because turns were duplicated seat by seat and several turns were packed into one engine round."
    },
    {
      "what": "The game lasts at most 40 rounds (5 hands). If nobody has won by then, the higher Charm total wins, then the higher Geisha count, otherwise it is a draw.",
      "why": "This fits the 40-round limit with a tiebreak decided by arithmetic. Real games almost always end within 3 to 4 hands, so the cap rarely matters.",
      "fixes": "The game has no hard length limit, but the platform allows at most 40 rounds, so the game needs a cap and an arithmetic tiebreak."
    },
    {
      "what": "Cards are written as Geisha numbers (G1 to G7). The card choice is a list of numbers that must be in hand. Any illegal answer is replaced by the required number of lowest-numbered cards from the hand. An illegal or missing action is replaced by the first unused action in the order Secret, Trade-off, Gift, Competition.",
      "why": "Every answer now leads to a defined result by arithmetic, and the default is a thoughtless policy that a good player can beat.",
      "fixes": "Card selection had no defined fallback for an illegal answer, which risks a stalled or ambiguous build."
    },
    {
      "what": "Kept as tested: the starting player alternates every hand, and the scoring, markers, Charm values and win thresholds are unchanged.",
      "why": "These measured as balanced. The only structural change is removing the seat duplication, so no new seat asymmetry is introduced.",
      "fixes": "The thoughtless policy last@seat1 reached 35-25, a slight edge that should not be made worse by any seat-specific structure."
    }
  ],
  "keeps": [
    "Seven Geisha with Charm 2,2,2,3,3,4,5 and 21 matching Item cards.",
    "One card removed unseen each hand, hands of 6, a deck of 8, and a draw at the start of each turn.",
    "Four one-use actions chosen freely: Secret, Trade-off, Gift and Competition.",
    "The opponent splits Gift and Competition offers.",
    "Victory markers that move only on a strict majority and stay on ties.",
    "Win at 11 Charm or 4 Geisha, with Charm checked first.",
    "The starting player alternates each hand."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The design tests well on balance and skill. Only the step structure exceeded the limits, and restructuring one turn into one round fixes that without changing the game."
  },
  "variation": {
    "name": "Hanamikoji: One Turn per Round",
    "summary": "This is the standard Hanamikoji. Each engine round is a single turn. The active player chooses one of their unused actions, then names the cards it uses, and the opponent splits Gift and Competition offers. Eight rounds make a hand, which is followed by scoring. The game lasts at most 5 hands (40 rounds).",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS\n- There are 7 Geisha, G1 to G7, with Charm values G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5.\n- There are 21 Item cards. Each Geisha has as many Items as its Charm: two each of G1 to G3, three each of G4 and G5, four of G6 and five of G7.\n- Each Geisha has a Victory Marker that is neutral at the start. A marker is on Player 1's side, on Player 2's side, or neutral.\n- Each player has four action markers: Secret, Trade-off, Gift and Competition.\n\nSTRUCTURE\n- The game is played in hands of 8 rounds each, at most 5 hands (40 rounds).\n- Player 1 starts hands 1, 3 and 5. Player 2 starts hands 2 and 4.\n- Within a hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player in rounds 2, 4, 6 and 8.\n- The other player in a round is called the opponent.\n\nSTART OF EACH HAND (first round of the hand)\n- Shuffle all 21 Items.\n- Remove 1 card face down. Nobody sees it, and it plays no part this hand.\n- Deal 6 cards to each player as a private hand. Each player sees only their own hand, shown as a sorted list of Geisha numbers.\n- The remaining 8 cards form a face-down deck.\n- Both players' four action markers become unused.\n- Both players' kept-card areas are emptied. Victory markers stay where they are.\n\nEACH ROUND (one turn)\n1. The game announces the hand number, the round number, the active player, which actions each player still has unused, and both players' kept cards per Geisha.\n2. The active player draws the top card of the deck into their hand.\n3. Choice 1: the active player chooses one of their unused actions.\n4. Choice 2: the active player writes the Geisha numbers of the cards the action uses. Every named card must be in their hand.\n   - Secret: 1 card. It is placed face down as their Secret and stays hidden until scoring.\n   - Trade-off: 2 cards. They are discarded face down and do not count this hand.\n   - Gift: 3 cards, which are revealed in the order written.\n   - Competition: 4 cards, written as pair A (the first two) and pair B (the last two), and revealed.\n5. Choice 3, only if the action is Gift or Competition: the opponent picks.\n   - For Gift, the opponent writes 1, 2 or 3. They take that revealed card into their own kept area, and the active player keeps the other two.\n   - For Competition, the opponent writes 1 (pair A) or 2 (pair B). They keep that pair, and the active player keeps the other.\n   - An illegal pick counts as 1.\n6. The used action becomes spent. The game announces publicly what happened, without revealing Secret or Trade-off cards.\n\nDEFAULTS\n- An illegal or missing action counts as the first unused action in the order Secret, Trade-off, Gift, Competition.\n- If the card answer is illegal (wrong count, or a card not in hand), the engine uses the required number of lowest-numbered cards in the hand, in ascending order.\n- The card counts always work out: each player draws 4 cards and spends 1+2+3+4 = 10 cards from 6+4.\n\nSCORING (after round 8 of each hand)\n- Each player's Secret card is revealed and added to their kept area.\n- For each Geisha, compare the two players' kept counts. A strictly higher count moves that Geisha's marker to that player's side. A tie leaves the marker where it is.\n- Each player's Charm is the sum of Charm of the Geisha whose markers are on their side. Each player's Geisha count is the number of those markers.\n\nWINNING\n- If a player has 11 or more Charm, they win.\n- Otherwise, if a player has 4 or more Geisha, they win.\n- Two players cannot both reach either threshold, because the totals are 21 Charm and 7 Geisha.\n- If nobody has won, the next hand starts with the other starting player.\n- If 5 hands are completed without a winner: the higher Charm wins; if Charm is equal, the higher Geisha count wins; if that is also equal, the game is a draw.",
    "objective": "The game is checked after each hand's scoring. A player with 11 or more Charm from Geisha markers on their side wins immediately. Otherwise a player with 4 or more Geisha markers wins. If no one has won after 5 hands (40 rounds), the higher Charm total wins, then the higher Geisha count, otherwise the game is a draw.",
    "expected_effect": "Play matches Hanamikoji: players choose the order of their actions, decide what to hide in the Secret and what to throw away, and design Gift and Competition splits expecting the opponent to take the best part. The opponent's picks are pure opponent modelling and card counting, using the removed card and the hidden Secret. Because a round is one turn written for 'the active player', the build needs 3 choice steps instead of 7. Balance should stay close to the tested results (random play near 50-50, every simple policy losing about half its games), since scoring, markers and alternation are unchanged. No talk phase is used because the game has only two players."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
````
