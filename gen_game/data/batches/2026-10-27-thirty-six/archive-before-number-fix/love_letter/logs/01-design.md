# 01 design

- time: 2026-10-27T18:08:40+00:00 (80.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 176201f2ca8b9f89, reply sha256 58ed791d20bbdf83

## Sent

````
Original game: Love Letter
Players in the original: 2 to 4

Original rules:
Love Letter uses 16 cards ranked 1 Guard to 8 Princess with special effects. Shuffle the deck and burn one card face down unseen. In 2 players also reveal 3 cards face up as out of play. Each player gets one hidden card. On your turn draw one card then choose and discard one of your two cards face up in front of you, applying its effect even if harmful. Guard guesses an opponent's hand, Priest looks at a hand, Baron compares hands to eliminate loser, Handmaid protects you, Prince makes a player discard, King trades hands, Countess must be discarded if you also hold King or Prince, Princess eliminates you if discarded. If eliminated, reveal hand without effect. Round ends when one player remains or deck empties; then remaining players compare hands, highest wins tie by sum of discards. Winner gains a token of affection, and first player next round is previous winner. First game player is who was most recently on a date. First to 7 tokens in 2p, 5 in 3p, 4 in 4p wins.
````

## Reply

````
```json
{
  "original_summary": "Love Letter is a 2-4 player card game played over several hands with a 16-card deck ranked 1 (Guard) to 8 (Princess). Each turn a player draws a card, then discards one of their two cards and applies its effect, aiming to be the last player standing or to hold the highest card when the deck runs out. Each hand won earns a token, and the first player to a set number of tokens wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy dominates. 'Always discard the lower card' advertises that you hold the higher one, so Guards and Barons punish it. 'Always keep the high card' leaves you open to Guards, and Princess holders get Prince-targeted. The Countess and Princess rules create forced and harmful plays that need thought. Seat edge is small, but the rule that the previous winner starts next creates a mild snowball. The first player is chosen by 'who was most recently on a date', which an engine cannot decide."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "A single hand has a lot of luck: a blind Guard hit, or a Baron against an unknown hand. Over a match of several hands, card counting, tracking information, reading bluffs and choosing targets give the better player a clear but not overwhelming edge."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Beginners can play legally and win hands through draws. Strong players do Bayesian card counting from discards and the face-up removed cards. They track what each Priest and Baron revealed, deduce hands after a King swap, and time Handmaid and Baron plays. They also manage what their own discards reveal. The game is far from solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and one card is burned unseen, so every Guard guess, Baron challenge and Prince target is an inference about another player's card. Discards leak information, and players reason about what opponents believe they hold."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Eliminations, card comparisons, the tiebreak by discard sum, and token counts are all arithmetic. Only the first-player rule ('most recently on a date') needs a human judgement."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and card-based with no board. However, a full match (7 tokens in a 2-player game) can run well past 40 turns. The Prince's 'discard and draw' and the eight distinct card effects must be packed into a flat step list. Hand-end and match-end checks are fine as conditional steps."
    }
  ],
  "problems": [
    "P1: Match length. The first to 7, 5 or 4 tokens can need far more than 40 turns, which breaks the platform's round limit.",
    "P2: The starting player is chosen by a non-arithmetic real-world fact ('most recently on a date').",
    "P3: 'Previous hand winner starts next' gives a snowball advantage to whoever already leads.",
    "P4: Several rules are left implicit for an automated engine: what happens when every opponent is protected, whether a Guard may guess Guard, what the Prince does when the deck is empty, what happens if a player breaks the Countess rule, and how a full tie at hand end is resolved.",
    "P5: Single-hand luck is high, and table talk (a real part of the bluffing) is unstructured and not modelled."
  ],
  "changes": [
    {
      "what": "One platform round equals one player's turn, and the match is capped at 40 turns. Win targets are lowered to 3 tokens with 2 players and 2 tokens with 3-4 players. At the turn cap, the player with the most tokens wins; a tie for most is a draw, and an unfinished hand is void.",
      "why": "Keeps the match inside 40 rounds while still allowing several hands, so luck averages out somewhat.",
      "fixes": "P1: Match length"
    },
    {
      "what": "Seat 1 starts the first hand. Each later hand starts with the seat after the previous hand's starter, regardless of who won.",
      "why": "Gives an arithmetic, fair first-player rule and removes the leader's extra tempo.",
      "fixes": "P2 and P3: first-player rule and snowball"
    },
    {
      "what": "Edge cases are made explicit. A Guard cannot name Guard. If no legal target exists, the card is discarded with no effect. The Prince on an empty deck gives the target the burned card. If a player illegally keeps the Countess, the engine plays the Countess instead. A full tie at hand end gives every tied player a token.",
      "why": "Lets the game be built without a judge and keeps every outcome arithmetic.",
      "fixes": "P4: implicit rules"
    },
    {
      "what": "Before each turn, every player still in the hand writes one short message at the same time, and all messages are then shown to everyone.",
      "why": "Turns Love Letter's table bluffing into structured reasoning: claiming a card, steering Guards toward a rival, or ganging up on the token leader. Because only one player can win, claims are self-interested and must be read critically.",
      "fixes": "P5: luck and unmodelled bluffing"
    },
    {
      "what": "The token tiebreak and the private Priest and Baron reveals use private messages. All discards, and the cards revealed by eliminated players, are public and listed in the turn announcement.",
      "why": "Makes the information available for inference exact and the same for every player, which rewards card counting over memory errors.",
      "fixes": "P5: luck and unmodelled bluffing"
    }
  ],
  "keeps": [
    "The 16-card deck with its exact composition and all eight card effects, including the Countess restriction and the Princess self-elimination.",
    "One hidden card in hand, draw one card, discard one, and apply its effect.",
    "The burned face-down card, plus 3 face-up removed cards in the 2-player game.",
    "A hand ends when one player remains or the deck is empty. The highest card wins, with ties broken by the sum of discards.",
    "Tokens of affection across several hands decide the match."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Love Letter is already a compact hidden-information deduction game that fits turn-based text play. It needs a turn cap with lowered token targets, an arithmetic first-player rule, explicit edge cases and structured talk, not a redesign."
  },
  "variation": {
    "name": "Love Letter: Sealed Court",
    "summary": "Classic Love Letter played turn by turn for at most 40 turns. Players race to 3 tokens (2 players) or 2 tokens (3-4 players), the starting seat rotates each hand, and before every turn all players at the table make one simultaneous public statement.",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "rules": "CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess. Seats are numbered 1 to N in a fixed order.\n\nSTARTING A HAND: Shuffle all 16 cards. Remove the top card face down; this is the burned card, which nobody sees. In a 2-player game, also remove the next 3 cards face up so that all players see them. Deal one card face down to each player as their hand. All players are back in the hand, nobody is protected, and every player's discard pile is empty. Seat 1 starts the first hand. Each later hand starts with the seat after the previous hand's starting seat, wrapping from N back to 1.\n\nTURNS: Each platform round is one turn by the active player. Play passes in seat order, skipping players eliminated from the current hand. A turn goes as follows.\n(1) TALK: every player still in the hand writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages bind nobody and may be false.\n(2) The active player loses any Handmaid protection from their own previous turn.\n(3) The active player draws the top card of the deck and now holds two cards, which only they can see.\n(4) PLAY: the active player chooses one of their two cards to discard face up onto their discard pile. If they hold the Countess together with the King or the Prince, they must discard the Countess; if they choose otherwise, the Countess is discarded instead. The Princess may be chosen, and doing so eliminates the player.\n(5) TARGET: if the card needs a target, the active player names one other player who is still in the hand and not protected. For the Guard they also name a card number from 2 to 8. The Prince may instead target the active player. If no legal target exists, the card has no effect.\n(6) EFFECT:\n- Guard (1): if the target's card equals the named number, the target is eliminated.\n- Priest (2): the target's card is shown privately to the active player.\n- Baron (3): the active player and the target privately show each other their cards. The lower card's holder is eliminated; on a tie nothing happens.\n- Handmaid (4): the active player cannot be targeted until the start of their next turn.\n- Prince (5): the target discards their card face up without applying its effect. If that card is the Princess, they are eliminated. Otherwise they draw the top card of the deck, or take the burned card if the deck is empty.\n- King (6): the active player and the target swap the cards in their hands.\n- Countess (7): no effect.\n- Princess (8): the active player is eliminated.\nAn eliminated player reveals their hand card face up onto their discard pile, with no effect, and takes no further part in this hand.\n(7) ANNOUNCE: everyone is told the card discarded, the target and guess (if any), every elimination and the revealed cards, and how many cards remain in the deck.\n\nEND OF A HAND: A hand ends immediately when only one player remains in it, and that player wins the hand. It also ends at the end of a turn in which the deck becomes empty. In that case, the remaining players reveal their cards: the highest card wins. If several players tie for the highest card, the one with the largest sum of discarded card values wins. If they are still tied, every tied player wins. Each winner of the hand gains 1 token. A new hand then starts on the next turn.\n\nMATCH END: The match ends as soon as a player reaches the token target at the end of a hand: 3 tokens with 2 players, 2 tokens with 3 or 4 players. It also ends after turn 40. A hand in progress at turn 40 is void and gives no tokens.",
    "objective": "A player who reaches the token target (3 tokens with 2 players, 2 tokens with 3-4 players) wins. If two or more players reach it at the end of the same hand, the match is a draw among them. If turn 40 ends first, the player with the most tokens wins, and a tie for the most tokens is a draw.",
    "expected_effect": "Play keeps Love Letter's core: card counting from public discards and the face-up removed cards, inferring hands from Priest and Baron reveals and King swaps, and choosing Guard guesses and Baron challenges by probability. Rotating the starting seat removes the leader's extra tempo, and the shortened targets fit several hands into 40 turns, so one lucky Guard hit decides less. Talk passes both tests. Only one player can win, so players disagree about whom the Guards and Barons should hit. Each player wants attacks aimed at someone else, especially at the token leader, and wants to bluff about their own card ('I'm holding the Princess', 'I just Priested seat 3; they have a Guard'). A player who simply follows a proposal can lose. They may waste a Guard on a false claim, attack a player who is not the real threat and leave the leader free, or reveal their own card through what they say. Strong players must test claims against the card count, and must decide when a true statement helps them more than a bluff."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 3,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
