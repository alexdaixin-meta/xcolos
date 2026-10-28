# Variation: Malý Mariáš (Little Mariáš)

A 12-card, 4-trick Mariáš for three players over 9 deals. Each deal, players bid in secret for the right to declare a trump suit and a card-point target out of 90. The two others defend together. Flek and re double the stakes, Hearts doubles them again, and the highest running total after 9 deals wins.

Players: 3 to 3, best with 3

## Review of the original

Mariáš is a Czech three-player trick-taking game with a 32-card deck. A declarer picks trump and a contract and plays against two defenders who are partners. Players must follow suit, head the trick and trump when void. Aces and Tens are worth 10 each, the last trick is worth 10, and marriages add points. Flek and re double the stakes, and there are special contracts (Betl, Durch, Seven, Hundred).

- **non_degenerate**: good. No simple policy wins. Always declaring loses against weak hands, and always passing gives up every strong hand. Flek every time pays double whenever the declarer makes the contract. The forehand advantage is balanced over a full rotation. Choices of trump, contract and card play decide most deals.
- **skill_sensitive**: good. Over many deals strong players beat weak ones reliably, through card counting, partnership defence and judging when to bid or flek. Any single deal is heavily card-driven.
- **headroom**: good. The game is deep and unsolved: inferring hands from play, defensive signalling, bid judgment and doubling psychology. A beginner who follows suit and bids only strong hands still scores.
- **reasoning_dependent**: good. Hands are hidden. Players must infer cards from the bidding and from voids shown in play, and plan over 10 tricks. Defenders must also cooperate without seeing each other's cards.
- **verifiable**: good. Card points, marriages and contract success are all arithmetic, and the stakes follow from the multipliers.
- **fits_platform**: bad. Ten tricks with must-head rules, a talon exchange, marriages, four special contracts and sequential flek/re chains exceed the step and choice limits. The previous built version crashed five times: drawing from an emptied deck, empty list searches for the trick winner, and unfilled {held} placeholders. It also showed empty bookkeeping fields to players.

## Problems

- P1: The full rules (32 cards, 10 tricks, talon exchange, marriages, Betl/Durch/Seven/Hundred) need far more steps and choices per round than the engine allows.
- P2: Dealing by repeated random index draws from a shrinking deck crashed with 'list index out of range' when the deck ran short or was not rebuilt.
- P3: Finding the trick winner by searching the trick list afterwards crashed with empty list comprehensions.
- P4: The 'must head the trick' duty and the illegal-card fallback made each play step hard to validate, and could produce a card that never landed in the trick.
- P5: Prompts embedded a {held} placeholder that the engine cannot fill, so players saw literal braces.
- P6: Internal bookkeeping fields (deal_result, last_card, trump before it was set) were printed empty to players.
- P7: The forehand who must name trump has a built-in edge or burden within a deal, so balance needs even rotation.
- P8: A sequential flek, then re, then further doubling chain costs several choice steps.

## Changes

