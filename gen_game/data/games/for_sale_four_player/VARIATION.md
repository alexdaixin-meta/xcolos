# Variation: For Sale: Sealed Bids - Four Player

Four players sealed-bid for properties over 7 rounds, then simultaneously play properties to capture cheques over 7 rounds; most cheques plus leftover coins wins.

Players: 4 to 4, best with 4

## Review of the original

For Sale: Sealed Bids adapts the two-phase For Sale auction for 3 players with simultaneous sealed buying bids and simultaneous property plays for cheques, won by most cheques plus leftover coins.

- **non_degenerate**: good. After the fix no bid is free: winner pays full bid, ranks 2-4 pay ceil(bid/2), so 0 risks LOW and 1 always costs 1. Always-0 gets only LOWs, always-max burns 18 coins in few rounds, always-play-high wastes high cards on low cheque boards; each loses to a counter.
- **skill_sensitive**: good. Only 2 of 30 properties and 2 of 30 cheques stay unseen; 28 of each are revealed in order. Bidding to price rank, saving coins (1 saved = 1 final money), and timing which property to spend on which 4-cheque board outweigh the small deck-order luck over 14 rounds.
- **headroom**: good. 7 buys and 7 sells with private budgets leave budget-tracking, bid-shading, and property-timing to improve; weak players still score cheques plus saved coins, so not hopeless and not solved.
- **reasoning_dependent**: good. Coins are private and bid amounts are never announced, only who took HIGH/SECOND/THIRD/LOW. Players must infer rivals' remaining coins and willingness to pay from 7 rounds of takes, and infer who is ahead from announced property and cheque takes.
- **open_play**: good. From a fixed deal at least two plans can win: economize and win on saved coins plus mid cheques, or pay for HIGH properties to capture 15s/14s. Whether to contest HIGH or settle for SECOND depends on rivals' bids, and whether to spend a high property depends on the 4-cheque board.
- **verifiable**: good. Final money = cheque total + remaining coins, both integers; winner is max, tie-break more remaining coins, then shared draw. No judge decides.
- **fits_platform**: good. Text-only, 14 fixed rounds, one simultaneous poll per round, one shuffle per phase, public hands and reveals, private coins/cheques, arithmetic ranking. No board, map, trading, or sequential auction.

## Problems

- Free minimal bids: under pay-half-rounded-down, bids of 1 cost 0 unless first, so 39 of 72 sealed bids were 1 and in 10 of 24 rounds every bid was 0 or 1, so rotating priority not reading rivals decided who took the best card.
- Three-player field only gave two rivals to model and an easier win, against the owner's request for four players and harder winning.
- Original open clockwise raise-or-pass auction cannot run on the turn-based simultaneous-poll engine.

## Changes

- 4 players, 18 coins each, 28 properties and 28 cheques used: 7 buying rounds and 7 selling rounds of 4 cards, bottom 2 of each deck unseen; buying rank 1 takes HIGH, rank 2 SECOND, rank 3 THIRD, rank 4 LOW; priority rotates ((r-1) mod 4)+1. (fixes: Three-player field only gave two rivals to model and an easier win, against the owner's request for four players and harder winning.): More opponents to model and harder win using original 4-player numbers, keeping two phases and deck sizes.
- Buying payments: first-ranked pays full bid, second-, third- and fourth-ranked each pay half their bid rounded UP (ceil). Bid range stays 0 to current coins, one simultaneous sealed bid, totals private. (fixes: Free minimal bids: under pay-half-rounded-down, bids of 1 cost 0 unless first, so 39 of 72 sealed bids were 1 and in 10 of 24 rounds every bid was 0 or 1, so rotating priority not reading rivals decided who took the best card.): Every positive bid now has real cost win or lose (1 always costs 1, 2 costs 1-2, etc.) while 0 is free but risks LOW, so amounts carry information about valuation and remaining budget.
- Kept sealed simultaneous buying and simultaneous selling instead of open auction. (fixes: Original open clockwise raise-or-pass auction cannot run on the turn-based simultaneous-poll engine.): Platform cannot run open ascending auction; sealed bids fit simultaneous polls and preserve bluff and inference.

## Kept from the original

- Two phases: buy properties with coins, then play properties to take cheques.
- Property cards 1-30 and cheques 0 and 2-15 two of each.
- Public property hands, private coins and private cheque totals, one shuffle per deck.
- Simultaneous selling where highest property takes highest cheque with no ties.
- Final money cheques plus remaining coins with coin tie-break and shared draw.

## The variation's rules

SETUP. 4 players numbered 1, 2, 3, 4. Each starts with 18 coins (private) and 0 cheques (private cheque total) and empty property hand (public). Property deck: cards 1 to 30, one each. Cheque deck: values 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15, two of each, 30 cheques. Game lasts 14 rounds: rounds 1-7 BUYING, rounds 8-14 SELLING. No talk phase: every choice is sealed to preserve bluff; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW. BUYING ROUND (rounds 1-7): 1. In round 1 only, shuffle the property deck. Only the top 28 cards will ever be used; the bottom 2 stay unseen. 2. Reveal the next 4 cards from the property deck. Sort them and call them HIGH, SECOND, THIRD, LOW by value. 3. All players at the same moment secretly submit a bid: whole number 0 up to current coins. 4. Rank bids highest to lowest. Break ties by priority order: in round r priority goes first to player ((r-1) mod 4)+1, then next number wrapping 4 to 1. 5. First-ranked takes HIGH and pays full bid. Second-ranked takes SECOND and pays half bid rounded UP. Third-ranked takes THIRD and pays half bid rounded UP. Fourth-ranked takes LOW and pays half bid rounded UP. Example: bid 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. 6. Payments go to the bank from private coins. 7. Announce publicly which player took HIGH, SECOND, THIRD, LOW. Bid amounts and coin totals are NOT announced. After round 7 each holds 7 properties. SELLING ROUND (rounds 8-14): 1. In round 8 only, shuffle the cheque deck. Only the top 28 cheques will ever be used; bottom 2 unseen. 2. Reveal the next 4 cheques from the cheque deck, sorted highest to lowest. 3. All players at the same moment secretly choose one property from own hand. 4. Reveal chosen properties. All properties are different so no ties. 5. Highest property adds highest cheque to cheque total; second-highest adds second-highest cheque; third adds third; lowest adds lowest. 6. Played properties are discarded. 7. Announce publicly who played which property and who took which cheque. Running cheque totals stay private. END. After round 14 hands are empty. Reveal cheque totals, remaining coins, and final money = cheque total + remaining coins.

Objective: Player with most final money (cheques plus remaining coins) wins. If tied for most, tied player with more remaining coins wins. If still tied, game is a draw among them.

Expected effect: Bidding 1 now costs 1 win or lose, so cheap bids signal real valuation and budget and can be read; mass 0/1 bidding no longer free-rides on priority because 0 concedes HIGH/SECOND. Players disagree on who gets HIGH versus who saves coins: all want HIGH cheap, but only one rank gets it each round, and a player who just follows a rival's low-bid suggestion pays by taking LOW while the suggester deviates to take HIGH. Four rivals widen inference and timing play in selling.

## Complexity (the designer's count, against the limits)

- steps_per_round: 5 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 14 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
