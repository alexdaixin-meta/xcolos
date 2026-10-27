# 04 design

- time: 2026-10-27T17:36:08+00:00 (54.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 edfc9ee0475ac731, reply sha256 00a81fe3b5deeee2

## Sent

````
Original game: Red7
Players in the original: 2 to 4

Original rules:
49 cards numbered 1-7 in seven spectrum colors Red Orange Yellow Green Blue Indigo Violet. Value beats color. Each player has a 7-card hand and a 1-card Palette. A Canvas card shows the current win rule. Red = highest card. Orange = most of one number. Yellow = most of one color. Green = most even cards. Blue = most different colors. Indigo = longest run. Violet = most cards below 4. Player left of current best starts. On your turn you must be winning by the Canvas rule at turn end. You may: play one card to your Palette, or discard one card to Canvas to change the rule (must be winning new rule after), or play to Palette then discard to Canvas (must be winning after). If you cannot or choose not to, you are eliminated. Last remaining player wins the round. With advanced scoring, winner banks Palette cards that satisfy the final rule as points; game ends when deck too small to deal.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: WINNER RULE CHECK, 2 players. Each hand gives the survivor 2 points and the other player 1, because the last eliminated player is always the loser. After k hands, if A has won a of them, the scores are A = k + a and B = 2k - a. So the score gap is simply hands won minus hands lost. No one can reach 6 points before hand 3. k=3 with a=3 or a=0 is a sweep, 6-3, and the match is decided. k=3 with a=1 or a=2 gives 4-5 or 5-4, so a 4th hand is played. In hand 4, a=3 gives 7-5 and a=1 gives 5-7, both decided. a=2 gives 6-6, a DRAW. Between equal players (p=0.5 per hand): P(sweep) = 2 x 1/8 = 0.25 and P(2-1 split) = 0.75. The 4th hand then draws whenever the trailing player wins it, so P(draw) = 0.75 x 0.5 = 0.375. With p=0.6 for the stronger player: P(sweep) = 0.216 + 0.064 = 0.28. P(strong leads 2-1) = 0.432, then a draw with probability 0.4, giving 0.173. P(weak leads 2-1) = 0.288, then a draw with probability 0.6, giving 0.173. So P(draw) is about 0.35. In 2 players the 1-point consolation does nothing except force a draw on every 2-2 split, so about a third of matches have no winner. THOUGHTLESS POLICIES: Always fold: eliminated on the first turn of every hand, scoring 1 against 2 each hand, so it always loses. Always play your strongest card under the current rule and never switch: it wastes high cards, and an opponent who switches the rule eliminates it (example below). It does not win or draw almost always. Always option (c): it burns two cards per turn. In an attrition game where each turn costs at least one card, it runs out first and loses. NO DOMINANT OPTION. Example: P's palette is 7V (Red key 71) and Q's is 2G. Q can discard a Green card to make the rule Green, giving Q a key of 122 against P's 0. P can answer by playing 6R, for a Green key of 163. Rule switches and card conservation are real trade-offs. SEAT AND ORDER: the non-leader acts first and spends cards first, so the leader has some tempo. But the leader is set by the dealt palette card, not by seat, so no seat has a fixed edge. In 3 players the 2/1/0 split rewards finishing order and works. The failure is the 2-player draw structure.
- change: Fix the 2-player draw structure. Option 1: in 2 players the hand winner scores 1 point, the loser scores 0, and the match goes to the first player with 3 points, so the match can never end on a 2-2 tie. Option 2: keep the 6-point target but break a tie for the most points in favour of the player who won the most recent hand.
The variation that was reviewed: Red3: CARDS. 21 cards: numbers 1 to 7 in each of three colours, Red, Green and Violet. Colour rank is Red 3, Green 2, Violet 1. Every card has a strength of number x 10 + colour rank (for example, 7 Red = 73 and 4 Violet = 41). A higher strength beats a lower one, so the number decides first and the colour breaks ties. A card is EVEN if its number is 2, 4 or 6. A card is LOW if its number is 1, 2 or 3.

RULES ON THE CANVAS. The Canvas shows one colour, and that colour is the current rule. Each living player has a KEY under the current rule:
- Red: key = strength of the highest card in your palette.
- Green: key = 100 x (number of even cards in your palette) + strength of your highest even card. The key is 0 if you have no even cards.
- Violet: key = 100 x (number of low cards in your palette) + strength of your highest low card. The key is 0 if you have no low cards.
You are LEADING if your key is strictly higher than every other living player's key. Because every card is unique, two non-zero keys can never be equal.

SETUP OF A HAND. Shuffle all 21 cards. Deal each player 5 cards as a hidden hand, then deal each player 1 card face up as the start of their palette. The remaining cards are set aside unseen. The Canvas starts as Red. All players are alive. The initial leader is the player with the highest palette card. The first turn goes to the next player in seat order after the leader.

A TURN. On your turn you choose exactly one of:
(a) play one card from your hand face up to your palette;
(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour (the card leaves play);
(c) do (a) and then (b), with two different cards;
(d) fold.
After your action, keys are recomputed under the current rule. If you are not leading, or you folded, or you named a card you do not hold, you are eliminated. Your palette stays visible but no longer counts. Play then passes to the next living player in seat order.

A ROUND is one pass of turns through every player in seat order, beginning with the player whose turn it is. Players already eliminated are skipped.

END OF A HAND. A hand ends the moment only one player is alive. That player scores 2 points. The player eliminated last in that hand (the one whose elimination left a single survivor) scores 1 point. Any others score 0. If the match is not over, a new hand is set up as above, starting at the next round.

END OF THE MATCH. After a hand ends, the match ends if any player has 6 or more points. The match also ends when round 40 is complete; a hand still unfinished at that point scores nothing.

INFORMATION. Palettes, the Canvas, all eliminations and all points are public. Hands and the set-aside cards are hidden. There is no table talk. Winner: When the match ends, the player with the most points wins. If two or more players share the most points, the match is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Red7 is a card-shedding survival game. Each turn a player adds a card to their face-up palette and/or changes the rule card that decides who is 'winning', and must be winning after their turn or be eliminated. The last player standing wins the hand. The reviewed variation, Red3, cut it to 21 cards, 3 colours, 3 rules and a points match to 6.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The card play in Red3 holds up against simple policies. Always-fold loses every hand. Always-play-strongest-and-never-switch loses to a rule switch: P has 7V (Red key 71) against Q's 2G, Q discards a Green card and leads 122 to 0. Always option (c) burns two cards a turn and runs out first. The leader is fixed by the dealt card, not the seat. The flaw is the 2-player scoring. Survivor 2 and last-eliminated 1 means the gap is just hands won minus hands lost, so every 2-2 split ends 6-6. That draws about 37% of matches between equals and about 35% at p=0.6."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Within a hand, card conservation and timing of rule switches decide survival, so skill shows. Over a 2-player match, though, a third of results are draws whatever the skill gap. At p=0.6 the stronger player wins only about 45% of matches outright. Each individual hand also carries real deal luck: the dealt palette fixes the first leader and the 5-card hand matters."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Strong play involves several things: holding high cards back, inferring opponents' hands from the unseen cards (21 cards, at most 18 dealt), switching to a rule the opponent cannot answer, and keeping enough cards to outlast them. A weak player still wins some hands through the deal."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the set-aside cards are hidden. Whether a switch to Green is safe depends on whether the opponent likely holds an even card that beats your key. That must be inferred from the cards visible in palettes and on the canvas, and from how the opponent has chosen to spend cards so far."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Keys are arithmetic on public palette cards, eliminations are mechanical and points are counted. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is turn-based text with hidden hands, one shuffle per hand and a 40-round cap. Each turn costs at least one card, so a hand lasts at most 6 rounds. The 21-card deck supports 2 or 3 players: 4 players would need 24 dealt cards, which the original's '2 to 4' cannot cover."
    }
  ],
  "problems": [
    "In 2 players the 2/1 hand scoring makes the score gap equal hands won minus hands lost, so any 2-2 split reaches 6-6 and the match is a draw (about 35-37% of matches).",
    "The 1-point consolation is meaningless in 2 players, because the loser of a hand is always the last eliminated.",
    "In 3 players a tie for most points at or above 6 (for example a hand winner going 4 to 6 while the runner-up goes 5 to 6) ends in a draw, and a tie at the round-40 cap also gives no winner.",
    "The stated player range must match the deck: 4 players cannot be dealt from 21 cards."
  ],
  "changes": [
    {
      "what": "In 2-player matches, a hand winner scores 1 point and the loser 0. The first player to 3 points wins (best of five hands).",
      "why": "An odd number of hands is needed to decide, so 2-2 can never end the match. A fifth hand always settles it, and the useless consolation point disappears.",
      "fixes": "In 2 players the 2/1 hand scoring makes the score gap equal hands won minus hands lost, so any 2-2 split reaches 6-6 and the match is a draw (about 35-37% of matches)."
    },
    {
      "what": "The 1-point consolation for the last-eliminated player applies only in 3-player matches.",
      "why": "Finishing order genuinely varies in 3 players and is worth fighting for there. In 2 players it adds nothing.",
      "fixes": "The 1-point consolation is meaningless in 2 players, because the loser of a hand is always the last eliminated."
    },
    {
      "what": "In 3 players, a tie for most points is broken in favour of the tied player who won the most recently completed hand. This applies both at the 6-point end and at the round-40 cap.",
      "why": "Each hand has exactly one survivor, so 'most recent hand winner' always picks out one player. It also rewards closing out the deciding hand.",
      "fixes": "In 3 players a tie for most points at or above 6 (for example a hand winner going 4 to 6 while the runner-up goes 5 to 6) ends in a draw, and a tie at the round-40 cap also gives no winner."
    },
    {
      "what": "The player count is fixed at 2 or 3.",
      "why": "The deal of 5 hidden cards plus 1 palette card per player needs 12 or 18 of the 21 cards. That always leaves some cards unseen, which keeps inference alive.",
      "fixes": "The stated player range must match the deck: 4 players cannot be dealt from 21 cards."
    }
  ],
  "keeps": [
    "Must be leading at the end of your own turn or be eliminated.",
    "Value beats colour: strength = number x 10 + colour rank.",
    "Discarding to the Canvas changes the rule, and play-then-discard is allowed.",
    "Three of Red7's rules: highest card, most evens, most cards below 4.",
    "Hidden hands, public palettes, last player standing wins the hand.",
    "A multi-hand match scored by hands survived."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The card play already rewards inference and planning. Only the match-scoring structure produced draws, and that is fixed with arithmetic winner rules inside the limits."
  },
  "variation": {
    "name": "Red3 Duel",
    "summary": "A 21-card, 3-colour Red7 for 2 or 3 players. You must lead under the current rule after your own turn, and you may change the rule by discarding. The match is first to 3 hands in a duel, or first to 6 points with a recent-winner tiebreak in 3 players, so every match has a winner.",
    "players": {
      "min": 2,
      "max": 3,
      "suggested": 2
    },
    "rules": "CARDS. There are 21 cards: numbers 1 to 7 in each of three colours, Red, Green and Violet. Colour rank is Red 3, Green 2, Violet 1. A card's strength is number x 10 + colour rank (7 Red = 73, 4 Violet = 41). Higher strength beats lower. A card is EVEN if its number is 2, 4 or 6. A card is LOW if its number is 1, 2 or 3.\n\nTHE RULE. The Canvas shows one colour, which is the current rule. Each living player has a KEY under the current rule:\n- Red: key = strength of the highest card in your palette.\n- Green: key = 100 x (number of even cards in your palette) + strength of your highest even card, or 0 if you have no even card.\n- Violet: key = 100 x (number of low cards in your palette) + strength of your highest low card, or 0 if you have no low card.\nYou are LEADING if your key is strictly higher than every other living player's key. If keys tie, including at 0, no tied player is leading.\n\nSETUP OF A HAND. Shuffle all 21 cards. Deal each player 5 cards as a hidden hand, then 1 card face up as their palette. The remaining cards (9 with 2 players, 3 with 3 players) are set aside unseen for this hand. The Canvas starts as Red. Everyone is alive. The initial leader is the player whose palette card has the highest strength. The first turn of the hand goes to the next player in seat order after that leader.\n\nA TURN. On your turn choose exactly one:\n(a) play one card from your hand face up to your palette;\n(b) discard one card from your hand to the Canvas, so the rule becomes that card's colour and the card leaves play;\n(c) do (a), then (b), with two different cards;\n(d) fold.\nThen recompute keys under the current rule. If you are not leading, or you folded, or you named a card you do not hold, you are eliminated. Your palette stays visible but no longer counts. If you have no cards left in hand when your turn comes, you can only fold. Play passes to the next living player in seat order.\n\nA ROUND is one pass of turns through all living players in seat order, starting with the player whose turn it is.\n\nEND OF A HAND. A hand ends the moment only one player is alive. That player is the hand winner.\n- With 2 players: the hand winner scores 1 point; the other scores 0.\n- With 3 players: the hand winner scores 2 points; the player whose elimination left one survivor scores 1; the first player eliminated scores 0.\nThe engine records the hand winner as the MOST RECENT HAND WINNER. If the match is not over, a new hand is set up at the start of the next round.\n\nEND OF THE MATCH.\n- With 2 players, the match ends when a player reaches 3 points.\n- With 3 players, the match ends after any hand in which a player reaches 6 or more points.\n- In either case, it also ends when round 40 is complete; an unfinished hand then scores nothing.\n\nINFORMATION. Palettes, the Canvas, eliminations, points and the most recent hand winner are public. Hands and set-aside cards are hidden. There is no table talk.",
    "objective": "The player with the most points when the match ends wins. With 2 players this is the first to 3 points, and a tie cannot occur at that end. If two or more players share the most points, which can happen in 3 players or at the round-40 cap, the tied player who won the most recently completed hand wins. If no hand was completed at all, the match is a draw.",
    "expected_effect": "Draws in 2-player matches go from about 35% to essentially 0. With p=0.6 per hand, the stronger player now wins the best of five about 68% of the time instead of about 45% outright. Every hand matters to the end, and hand 5 is a true decider. In 3 players the recent-winner tiebreak removes draws and makes winning the deciding hand worth more than limping into second. Talk is left out: play is sequential and hidden-hand inference is the core skill, so cheap, unenforceable claims would add steps without adding a real decision. Within a hand, play is unchanged: players weigh when to spend high cards, infer from visible and discarded cards what opponents can answer, and switch rules to strand them."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 3,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
