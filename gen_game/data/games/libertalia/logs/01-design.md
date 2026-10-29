# 01 design

- time: 2026-10-27T22:04:09+00:00 (68.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e17e07973de69b14, reply sha256 56311e84bf7472e0

## Sent

````
Original game: Libertalia
Players in the original: 2 to 6

Original rules:
Game is 3 campaigns of 6 looting days plus a rest day. Each player has 30 cards of one color. At start of campaign 1, one player draws 9 random cards and all players take the same 9 into hand; later campaigns each player keeps 3 unplayed cards and draws 6 new common cards. Each day, booty tokens (chests 5, jewels 3, goods 1, maps, cursed -3, sabers, officers) are placed in 6 spaces, N tokens per space where N=player count. Sunrise: all simultaneously choose 1 hand card face down then reveal. Order characters by rank number, tie by influence value in silver mark. Day: in ascending rank order resolve each character's day ability. Dusk: in descending rank order each player takes one remaining booty token from that day's space and resolves dusk ability and saber/officer effects. Character goes to player's den face up. Night: all dens resolve night abilities simultaneously. Rest day: score dens: doubloons + chests*5 + jewels*3 + goods*1 + 12 per set of 3 maps -3 per cursed relic. Add to total track. Discard all characters in dens/graveyard, return booty and doubloons, give each 10 doubloons to start next campaign.
````

## Reply

````
```json
{
  "original_summary": "Libertalia is a 2-6 player pirate game over 3 campaigns. Every player holds the same hand of numbered characters. Each day all players secretly play one card at the same time. Lower ranks act first with their day abilities, and higher ranks pick booty first at dusk. Dens are scored for doubloons and treasure at the end of each campaign.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Hands are identical and play is simultaneous, so no seat has a built-in edge. Always playing the highest rank is exploited by killer characters and by ties. Always playing low gives up booty. Choices clearly change the outcome."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skilled players win more often in tabletop play. But the booty layout and the common card draw add variance. Some character interactions are chaotic chains whose outcome is hard to read, so the link from a good read to a good result is noisy."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Predicting which card the others will commit, and when they will, gives deep play. Weak players still collect some booty every day."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The core is opponent modelling. Everyone holds the same cards, so you infer from the cards already spent and from the visible booty which card each rival will play now. You also plan which cards to save across days."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scoring is pure arithmetic: doubloons plus token values plus map sets minus curses."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "About 40 distinct character abilities, many chaining across day, dusk and night phases. Per-day sequential booty picks for up to 6 players, saber and officer side effects, and 3 campaigns of 6 days. This far exceeds the step, attribute and choice limits."
    }
  ],
  "problems": [
    "There are far too many character abilities with phase-chained effects (day, dusk, night) to build within 20 steps per round.",
    "Sequential booty picking by up to 6 players needs more than 4 choice steps per round. The choice is also mostly obvious, since everyone takes the most valuable token.",
    "Side tokens (maps in sets, sabers, officers) add state and rule chains without adding much inference.",
    "Ties are broken by fixed player influence numbers, which gives some seats a permanent edge in ties.",
    "The game is too long: 3 campaigns of 6 days, card keeping and redraws.",
    "The variable player count of 2-6 makes booty rows and balance hard to fix. With 2 players under a highest-total rule, the game is purely zero-sum."
  ],
  "changes": [
    {
      "what": "Reduce the character set to 7 cards, ranked 1-7, each with one simple arithmetic ability resolved in a single phase.",
      "why": "This keeps the mind-game of identical hands while fitting the step limit.",
      "fixes": "There are far too many character abilities with phase-chained effects (day, dusk, night) to build within 20 steps per round."
    },
    {
      "what": "Booty is assigned automatically: non-tied players take tokens from best to worst in descending rank order.",
      "why": "Picking the highest token was nearly forced anyway. Automating it removes choice steps while rank still decides who gets what.",
      "fixes": "Sequential booty picking by up to 6 players needs more than 4 choice steps per round. The choice is also mostly obvious, since everyone takes the most valuable token."
    },
    {
      "what": "Booty is plain numeric tokens (5, 3, 1, and -3 for a cursed relic) in a daily row drawn from a fixed list of 6 rows.",
      "why": "This is one random draw per round with no set collection. The cursed relic preserves the pressure not to end up last.",
      "fixes": "Side tokens (maps in sets, sabers, officers) add state and rule chains without adding much inference."
    },
    {
      "what": "Same-rank ties become a Clash: all tied characters get nothing and their abilities do not fire.",
      "why": "Removing seat-based tie-breaks deletes the seat edge. Clashes also punish predictable play, because copying the obvious card is risky.",
      "fixes": "Ties are broken by fixed player influence numbers, which gives some seats a permanent edge in ties."
    },
    {
      "what": "Use 2 campaigns of 5 days. Each player gets the same 7-card hand per campaign and plays 5, so 2 cards go unused. The hand is refreshed for campaign 2.",
      "why": "10 rounds stays within limits. Saving cards is still a multi-round plan, and the shrinking known hands drive inference.",
      "fixes": "The game is too long: 3 campaigns of 6 days, card keeping and redraws."
    },
    {
      "what": "Fix the game at exactly 3 players, with a simultaneous one-message talk phase before cards are played.",
      "why": "With 3 players, one rival's loss is not automatically the other's gain, and booty rows can be balanced. Talk allows bluffing and feinting about which card you will play.",
      "fixes": "The variable player count of 2-6 makes booty rows and balance hard to fix. With 2 players under a highest-total rule, the game is purely zero-sum."
    }
  ],
  "keeps": [
    "All players hold the identical set of characters, so the game is reading what rivals will play from the same options.",
    "Cards are chosen secretly at the same time, then revealed.",
    "Higher rank takes the better booty first, while low ranks have abilities that profit or punish high ranks.",
    "A cursed relic that hurts whoever is left holding it.",
    "Campaign structure with unused cards, so you must decide which characters to spend and which to waste.",
    "Doubloon scoring summed into a total; the richest pirate wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The heart of Libertalia, simultaneous play from identical hands with rank-ordered booty, is a strong opponent-modelling game. It survives a cut to 7 simple characters and auto-assigned booty."
  },
  "variation": {
    "name": "Libertalia: Shared Hand",
    "summary": "Three pirates hold identical hands of 7 ranked characters. Each day a booty row is revealed, players talk, then all secretly play one character. High ranks grab the best booty, low ranks have tricks, and identical cards clash and get nothing. There are 2 campaigns of 5 days, and the highest doubloon total wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP: 3 players, each with a score of 0 doubloons. The game has 2 campaigns of 5 days (10 rounds). At the start of each campaign every player receives the same 7-card hand: ranks 1 to 7, one card of each rank. Cards played are removed from the owner's hand. The 2 cards left after day 5 are discarded unused, and a fresh full hand is dealt for campaign 2. Which cards each player has played is public once revealed.\n\nCHARACTERS:\n- Rank 1, Cabin Boy: takes no booty. Gains 3 doubloons.\n- Rank 2, Gunner: takes booty normally. Every other non-clashed player who played rank 6 or 7 loses 3 doubloons.\n- Rank 3, Quartermaster: takes booty normally. Gains 1 doubloon for each other non-clashed player who played a higher rank.\n- Rank 4, Bosun: takes booty normally. If the token taken is negative, it counts as 0.\n- Rank 5, Merchant: takes booty normally. Gains 2 extra doubloons if the token taken is worth 3 or more.\n- Rank 6, Captain: takes booty normally. No ability.\n- Rank 7, Admiral: takes booty normally. Pays a wage: loses 2 doubloons.\n\nBOOTY ROWS: each day one row is drawn at random, each equally likely, with replacement, from: A [5,3,1], B [5,1,-3], C [3,3,1], D [5,3,-3], E [3,1,-3], F [5,5,-3]. The values are the tokens, listed best to worst.\n\nEACH DAY (ROUND):\n1. Draw the booty row and announce it to all players.\n2. Talk: everyone writes one short message at the same time. All messages are then shown to everyone. Messages are not binding.\n3. All players secretly and simultaneously choose one card from their hand.\n4. Reveal all cards.\n5. Clash: if two or three players played the same rank, all of those players are clashed. They take no booty, their abilities do not fire, and their cards are still spent.\n6. Booty: non-clashed players other than the Cabin Boy are ordered by rank, highest first. The first takes the best token, the second the next, and so on. Tokens left over are discarded.\n7. Abilities of non-clashed characters resolve at the same time, as listed above. Gunner and Quartermaster count only non-clashed players.\n8. Each player adds their token value plus or minus their ability effects to their score.\n9. After day 5, discard leftover cards and deal fresh hands. After day 10, the game ends.\n\nThe Cabin Boy's +3 still applies when other players take booty. Scores can go negative.",
    "objective": "After 10 rounds, the player with the highest doubloon total wins. If two or more players share the highest total, they draw.",
    "expected_effect": "Every round is a read of two rivals choosing from known, shrinking hands. Players disagree about who gets the best token, and only one can. A player who follows a rival's talk ('I'm playing the Admiral') may walk into a clash or a Gunner shot, or concede the top token, so following can lose. Simple policies lose. Always-highest is predictable, so rivals clash it or Gunner it. Always-lowest wastes the Admiral and Captain late and gets the worst booty. The cursed rows (B, D, E, F) make the Bosun and the Cabin Boy valuable at the right moment. Because each card can be used only once per campaign, timing which day to spend the Admiral is a multi-round plan. The draw only changes what is worth doing, since all players face the same row with the same cards, so reads, not luck, decide the winner."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 2,
    "attributes": 17,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
