# Variation: Cuttle Lite: Grace Turn (rev. 3)

A two-player race to a point threshold. Exact point ranks are hidden behind bands, each player holds one Jack and one King, and scuttles refund a card when they succeed, so reading the opponent and timing your answer decides the race.

Players: 2 to 2, best with 2

## Review of the original

Cuttle is a two-player card duel with a standard deck. Each turn you draw or play one card: as points (race to 21, lowered by Kings), as a scuttle that destroys an opponent's point card, as a one-off effect, or as a permanent (8, J, Q, K). A 2 can counter a one-off at instant speed.

- **non_degenerate**: weak. The full original has real counterplay: Queens protect, 2s counter, Jacks can be re-stolen. That keeps 'play highest card' from dominating. The reduced variation (rev. 2) lost this. Kings dominated any point card of rank 5 or less, Jacks had no counter, and 10s could not be scuttled. With 6-6 deals and only a 2-point threshold offset, the first seat was about one tempo (about 5.5 points) ahead, against an offset worth 2.
- **skill_sensitive**: weak. In the original, skill matters through timing counters and card economy, but deal variance is large: who holds the Kings, Jacks and 2s. In rev. 2 the greedy policy 'King, then highest card as points' was close to optimal. The 8 Jacks and Kings plus the 10s, all dealt at random, decided most races, with an estimated chance share above 50%.
- **headroom**: good. Both seats can win and weak players still score points. The original rewards long-term card counting, threat assessment and holding answers. There is room to improve once the special cards stop being lottery tickets.
- **reasoning_dependent**: weak. Hands are hidden and the scrap pile is public, so inference exists. In rev. 2 it was thin. Scuttles were blind and weak and could not touch 10s, so reading H-band cards rarely mattered. Jacks had an obvious target, the public H band.
- **verifiable**: good. Points, thresholds and the win check are pure arithmetic on tracked card ranks. No judge is needed.
- **fits_platform**: weak. The original is turn-based text with no board, but it has many one-off effects, instant-speed 2 counters (which break turn order) and the 8 reveal. That is too many rules for the step limits. The rev. 2 cut-down fits, but needs rebalancing.

## Problems

- P1 Seat edge: with equal hands, moving first is worth about one card (about 5.5 points), and a 2-point threshold gap does not offset it.
- P2 Deal luck in special cards: Jacks and Kings are shuffled into the deck, so who holds them largely decides the race.
- P3 Jacks are unanswerable 20-point swings (steal = minus 10 to the opponent, plus 10 to you), aimed at the public H band, so no thought is needed.
- P4 Kings dominate low point plays: 5 threshold points that cannot be removed.
- P5 10s are effectively immune, because scuttle needs a strictly greater rank.
- P6 Scuttle is a pure 1-for-1 card loss that gains no tempo, so it is rarely right and the band inference attached to it rarely matters.
- P7 Greedy 'King, then highest card' is near-optimal, so a reasoning player is not reliably favoured.
- P8 Instant-speed 2 counters and the many one-off effects of the original exceed what the engine builds.

## Changes

- Jacks and Kings are removed from the shuffle. Each player receives exactly 1 Jack and 1 King at setup, and the deck is the 40 number cards only. (fixes: P2 Deal luck in special cards): Special cards stop being a lottery. Both players hold the same tools, so what matters is when and where they are used.
- Jack no longer steals. It sends the chosen opponent point card, or the opponent's King, to the scrap pile. (fixes: P3 Jacks are unanswerable 20-point swings): The maximum swing falls from 20 to 10 (or 5 threshold points). There is now a real choice between killing a high point card and killing the King. Each player has only one Jack, so timing it for the opponent's grace turn is the key decision.
- A King in play can be destroyed by the opponent's Jack, which restores the threshold. (fixes: P4 Kings dominate low point plays): The King is still a strong early play, but it is contestable. Since both players have one, it gives neither an edge.
- Scuttle succeeds when your rank is greater than OR EQUAL to the target's rank. (fixes: P5 10s are effectively immune): A 10 can now remove a 10. Reading which 8s, 9s and 10s are already in the scrap pile decides whether an H-band scuttle is safe.
- A successful scuttle refunds one card: the scuttler draws the top card of the draw pile, if it is not empty and their hand holds fewer than 8 cards. A failed scuttle refunds nothing. (fixes: P6 Scuttle is a pure 1-for-1 card loss): Scuttle becomes tempo-neutral when it works and a loss when it misses. Accurate inference about hidden ranks now pays directly, and blind guessing is punished.
- Seat offset: First receives 5 number cards and has a base threshold of 31. Second receives 6 number cards and has a base threshold of 30. (fixes: P1 Seat edge): This restores the original Cuttle offset of one card fewer for the player who moves first, plus a 1-point nudge. Rough race estimate: First needs a 4-play sum of 26 or more from 5 cards (about 45%); Second needs 25 or more from the top 4 of 6 (about 70%). First is 2 turns ahead in tempo, so the race lands near 50/50. If the pipeline shows a residual edge, the base thresholds are the tuning knob.
- All one-offs, Queens, 8s and instant-speed 2s are dropped. Only POINTS, SCUTTLE, JACK, KING, DRAW and PASS remain, all on your own turn. (fixes: P8 Instant-speed 2 counters and the many one-off effects): This keeps one choice step per turn and stays within the engine limits.
- The opponent sees only bands (L/M/H) of your point cards, not your exact total. Wins are checked at the start of your next turn, giving a one-turn grace. (fixes: P7 Greedy 'King, then highest card' is near-optimal): The defender must infer from bands and the scrap pile whether the attacker has reached the threshold. They must then decide whether to spend their single Jack or a high card to deny it. Greedy play never defends, so a reasoner can deny greedy's winning turn while greedy cannot deny theirs.

