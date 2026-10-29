# Variation: Duplicate California Jack (Compact)

California Jack with 28 cards, played as two deals over the same shuffled stock. Players swap hands for the second deal, and the second deal is played open. The first deal tests inference from hidden information. The second tests planning against a known layout and a known score to beat.

Players: 2 to 2, best with 2

## Review of the original

California Jack is a two-player trick-taking game played with a face-up stock. After each trick the winner draws the exposed top card and the loser draws the next card. Each deal awards points for capturing the Ace, Deuce and Jack of trump and for winning the most card points, and the first player to 10 points wins.

- **non_degenerate**: good. No simple policy wins. 'Always play your highest card' wastes trumps and Tens early and hands the opponent the good exposed stock cards. 'Always play low' gives up High, Jack and the Tens. Seat edge: the non-dealer leads first, but the deal alternates. In the previous variation the duplicate replay gave each player each hand with the lead once, which removed the seat edge.
- **skill_sensitive**: weak. In the original, a single deal is strongly shaped by who holds the Ace and Jack of trump and by the order of the stock. The match is first to 10, about three deals, which is too few for skill to wash out the cards. The previous variation's duplicate structure fixed this: the same stock and hands are played twice with the players swapped, so the card luck cancels.
- **headroom**: good. A weak player still captures some cards and points. A strong player can keep improving in several ways: deciding when to win a trick to take a valuable exposed card and when to lose it, counting trumps, keeping a trump to guard the Ten, and planning the last no-draw tricks once the stock is empty.
- **reasoning_dependent**: good. The opponent's hand is hidden, and so is every stock card except the top one. Players must infer the opponent's holding from what they drew and played, and must plan whether winning the current trick is worth it, given the visible top card and the unseen card beneath it. In the previous variation the second deal was open, but it rewarded planning against a known record of what happened in deal 1.
- **verifiable**: good. Trick winners, captured honours, card points and match points all follow by arithmetic from the cards played. No judge is needed.
- **fits_platform**: weak. The game is turn-based and text-only, with no board. The original 52-card deck with 6-card hands and first-to-10 scoring is long. The previous variation shrank it to 28 cards and 28 rounds but failed the build check: it really needed about 30-35 steps per round against a limit of 20, and about 22 attributes against a limit of 20. It also left a tie unresolved in its replacement rule for illegal plays.

## Problems

- P1: The original is too long and luck-heavy for the platform. A 52-card deck and first-to-10 means many deals, each dominated by who holds the trump honours.
- P2: The previous variation's per-round step list ran to about 30-35 steps (limit 20). Rank comparison and card-point lookup were done by conditional ladders, the follow rule was enforced by replacement afterwards, and the deal-2 reset was spread over many steps.
- P3: The previous variation needed about 22 attributes (limit 20). It had separate recorded stock and hands, a separate deal-1 record, three honour-holder attributes and a deal counter.
- P4: The previous variation's rule 'an illegal choice is replaced by the lowest-ranked legal card' had no tiebreak when several cards share the lowest rank.
- P5: Seat and deal luck. Whoever leads, and whoever is dealt the trump honours, gains an edge that reasoning cannot overcome within a single deal.

## Changes

- Keep the 28-card deck (A, K, Q, J, 10, 9, 2 in four suits), 4-card hands and a 20-card stock, giving 2 deals of 14 tricks (28 rounds). (fixes: P1): This keeps the stock-drawing structure and the honours while making a match short and finite.
- Keep the duplicate replay. Deal 2 reuses the identical stock, with the two initial hands swapped and the other player leading. Deal 2 is played open. (fixes: P5): Each player plays each hand once, with the lead, against the same stock. Card luck and seat edge cancel, and the difference in results comes from play.
- Each card is a list item carrying three stored numbers: suit, rank value (2=1, 9=2, 10=3, J=4, Q=5, K=6, A=7) and card points (10=10, A=4, K=3, Q=2, J=1, 9=0, 2=0). (fixes: P2): The trick winner and the points become single arithmetic expressions instead of conditional ladders. This cuts several steps.
- Before the follower chooses, one step computes the follower's legal list: led-suit cards if any, else trumps if any, else the whole hand. The follower chooses only from that list. (fixes: P2, P4): Illegal plays become impossible, so the replacement steps disappear.
- Award High, Low and Jack as match points the moment they are captured, in one step: the trick winner gains 1 match point for each of A, 2 and J of trump among the two cards. (fixes: P2, P3): Each honour is captured exactly once per deal, so scoring it at capture is equivalent to scoring at the end of the deal. This removes three holder attributes and the end-of-deal honour checks.
- Use one 'initial deal' record (the stock order plus both hands, stored once). Use one match-long log, so the deal-1 entries stay visible in deal 2 and no separate deal-1 record is needed. Derive the deal from the round number. (fixes: P3): Attributes fall to 16.
- Do the deal-2 reset in two steps that run only after round 14 (on the condition round == 14). The first restores the stock and swaps the hands. The second clears the deal points and makes B the leader. (fixes: P2): The reset was the largest step cost.
- Fix a full card order for the default play: lowest rank value, ties broken by suit order Clubs < Diamonds < Hearts < Spades. Hands are always listed in this order. (fixes: P4): Every fallback and listing is unambiguous.