- Shrink the deck to 12 cards: four suits (Hearts, Bells, Leaves, Acorns) times three ranks (A, 10, K). Deal 4 cards each with no talon, for 4 tricks per deal. Drop marriages and the special contracts. Card values stay A=10 and 10=10, and the last trick stays 10, so the total is still 90. (fixes: P1): This keeps the 90-point economy, the trump choice and follow/trump play, while one trick fits in one round with at most 4 choice steps.
- At the start of each deal, build a fresh list of the 12 card codes 0 to 11 and shuffle it once. Seat 1 takes positions 1-4, seat 2 positions 5-8, seat 3 positions 9-12. There are no index draws from a shrinking deck. (fixes: P2): A fixed-size permutation sliced at fixed positions cannot run out, and it is the round's only random draw.
- Track the trick winner with a running best_key and best_seat. The leader's card sets them. Each later card replaces them only if its key is strictly greater. The key is rank (K=0, 10=1, A=2), plus 10 if trump, plus 5 if of the led suit. (fixes: P3): No list search is needed, so nothing can come back empty.
- Use plain follow-suit: follow the led suit if able, otherwise trump if able, otherwise any card. An illegal or unheld card is replaced by the lowest-code legal card. A hand always has a card when its owner plays. (fixes: P4): Each play is one validated step, and the played card always exists and always enters the trick.
- Prompts contain no placeholders except {seat} and {value}. Each player's own hand is shown through their private hand attribute in their state view. (fixes: P5): Players never see unfilled braces.
- Hide the bookkeeping attributes (best_key, led_suit, deck, the bid's raw fields). Show only hand, score, trump, declarer, contract, multiplier, cards in the current trick, trick number and the points taken so far. (fixes: P6): The state view holds only usable information.
- Play 9 deals, with the eldest hand rotating 1, 2, 3, 1, ... so each seat is eldest exactly 3 times. The eldest cannot pass: an invalid entry or PASS from the eldest counts as '50 A'. Bid ties go to the player nearest the eldest in seat order. (fixes: P7): This preserves Mariáš's forced forehand while spreading that burden and privilege evenly.
- Make flek and re one simultaneous poll after trick 1. Each defender says FLEK or NO, and the declarer says RE or NO at the same moment. Any flek doubles the stake. RE doubles it again only if at least one flek was given. (fixes: P8): One choice step replaces a sequential chain, and the declarer must predict whether the defenders will flek.

## Kept from the original

- Three players: one declarer against two defenders in a temporary partnership
- The declarer names trump; must follow suit, else must trump
- Aces and Tens are 10 each and the last trick is 10, for a total of 90 card points
- Bidding a contract level with a forced forehand
- Flek and re doubling
- Hearts as trump doubles the stakes
- Zero-sum settlement: the declarer is paid by or pays each defender

## The variation's rules

CARDS. There are 12 cards: four suits, Hearts (H), Bells (B), Leaves (L) and Acorns (A), each with three ranks, Ace (A), Ten (10) and King (K). A card is written rank then suit, for example AH, 10L, KB. Internally, card code = 3 x suit index + rank index, with suits H=0, B=1, L=2, A=3 and ranks K=0, 10=1, A=2. Rank order within a suit is A > 10 > K. Card points: each Ace 10, each Ten 10, each King 0. Whoever wins the 4th (last) trick of a deal gets 10 more. The total per deal is 90.

STRUCTURE. The match is 9 deals of 4 tricks each, which is 36 rounds. Each round is one trick. The eldest hand of deal d is seat ((d-1) mod 3)+1, so seats 1, 2, 3, 1, 2, 3, 1, 2, 3. Every player starts with score 0.

WHAT PLAYERS SEE. Each player sees their own hand (private), all scores, the current deal and trick number, the declarer, contract and trump once set, the stake multiplier, the cards played so far in the current trick with who played them, the card points taken so far by the declarer and by the defenders, and every public announcement. Internal working values are not shown.

ROUND STEPS (steps marked [trick 1] or [trick 2] happen only in that trick of a deal):
1. [trick 1] Deal. Build the list of the 12 codes 0-11, shuffle it once, and give positions 1-4 to seat 1, positions 5-8 to seat 2 and positions 9-12 to seat 3. Reset the declarer points, defender points and multiplier to 1.
2. [trick 1] Bid (simultaneous, secret). Each player answers 'PASS' or 'N S', where N is 50, 60, 70, 80 or 90 and S is H, B, L or A. The eldest may not pass: PASS or any invalid answer from the eldest counts as '50 A'. An invalid answer from anyone else counts as PASS.
3. [trick 1] Resolve the bid. The highest N becomes the declarer, with contract N and trump S. On a tie, the tied player first in seat order starting from the eldest wins. The other two are defenders. Set base stake = N/10 - 4 (so 50→1, 60→2, 70→3, 80→4, 90→5). The declarer leads trick 1. Announce all bids, the declarer, the contract and the trump.
4. [trick 2] Flek poll (simultaneous). Each defender answers FLEK or NO, and the declarer answers RE or NO. Invalid answers count as NO.
5. [trick 2] Resolve. If at least one defender said FLEK, the multiplier is doubled. If, in addition, the declarer said RE, it is doubled again. Announce all answers and the multiplier.
6. First card. The leader names a card from their hand.
7. Resolve the first card. If the card is not in the leader's hand, the lowest-code card in their hand is played instead. Remove it from the hand and add it to the trick. Set led suit to its suit. Set best_key = rank index + (10 if its suit is trump) + 5, and set best_seat = the leader. Announce the card.
8. Second card. The next seat clockwise, (leader mod 3)+1, names a card.
9. Resolve the second card. The card is legal if: it is of the led suit; or the hand has no led-suit card and the card is trump; or the hand has neither led-suit cards nor trumps. If the named card is not held or not legal, play instead the lowest-code held card of the led suit, else the lowest-code held trump, else the lowest-code held card. Remove the card from the hand and add it to the trick. Its key = rank index + (10 if trump) + (5 if of the led suit). If its key is greater than best_key, set best_key to it and best_seat to this seat. Announce the card.
10. Third card. The next seat names a card.
11. Resolve the third card exactly as in step 9.
12. Award the trick. Add the trick's card points, plus 10 if this is trick 4, to the declarer's points if best_seat is the declarer, otherwise to the defenders' points. Set leader = best_seat. Announce the winner and the running points.
13. [trick 4] Settle the deal. Stake = base stake x multiplier x (2 if trump is Hearts, else 1). If the declarer's points are at least the contract N, the declarer gains 2 x stake and each defender loses stake. Otherwise the declarer loses 2 x stake and each defender gains stake. Announce the result and the scores.
14. Advance. Add 1 to the trick number. After trick 4, reset it to 1, add 1 to the deal number and rotate the eldest. After deal 9, the match ends.

There is no discussion phase. Hands are always non-empty when their owner must play, because each player plays exactly one card per trick and holds 4 cards for 4 tricks.

Objective: After 9 deals, the player with the highest score wins. If two or three players tie for highest, those players draw. Scores are the sum of the zero-sum deal settlements in step 13.

Expected effect: Bidding becomes a real judgment: hand strength, choice of trump, the risk of a Hearts contract and the stake level. The forced eldest must handle weak hands, which is spread evenly by rotation. The simultaneous flek/re poll rewards reading hand strength from the bids. Defenders must cooperate within a deal through card play alone (they read each other's discards and voids), while remaining rivals for the overall win, since both gain or lose equally in a deal but only one can finish first. Card counting over 4 tricks with 12 known cards rewards inference: by trick 3 a careful player can often deduce the remaining hands exactly. Simple policies all lose. Always passing leaves the eldest stuck with forced 50s and gives up strong hands. Always bidding 90 fails most deals at the maximum stake. Always flekking pays double whenever the declarer bid soundly. Always re-ing costs the declarer double whenever a flekked contract fails. Deal luck stays, but 9 deals and the freedom to bid low or pass let good players limit its effect. Talk is left out: the only conflict within a deal is declarer against defenders, and public talk between the defenders would reveal their hands to the declarer as well.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
