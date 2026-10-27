# 03 design

- time: 2026-10-27T20:44:18+00:00 (110.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 7575881191e394e3, reply sha256 4575c76539eaf29d

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: There is real inference:
- reading the 3 revealed cards and the public discards;
- Priest then Guard for a certain kill;
- timing a Baron only with a high card;
- inferring a held Princess from a player who keeps a card;
- King-swap reads.

But chance dominates for three reasons.

1. The Princess is in play in 10/14 of hands. Its holder wins every Baron and every showdown. With the Prince removed, the only counters are a correct Guard guess of 8 or the single King. A blind 8-guess hits about 1/9 per Guard, and there are 5 Guards, some burned or revealed. So the player dealt or drawing the Princess wins that hand an estimated 65–75% of the time regardless of skill. In the 4/14 of hands without the Princess, the Countess or King plays a similar role.
2. Single-card hands, 4 draws each, and Guard guesses at 2/9 to 1/9 make each hand roughly 60–70% draw-determined. My estimate is that a strong player wins about 55–60% of hands against a weak one.
3. The match is cut from first-to-7 (original 2p) to first-to-3, at most 5 decisive hands. A 57% per-hand edge becomes only about 60–62% in a best-of-5.

If both play the intended strategy (keep high cards, Priest then Guard, Baron only when high), the hand usually goes to whoever is dealt or draws the Princess, so the deal decides. The better reasoner is not clearly favoured, and chance alone often decides the match.
- change: Restore Prince-type counterplay to the Princess. Replace one Guard with a Prince (rank 5, if the opponent is not protected: the opponent discards their card without effect and takes the burned card, and discarding the Princess this way eliminates them). Extend the Countess rule to 'King or Prince'. This gives a sensible player a way to beat a dealt Princess.
- change: Lengthen the match within the 40-turn cap. Raise the target to 4 tokens, and remove 4 cards face up instead of 3 so the deck holds 7 cards (hands of at most 7 turns, typically about 4–5 because of eliminations). Keep the existing cap resolution: deck-empty showdown, then more tokens wins, equal tokens is a draw.
- change: Correct the false claim that the 40-turn cap cannot be reached. State that no-token hands or long hands can reach it, and that the cap rule then decides.
- change: Optional, to reward inference over the deal: award 2 tokens instead of 1 for a hand won by a correct Guard guess, with the target raised accordingly, so reading the opponent counts for more than holding the top card at showdown.
The variation that was reviewed: Love Letter: Heads-Up: CARDS (14):
- 5 Guard (rank 1)
- 2 Priest (rank 2)
- 2 Baron (rank 3)
- 2 Handmaid (rank 4)
- 1 King (rank 6)
- 1 Countess (rank 7)
- 1 Princess (rank 8)

STARTING A HAND:
1. Gather all 14 cards and shuffle them.
2. Set the top card aside face down. Nobody sees it, and it takes no part in the hand.
3. Reveal the next 3 cards face up as out of play. Everyone sees them.
4. Deal 1 card face down to each player as their hand. 8 cards remain in the draw deck.
5. Clear both players' protection, elimination and discard piles.
6. Starting player: in hand 1 it is chosen at random. In later hands it is the player who lost the previous hand. If the previous hand gave no token, it is the player who did not start the previous hand.

A TURN (players alternate, starting with the starting player):
1. If the active player is protected, their protection ends now.
2. The active player draws the top card of the deck, so they hold 2 cards. Only they see their cards.
3. The active player chooses one of their 2 cards to discard face up. Discards are public, and their ranks are added to that player's discard sum.
   - If they hold the Countess together with the King, they must discard the Countess.
   - They may discard the Princess, but then they are eliminated.
4. The discarded card's effect applies:
   - Guard: if the opponent is not protected, the active player names one rank other than 1 (2, 3, 4, 6, 7 or 8). If the opponent's card has that rank, the opponent is eliminated.
   - Priest: if the opponent is not protected, the active player privately sees the opponent's card.
   - Baron: if the opponent is not protected, both players privately see each other's card. The player with the lower rank is eliminated. On equal ranks nothing happens.
   - Handmaid: the active player is protected until the start of their next turn. Cards discarded by the opponent have no effect on a protected player.
   - King: if the opponent is not protected, the two players swap their hand cards.
   - Countess: no effect.
   - Princess: the active player is eliminated.
5. The discard and its public outcome are announced: the guess named, whether someone was eliminated, whether a swap happened. The cards seen privately through a Priest or Baron are not announced, except that an eliminated player's card is revealed.

END OF A HAND:
- If a player is eliminated, the other player wins the hand.
- Otherwise, if the deck is empty at the end of a turn, both players reveal their cards and the higher rank wins the hand.
- If the ranks are equal, the higher discard sum wins the hand.
- If the discard sums are also equal, nobody wins the hand.
- The hand's winner gains 1 token.
- If the game has not ended, a new hand starts as described above.

END OF THE GAME:
- The first player to reach 3 tokens wins at once.
- There is a hard cap of 40 turns, which cannot be reached in normal play because a hand lasts at most 8 turns and the match at most 5 hands. If the cap is reached anyway, any hand in progress is resolved as if the deck were empty. Then the player with more tokens wins, and equal tokens is a draw. Winner: The first player to hold 3 tokens wins. If the 40-turn cap is reached first, the player with more tokens wins, and equal tokens is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2–4 player card game with a 16-card deck ranked 1 (Guard) to 8 (Princess). Each player holds one hidden card, draws a second each turn and discards one for its effect: guessing, peeking, comparing, protecting, forcing a discard or swapping. The last player standing, or the highest card when the deck runs out, wins a token, and first to a set number of tokens wins the match. The variation reviewed here is a 2-player, 14-card version with no Princes, played first to 3 tokens.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No fixed policy wins outright. 'Always discard the lower card' loses to Guard guesses and Barons, and 'always Baron' loses when holding low. But the previous variation removed both Princes, so a dealt Princess has almost no counter. The 'policy' of having been dealt the Princess wins about 65–75% of hands. The starting player was also tied to the previous result, so a hand's outcome carried into seat order."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Single-card hands, about 4 draws each, and blind Guard guesses at 1/9 to 2/9 make each hand roughly 60–70% decided by the draw. The estimated per-hand edge of a strong player is about 55–60%. A first-to-3 match (at most 5 hands) turns that into only about 60% for the match."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "There are real skills: counting the revealed and discarded cards, Priest then Guard, timing the Baron, reading a held card. But every hand is worth the same single token, so a player who reads the situation perfectly gains no more from a hand they understand well than from one they are guessing in. Skill has no way to grow its payoff."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hidden hands, a burned card and private Priest/Baron information mean players must infer the opponent's card from the visible cards, the discards and what the opponent chooses to keep."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, rank comparisons, discard sums and token counts are all arithmetic. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based, text-only and uses hidden hands, so it fits. But it falsely claimed the 40-turn cap could not be reached. Hands of up to 8 turns across up to 5 hands can exceed 40 turns, so the length was never guaranteed."
    }
  ],
  "problems": [
    "P1: The Princess has too few counters. With no Prince, a dealt or drawn Princess wins most hands whatever the skill of either player.",
    "P2: Every hand is worth exactly 1 token, so a skilled player cannot win big when the read is clear and lose small when the card is weak. Card luck is passed straight into the score.",
    "P3: The match is too short (first to 3, at most 5 hands), so a modest per-hand edge barely shows in the result.",
    "P4: The length claim was false. Long hands or no-token hands could hit the 40-turn cap partway through the match.",
    "P5: The starting seat depended on the previous hand's result, which adds a small, uncontrolled carry-over from luck."
  ],
  "changes": [
    {
      "what": "Restore the original 16-card deck, including 2 Princes (rank 5). A Prince makes a chosen player (yourself, or an unprotected opponent) discard their card without its effect and draw a replacement; a Princess discarded this way eliminates its holder. The Countess must be discarded if held with the King or a Prince.",
      "why": "Five Guards plus two Princes give a thinking player real ways to beat a Princess holder. This brings back the original game's balance of counters.",
      "fixes": "P1"
    },
    {
      "what": "Add an affection stake. After seeing their dealt card, both players secretly and simultaneously choose a stake of 1, 2 or 3. The stakes are then revealed, and the hand's winner gains tokens equal to the sum of both stakes.",
      "why": "Card luck becomes a sizing decision, as in poker: stake high on strength, low on weakness, or bluff. A revealed stake is also a signal to read. A stake of 3 invites a Guard guess of 8 or a Prince, so a Princess holder must hide by staking modestly. Skill now changes how many tokens move, not only who wins the hand.",
      "fixes": "P2"
    },
    {
      "what": "Reveal 5 cards face up as out of play instead of 3, which leaves 8 cards to draw (hands of at most 8 turns). Replace first-to-N with a fixed-length match: a new hand starts only while fewer than 32 turns have been played, and when a hand ends at 32 or more turns, the game ends. The higher token total wins.",
      "why": "This gives about 6–8 hands with stakes, instead of at most 5 one-token hands, so the skilled player's edge accumulates. It also guarantees the match ends by turn 39, inside the 40-turn limit. More revealed cards also give more to count.",
      "fixes": "P3, P4"
    },
    {
      "what": "The starting player alternates strictly: random for hand 1, then the other player each hand.",
      "why": "Seat order is balanced and no longer depends on the last hand's result.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "The original 16-card deck and its eight card effects, including the Countess rule and Princess self-elimination",
    "Draw one, discard one, with the effect applied even if it hurts you",
    "A burned unseen card, plus face-up cards out of play in 2-player games",
    "Showdown by highest rank, ties broken by discard sum",
    "Tokens of affection as the score"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core is strong and fits the platform. Luck can be brought down to size with restored counters, stake sizing that rewards reading the situation, and a longer, fixed-length match, all within the limits."
  },
  "variation": {
    "name": "Love Letter: Sealed Stakes",
    "summary": "Heads-up Love Letter with the full 16-card deck. Before each hand, both players secretly stake 1–3 tokens of affection on it, and the hand's winner takes the sum of both stakes. The match runs about 6–8 hands, and the higher token total wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS (16):\n- 5 Guard (rank 1)\n- 2 Priest (rank 2)\n- 2 Baron (rank 3)\n- 2 Handmaid (rank 4)\n- 2 Prince (rank 5)\n- 1 King (rank 6)\n- 1 Countess (rank 7)\n- 1 Princess (rank 8)\n\nBoth players start the match with 0 tokens. Token totals are always public. The match counts turns played.\n\nSTARTING A HAND (happens whenever a new hand begins):\n1. Shuffle all 16 cards.\n2. Burn the top card: set it aside face down, unseen by anyone.\n3. Reveal the next 5 cards face up as out of play. Both players see them.\n4. Deal 1 card face down to each player as their hand. 8 cards remain in the draw deck.\n5. Clear both players' protection, elimination flag, discard pile and discard sum.\n6. Starting player: in hand 1 it is chosen at random. In each later hand it is the player who did not start the previous hand.\n7. STAKE: each player looks at their own card. Both then choose, at the same moment and in secret, a stake of 1, 2 or 3. The two stakes are revealed to both players. The pot for this hand is stake A plus stake B, so it is between 2 and 6.\n\nA TURN (players alternate, beginning with the starting player; every turn adds 1 to the turn count):\n1. If the active player is protected, their protection ends now.\n2. The active player draws the top card of the deck and now holds 2 cards. Only they see them.\n3. The active player chooses one of their 2 cards to discard face up. The card's rank is added to their discard sum.\n   - If one of the 2 cards is the Countess and the other is the King or a Prince, they must discard the Countess.\n   - They may discard the Princess, but that eliminates them.\n4. The discarded card's effect applies:\n   - Guard: if the opponent is not protected, name one rank from 2 to 8. If the opponent's card has that rank, the opponent is eliminated.\n   - Priest: if the opponent is not protected, the active player privately sees the opponent's card.\n   - Baron: if the opponent is not protected, both players privately see each other's card. The lower rank is eliminated. Equal ranks: nothing happens.\n   - Handmaid: the active player is protected until the start of their own next turn. While a player is protected, the opponent's discards have no effect on them.\n   - Prince: choose a player, either yourself or the opponent. You may choose the opponent only if they are not protected. The chosen player discards their hand card face up without its effect, and its rank is added to their discard sum. If that card is the Princess, they are eliminated. Otherwise they draw the top card of the deck, or take the burned card if the deck is empty.\n   - King: if the opponent is not protected, the two players swap hand cards.\n   - Countess: no effect.\n   - Princess: the active player is eliminated.\n5. Announce publicly: the card discarded, any rank named, any Prince target and the card it discarded, any elimination together with the eliminated player's card, and whether a swap happened. Cards seen privately through a Priest or Baron are not announced.\n\nEND OF A HAND (checked at the end of every turn):\n- If a player is eliminated, the other player wins the hand.\n- Otherwise, if the deck is empty, both players reveal their cards. The higher rank wins. If the ranks are equal, the higher discard sum wins. If the sums are also equal, nobody wins the hand.\n- The winner of the hand gains tokens equal to the pot. If nobody wins, no tokens are given.\n\nEND OF THE MATCH:\n- When a hand ends, if fewer than 32 turns have been played in total, a new hand starts.\n- If 32 or more turns have been played, the match ends.\n- A hand lasts at most 8 turns, so the match always ends by turn 39.",
    "objective": "When the match ends, the player with more tokens wins. Equal token totals are a draw.",
    "expected_effect": "The Princess is no longer an automatic winner. With 5 Guards and 2 Princes, and a stake that can betray a strong card, the holder must disguise it: a stake of 3 invites a Guard guess of 8 or a Prince, so strong hands are often staked at 2, and bluff stakes of 3 on weak cards become possible. Reading the opponent's stake, counting the 5 revealed cards and the discards, and sizing your own stake decide how many tokens move each hand. A weaker player stakes mechanically and loses the large pots. Over 6–8 hands with pots of 2 to 6, the skill edge should accumulate much more than in the earlier first-to-3 format. Some per-hand card luck remains, as in the original, but sizing lets good play limit losses on bad deals. Every simple policy can lose. 'Always stake 3' exposes strong hands and pays out large pots on weak ones. 'Always stake 1' wins little when holding strength. 'Always discard the lower card' loses to Guards and Barons."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
