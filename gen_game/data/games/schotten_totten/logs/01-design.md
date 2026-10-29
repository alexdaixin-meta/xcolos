# 01 design

- time: 2026-10-27T17:08:29+00:00 (64.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 5a6d3a91c86df9df, reply sha256 acbe979a87573fbd

## Sent

````
Original game: Schotten Totten
Players in the original: 2 to 2

Original rules:
Two players contest nine Stone tiles in a line. 54 Clan cards (6 colors x values 1-9) are shuffled; each player draws 6 cards. On a turn, play one card from hand face-up to your side of any unclaimed Stone, max 3 cards per player per Stone, cards cannot move after placed, then draw one card if deck remains. After playing, you may claim any Stone where both sides have 3 cards, or claim early if you can prove opponent cannot beat you using only cards already on table. Strongest formation wins Stone in order: Straight Flush (same color consecutive values), Three of a Kind, Flush, Straight, High sum. Tie broken by higher sum, then by who completed 3 first. Claimed Stones are removed from play. First to claim 5 Stones total or 3 adjacent Stones wins immediately.
````

## Reply

````
```json
{
  "original_summary": "Schotten Totten is a two-player card game. Players lay cards from a hidden six-card hand onto their side of nine Stones in a line. Each side of a Stone is completed with three cards forming poker-like formations, the stronger formation claims the Stone, and the first player to 5 Stones or to 3 adjacent Stones wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "A thoughtless policy, such as always playing the lowest card to the leftmost open Stone, breaks up its own formations and loses most Stones to a player who builds flushes and straights. Neither seat has a clear edge: the first player has tempo, and the second sees one more card before committing. Every placement is permanent, so choices decide the outcome."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Card counting, managing the hand, and timing commitments to win the 'who completed first' tie-break all give experienced players a reliable edge. Draw luck matters within a single game, but six-card hands and nine Stones give many decisions that smooth it out."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still wins Stones with naturally strong hands. A strong player keeps gaining from tracking which cards are gone, from sacrificing Stones deliberately, and from forcing the opponent to spoil formations when they run out of safe plays."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the deck order are hidden. Players must infer what the opponent is holding back from the cards visible on the table, and plan which Stones to contest over many turns."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "Comparing formations at the end is arithmetic. The early-claim rule, which requires 'proving' the opponent cannot beat you, is an open-ended search over unseen cards, and the engine cannot check it simply."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only, but it breaks the platform limits in several ways. The '3 adjacent Stones' win depends on adjacency. Nine Stones with two sides each need 18 side attributes plus hands and deck, which exceeds the 20-attribute limit. Each round has two random draws, but only one is allowed. A full game takes about 50 or more turns, and the limit is 40 rounds."
    }
  ],
  "problems": [
    "The '3 adjacent Stones' victory depends on adjacency in a line, which is a spatial element the platform excludes.",
    "Nine Stones need 18 side attributes plus hands, deck and scores, which is more than 20 attributes.",
    "A round in which both players play and draw has two random draws, but the limit is one.",
    "A full game runs past 40 rounds.",
    "The early-claim 'proof' rule cannot be checked by simple arithmetic.",
    "Recognising formations is described in words and needs an exact arithmetic definition for the engine."
  ],
  "changes": [
    {
      "what": "Remove the adjacency win. The game is won by claiming 3 of the 5 Stones, which is a strict majority.",
      "why": "This keeps a 'first to a majority' race without any spatial relation.",
      "fixes": "The '3 adjacent Stones' victory depends on adjacency in a line, which is a spatial element the platform excludes."
    },
    {
      "what": "Use 5 Stones instead of 9, and a 36-card deck (4 colours x values 1-9) instead of 54 cards.",
      "why": "Ten Stone-side lists plus hands, deck and claim tracking fit within 20 attributes. The smaller deck keeps formations about as frequent relative to the number of Stones.",
      "fixes": "Nine Stones need 18 side attributes plus hands, deck and scores, which is more than 20 attributes."
    },
    {
      "what": "Make one round equal one player's turn. Players alternate, and each round has at most one draw.",
      "why": "This gives exactly one chance event per round.",
      "fixes": "A round in which both players play and draw has two random draws, but the limit is one."
    },
    {
      "what": "Fix the length at 30 rounds: 5 Stones x 3 cards x 2 players. The game can end earlier when someone reaches 3 Stones.",
      "why": "This keeps the game within 40 rounds.",
      "fixes": "A full game runs past 40 rounds."
    },
    {
      "what": "Remove early claims. A Stone is resolved automatically as soon as both sides hold 3 cards. The tie-break 'player who completed their side first' is kept and tracked with one attribute per Stone.",
      "why": "Every resolution becomes pure arithmetic, while the tempo element of the tie-break survives.",
      "fixes": "The early-claim 'proof' rule cannot be checked by simple arithmetic."
    },
    {
      "what": "Define formation strength numerically: strength = sum of values + a tier bonus. The bonus is 120 for a Straight Flush, 90 for Three of a Kind, 60 for a Flush, 30 for a Straight, and 0 otherwise.",
      "why": "The highest possible sum is 27, which is less than the 30-point gap between tiers. So the formula reproduces the original order exactly, and a single calculation compares two sides.",
      "fixes": "Recognising formations is described in words and needs an exact arithmetic definition for the engine."
    }
  ],
  "keeps": [
    "Two players lay cards from a hidden hand onto their own side of contested Stones.",
    "Each side of a Stone holds three permanent cards, scored in the original formation order: Straight Flush > Three of a Kind > Flush > Straight > High sum.",
    "The tie-break by higher sum and then by who completed first.",
    "A forced play every turn, so a player who runs out of good moves must spoil a formation.",
    "Drawing one card after each play while the deck lasts.",
    "Racing to claim a majority of the Stones."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Schotten Totten is inference from hidden hands, card counting and forced commitment. All of it survives when cut to 5 Stones, with alternating single turns and arithmetic Stone resolution, which fits the limits."
  },
  "variation": {
    "name": "Schotten Totten: Five Stones",
    "summary": "A compact two-player Schotten Totten. Players alternate placing one card from a hidden 6-card hand onto their side of one of 5 Stones. Each Stone is resolved arithmetically when both sides hold 3 cards, and the first to claim 3 Stones wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS: A deck of 36 cards, 4 colours (Red, Blue, Green, Yellow) x values 1-9, each card written like 'R7'. There are 5 Stones numbered 1-5. Each Stone has a side for Player A and a side for Player B, and each side holds at most 3 cards.\n\nSETUP: Shuffle the deck. Deal 6 cards face down to each player. Each hand is private: only its owner sees it. The remaining 24 cards form a face-down draw pile. Randomly decide which player is A; A takes the first turn.\n\nROUNDS: The game has at most 30 rounds. In odd rounds Player A is active; in even rounds Player B is active. Each round:\n(1) The engine announces to both players the cards on every side of every Stone, which Stones are claimed and by whom, each player's number of claimed Stones, and how many cards remain in the draw pile.\n(2) The active player chooses one card from their hand.\n(3) The active player chooses one Stone that is unclaimed and whose side for that player holds fewer than 3 cards. A player always has such a Stone and a card to play, and must play.\n(4) The card moves from the hand to that player's side of the chosen Stone, face up. Cards never move again.\n(5) If this card was the third card on that side and the other side has fewer than 3 cards, record this player as that Stone's 'first finisher'.\n(6) If the draw pile is not empty, the active player draws its top card into their hand.\n(7) For each unclaimed Stone where both sides now hold 3 cards, resolve it, as described below.\n(8) If either player has claimed 3 Stones, the game ends immediately and that player wins.\n\nSTRENGTH OF A SIDE: Let the three values sum to S. The side has one formation:\n- Straight Flush: all three cards share a colour, the values are all different, and highest minus lowest equals 2. Bonus 120.\n- Three of a Kind: all three values are equal. Bonus 90.\n- Flush: all three cards share a colour (and the side is not a Straight Flush). Bonus 60.\n- Straight: the values are all different and highest minus lowest equals 2 (and the side is not a Straight Flush). Bonus 30.\n- Otherwise: bonus 0.\nStrength = S + bonus.\n\nRESOLVING A STONE: The side with the higher strength claims the Stone. If the strengths are equal, the first finisher of that Stone claims it. A claimed Stone stays on the table with its cards visible, but it can no longer be played on.\n\nEND OF CARDS: After round 30 every Stone has been resolved. If no one has reached 3 Stones (possible only if the game has not yet ended), the player with more claimed Stones wins. Equal counts are a draw.",
    "objective": "The first player to claim 3 of the 5 Stones wins immediately. If the game reaches the end of round 30 without this, the player with more claimed Stones wins, and equal counts are a draw. With the first-finisher tie-break every resolved Stone has an owner, so in practice someone reaches 3.",
    "expected_effect": "Play keeps the original's tension. Players should hold strong partial formations back, count which values and colours are gone in order to judge whether an opponent's two-card start can still become a Straight Flush or Three of a Kind, and race to complete a side first so they win ties. The forced play every turn creates late-game squeeze: a player whose safe moves run out must dump cards onto Stones they are willing to concede, and choosing which Stones to give up becomes a key decision. Five Stones with a 3-Stone majority makes each Stone weighty, so sacrificing one Stone to secure two others is a real plan. The 6-card hand and alternating turns give enough decisions per game that skill outweighs the draw. Talk is omitted, because in a two-player zero-sum race it adds no reasoning beyond bluffing that the hidden hand already supplies."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 2,
    "attributes": 20,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
