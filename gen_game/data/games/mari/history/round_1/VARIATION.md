# Variation: Little Bidding Mariáš

A 3-player, 20-card Mariáš played over 6 deals of 6 tricks. Each deal opens with a sealed simultaneous bid for the contract and trump suit. The highest bidder plays alone against the other two, trying to reach the contract with card points and marriages.

Players: 3 to 3, best with 3

## Review of the original

Mariáš is a Czech three-player trick-taking game with a 32-card deck. In each deal one declarer chooses trump and a contract and plays alone against two defenders who work as a partnership. Points come from Aces, Tens, the last trick and King-Ober marriages, and the game adds doubling (Flek), stakes doubled for Hearts as trump, and special contracts (Betl, Durch, 7, 100).

- **non_degenerate**: good. No simple policy wins. Always bidding high fails contracts, and always passing leaves the eldest stuck with weak forced games. The declarer role rotates, so no seat has a built-in edge. Card choices decide tricks.
- **skill_sensitive**: good. Judging hand strength, choosing trump, cooperating on defence and counting cards all reliably beat naive play over many deals. Card luck within a single deal is large, but it averages out across a session.
- **headroom**: good. Inferring the unseen hands, timing trumps and protecting Tens is never fully solved. A weak player still scores when they hold strong cards.
- **reasoning_dependent**: good. Hands are hidden. Players must infer the other holdings from the bid and the cards played, defenders must coordinate without talking, and the declarer must plan over 10 tricks.
- **verifiable**: good. Card points, marriages and contract success are all arithmetic.
- **fits_platform**: bad. There are 32 cards, 10 tricks and several deals, so the game runs far past 40 rounds. The talon exchange, Flek/Re chains and four special contracts with their own rules are conditional blocks the flat step list cannot hold. Legality and marriage checks also exceed the step budget.

## Problems

- P1: The original is too long and too branchy for the platform: 32 cards, 10 tricks, a talon exchange, a Flek/Re doubling dialogue and four special contracts (Betl, Durch, 7, 100) that each need their own block of rules.
- P2: The previous variation understated its step budget. Its real count was about 24 steps per round, above the limit of 20, because trick-winner computation, marriage detection and end-of-deal scoring were not compacted.
- P3: The previous fallback for an illegal card ('lowest-ranked legal card') had no tie-break when several legal cards share a rank in different suits.
- P4: The previous variation had no rule for an invalid bid value or a missing or invalid trump suit, so trump could be undefined, for example when the eldest submitted PASS without a suit.
- P5: The previous variation claimed 20 attributes, at the cap, without listing them, so feasibility was not shown.
- P6: The previous legality rule 'if no trump has yet been played' was ambiguous when trump itself is led.

## Changes

- Keep the 20-card, 6-trick, 6-deal match (36 rounds). Use a single numeric contract with a sealed simultaneous bid. Drop Flek, the special contracts and the talon exchange; the talon stays as unseen dead cards. (fixes: P1: The original is too long and too branchy for the platform.): This keeps bidding, trump choice, marriages, partnership defence and the Hearts doubling while fitting 36 rounds with no conditional blocks.
- Encode every card as a number, code = suit*5 + rank (suits Hearts=0, Bells=1, Leaves=2, Acorns=3; ranks U=0, O=1, K=2, 10=3, A=4). The trick winner is the card with the maximum key = rank + 10*(is trump) + 5*(is led suit), computed in one calc step. Marriages for all players are found in one calc step at bidding. Tally, S, the fail transform, Hearts doubling and the score update are merged into one calc step. Give an explicit 18-step list. (fixes: P2: The previous variation understated its step budget.): This brings the real step count to 18, within the limit of 20.
- Fallback for an illegal card: the legal card with the lowest rank; among equal ranks, the first in the suit order Hearts, Bells, Leaves, Acorns. (fixes: P3: The previous fallback had no tie-break.): This makes the fallback a single, fully determined card.
- A bid not in the list counts as PASS. The eldest's PASS or invalid bid counts as 50. A missing or invalid suit defaults to the suit in which that bidder holds the most cards, ties broken by the suit order Hearts, Bells, Leaves, Acorns. (fixes: P4: The previous variation had no rule for an invalid bid or suit.): Contract and trump are now always defined.
- List the attributes explicitly. Use one list of the cards in the current trick instead of separate led-suit, best-card, winner and trick-points attributes. Derive the defenders' trick count as (tricks completed − declarer's tricks), and derive the eldest from the round number. The total is 16. (fixes: P5: The previous variation claimed 20 attributes without listing them.): This shows feasibility with headroom under the cap of 20.
- Restate the follow rule: if you hold the led suit you must play it, and you must beat the highest card of the led suit in the trick if you can. The beating duty is lifted only when the led suit is not trump and a trump has already been played to the trick. (fixes: P6: The previous legality rule was ambiguous when trump is led.): This removes the ambiguity when trump is led.

