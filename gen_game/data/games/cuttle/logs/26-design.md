# 26 design

- time: 2026-10-27T18:01:32+00:00 (97.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 179cf8cff091d181, reply sha256 d036437b5469d6f1

## Sent

````
Original game: Cuttle
Players in the original: 2 to 2

Original rules:
Two players share a standard 52-card deck. Deal 6 cards to dealer and 5 to opponent, rest is draw pile; scrap pile is face-up discard showing top only. On your turn do exactly one: draw one card, or play one card from hand. Number cards A,2-10 can be point cards worth their value (A=1) placed on your side; first to 21+ points wins, but kings reduce requirement to 14/10/7/5 for 1-4 kings you control. A point card can also scuttle: play a higher rank, or equal rank with higher suit C<D<H<S, to discard both cards. Cards  A,2-7,9 can be one-offs discarded after use for effects like wipe points, destroy permanents, recover from scrap, force opponent discard 2, draw 2, play top of deck immediately, bounce a permanent. 8,J,Q,K are permanents staying on table: 8 forces opponent to reveal hand, J stacked on a point card steals it, Q protects your other points/permanents from single-target effects, K lowers win threshold. 2 can be played on opponent's turn to counter a one-off. If draw pile empty you may pass; three passes ends game with no winner.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: SEAT EDGE. The original Cuttle offsets moving first by dealing the dealer 6 cards and the opponent 5. This variation deals 6 and 6. The only offset is that the second seat's threshold is 2 points lower (32 vs 30).
Rough race with highest-card-first play (expected top order statistics of 6 cards from ranks 1-10):
| plays | expected sum |
|---|---|
| 1 | 9.2 |
| 2 | 16.8 |
| 3 | 23.1 |
| 4 | 28.0 |
| 5 | 31.6 |
So both seats need about 5 point plays.
- First reaches its threshold on turn 9 and its win check comes on turn 11.
- Second reaches its threshold on turn 10 and its win check comes on turn 12.
One tempo is worth one card, about 5.5-6 points, but the offset is only 2 points. The higher threshold costs First an extra card only when its sum lands at exactly 30-31, roughly 15-20% of races. This is unquantified, but it likely gives First a clear edge.
THOUGHTLESS POLICIES under the WINNER RULE:
- Always PASS: loses to any player who plays points. It fails as a policy, which is fine.
- Always DRAW: stalls at hand 8, then PASSes, and loses. Fine.
- Policy A, 'play King if held, else the highest number card as POINTS, else DRAW':
  - vs random: wins almost always, because random players waste turns on failed scuttles and PASS.
  - vs sensible: SCUTTLE is a 1-for-1 card trade that gains no tempo. It is blind, since only bands are shown, and a failure just burns your card. It can never remove a 10, because success needs a strictly greater rank and 10 is the maximum.
  - The sensible deviations from A are rare: a Jack, or a grace-turn scuttle. Policy A is close to optimal and wins or draws most of its games.
DOMINATED OPTIONS:
- KING dominates POINTS with any card of rank 5 or less. It is worth 5 threshold points, is permanent, and is immune to both scuttle and Jack. A point card of rank 5 or less is worth at most 5 and is vulnerable.
- POINTS with a 10 dominates POINTS with a 9: it is worth more, and only a Jack can remove it.
JACK has no counter, because Queens and 2s were removed. It swings up to 20 points (minus 10 to the opponent, plus 10 to you), and the public H band shows exactly where to aim it.
Both players can win, but the numbers favour the first seat and the holder of Jacks, Kings and 10s, not better play.
- reasoning_over_luck FAILED: The decisive resources are all dealt at random:
- 10s cannot be scuttled.
- Jacks are unanswerable swings of up to 20 points.
- Kings are 5 unremovable points each.
With 6 cards each and an average rank of 5.5, an opening hand often already holds about 30 points. The game typically ends around turns 9-14, so the deal largely sets the race.
Suppose both players follow the intended good strategy: play high, save the Jack for the opponent's grace turn, and play Kings early. Then the winner is mostly whoever was dealt or drew more of the 8 J/K cards and the 10s.
Examples:
- A hand of 10,10,10,K against a hand with no Jack is unstoppable. First reaches 30 against a threshold of 27 on turn 7 and wins at the turn-9 check.
- A player with 2 Jacks wins most races against a player with none.
Reasoning exists but is thin:
- inferring 8, 9 or 10 inside an H band from the scrap pile and failed scuttles;
- timing a Jack for the grace turn.
Scuttle inference rarely matters, because scuttle is weak and cannot touch 10s.
Estimated chance share of the result: above 50%. A good reasoner is not clearly favoured over a greedy play-highest-card policy.
- change: Seat balance: restore a real offset for moving first and justify it numerically. Either deal First 5 cards and Second 6, or tune the threshold gap (e.g. 34 vs 30) using a simple race simulation.
- change: Make 10s removable: let SCUTTLE succeed on rank greater than or equal to the target, or let any H-band scuttle hit an H target, so that playing a 10 is not near-immune.
- change: Limit Jacks: allow them to target only L or M band cards, or send the stolen card to the scrap pile instead of the thief's pile, or let the target discard a card of equal or higher rank to block. Any one of these turns a free 20-point swing into a decision.
- change: Make Kings contestable or weaker, e.g. minus 3 threshold each, or removable by a Jack or by a scuttle with a 10, so that KING no longer dominates low point plays.
- change: Reduce deal luck, e.g. give each player 1 Jack and 1 King at setup outside the shuffle and deal the rest, so that the special cards are not decided by the deal and play revolves around timing and inference.
- change: Strengthen inference, e.g. a failed scuttle publicly reveals 'higher or equal', and a successful one reveals the rank to both players. Then show by worked example that a reasoning player beats the greedy 'King, then highest card' policy most of the time.
The variation that was reviewed: Cuttle Lite: Blind Scuttle (rev. 2): DECK: 48 cards. Number cards of rank 1 to 10, four of each (40 cards). 4 Jacks (J). 4 Kings (K). There are no suits.

STORED STATE (17 attributes). Per player: hand (list), point_pile (list of ranks), point_view (list of band letters, kept parallel to point_pile), points, king_count, is_first, standing. Shared: draw_pile, scrap_pile, turn. Two values are derived, not stored: hand_count = number of cards in hand, and threshold = (32 if is_first else 30) − 5 × king_count.

SETUP:
- Shuffle the deck.
- Deal 6 cards to each player's hidden hand. The remaining 36 cards are the face-down draw pile, and the scrap pile is empty.
- Choose one seat at random to have is_first = true; the other has is_first = false. These never change.
- Each player starts with an empty point_pile, an empty point_view, points 0, king_count 0 and standing 0.
- Set turn = 1. The First player acts on odd turns and the other player on even turns.

BANDS: a number card's band is L if its rank is 1-3, M if 4-7, and H if 8-10.

POSITIONS: a target position is a whole number from 1 to the current length of the opponent's point_pile, counted from the oldest card (position 1). When a card is removed from a pile, the cards after it each move down one position. Every removal, insertion or move applied to a point_pile is applied in the same way, at the same position, to that player's point_view.

VISIBILITY:
- Private to each player: their own hand, their exact point_pile, their points and their threshold arithmetic.
- Public to both: each player's hand_count, point_view, king_count and is_first; the draw pile size; the full scrap pile.

EACH TURN (turns 1 to 40), for the acting player:
1. WIN CHECK: if the acting player's points ≥ their threshold, set their standing = 1000 and end the game. This is the only way to win before the end.
2. CHOOSE: the acting player gives one reply with three fields: action, card rank (if needed) and target position (if needed). The actions are:
   - PASS: nothing happens.
   - DRAW: legal only if the draw pile is not empty and hand_count < 8. Move the top draw-pile card into your hand.
   - POINTS: name a number card in your hand. Remove it from your hand, append its rank to the end of your point_pile, and append its band to the end of your point_view.
   - SCUTTLE: name a number card in your hand and a target position in the opponent's point_pile.
     • Success: if your rank is strictly greater than the target's rank, your card and the target card both go to the scrap pile, and the target's entries are removed from the opponent's point_pile and point_view.
     • Failure: otherwise, only your card goes to the scrap pile, and nothing else is revealed.
   - JACK: play a Jack from your hand and name a target position in the opponent's point_pile. Remove that card from the opponent's point_pile and point_view, and append it (rank and band) to the end of your own. The Jack goes to the scrap pile.
   - KING: play a King from your hand. It stays in front of you permanently, and your king_count increases by 1.
3. VALIDATE: a reply that is missing or unparseable, names a card you do not hold, names a target that does not exist, or breaks the DRAW conditions counts as PASS.
4. RECOMPUTE: for both players, points = sum of the ranks in their point_pile.
5. ADVANCE: turn increases by 1. If turn is now 41, the game ends at once with no further win check. Each player's standing = −max(threshold − points, 0).

The one-turn grace follows from the timing. Reaching your threshold during your turn only wins at the start of your next turn, so the opponent has one turn to scuttle or steal you back below it. Winner: If a start-of-turn win check sets a player's standing to 1000, that player wins. If the game ends after turn 40, each standing equals minus that player's shortfall to their own threshold. The higher standing (the smaller shortfall) wins, and equal standings are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Cuttle is a two-player card duel with a standard deck. Each turn you draw or play one card: as points (race to 21, lowered by Kings), as a scuttle that destroys an opponent's point card, as a one-off effect, or as a permanent (8, J, Q, K). A 2 can counter a one-off at instant speed.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "The full original has real counterplay: Queens protect, 2s counter, Jacks can be re-stolen. That keeps 'play highest card' from dominating. The reduced variation (rev. 2) lost this. Kings dominated any point card of rank 5 or less, Jacks had no counter, and 10s could not be scuttled. With 6-6 deals and only a 2-point threshold offset, the first seat was about one tempo (about 5.5 points) ahead, against an offset worth 2."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, skill matters through timing counters and card economy, but deal variance is large: who holds the Kings, Jacks and 2s. In rev. 2 the greedy policy 'King, then highest card as points' was close to optimal. The 8 Jacks and Kings plus the 10s, all dealt at random, decided most races, with an estimated chance share above 50%."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Both seats can win and weak players still score points. The original rewards long-term card counting, threat assessment and holding answers. There is room to improve once the special cards stop being lottery tickets."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Hands are hidden and the scrap pile is public, so inference exists. In rev. 2 it was thin. Scuttles were blind and weak and could not touch 10s, so reading H-band cards rarely mattered. Jacks had an obvious target, the public H band."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Points, thresholds and the win check are pure arithmetic on tracked card ranks. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original is turn-based text with no board, but it has many one-off effects, instant-speed 2 counters (which break turn order) and the 8 reveal. That is too many rules for the step limits. The rev. 2 cut-down fits, but needs rebalancing."
    }
  ],
  "problems": [
    "P1 Seat edge: with equal hands, moving first is worth about one card (about 5.5 points), and a 2-point threshold gap does not offset it.",
    "P2 Deal luck in special cards: Jacks and Kings are shuffled into the deck, so who holds them largely decides the race.",
    "P3 Jacks are unanswerable 20-point swings (steal = minus 10 to the opponent, plus 10 to you), aimed at the public H band, so no thought is needed.",
    "P4 Kings dominate low point plays: 5 threshold points that cannot be removed.",
    "P5 10s are effectively immune, because scuttle needs a strictly greater rank.",
    "P6 Scuttle is a pure 1-for-1 card loss that gains no tempo, so it is rarely right and the band inference attached to it rarely matters.",
    "P7 Greedy 'King, then highest card' is near-optimal, so a reasoning player is not reliably favoured.",
    "P8 Instant-speed 2 counters and the many one-off effects of the original exceed what the engine builds."
  ],
  "changes": [
    {
      "what": "Jacks and Kings are removed from the shuffle. Each player receives exactly 1 Jack and 1 King at setup, and the deck is the 40 number cards only.",
      "why": "Special cards stop being a lottery. Both players hold the same tools, so what matters is when and where they are used.",
      "fixes": "P2 Deal luck in special cards"
    },
    {
      "what": "Jack no longer steals. It sends the chosen opponent point card, or the opponent's King, to the scrap pile.",
      "why": "The maximum swing falls from 20 to 10 (or 5 threshold points). There is now a real choice between killing a high point card and killing the King. Each player has only one Jack, so timing it for the opponent's grace turn is the key decision.",
      "fixes": "P3 Jacks are unanswerable 20-point swings"
    },
    {
      "what": "A King in play can be destroyed by the opponent's Jack, which restores the threshold.",
      "why": "The King is still a strong early play, but it is contestable. Since both players have one, it gives neither an edge.",
      "fixes": "P4 Kings dominate low point plays"
    },
    {
      "what": "Scuttle succeeds when your rank is greater than OR EQUAL to the target's rank.",
      "why": "A 10 can now remove a 10. Reading which 8s, 9s and 10s are already in the scrap pile decides whether an H-band scuttle is safe.",
      "fixes": "P5 10s are effectively immune"
    },
    {
      "what": "A successful scuttle refunds one card: the scuttler draws the top card of the draw pile, if it is not empty and their hand holds fewer than 8 cards. A failed scuttle refunds nothing.",
      "why": "Scuttle becomes tempo-neutral when it works and a loss when it misses. Accurate inference about hidden ranks now pays directly, and blind guessing is punished.",
      "fixes": "P6 Scuttle is a pure 1-for-1 card loss"
    },
    {
      "what": "Seat offset: First receives 5 number cards and has a base threshold of 31. Second receives 6 number cards and has a base threshold of 30.",
      "why": "This restores the original Cuttle offset of one card fewer for the player who moves first, plus a 1-point nudge. Rough race estimate: First needs a 4-play sum of 26 or more from 5 cards (about 45%); Second needs 25 or more from the top 4 of 6 (about 70%). First is 2 turns ahead in tempo, so the race lands near 50/50. If the pipeline shows a residual edge, the base thresholds are the tuning knob.",
      "fixes": "P1 Seat edge"
    },
    {
      "what": "All one-offs, Queens, 8s and instant-speed 2s are dropped. Only POINTS, SCUTTLE, JACK, KING, DRAW and PASS remain, all on your own turn.",
      "why": "This keeps one choice step per turn and stays within the engine limits.",
      "fixes": "P8 Instant-speed 2 counters and the many one-off effects"
    },
    {
      "what": "The opponent sees only bands (L/M/H) of your point cards, not your exact total. Wins are checked at the start of your next turn, giving a one-turn grace.",
      "why": "The defender must infer from bands and the scrap pile whether the attacker has reached the threshold. They must then decide whether to spend their single Jack or a high card to deny it. Greedy play never defends, so a reasoner can deny greedy's winning turn while greedy cannot deny theirs.",
      "fixes": "P7 Greedy 'King, then highest card' is near-optimal"
    }
  ],
  "keeps": [
    "Two-player race to a point threshold using number cards as points.",
    "Each turn: draw one card or play one card.",
    "Scuttle: destroy an opponent's point card with a card of high enough rank.",
    "Jack as the anti-point-card weapon; King as a permanent that lowers your threshold.",
    "Public scrap pile and hidden hands; the first seat gets one card fewer, as in the original deal."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core race-versus-disruption tension survives a cut-down. Fixing the special-card lottery, scuttle economics and the seat offset makes the game turn on inference about hidden ranks and on the timing of single-use answers."
  },
  "variation": {
    "name": "Cuttle Lite: Grace Turn (rev. 3)",
    "summary": "A two-player race to a point threshold. Exact point ranks are hidden behind bands, each player holds one Jack and one King, and scuttles refund a card when they succeed, so reading the opponent and timing your answer decides the race.",
    "players": {"min": 2, "max": 2, "suggested": 2},
    "rules": "DECK: 40 number cards, ranks 1 to 10, four of each, no suits. Separately, 2 Jacks and 2 Kings, which are not shuffled into the deck.\n\nSTORED STATE (17 attributes):\n- Per player: hand (list), point_pile (list of ranks), point_view (list of band letters, parallel to point_pile), points, king_in_play (0 or 1), is_first, standing.\n- Shared: draw_pile, scrap_pile, turn.\n- Derived, not stored: hand_count = number of cards in hand; threshold = (31 if is_first else 30) - 5 x king_in_play.\n\nSETUP:\n1. Choose one seat at random to be First (is_first = true); the other is Second. These never change.\n2. Shuffle the 40 number cards.\n3. Deal 5 number cards to First and 6 to Second, face down.\n4. Add 1 Jack and 1 King to each player's hand. First holds 7 cards and Second holds 8.\n5. The remaining 29 cards form the face-down draw pile. The scrap pile starts empty.\n6. Each player starts with an empty point_pile and point_view, points 0, king_in_play 0 and standing 0.\n7. Set turn = 1. First acts on odd turns and Second on even turns.\n\nBANDS: a number card's band is L for ranks 1-3, M for 4-7 and H for 8-10.\n\nPOSITIONS:\n- A target is either a position from 1 to the length of the opponent's point_pile, counted from the oldest card, or the word KING, meaning the opponent's King in play.\n- When a card is removed from a point_pile, the later cards shift down one position.\n- Every change to a point_pile is mirrored in that player's point_view.\n\nVISIBILITY:\n- Private to each player: their hand, the exact ranks in their point_pile, and their points.\n- Public: each player's hand_count, point_view, king_in_play and is_first; the draw pile size; the full scrap pile (in order); and every action taken, with the card played and the target named.\n- Because scrapped cards are public, a successful scuttle or Jack reveals the destroyed card's rank. A failed scuttle shows only that the target's rank was higher than the card spent.\n\nEACH TURN (turns 1 to 40), for the acting player:\n1. WIN CHECK: if the acting player's points >= their threshold, their standing = 1000 and the game ends. This is the only way to win early. Reaching the threshold during your own turn therefore gives the opponent one turn to knock you back below it.\n2. CHOOSE: the acting player replies with an action, a card (if needed) and a target (if needed). The actions are:\n   - PASS: nothing happens.\n   - DRAW: legal only if the draw pile is not empty and hand_count < 8. Take the top card of the draw pile into your hand.\n   - POINTS: play a number card from your hand. Append its rank to your point_pile and its band to your point_view.\n   - SCUTTLE: play a number card from your hand at a target position in the opponent's point_pile.\n     Success, if your rank >= the target's rank: both cards go to the scrap pile and the target is removed from the opponent's point_pile and point_view. Then, if the draw pile is not empty and your hand_count < 8, take the top draw card into your hand.\n     Failure, otherwise: only your card goes to the scrap pile.\n   - JACK: play your Jack at a target. If the target is a position, that point card goes to the scrap pile and is removed from the opponent's point_pile and point_view. If the target is KING and the opponent's king_in_play = 1, the King goes to the scrap pile and their king_in_play becomes 0. The Jack goes to the scrap pile.\n   - KING: play your King. Your king_in_play becomes 1, which lowers your threshold by 5.\n3. VALIDATE: a reply that is missing or unparseable, names a card not in your hand, names a target that does not exist (including KING when no King is in play), or breaks the DRAW conditions counts as PASS.\n4. RECOMPUTE: for both players, points = sum of the ranks in their point_pile.\n5. ADVANCE: turn increases by 1. If turn becomes 41, the game ends with no further win check, and each player's standing = -max(threshold - points, 0).",
    "objective": "If a start-of-turn win check finds the acting player's points at or above their threshold, that player wins. If the game reaches the end of turn 40 instead, each player's standing is minus their shortfall to their own threshold. The higher standing (the smaller shortfall) wins, and equal standings are a draw.",
    "expected_effect": "Thoughtless policies now lose.\n- Always PASS and always DRAW lose to anyone who plays points.\n- Blind always-SCUTTLE burns low cards on failed hits.\n- Greedy 'King, then highest card as points' never defends. A reasoning opponent can deny its winning turn with a Jack on its 10 or King, or with a 10-on-10 scuttle, while greedy cannot deny theirs.\n\nWhat good play involves:\n- Estimating the opponent's exact total from bands and the public scrap pile, to know when the grace turn has come.\n- Saving the single Jack for that turn, and choosing between a high card and the King.\n- Counting the H-band cards in the scrap pile to judge whether an 8 or 9 scuttle will land.\n- Using successful scuttles (which refund a card) to trade low cards against L-band targets without losing tempo.\n- Laying point cards so as not to expose a decisive card to a cheap scuttle.\n\nThe seat offset (one card fewer and threshold 31 for First) is estimated to bring the seats near 50/50; the pipeline should confirm or retune the base thresholds. Number-card variance remains, but Jacks and Kings are equal for both and no card is immune. The chance share should fall to roughly a third, so the better reader should win most games. Talk is omitted: this is a two-player zero-sum game, so messages could only be bluffs with no stake, and the hidden-band inference already carries the reading-the-opponent element."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 1,
    "attributes": 17,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
