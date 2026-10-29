# 01 design

- time: 2026-10-28T06:13:13+00:00 (60.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 4da83e0630099784, reply sha256 ba0e3993f68ca840

## Sent

````
Original game: Cash and Guns
Players in the original: 4 to 8

Original rules:
Setup 8 loot piles face down, each player gets 5 Click and 3 Bang! cards plus a foam gun. Game lasts 8 rounds. Each round: 1) Reveal 8 loot cards. 2) Each player secretly selects one remaining Bullet card face down. 3) All simultaneously point guns at another player. 4) Current Godfather may force one player to point elsewhere. 5) Simultaneously each player chooses to lie down and abandon loot but avoid being shot, or stay up shouting Banzai. If your target lay down you discard your bullet unused. 6) Standing shooters reveal bullets. Bang! wounds target, target lies down and misses loot share; multiple wounds possible. 3 wounds eliminates a player. All Bang! and Click effects happen simultaneously. 7) In Godfather order clockwise, each standing survivor takes one remaining loot card or flips the Godfather token to become next Godfather. Distribution may circle multiple times. After 8 rounds, alive players total cash; player with most diamond cards gets $60000 bonus; richest wins, most wounds breaks tie.
````

## Reply

````
```json
{
  "original_summary": "Cash and Guns is a 4-8 player bluffing game about gangsters splitting loot. Each round every player secretly loads a Bang! or Click card, points a foam gun at a rival, and then decides whether to stay standing for a share of the loot or lie down to avoid being shot. Over 8 rounds the richest survivor wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always lying down earns nothing. Always standing attracts the Bangs of every rival who wants a bigger share. Firing all three Bangs early tells rivals that your later shots are Clicks. The Godfather token gives some edge in draft order and in redirecting guns, but players draft for it, so no seat is fixed in advance."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading bluffs and counting Bangs matters. But the face-up loot draft is chaotic and partly table-dependent with up to 8 players. With many shooters it is often unclear who can be blamed or punished, so skill shows only noisily."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Choices keep getting deeper: when to spend a scarce Bang, whom to aim at, and how to read who is bluffing from who is holding. A weak player still collects loot in the rounds nobody aims at them."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each loaded bullet is hidden, and each player's remaining Bang count is partly hidden, because bullets discarded against a lying-down target are never revealed. Choosing to stand or lie down is inference about whether the gun on you is loaded."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Wounds, eliminations and cash totals are all counts. The diamond bonus and the tie-break by wounds are arithmetic too."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The game uses physical foam guns. It has a Godfather redirect sub-phase and a loot draft that circles the table an unknown number of times, which is a variable-length sequential block. That block, plus the separate diamond majority, exceeds the per-round choice-step budget."
    }
  ],
  "problems": [
    "The loot draft is a variable-length sequence of picks that can circle the table several times. The engine cannot build that, and it would need far more than 4 choice steps per round.",
    "The Godfather redirect adds an extra sequential choice phase and a seat-like advantage, and it is hard to fit beside aiming and standing.",
    "Card-level loot types (cash values, diamonds, special cards) and the separate diamond-majority bonus add hidden-state bookkeeping without adding much inference.",
    "With up to 8 players the shooting becomes chaotic and skill shows only noisily.",
    "Physical gun pointing has to become a text choice."
  ],
  "changes": [
    {
      "what": "Replace the loot draft with an equal split of a single round pot among the players who are still standing and unwounded. The pot size is one random draw, announced before any choice.",
      "why": "The split keeps the incentive that each rival removed raises your share. It needs only one step. Announcing the pot first gives planning content: save Bangs for big pots, stand when the pot is worth the risk.",
      "fixes": "The loot draft is a variable-length sequence of picks that can circle the table several times. The engine cannot build that, and it would need far more than 4 choice steps per round."
    },
    {
      "what": "Remove the Godfather token and redirect.",
      "why": "This removes a sequential sub-phase and a positional edge, and keeps the round to three simultaneous choices.",
      "fixes": "The Godfather redirect adds an extra sequential choice phase and a seat-like advantage, and it is hard to fit beside aiming and standing."
    },
    {
      "what": "Drop loot card types and the diamond bonus. Loot is plain cash in thousands.",
      "why": "This keeps the single strong hidden element, which is the bullet hand.",
      "fixes": "Card-level loot types (cash values, diamonds, special cards) and the separate diamond-majority bonus add hidden-state bookkeeping without adding much inference."
    },
    {
      "what": "Limit play to 3-5 players, suggested 4. Keep exactly 8 rounds and 8 bullets (3 Bang, 5 Click), with one bullet spent every round.",
      "why": "With fewer players, who shot whom matters and can be remembered and punished. Because every card is spent exactly once, Bang-counting is a precise inference problem.",
      "fixes": "With up to 8 players the shooting becomes chaotic and skill shows only noisily."
    },
    {
      "what": "Turn pointing into a simultaneous text choice of a target and a bullet. Targets are then announced openly before the stand-or-lie decision. Add one simultaneous message per round before aiming.",
      "why": "Players still see exactly who is aiming at them, as in the original. The message adds threats, bluffs and temporary alliances. Only one player can win, so following a proposal can cost you.",
      "fixes": "Physical gun pointing has to become a text choice."
    }
  ],
  "keeps": [
    "Secret Bang!/Click bullets, 3 Bang and 5 Click per player, one spent each round",
    "Open aiming at a chosen rival, then a simultaneous stand-or-lie-down decision",
    "Lying down forfeits loot but avoids wounds",
    "A bullet aimed at a player who lies down is discarded unrevealed",
    "Wounded players miss the loot",
    "3 wounds eliminates a player",
    "8 rounds",
    "Richest survivor wins, ties broken by most wounds"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core bluff of a hidden bullet, a visible gun and a stand-or-duck choice fits simultaneous polls well once the draft and the Godfather are removed."
  },
  "variation": {
    "name": "Cash and Guns: Standoff",
    "summary": "Gangsters secretly load a Bang or Click bullet and openly aim at a rival. Then each decides whether to stand for a share of the round's loot or duck to stay safe. Every player has exactly 3 real bullets for 8 rounds, so counting and bluffing decide who survives richest.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP: Each player starts with 0 cash, 0 wounds and a private hand of 8 bullet cards: 3 Bang and 5 Click. Only the owner knows which cards remain in their hand. The game lasts 8 rounds.\n\nEACH ROUND:\n1. LOOT. The engine draws a whole number uniformly from 6 to 14. That number, in thousands of dollars, is this round's pot. It is announced to everyone.\n2. TALK. Every living player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing said is binding.\n3. AIM. At the same time, every living player secretly chooses:\n   - a target, which is any other living player;\n   - one bullet card from their hand, Bang or Click, which must be a card they still hold.\n4. GUNS SHOWN. Everyone's target is announced publicly. Bullets stay hidden.\n5. STAND OR DUCK. At the same time, every living player chooses Stand or Duck. The choices are then announced.\n6. FIRE. Each player's chosen bullet is removed from their hand whatever happens.\n   - A bullet is FIRED only if its shooter Stood and its target Stood. Fired bullets are revealed publicly.\n   - A shooter who Ducked, or whose target Ducked, discards the bullet face down. Its type is never revealed.\n   - Each fired Bang gives its target 1 wound. A player hit by several Bangs takes several wounds. All shots happen at once, so a player who is wounded still fires their own bullet.\n7. ELIMINATION. A player with 3 or more wounds is eliminated. They keep their cash for the record but cannot win, and they take no further part.\n8. SPLIT. Count the players who Stood, were not wounded this round, and were not eliminated. These are the SHARERS. Each sharer gains the pot divided equally among them, which may be fractional. If there are no sharers, the pot is lost. Players who Ducked or were wounded this round gain nothing.\n9. END CHECK. If only one player is alive, the game ends. If no player is alive, the game ends in a draw. Otherwise, after round 8, the game ends.\n\nNOTES: Each player has used all 8 cards by the end of round 8. Revealed bullets are public. Discarded bullets are not, so a player's remaining Bang count can be inferred only from what was revealed.",
    "objective": "Only players still alive at the end can win. The living player with the highest cash wins. If living players are tied on cash, the one among them with the most wounds wins. If still tied, the game is a draw. If exactly one player is alive, that player wins. If no player is alive, the game is a draw.",
    "expected_effect": "Players must decide when a Bang is worth spending (big pots, a leader to stop) and when a Click is a safe bluff. They must read whether the gun on them is loaded from the opponent's remaining Bangs, the pot size and the talk. Always ducking scores nothing. Always standing gets a player shot out by rivals who gain from removing a sharer. Burning Bangs early makes later threats empty. Talk matters because players disagree about who should be shot: everyone wants the others removed, not themselves. A player who goes along with a proposed truce ('nobody loads Bang this round') can be betrayed by a rival who stands with a Bang and takes a bigger share. A player who agrees to gang up on the leader can be next once the leader falls. The random pot affects every sharer equally, so it rewards timing rather than deciding the winner."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 8
  }
}
```
````