## Kept from the original

- A lone declarer against a two-player defending partnership, chosen anew each deal.
- The rank order A, 10, K, O, U, with Aces and Tens worth 10 each and 10 for the last trick.
- The duties to follow suit, to beat the trick (head it) and to trump.
- King+Ober marriages worth 40 in trump and 20 otherwise, counting only if the holder's side wins a trick.
- A contract the declarer must reach, with a heavier penalty for failing.
- Doubled stakes when Hearts are trump.
- The eldest hand rotating and obliged to play if nobody bids.

## The variation's rules

CARDS. There are 20 cards in four suits, Hearts, Bells, Leaves and Acorns, each with ranks A, 10, K, O (Ober) and U (Unter). Within a suit the ranks run from highest to lowest A, 10, K, O, U. Each Ace and each Ten is worth 10 card points; all other cards are worth 0. Winning the 6th (last) trick of a deal is worth 10 more points, so the deal has 90 card points in total. Internally each card has the code suit*5 + rank, with suits Hearts=0, Bells=1, Leaves=2, Acorns=3 and ranks U=0, O=1, K=2, 10=3, A=4. Players see and name cards by their names, for example 'Ten of Leaves'. Suit order for tie-breaks is Hearts, Bells, Leaves, Acorns.

MATCH. The match has 6 deals of 6 tricks each, 36 rounds in total. Each round is one trick. Players are seated P1, P2, P3, and seat order is cyclic (P1, P2, P3, P1, ...). The eldest is P1 in deals 1 and 4, P2 in deals 2 and 5, and P3 in deals 3 and 6. Every score starts at 0. Players may not exchange messages at any time; defenders cooperate only through their card play.

DEAL (first round of each deal). The engine shuffles all 20 cards and deals 6 to each player privately. The remaining 2 cards are the talon: face down, seen by no one, and out of play for the whole deal.

BIDDING (first round of each deal, one simultaneous poll). Every player privately submits one answer containing a bid and a suit. A bid is PASS or one of 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150. A suit is Hearts, Bells, Leaves or Acorns.
- Any bid not in this list counts as PASS.
- The eldest may not pass: an eldest PASS or invalid bid counts as 50.
- A missing or invalid suit becomes the suit in which that player holds the most cards, ties broken by the suit order.
All bids and suits are then revealed together. The highest bid wins. If bids are equal, the eldest wins the tie first, then the next player in seat order after the eldest. The winner is the declarer, their bid is the contract T, and their suit is trump. The other two players are the defenders and form a team for this deal.

MARRIAGES (announced right after bidding). Every player who holds both the K and the O of one suit has a marriage in that suit. A marriage is worth 40 in the trump suit and 20 in any other suit, and it belongs to its holder's side (declarer or defenders). The engine publicly announces every marriage, its holder and its value. At the end of the deal a side's marriages count only if that side won at least one trick.