## Kept from the original

- Two-player race to a point threshold using number cards as points.
- Each turn: draw one card or play one card.
- Scuttle: destroy an opponent's point card with a card of high enough rank.
- Jack as the anti-point-card weapon; King as a permanent that lowers your threshold.
- Public scrap pile and hidden hands; the first seat gets one card fewer, as in the original deal.

## The variation's rules

DECK: 40 number cards, ranks 1 to 10, four of each, no suits. Separately, 2 Jacks and 2 Kings, which are not shuffled into the deck.

STORED STATE (17 attributes):
- Per player: hand (list), point_pile (list of ranks), point_view (list of band letters, parallel to point_pile), points, king_in_play (0 or 1), is_first, standing.
- Shared: draw_pile, scrap_pile, turn.
- Derived, not stored: hand_count = number of cards in hand; threshold = (31 if is_first else 30) - 5 x king_in_play.

SETUP:
1. Choose one seat at random to be First (is_first = true); the other is Second. These never change.
2. Shuffle the 40 number cards.
3. Deal 5 number cards to First and 6 to Second, face down.
4. Add 1 Jack and 1 King to each player's hand. First holds 7 cards and Second holds 8.
5. The remaining 29 cards form the face-down draw pile. The scrap pile starts empty.
6. Each player starts with an empty point_pile and point_view, points 0, king_in_play 0 and standing 0.
7. Set turn = 1. First acts on odd turns and Second on even turns.

BANDS: a number card's band is L for ranks 1-3, M for 4-7 and H for 8-10.

POSITIONS:
- A target is either a position from 1 to the length of the opponent's point_pile, counted from the oldest card, or the word KING, meaning the opponent's King in play.
- When a card is removed from a point_pile, the later cards shift down one position.
- Every change to a point_pile is mirrored in that player's point_view.

VISIBILITY:
- Private to each player: their hand, the exact ranks in their point_pile, and their points.
- Public: each player's hand_count, point_view, king_in_play and is_first; the draw pile size; the full scrap pile (in order); and every action taken, with the card played and the target named.
- Because scrapped cards are public, a successful scuttle or Jack reveals the destroyed card's rank. A failed scuttle shows only that the target's rank was higher than the card spent.

EACH TURN (turns 1 to 40), for the acting player:
1. WIN CHECK: if the acting player's points >= their threshold, their standing = 1000 and the game ends. This is the only way to win early. Reaching the threshold during your own turn therefore gives the opponent one turn to knock you back below it.
2. CHOOSE: the acting player replies with an action, a card (if needed) and a target (if needed). The actions are:
   - PASS: nothing happens.
   - DRAW: legal only if the draw pile is not empty and hand_count < 8. Take the top card of the draw pile into your hand.
   - POINTS: play a number card from your hand. Append its rank to your point_pile and its band to your point_view.
   - SCUTTLE: play a number card from your hand at a target position in the opponent's point_pile.
     Success, if your rank >= the target's rank: both cards go to the scrap pile and the target is removed from the opponent's point_pile and point_view. Then, if the draw pile is not empty and your hand_count < 8, take the top draw card into your hand.
     Failure, otherwise: only your card goes to the scrap pile.
   - JACK: play your Jack at a target. If the target is a position, that point card goes to the scrap pile and is removed from the opponent's point_pile and point_view. If the target is KING and the opponent's king_in_play = 1, the King goes to the scrap pile and their king_in_play becomes 0. The Jack goes to the scrap pile.
   - KING: play your King. Your king_in_play becomes 1, which lowers your threshold by 5.
3. VALIDATE: a reply that is missing or unparseable, names a card not in your hand, names a target that does not exist (including KING when no King is in play), or breaks the DRAW conditions counts as PASS.
4. RECOMPUTE: for both players, points = sum of the ranks in their point_pile.
5. ADVANCE: turn increases by 1. If turn becomes 41, the game ends with no further win check, and each player's standing = -max(threshold - points, 0).

Objective: If a start-of-turn win check finds the acting player's points at or above their threshold, that player wins. If the game reaches the end of turn 40 instead, each player's standing is minus their shortfall to their own threshold. The higher standing (the smaller shortfall) wins, and equal standings are a draw.

Expected effect: Thoughtless policies now lose.
- Always PASS and always DRAW lose to anyone who plays points.
- Blind always-SCUTTLE burns low cards on failed hits.
- Greedy 'King, then highest card as points' never defends. A reasoning opponent can deny its winning turn with a Jack on its 10 or King, or with a 10-on-10 scuttle, while greedy cannot deny theirs.

What good play involves:
- Estimating the opponent's exact total from bands and the public scrap pile, to know when the grace turn has come.
- Saving the single Jack for that turn, and choosing between a high card and the King.
- Counting the H-band cards in the scrap pile to judge whether an 8 or 9 scuttle will land.
- Using successful scuttles (which refund a card) to trade low cards against L-band targets without losing tempo.
- Laying point cards so as not to expose a decisive card to a cheap scuttle.

The seat offset (one card fewer and threshold 31 for First) is estimated to bring the seats near 50/50; the pipeline should confirm or retune the base thresholds. Number-card variance remains, but Jacks and Kings are equal for both and no card is immune. The chance share should fall to roughly a third, so the better reader should win most games. Talk is omitted: this is a two-player zero-sum game, so messages could only be bluffs with no stake, and the hidden-band inference already carries the reading-the-opponent element.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