## Kept from the original

- The face-up stock, where the trick winner takes the exposed top card and the loser takes the next one, so winning or losing a trick on purpose is the central decision.
- Trump is set by the suit of the stock's top card.
- The follow rule: follow suit, else trump, else any card.
- The four scoring items: High (Ace of trump), Low (Deuce of trump), Jack of trump, and Game (most card points, with Ten 10, Ace 4, King 3, Queen 2, Jack 1).
- The no-draw endgame once the stock is empty.
- The tie-break spirit of the original: honours and Game decide first, card points break ties.

## The variation's rules

DECK: 28 cards in 4 suits: Clubs, Diamonds, Hearts, Spades. Each suit has the ranks A, K, Q, J, 10, 9, 2. Each card carries a rank value (2=1, 9=2, 10=3, J=4, Q=5, K=6, A=7; higher wins) and card points (10=10, A=4, K=3, Q=2, J=1, 9=0, 2=0). Each suit holds 20 card points, 80 in total.

CARD ORDER: Whenever cards are listed or a default card is needed, order them by rank value, lowest first, with ties broken by suit order Clubs < Diamonds < Hearts < Spades. Hands are always shown in this order.

SETUP: Shuffle the deck once. Deal 4 cards face down to Player A and 4 to Player B. The other 20 cards form the stock in shuffled order. The suit of the stock's top card is trump for the whole match. The engine privately stores this initial deal (stock order, hand A, hand B) for deal 2. Match points and match card points start at 0 for both players.

MATCH: 28 rounds, one trick per round. Deal 1 is rounds 1-14, and Player A leads round 1. Deal 2 is rounds 15-28, and Player B leads round 15.

INFORMATION: Every round, both players see the following: the trump suit; the top stock card, or 'stock empty'; the number of stock cards left; the match log of every card played and drawn so far, with who played or drew it and who won each trick; both players' match points and match card points; and the current deal card points. In deal 1 (rounds 1-14), each player also sees their own hand only. The opponent's hand and the stock below the top card are hidden. In deal 2 (rounds 15-28), everything is open: both hands face up, the full remaining stock in order, and the stored initial deal.

EACH ROUND:
1. Show the information above.
2. The leader chooses any card from their hand and plays it face up.
3. The engine lists the follower's legal cards: all their cards of the led suit if they have any; otherwise all their trumps if they have any; otherwise their whole hand.
4. The follower chooses one card from that legal list and plays it face up.
If a player gives no valid answer in step 2 or 4, they play the first card of their allowed cards in CARD ORDER.
5. Both played cards leave the hands.
6. Trick winner: the follower wins if they played a trump and either the led card is not a trump or the follower's rank value is higher. The follower also wins if they followed the led suit with a higher rank value. In every other case the leader wins.
7. The winner adds the card points of both cards to their deal card points.
8. Honours: for each of the Ace of trump, the 2 of trump and the Jack of trump among the two played cards, the winner gains 1 match point at once (High, Low and Jack).
9. Append both plays and the trick winner to the match log.
10. If the stock is not empty, the winner takes the top stock card and the loser takes the next one. Both draws are logged and the new top card is revealed. The stock empties after trick 10 of each deal, and tricks 11-14 are played out with no drawing.
11. The winner leads the next round.

END OF DEAL (after rounds 14 and 28): The player with more deal card points gains 1 match point for Game. If both have 40, nobody gains it. Each player adds their deal card points to their match card points.

DEAL 2 RESET (after round 14 has been scored): Restore the stock to its stored order, so trump is unchanged. Player A receives Player B's stored initial hand, and Player B receives Player A's stored initial hand. Set both deal card points to 0. Player B leads round 15. The match log is kept, so the whole of deal 1 stays visible.

END: After round 28 has been scored, the match ends.

Objective: The player with more match points wins. Each deal awards at most 4: High, Low, Jack and Game. If match points are tied, the player with more match card points wins (the two totals add to 160). If both have 80, the match is a draw.

Expected effect: Because both players play the same stock with each hand, the result measures who played the same cards better rather than who was dealt the trump Ace. In deal 1, players must infer the opponent's hand from draws and plays. They must also decide when to lose a trick on purpose to avoid giving up a Ten or to take a better second card, and when to spend a trump to capture an exposed honour. In deal 2, the player holding each hand knows exactly how that hand fared in deal 1 and what match score they must beat, so play becomes precise planning against a fully visible layout. Simple policies can lose: always-highest wastes trumps, always-lowest gives up High, Jack and the Tens, and always-first-listed is the same as always-lowest. The precomputed legal list removes illegal plays, and all scoring is plain addition.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 28 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
