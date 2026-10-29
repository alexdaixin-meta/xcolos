# 29 design

- time: 2026-10-27T17:58:47+00:00 (97.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ac29f84ba2fe56d4, reply sha256 0167f769fac01331

## Sent

````
Original game: Air Land And Sea
Players in the original: 2 to 2

Original rules:
Place Air, Land, Sea boards in a row. Shuffle 18 battle cards, deal 6 face-down to each player as hand. Shuffle 2 supreme commander cards, deal one to each; red goes first each battle. A battle: players alternate taking one action: Deploy a card face-up from hand to its matching theater on your side, covering any cards already there and immediately resolving its instant or ongoing ability, Improvise a card face-down to any theater as strength 2 with no ability, or Withdraw and concede the battle. Covered cards cannot be flipped but keep abilities and can move. Abilities may flip, move, draw, or modify strength, and may affect adjacent theaters. After both play 6 cards or one withdraws, total strength per theater per side; who has higher sum controls it. Most theaters controlled wins the battle. Score VPs based on how many cards opponent still held when battle ended; withdrawing gives opponent fewer VPs. First to 12 VPs wins the match.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rework the action economy so no single fixed action dominates.
1. Make IMPROVISE a real alternative to deploying. Options:
   - Let a face-down card add improvise_strength plus a bonus.
   - Or let it count toward a tie-break.
   - Or cap face-up deploys per theater, so placement matters more than raw card number.
2. Make WITHDRAW a sensible choice when behind, rather than a pure giveaway. Options:
   - Reduce the withdrawal VP for early withdrawal.
   - Or award the battle winner VP scaled by the margin or the number of theaters held, so losing a full battle costs clearly more than conceding.
3. Add a reason to vary play beyond 'dump the highest card in its own theater'. Options:
   - Theater-specific effects.
   - Or let the second player see the first player's commitment and respond.
4. Re-check that neither 'always first option' nor 'always last option' beats random seats overwhelmingly.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- against random seats the results were {'seat 2': 31, 'seat 1': 28, 'seats 1 and 2': 1}
- a thoughtless policy `first@seat1`: won 60, lost 0, drew 0
- a thoughtless policy `first@seat2`: won 59, lost 0, drew 1
- a thoughtless policy `last@seat1`: won 0, lost 60, drew 0
- a thoughtless policy `last@seat2`: won 0, lost 60, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Air, Land and Sea is a two-player card duel fought over a series of battles. Players alternate placing cards into three theaters, either face-up in the card's own theater with its ability or face-down anywhere as strength 2, or they withdraw to concede. Whoever controls more theaters wins the battle, victory points depend on how early a loser withdraws, and the first player to 12 VP wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the tested variation, 'always first option' won 60-0 as seat 1 and 59-0-1 as seat 2 against random seats, and 'always last option' (withdraw) lost every match. The first option was an always-good action, so the interesting choices (improvise or withdraw) were pointless. The original also gives the first player a built-in edge through tie wins and initiative."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The design intent rewards placement and timing, but a fixed policy matched or beat all play, so skill showed up only as 'don't do anything else'. Hand quality from the deal also swings single battles strongly."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Once 'deploy the first card face-up' is known to win, nothing remains to improve. The original's ability interactions have headroom, but they cannot be built within the limits."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The core is reasoning-rich. Opponents' hands are hidden, six cards are undealt, face-down cards hide their identity, and deciding when to withdraw requires predicting the battle's outcome. The tested build simply did not reward any of it."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Theater control, battle results and VP are sums and comparisons."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The three 'boards' are just three counters per side, which is fine. However, 18 unique card abilities (flip, move, draw, adjacency, ongoing effects) far exceed the step and attribute limits. Alternating turns with a first-player tie edge also introduces seat asymmetry."
    }
  ],
  "problems": [
    "P1: The first listed action (deploy face-up) dominated. A thoughtless 'always first option' policy won every decided match from either seat.",
    "P2: Improvise (face-down, strength 2) was almost never better than deploying, so the hidden-card bluff and flexibility choice was dead.",
    "P3: Withdraw was a pure giveaway. 'Always last option' lost 100%, and withdrawing never saved enough VP to be a real decision.",
    "P4: Play reduced to 'dump the strongest card in its own theater'. There was no reason to read the opponent or vary allocation.",
    "P5: There was seat asymmetry: the first player moves first and wins ties.",
    "P6: The 18 unique card abilities with flip, move and adjacency effects are too complex to build within 20 steps and 20 attributes."
  ],
  "changes": [
    {
      "what": "Split each turn into two choices: which card (hand listed in random dealt order) and which theater (Air, Land, Sea). The card is automatically face-up if the theater matches its own, otherwise face-down. There is no 'deploy' option at the top of a list.",
      "why": "'Always first option' now means playing a random card into Air every time. That piles all strength into one theater and usually loses Land and Sea, so the first option is a bad policy rather than a dominant one.",
      "fixes": "P1"
    },
    {
      "what": "Face-down cards count as strength 3 (not 2) in any theater.",
      "why": "Cards of strength 1-3 are now at least as good face-down, and face-down play lets you contest a theater where you hold no matching cards. Improvising becomes a frequent, real decision.",
      "fixes": "P2"
    },
    {
      "what": "Battle wins pay 4 VP, or 6 VP for controlling all three theaters. Withdrawing at the start of battle round k gives the opponent 2 + floor((k-1)/2) VP (2, 2, 3, 3, 4, 4). If both withdraw in the same round, nobody scores.",
      "why": "Conceding early with a bad hand saves 2-4 VP against a likely loss, especially a sweep. Withdrawing every time still never scores, so 'always last option' still loses, while timely withdrawal becomes a skill.",
      "fixes": "P3"
    },
    {
      "what": "Both players choose at the same moment each round, and placements are revealed after each round. Face-down identities stay hidden, and six cards per battle are never dealt.",
      "why": "Each round becomes a blind allocation contest: guess where the opponent will commit, concede a theater cheaply, or win it narrowly. Players must also infer the opponent's remaining hand from the known 18-card deck, revealed face-up cards and the unknown undealt cards.",
      "fixes": "P4"
    },
    {
      "what": "Simultaneous turns replace alternation, and tied theaters are controlled by nobody.",
      "why": "This removes the first-player initiative and tie advantage, so neither seat has a structural edge.",
      "fixes": "P5"
    },
    {
      "what": "Card abilities are removed. Cards are only a theater and a strength (1-6).",
      "why": "This keeps the game inside the step and attribute limits, while placement, bluffing and withdrawal timing carry the depth.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Three theaters (Air, Land, Sea) on each side, with control by higher total strength and the battle won by controlling more theaters.",
    "An 18-card deck of Air, Land and Sea cards, with six dealt to each player per battle.",
    "Face-up deployment in a card's own theater versus face-down improvisation anywhere at a fixed strength.",
    "Withdrawal as a concession whose cost grows the later you withdraw.",
    "A match of several battles, with the first to 12 VP winning."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (hidden hands, three-front allocation, a face-down bluff option and concession timing) is rich in inference and fits the engine once abilities are removed and play is made simultaneous."
  },
  "variation": {
    "name": "Air, Land and Sea: Three Fronts",
    "summary": "Two commanders secretly commit one card per round across three theaters for six rounds per battle. Each card goes face-up in its own theater or face-down anywhere as strength 3, and a commander may withdraw early to limit losses. The first to 12 VP wins the match.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK. There are 18 cards. Each has a theater (Air, Land or Sea) and a strength from 1 to 6, giving exactly one card of each strength per theater (Air 1-6, Land 1-6, Sea 1-6). Both players know the full deck list.\n\nMATCH STRUCTURE. The match lasts at most 36 rounds. It is a sequence of battles, and each battle lasts up to 6 battle rounds. Battle round 1 of the first battle is match round 1. When a battle ends, the next battle begins in the next match round, but only if at least 6 match rounds remain (the next round is 31 or earlier). Otherwise the match ends.\n\nSTART OF A BATTLE (battle round 1 only). Shuffle all 18 cards. Deal 6 privately to each player; this is the round's one random draw. The remaining 6 stay unseen for this battle. Each player's hand is shown to them in the order dealt. Both players' strength in each theater is set to 0.\n\nEACH BATTLE ROUND, in order:\n1. WITHDRAW DECISION (simultaneous). Each player secretly chooses 'Fight' or 'Withdraw'.\n   - If exactly one player withdraws in battle round k, the other player gains 2 + floor((k-1)/2) VP. That is 2 VP in rounds 1-2, 3 VP in rounds 3-4 and 4 VP in rounds 5-6. The battle ends immediately.\n   - If both withdraw, nobody scores and the battle ends.\n2. CARD CHOICE (simultaneous). Each player secretly picks one card from their hand.\n3. THEATER CHOICE (simultaneous). Each player secretly names Air, Land or Sea.\n4. PLACEMENT. Each chosen card leaves its owner's hand and is placed on its owner's side in the named theater.\n   - If the named theater matches the card's own theater, the card is face-up and adds its printed strength.\n   - Otherwise it is face-down and adds exactly 3 strength.\n5. REVEAL. Both players are told every new placement. Face-up cards show their identity. A face-down card is shown only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced.\n6. If this was battle round 6 (both hands empty), the battle is resolved.\n\nRESOLVING A BATTLE.\n- In each theater, the player with the higher strength controls it. A tie means nobody controls it.\n- The player controlling more theaters wins the battle. If both control the same number, the player with the higher total strength across all three theaters wins.\n- If that is also equal, the battle is drawn and nobody scores.\n- The winner gains 4 VP, or 6 VP if they control all three theaters.\n- All face-down identities are then revealed to both players.\n\nAFTER EACH ROUND, the match ends if either player has 12 or more VP.",
    "objective": "The first player to reach 12 VP at the end of a round wins. Only one player can score in any battle, so both can never reach 12 together. If the match ends because the round limit allows no further full battle, the player with more VP wins. Equal VP is a draw.",
    "expected_effect": "Thoughtless policies now lose. 'Always first option' (Fight, the first dealt card, Air) stacks everything in Air and is out-controlled in Land and Sea. 'Always last option' withdraws every battle and never scores. Random play spreads cards badly and wastes high cards face-down. Good play involves several skills: playing 4-6s face-up and 1-3s face-down to contest weak theaters; reading where the opponent is committing from earlier reveals; deliberately conceding one theater to win two narrowly; counting the opponent's possible remaining cards from the known deck, their face-ups and the six unknown undealt cards; and withdrawing early from hopeless hands to deny a 4-6 VP win. Simultaneous play and nobody-wins-ties remove the seat edge. The deal varies hand strength, but early withdrawal caps the loss from a bad hand, and a 12 VP race over several battles lets skill dominate. Talk is omitted because the game has two players and is purely competitive."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 3,
    "attributes": 15,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
