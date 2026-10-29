# 01 design

- time: 2026-10-27T17:32:39+00:00 (86.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 404a215a13983326, reply sha256 8840344dde92afab

## Sent

````
Original game: Red7
Players in the original: 2 to 4

Original rules:
49 cards numbered 1-7 in seven spectrum colors Red Orange Yellow Green Blue Indigo Violet. Value beats color. Each player has a 7-card hand and a 1-card Palette. A Canvas card shows the current win rule. Red = highest card. Orange = most of one number. Yellow = most of one color. Green = most even cards. Blue = most different colors. Indigo = longest run. Violet = most cards below 4. Player left of current best starts. On your turn you must be winning by the Canvas rule at turn end. You may: play one card to your Palette, or discard one card to Canvas to change the rule (must be winning new rule after), or play to Palette then discard to Canvas (must be winning after). If you cannot or choose not to, you are eliminated. Last remaining player wins the round. With advanced scoring, winner banks Palette cards that satisfy the final rule as points; game ends when deck too small to deal.
````

## Reply

````
```json
{
  "original_summary": "Red7 is a 2-4 player elimination card game. Each turn you must end up winning under the current Canvas rule, either by adding a card to your face-up Palette or by discarding a card to the Canvas to change which of seven colour-rules decides the leader. If you cannot, you are out. The last player standing wins the hand, and hands are scored over a match.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy survives. 'Always play your highest card' loses as soon as an opponent switches the rule to Green or Violet. 'Always switch the rule' runs out of cards. 'Pass' means elimination. Starting order follows the dealt palettes, so no seat is fixed as the favourite."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card economy matters: making the smallest move that keeps the lead, and saving rule-changers for later. Still, a single hand is strongly decided by the deal. Only multi-hand scoring lets skill show through, and the advanced scoring is an optional rule."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win hands they were dealt well. Strong players gain by counting cards, conserving them and timing rule switches. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must work out from palettes, canvas changes and visible cards what opponents can still answer, and plan several turns of card spending ahead."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "Every rule is arithmetic in principle. Rules like 'most different colours' and 'longest run', with their tie-breaks, are long computations over sets, which invites errors or a referee ruling."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Text and turn-based, which suits the platform. But seven rules, 49 cards and up to 4 players' palette statistics go far beyond 20 attributes and 20 steps per round. Orange, Yellow, Blue and Indigo each need per-number or per-colour count tables."
    }
  ],
  "problems": [
    "P1: Seven win rules (several needing per-colour or per-number counts and run detection) far exceed the attribute and step limits.",
    "P2: A 49-card deck with 4 players makes palette tracking and tie-break computation too heavy to build reliably.",
    "P3: A single hand is largely decided by the deal, and multi-hand scoring is optional, so luck can swamp skill.",
    "P4: The original advanced scoring (banking qualifying palette cards under each rule) needs extra per-rule sums, and its match length is unbounded in rounds.",
    "P5: There is no clean arithmetic definition of 'winning' under every rule without long tie-break chains."
  ],
  "changes": [
    {
      "what": "Cut to three colours and three rules: Red (highest card), Green (most even cards), Violet (most cards below 4).",
      "why": "Each rule reduces to a single number per player built from a few tracked palette statistics. The core loop of switching the rule to one you lead is kept.",
      "fixes": "P1"
    },
    {
      "what": "Use a 21-card deck (numbers 1-7 in three colours) and allow 2-3 players with 5-card hands.",
      "why": "Small enough to track each player in a handful of attributes. There are still enough cards that counting what is unseen is real inference.",
      "fixes": "P2"
    },
    {
      "what": "Encode every card as one strength number (number x 10 + colour rank) and define each rule as a single key per player. The actor must hold the strictly highest key, otherwise they are out.",
      "why": "Leadership becomes one comparison with no ties possible between non-zero keys. Legality checking is replaced by 'end your turn not leading and you are eliminated', which matches the original's consequence.",
      "fixes": "P5"
    },
    {
      "what": "Make the match mandatory. The last survivor of a hand scores 2 and the last player eliminated scores 1. The match ends when someone reaches 6 points at the end of a hand, or at the 40-round cap.",
      "why": "Several hands average out the deal. The runner-up point rewards surviving longer even in a bad hand. A fixed cap keeps the game short.",
      "fixes": "P3"
    },
    {
      "what": "Replace qualifying-card banking with fixed placement points.",
      "why": "This removes per-rule sum tracking while still rewarding hand wins and survival.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Value beats colour, with a colour tie-break order (Red highest).",
    "Hidden hand plus a face-up palette.",
    "The Canvas rule changes when a card is discarded to it.",
    "Each turn: play to the palette, discard to the canvas, or both. You must end the turn winning or be eliminated.",
    "The starting player is the one after the initial leader.",
    "Last player standing wins the hand, scored over multiple hands."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core choice (spend a card to stay ahead, or change the rule) and the hidden-hand inference survive a cut to three rules, which fits the limits."
  },
  "variation": {
    "name": "Red3",
    "summary": "A compact Red7. Three colour-rules, a 21-card deck and hidden 5-card hands. Each turn you must end up leading under the current Canvas rule or be eliminated. Hands are scored over a match.",
    "players": {
      "min": 2,
      "max": 3,
      "suggested": 3
    },
    "rules": "CARDS. 21 cards: numbers 1 to 7 in each of three colours, Red, Green and Violet. Colour rank is Red 3, Green 2, Violet 1. Every card has a strength of number x 10 + colour rank (for example, 7 Red = 73 and 4 Violet = 41). A higher strength beats a lower one, so the number decides first and the colour breaks ties. A card is EVEN if its number is 2, 4 or 6. A card is LOW if its number is 1, 2 or 3.\n\nRULES ON THE CANVAS. The Canvas shows one colour, and that colour is the current rule. Each living player has a KEY under the current rule:\n- Red: key = strength of the highest card in your palette.\n- Green: key = 100 x (number of even cards in your palette) + strength of your highest even card. The key is 0 if you have no even cards.\n- Violet: key = 100 x (number of low cards in your palette) + strength of your highest low card. The key is 0 if you have no low cards.\nYou are LEADING if your key is strictly higher than every other living player's key. Because every card is unique, two non-zero keys can never be equal.\n\nSETUP OF A HAND. Shuffle all 21 cards. Deal each player 5 cards as a hidden hand, then deal each player 1 card face up as the start of their palette. The remaining cards are set aside unseen. The Canvas starts as Red. All players are alive. The initial leader is the player with the highest palette card. The first turn goes to the next player in seat order after the leader.\n\nA TURN. On your turn you choose exactly one of:\n(a) play one card from your hand face up to your palette;\n(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour (the card leaves play);\n(c) do (a) and then (b), with two different cards;\n(d) fold.\nAfter your action, keys are recomputed under the current rule. If you are not leading, or you folded, or you named a card you do not hold, you are eliminated. Your palette stays visible but no longer counts. Play then passes to the next living player in seat order.\n\nA ROUND is one pass of turns through every player in seat order, beginning with the player whose turn it is. Players already eliminated are skipped.\n\nEND OF A HAND. A hand ends the moment only one player is alive. That player scores 2 points. The player eliminated last in that hand (the one whose elimination left a single survivor) scores 1 point. Any others score 0. If the match is not over, a new hand is set up as above, starting at the next round.\n\nEND OF THE MATCH. After a hand ends, the match ends if any player has 6 or more points. The match also ends when round 40 is complete; a hand still unfinished at that point scores nothing.\n\nINFORMATION. Palettes, the Canvas, all eliminations and all points are public. Hands and the set-aside cards are hidden. There is no table talk.",
    "objective": "When the match ends, the player with the most points wins. If two or more players share the most points, the match is a draw.",
    "expected_effect": "Every turn forces the cheapest card spend that keeps the lead. Players weigh adding to the palette under the current rule against switching to Green or Violet, where their palette is stronger. They must hold back rule-changers and infer, from what has been played and discarded, whether an opponent can answer. With 18 of 21 cards in play, counting the unseen cards is valuable. The multi-hand match and the 1-point runner-up reward cut the effect of a single deal: a skilled player recovers by surviving bad hands and converting good ones. Talk is left out. Turns are sequential and actions already reveal information, so messages would mostly add kingmaking ('everyone eliminate the leader'), not reasoning about one's own hand. Simple policies lose. Folding scores nothing. 'Always play the highest card' is beaten by any opponent who switches to Green or Violet. 'Always switch the rule' runs out of cards within a few turns."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
