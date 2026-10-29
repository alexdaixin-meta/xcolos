# 23 design

- time: 2026-10-27T17:59:02+00:00 (60.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 0829909e785eed33, reply sha256 cafdd73f3cc874f5

## Sent

````
Original game: Cuttle
Players in the original: 2 to 2

Original rules:
Two players share a standard 52-card deck. Deal 6 cards to dealer and 5 to opponent, rest is draw pile; scrap pile is face-up discard showing top only. On your turn do exactly one: draw one card, or play one card from hand. Number cards A,2-10 can be point cards worth their value (A=1) placed on your side; first to 21+ points wins, but kings reduce requirement to 14/10/7/5 for 1-4 kings you control. A point card can also scuttle: play a higher rank, or equal rank with higher suit C<D<H<S, to discard both cards. Cards  A,2-7,9 can be one-offs discarded after use for effects like wipe points, destroy permanents, recover from scrap, force opponent discard 2, draw 2, play top of deck immediately, bounce a permanent. 8,J,Q,K are permanents staying on table: 8 forces opponent to reveal hand, J stacked on a point card steals it, Q protects your other points/permanents from single-target effects, K lowers win threshold. 2 can be played on opponent's turn to counter a one-off. If draw pile empty you may pass; three passes ends game with no winner.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Limits stated: steps 14, choice steps 3, hidden elements 3 (hands, exact point piles, draw pile), random draws 1 (DRAW), rounds 40. All are within limits, except that the attribute claim of 20 does not hold up.

Minimal stored state:
- Per player (×2 = 18): hand, point_pile, points, king_count, won, is_first, threshold, shortfall, point_pile_view.
- Shared: draw_pile, scrap_pile, turn.
That totals 21, already over 20, before hand_count, base, or a record of the announced exact rank after a failed scuttle. The rules require that announcement to be visible to both players, yet the VISIBILITY section keeps exact point cards private, so it needs its own stored public attribute.

Ambiguities a model cannot resolve from the text:
1. 'Target position' has no stated indexing (0- or 1-based).
2. It is not stated whether positions shift after a scuttle removes a card or a Jack moves one, or how a previously announced rank stays attached to its card after shifting.
3. point_pile_view needs a per-card rank-to-band map with no stated operation. With a flat step list and no lookup, mapping a variable-length list may not fit in 14 steps.

Other checks:
- Turn-41 handling is defined.
- Two players, so no talk is needed; this is fine.
- No board, judge, or clock is required.
- The game is finite and decided by arithmetic, but it is not specifiable within the attribute limit as written.
- change: Bring stored attributes to 20 or fewer and list them explicitly. For example: derive base from is_first inside the threshold formula, compute hand_count as the length of hand rather than storing it, and merge threshold and shortfall into a single shortfall computation.
- change: Add one explicit public attribute for revealed exact ranks (e.g. a per-player list parallel to point_pile, marked revealed or unknown) and count it within the limit. Alternatively, drop the announcement and make a failed scuttle reveal nothing beyond the scrapped card.
- change: Define target positions as 1-based indices into the current point pile, state that later cards shift down after a removal or Jack move, and state that revealed marks move with their card.
- change: Specify the band computation as a concrete per-card operation that fits the flat step list (e.g. store each point card's band beside it when it is placed, so no list mapping is needed), and recount steps_per_round to confirm it is at most 20.
The variation that was reviewed: Cuttle Lite: Blind Scuttle: DECK: 48 cards: number cards of rank 1 to 10 (four of each, 40 cards), 4 Jacks (J) and 4 Kings (K). There are no suits.

SETUP: Shuffle the deck. Deal 6 cards to each player's hidden hand. The remaining 36 cards form the face-down draw pile. The scrap pile starts empty. Choose one seat at random and mark it First (is_first = true); the other seat gets is_first = false. These marks never change. Each player starts with an empty point pile, points 0, king_count 0 and won 0. Set turn = 1. The First player acts on turn 1, and turns then alternate.

THRESHOLD: base = 32 for the First player and 30 for the other. threshold = base − 5 × king_count. shortfall = max(threshold − points, 0).

VISIBILITY: Your hand, your exact point cards, your points and your shortfall are known only to you. Both players see:
- each player's hand_count;
- each player's king_count and is_first;
- the size of the draw pile and the scrap pile's contents;
- each player's point_pile_view, which is the band of every point card in order: Low = rank 1-3, Mid = 4-7, High = 8-10.

EACH TURN (turn 1 to 40):
1. WIN CHECK: if the acting player's points ≥ threshold, set that player's won = 1 and end the game immediately. This is the only place won is ever set.
2. The acting player chooses one action. If the reply is missing, illegal or unparseable, the action is PASS.
   - PASS: nothing happens. Always legal; this is the default.
   - DRAW: legal only if the draw pile is not empty and your hand has fewer than 8 cards. Take the top card of the draw pile into your hand.
   - POINTS: choose a number card from your hand and place it in your point pile.
   - SCUTTLE: choose a number card from your hand and a target position in the opponent's point pile.
     • If your card's rank is strictly higher than the target's rank, both cards go to the scrap pile.
     • Otherwise, only your card goes to the scrap pile, the target stays, and the target's exact rank is announced to both players.
   - JACK: play a Jack from your hand and choose a target position in the opponent's point pile. Move that point card to the end of your own point pile; the Jack goes to the scrap pile.
   - KING: play a King from your hand. It stays on your side permanently, and your king_count increases by 1.
   An action that names a card you do not hold, or a target that does not exist, is illegal and counts as PASS.
3. RECOMPUTE for both players: points = sum of ranks in their point pile; threshold = base − 5 × king_count; shortfall = max(threshold − points, 0); point_pile_view from the bands.
4. Increase turn by 1. If turn is now 41, the game ends at once: no win check and no action takes place, and won stays 0 for both players. Otherwise the other player acts next.

Note: a player who reaches the threshold during their own turn wins only at the start of their next turn. The opponent therefore gets one turn to scuttle or steal them back below it. Winner: If a start-of-turn win check sets won = 1, that player wins. If the game ends after turn 40, both won flags are 0 and the player with the smaller shortfall wins; equal shortfalls are a draw. Standing = won × 1000 − shortfall, and the higher standing wins.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Cuttle is a two-player combat card game with a standard 52-card deck. Players race to 21 points using number cards, while using scuttles, one-off effects and permanents (8, J, Q, K) to destroy, steal or protect point cards. Kings lower the target.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No single action dominates. Always playing points gets scuttled or stolen. Always drawing never scores. Always scuttling runs out of cards. The dealer gets 6 cards to the opponent's 5 to offset moving second. The one real flaw is that three passes on an empty deck end with no winner, a result a losing player can steer toward."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Good timing of scuttles, kings and counters wins reliably over many games. In a single game, the draw of jacks, kings and 2s can decide the outcome, and the full one-off list makes card quality swing hard."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Hand reading, tempo, when to commit points and when to hold threats can be improved at length. A weak player still scores by laying points."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, so players must infer threats from the scrap pile, from draws and from what the opponent declines to do. The point piles are public, which removes inference on that side."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Reaching the threshold is arithmetic on card values and king count."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "About eight distinct one-off effects, Queen protection, out-of-turn 2-counters (an interrupt inside the other player's turn), suit comparisons and an open-ended length exceed the step and attribute limits. The previous cut-down version also failed, on attribute count (21 or more stored) and on ambiguous positions and band mapping."
    }
  ],
  "problems": [
    "P1: The full card-effect list, the Queen protection and the out-of-turn 2-counter need far more steps than allowed, and interrupts are not a flat step list.",
    "P2: Open-ended length. Three passes give no winner, which the trailing player can force.",
    "P3: Point piles are fully public, so the board side holds nothing to infer. Scuttling is a lookup.",
    "P4 (previous variation): Stored attributes reached 21 or more (threshold, shortfall, won and the announced-rank record stored separately), over the limit of 20.",
    "P5 (previous variation): The failed-scuttle announcement needed its own public per-card store that the attribute count did not include.",
    "P6 (previous variation): Target positions had no stated indexing, and it was unclear how positions and revealed marks shift after a removal or a Jack move.",
    "P7 (previous variation): point_pile_view needed a list-wide rank-to-band mapping with no operation that fits a flat step list.",
    "P8 (previous variation): Choice steps and step count were stated loosely. Action, card and target should be one structured reply, so the count is honest."
  ],
  "changes": [
    {
      "what": "Keep the reduced card set: ranks 1-10 ×4, 4 Jacks, 4 Kings, no suits. Only points, scuttle, Jack steal and King are kept as actions.",
      "why": "This keeps Cuttle's core (race to a threshold, scuttle, steal, kings lower the target) inside a flat list of about 13 steps.",
      "fixes": "P1"
    },
    {
      "what": "Fixed 40 turns. A win is checked at the start of the acting player's turn. After turn 40, the smaller shortfall to the player's own threshold wins, and equal shortfalls draw.",
      "why": "Every game ends with an arithmetic winner. Stalling cannot force a no-result, because it keeps your shortfall high.",
      "fixes": "P2"
    },
    {
      "what": "Exact point cards stay private. Only each card's band (Low 1-3, Mid 4-7, High 8-10) is public.",
      "why": "A scuttle becomes a bet under uncertainty, and it must be read from bands, the scrap pile and the opponent's behaviour.",
      "fixes": "P3"
    },
    {
      "what": "Remove the stored threshold, shortfall and won attributes. The threshold is computed inline as (32 if is_first else 30) − 5 × king_count. A single per-player 'standing' is set to 1000 on a win, or to −shortfall at the end. hand_count is the length of hand. The 17 stored attributes are listed explicitly.",
      "why": "This brings the state well under 20.",
      "fixes": "P4"
    },
    {
      "what": "Drop the failed-scuttle announcement. A failed scuttle only scraps the attacker's card, which is visible in the scrap pile.",
      "why": "No extra per-card public store is needed. The attacker still learns that the target is at least their rank, which is useful inference.",
      "fixes": "P5"
    },
    {
      "what": "Positions are 1-based indices into the current point pile. Removal closes the gap, and later cards shift down by one. A Jack move appends the card to the end of the thief's pile. Every pile operation is applied identically, at the same index, to the parallel band list.",
      "why": "Players and the builder can resolve every target without ambiguity.",
      "fixes": "P6"
    },
    {
      "what": "Store each card's band at the moment it is placed. The POINTS step appends the rank to point_pile and the band letter, computed from that one rank, to point_view. Scuttle and Jack apply the same remove or append to both lists.",
      "why": "No list-wide mapping is needed, only single-element operations.",
      "fixes": "P7"
    },
    {
      "what": "One structured choice per turn (action, card rank, target position). Step count recounted at 13.",
      "why": "This gives honest complexity numbers within the limits.",
      "fixes": "P8"
    }
  ],
  "keeps": [
    "A race to a point threshold using number cards as points",
    "Scuttling: destroy an enemy point card with a strictly higher number card, at the cost of your own card",
    "Jacks steal an opponent's point card",
    "Kings permanently lower your own threshold by a fixed step",
    "Hidden hands, a shared draw pile and a public scrap pile",
    "One action per turn: draw, play points or play an effect",
    "The opponent gets a response turn before a threshold-crossing win counts"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The race, scuttle, steal and king core fits in about 13 steps and 17 attributes. Hiding exact point values behind bands gives real inference, so the adapted game is buildable and still recognisably Cuttle."
  },
  "variation": {
    "name": "Cuttle Lite: Blind Scuttle (rev. 2)",
    "summary": "Two players race to a personal point threshold, 32 for the first player and 30 for the second, lowered by 5 per King. Exact point cards are private and only their bands are public. Scuttles are blind guesses and Jacks steal. A threshold-crossing player must survive the opponent's next turn to win, and after 40 turns the smaller shortfall wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 48 cards. Number cards of rank 1 to 10, four of each (40 cards). 4 Jacks (J). 4 Kings (K). There are no suits.\n\nSTORED STATE (17 attributes). Per player: hand (list), point_pile (list of ranks), point_view (list of band letters, kept parallel to point_pile), points, king_count, is_first, standing. Shared: draw_pile, scrap_pile, turn. Two values are derived, not stored: hand_count = number of cards in hand, and threshold = (32 if is_first else 30) − 5 × king_count.\n\nSETUP:\n- Shuffle the deck.\n- Deal 6 cards to each player's hidden hand. The remaining 36 cards are the face-down draw pile, and the scrap pile is empty.\n- Choose one seat at random to have is_first = true; the other has is_first = false. These never change.\n- Each player starts with an empty point_pile, an empty point_view, points 0, king_count 0 and standing 0.\n- Set turn = 1. The First player acts on odd turns and the other player on even turns.\n\nBANDS: a number card's band is L if its rank is 1-3, M if 4-7, and H if 8-10.\n\nPOSITIONS: a target position is a whole number from 1 to the current length of the opponent's point_pile, counted from the oldest card (position 1). When a card is removed from a pile, the cards after it each move down one position. Every removal, insertion or move applied to a point_pile is applied in the same way, at the same position, to that player's point_view.\n\nVISIBILITY:\n- Private to each player: their own hand, their exact point_pile, their points and their threshold arithmetic.\n- Public to both: each player's hand_count, point_view, king_count and is_first; the draw pile size; the full scrap pile.\n\nEACH TURN (turns 1 to 40), for the acting player:\n1. WIN CHECK: if the acting player's points ≥ their threshold, set their standing = 1000 and end the game. This is the only way to win before the end.\n2. CHOOSE: the acting player gives one reply with three fields: action, card rank (if needed) and target position (if needed). The actions are:\n   - PASS: nothing happens.\n   - DRAW: legal only if the draw pile is not empty and hand_count < 8. Move the top draw-pile card into your hand.\n   - POINTS: name a number card in your hand. Remove it from your hand, append its rank to the end of your point_pile, and append its band to the end of your point_view.\n   - SCUTTLE: name a number card in your hand and a target position in the opponent's point_pile.\n     • Success: if your rank is strictly greater than the target's rank, your card and the target card both go to the scrap pile, and the target's entries are removed from the opponent's point_pile and point_view.\n     • Failure: otherwise, only your card goes to the scrap pile, and nothing else is revealed.\n   - JACK: play a Jack from your hand and name a target position in the opponent's point_pile. Remove that card from the opponent's point_pile and point_view, and append it (rank and band) to the end of your own. The Jack goes to the scrap pile.\n   - KING: play a King from your hand. It stays in front of you permanently, and your king_count increases by 1.\n3. VALIDATE: a reply that is missing or unparseable, names a card you do not hold, names a target that does not exist, or breaks the DRAW conditions counts as PASS.\n4. RECOMPUTE: for both players, points = sum of the ranks in their point_pile.\n5. ADVANCE: turn increases by 1. If turn is now 41, the game ends at once with no further win check. Each player's standing = −max(threshold − points, 0).\n\nThe one-turn grace follows from the timing. Reaching your threshold during your turn only wins at the start of your next turn, so the opponent has one turn to scuttle or steal you back below it.",
    "objective": "If a start-of-turn win check sets a player's standing to 1000, that player wins. If the game ends after turn 40, each standing equals minus that player's shortfall to their own threshold. The higher standing (the smaller shortfall) wins, and equal standings are a draw.",
    "expected_effect": "Scuttles become decisions under uncertainty. An H-band card is worth attacking with a 10, but an M card might be a 4 or a 7, and a failed scuttle wastes a card. Players track the scrap pile and draws to estimate which high cards and Jacks the opponent may still hold. They weigh committing points against waiting, and time Kings so the threshold drops just as their points close the gap, sometimes keeping a Jack to answer an opponent who crosses. Simple policies all lose. Always-PASS never scores. Always-DRAW never scores and stalls at 8 cards. Dumping the highest card as points is easily scuttled. The First player moves first but needs 2 more points, which offsets the tempo edge. The fixed 40-turn end with a shortfall comparison removes the no-winner stall."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 1,
    "attributes": 17,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
