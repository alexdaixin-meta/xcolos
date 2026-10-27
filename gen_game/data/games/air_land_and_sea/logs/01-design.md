# 01 design

- time: 2026-10-27T17:21:45+00:00 (58.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4d68a1bc59a34faf, reply sha256 b699544a372b9c5f

## Sent

````
Original game: Air Land And Sea
Players in the original: 2 to 2

Original rules:
Place Air, Land, Sea boards in a row. Shuffle 18 battle cards, deal 6 face-down to each player as hand. Shuffle 2 supreme commander cards, deal one to each; red goes first each battle. A battle: players alternate taking one action: Deploy a card face-up from hand to its matching theater on your side, covering any cards already there and immediately resolving its instant or ongoing ability, Improvise a card face-down to any theater as strength 2 with no ability, or Withdraw and concede the battle. Covered cards cannot be flipped but keep abilities and can move. Abilities may flip, move, draw, or modify strength, and may affect adjacent theaters. After both play 6 cards or one withdraws, total strength per theater per side; who has higher sum controls it. Most theaters controlled wins the battle. Score VPs based on how many cards opponent still held when battle ended; withdrawing gives opponent fewer VPs. First to 12 VPs wins the match.
````

## Reply

````
```json
{
  "original_summary": "Air, Land and Sea is a two-player card game. Over several battles, players alternate playing cards from a six-card hand into three theaters. A card goes face-up to its matching theater and uses its special ability, or face-down to any theater as a flat strength 2. A player may withdraw early to give away fewer victory points, and the first to 12 VP wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy dominates. Always withdrawing hands the opponent points every battle. Always improvising caps you at strength 2 per card. Always playing your highest card telegraphs your strength and can be out-concentrated. The first player wins ties, which is a seat edge, but the role alternates between battles."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Choosing where to spend cards, when to bluff face-down, and when to withdraw early decides close battles. Strong players beat weak ones across a match even though each hand is dealt at random."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading the opponent's hand from what they play, timing a withdrawal, and spreading strength across theaters all leave room to improve. A beginner can still win single battles with a good deal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, 6 of the 18 cards are never dealt, and face-down cards hide their identity. Players must infer the opponent's remaining strength, which theaters they can still reinforce, and whether a face-down card is a bluff."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "Theater sums and VP are arithmetic. However, 18 distinct card abilities (flip, move, adjacent-theater effects, ongoing modifiers, covered cards keeping abilities) create long rule chains, and their interactions often need interpretation."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. But the unique abilities, especially move and flip with adjacency, need far more steps and state than the limits allow. 'First to 12' with a variable number of battles also has an open-ended length."
    }
  ],
  "problems": [
    "Eighteen unique card abilities, including adjacency, move and flip interactions, far exceed the step and attribute limits and invite rule disputes.",
    "Adjacency between theaters gives the game a spatial flavour the platform excludes.",
    "'First to 12 VP' gives a variable match length. With ties going to the first player, an odd number of battles can leave one seat with an extra first-player battle.",
    "The withdrawal VP table depends on seat and has several cases, which adds bookkeeping without adding much reasoning."
  ],
  "changes": [
    {
      "what": "Remove all card abilities. Cards are just Air, Land or Sea with a strength from 1 to 6. Deploying face-up gives the printed strength in the matching theater; improvising face-down gives strength 2 in any theater.",
      "why": "This keeps the core tension (bluffing face-down versus committing face-up, and spreading strength across theaters) while fitting the step budget and leaving nothing to interpret.",
      "fixes": "Eighteen unique card abilities, including adjacency, move and flip interactions, far exceed the step and attribute limits and invite rule disputes."
    },
    {
      "what": "The three theaters are independent labelled piles with no adjacency.",
      "why": "This removes every spatial relation.",
      "fixes": "Adjacency between theaters gives the game a spatial flavour the platform excludes."
    },
    {
      "what": "The match is exactly 4 battles of 6 rounds each (24 rounds). The first player alternates each battle, and the higher VP total wins.",
      "why": "Each player is first player exactly twice, so the tie-break edge balances out and the length is fixed. The game is zero-sum, so there is no cooperative option for 'higher total wins' to collapse.",
      "fixes": "'First to 12 VP' gives a variable match length. With ties going to the first player, an odd number of battles can leave one seat with an extra first-player battle."
    },
    {
      "what": "Use a single withdrawal table that depends only on how many cards the withdrawing player still holds: 4 or more gives the opponent 2 VP, 2 to 3 gives 3 VP, and 1 gives 4 VP. A battle fought to the end gives the winner 6 VP.",
      "why": "The table stays simple but keeps the identity of the game: withdraw early to save points, at the cost of conceding the battle.",
      "fixes": "The withdrawal VP table depends on seat and has several cases, which adds bookkeeping without adding much reasoning."
    }
  ],
  "keeps": [
    "Three theaters (Air, Land, Sea) and an 18-card deck dealt 6 to each player per battle, with 6 cards unseen.",
    "Deploy face-up to the matching theater, or improvise face-down to any theater as strength 2.",
    "Withdrawing early concedes the battle but gives the opponent fewer VP.",
    "Controlling at least two of the three theaters wins the battle, and the first player wins ties within a theater.",
    "Hidden hands and bluffing with face-down cards."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Cut down to its core of hidden-hand allocation, face-down bluffing and timed withdrawal, the game fits the limits and still demands inference and planning."
  },
  "variation": {
    "name": "Three Fronts",
    "summary": "A two-player match of 4 battles. In each battle, players alternate placing six hidden-hand cards into Air, Land and Sea, either face-up for full strength in the matching theater or face-down as a strength-2 bluff anywhere. They decide when to withdraw to limit losses. The higher VP total after 4 battles wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS\n- The deck has 18 cards: Air 1–6, Land 1–6 and Sea 1–6.\n- There are three theaters: Air, Land and Sea. Each player has their own side of each theater.\n- Each player has a VP score starting at 0.\n\nSTRUCTURE\n- The match has 4 battles of 6 rounds each, 24 rounds in total.\n- Player A is first player in battles 1 and 3. Player B is first player in battles 2 and 4.\n\nSTART OF EACH BATTLE (rounds 1, 7, 13 and 19)\n- Shuffle all 18 cards and deal 6 privately to each player.\n- The remaining 6 cards are set aside unseen for the whole battle.\n- All theaters start empty.\n\nEACH ROUND\nIf the battle has not ended by withdrawal, the first player takes one action, then the second player takes one action. Both players see the result of each action before the next one.\n\nThe three possible actions are:\n1. DEPLOY: place a card from your hand face-up on your side of the theater matching its suit (an Air card to Air, and so on). It counts its printed strength (1–6).\n2. IMPROVISE: place a card from your hand face-down on your side of any theater. It counts strength 2. The opponent sees only that a face-down card was placed there; the owner knows what the card is.\n3. WITHDRAW: concede the battle immediately. You may withdraw only while you still hold at least 1 card. The opponent scores VP by the number of cards you still hold:\n   - 4 or more cards: 2 VP.\n   - 2 or 3 cards: 3 VP.\n   - 1 card: 4 VP.\n   After a withdrawal, no further actions are taken in that battle, and the remaining rounds of the battle pass with no actions.\n\nCards placed later stack on earlier ones. Every card on your side counts, whether or not it is covered.\n\nEND OF A BATTLE FOUGHT TO THE END (after round 6 of the battle, when both players have played all 6 cards)\n- For each theater, add up each player's strength on their side.\n- The higher sum controls the theater. On an equal sum, including 0–0, the first player of that battle controls it.\n- The player controlling 2 or 3 theaters wins the battle and scores 6 VP.\n- The face-down cards are then revealed for the record.\n\nEND OF MATCH\nAfter round 24, compare VP totals.",
    "objective": "After 4 battles, the player with more VP wins. Equal VP is a draw.",
    "expected_effect": "Play revolves around allocation under hidden information. Each player has about 21 points of printed strength spread across suits they did not choose. They must decide which two theaters to fight for, whether to fake strength with face-down cards in a theater they cannot reach face-up, and when a battle is lost badly enough to withdraw for 2 VP instead of giving up 6. The second player sees more before each move but loses ties, and alternating first player across 4 battles balances the two seats. Simple policies lose:\n- Always withdrawing gives up 8 VP per match.\n- Always improvising totals only 12 strength against an average of about 21.\n- Always playing the highest card face-up is predictable and gets out-concentrated.\nRandom deals affect single battles, but well-timed withdrawals cap losses, and four battles let skill decide the match."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 2,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 24
  }
}
```
````