PLAYING A TRICK. The declarer leads the first trick of the deal. After that, the winner of the previous trick leads. Starting with the leader, each player in seat order plays one card, and each card is announced to all. The leader may play any card. For the other players:
(a) If you hold a card of the led suit, you must play that suit. You must also play one that beats the highest card of the led suit already in the trick, if you can. This beating duty is lifted only when the led suit is not trump and a trump has already been played to this trick.
(b) If you hold no card of the led suit but hold a trump, you must play a trump. It must beat the highest trump already in the trick, if you can.
(c) Otherwise you may play any card.
If a player names a card that is illegal or not in their hand, the engine plays for them the legal card of lowest rank; among equal ranks, the first in the suit order.
The trick is won by the highest trump in it, or by the highest card of the led suit if it holds no trump. Equivalently, each card gets the key rank + 10 if it is trump + 5 if it is of the led suit, and the highest key wins. The card points of the trick, plus 10 if it is the 6th trick, go to the winner's side: the declarer alone, or the defenders together. The engine announces the trick winner and both sides' running points.

END OF DEAL (after the 6th trick).
1. The declarer's tally is the declarer's points (including any last-trick 10), plus the declarer's marriages if the declarer won at least 1 trick, minus the defenders' marriages if the defenders won at least 1 trick.
2. Let S = (T − 40) / 10, so a contract of 50 gives S = 1 and 150 gives S = 11.
3. If the tally is at least T, the contract is made and S is unchanged. Otherwise S becomes −(S + 1).
4. If trump is Hearts, S is doubled.
5. The declarer's score changes by 2×S, and each defender's score changes by −S.
6. The engine announces the tally, whether the contract was made, and all scores.

ENGINE STEP LIST (per round; steps marked [trick 1] run only in the first round of a deal, and steps marked [trick 6] only in the last).
1. [trick 1] Shuffle and deal 6 hidden cards to each player and 2 to the talon.
2. [trick 1] Reset the declarer's points, the defenders' points and the declarer's tricks to 0.
3. [trick 1] Simultaneous poll: bid and suit.
4. [trick 1] Calc: apply the invalid-input rules; set declarer, T, trump, and leader = declarer.
5. [trick 1] Calc: the marriage values of the declarer's side and of the defenders' side.
6. [trick 1] Announce the bids, declarer, contract, trump and marriages.
7. Clear the list of cards in the current trick.
8. The leader chooses a card.
9. Validate or apply the fallback; remove the card from the hand, add it to the trick list, announce it.
10. The next player chooses a card.
11. Validate, remove, add and announce as in step 9.
12. The third player chooses a card.
13. Validate, remove, add and announce as in step 9.
14. Calc the trick winner by maximum key. Add the trick points (+10 on trick 6) to the winner's side, add 1 to the declarer's tricks if the declarer won, set the leader to the winner, and announce.
15. [trick 6] Calc the tally, S, the fail transform, Hearts doubling and all score changes.
16. [trick 6] Announce the tally, the result and the scores.
17. Advance the round counter.
18. [round 36] End the match and decide the winner.

ATTRIBUTES (16). Per player (4): score, hand, bid, bid suit. Table (12): round number, talon, declarer, contract T, trump, leader, cards in the current trick, declarer's points, defenders' points, declarer's tricks, declarer-side marriage value, defender-side marriage value. The deal number, trick number and eldest are derived from the round number. The defenders' trick count is (tricks completed − declarer's tricks).

Objective: After round 36 (6 deals), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw. Every deal is zero-sum (the declarer gains 2×S, and each defender loses S), so the totals always sum to 0.

Expected effect: The sealed simultaneous bid makes each player weigh their own hand against what the others might hold. They must also guess whether a rival will outbid them, because overbidding is punished by the extra −1 on failure and by doubling under Hearts. The eldest's forced 50 rewards careful trump choice and good declarer play with weak cards. Defenders must coordinate through their card play alone: signalling by the suits they discard, saving Tens, and timing the last trick. Simple policies lose. Always bidding 150 fails essentially every time, at −24 or worse per deal. Always passing leaves the eldest exposed to forced 50 contracts and hands every profitable contract to the opponents. Always naming Hearts doubles losses as much as gains. Each player is eldest twice, so seats are balanced. There is no talk: the only conflict is between the declarer and the defending team, the defenders share one objective, and messages would only allow illegal signalling.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
