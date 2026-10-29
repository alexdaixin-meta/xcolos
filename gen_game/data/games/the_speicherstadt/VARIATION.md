# Variation: Speicherstadt Queues (Even Rotation)

Players secretly hold a contract colour and queue workers on three goods per round. The first worker in each queue is offered the good at the queue's length, and the price falls by 1 with each decline. Over 12 rounds every seat holds every priority position equally often. Players infer rivals' colours from public queues and purchases, deny them, and bluff in simultaneous talk.

Players: 3 to 4, best with 4

## Review of the original

The Speicherstadt is a 2-5 player worker-placement auction. Players stack workers above revealed cards, the bottom worker may buy at a price equal to the stack height, and each decline drops the price by one for the next worker. Goods bought fill contracts or are sold, and the highest final total wins. The reviewed variation, Speicherstadt Queues, reduced this to 10 rounds of three one-good lots with secret contract colours, sealed price limits and a priority-ordered queue.

- **non_degenerate**: weak. In the reviewed variation, no simple policy wins. Always pass ends on 26 coins and loses to anyone who buys a good at or below its value. Always bid 6 on lots 1 and 2 pays 3-4 for goods that are 80% likely worth 2, and it leaves Lot 3 cheap for others. Always bid 1 only buys when last in the queue. Seat order did build in an edge, though. Priority leader = ((r-1) mod N)+1 over 10 rounds gives seat 1 four leads and seats 2-3 three leads at N=3. At N=4, seats 1-2 lead 3 times and seats 3-4 lead twice. Each extra lead is worth about 2-4 points in games scoring 30-45.
- **skill_sensitive**: good. Four skills separate players: setting limits by a good's value to you, spending 2 workers where queues will be short, buying to deny a rival's inferred colour, and hiding your own colour. All decks are equally supplied in each colour, so deal luck is limited to the order goods arrive.
- **headroom**: good. A weak player who buys own-colour goods at 5 or less still scores above the pass baseline. A strong player keeps improving by reading queue and buy histories for rivals' colours, timing denial buys, and bluffing in talk.
- **reasoning_dependent**: good. Contract colours are hidden and limits are sealed. What each player queued for and bought is public, so rivals' colours must be inferred from behaviour. With 5 colours and 3-4 players, some colours belong to nobody, and spotting them is valuable.
- **verifiable**: good. Purchases follow from limits, coins and priority order by fixed rules. The score is coins + 5 per own-colour good + 2 per other good, and the winner is the higher score with an arithmetic tie-break.
- **fits_platform**: good. The game uses sealed simultaneous numeric bids, one deck draw per round, simultaneous talk and 10 rounds. It has no board. The step count is about 12 per round.

## Problems

- Seat edge: over 10 rounds the rotating priority leader gives some seats more lead rounds and more early-queue positions than others (N=3: 4/3/3; N=4: 3/3/2/2). Leading is worth about 2-4 points, so seat order alone skews results.
- The rest of the priority order is also unbalanced: with 10 rounds, seats do not hold each queue position (2nd, 3rd, 4th) equally often, so the edge extends beyond the lead.
- Allowing 2 players turns the higher-total rule into a pure difference contest, and 5 players cannot be made to rotate evenly through the round count.

## Changes

- Play exactly 12 rounds with a 36-card deck: 6 colours (add Orange) × 6 cards each. Contracts are dealt from the 6 colours. (fixes: Seat edge: over 10 rounds the rotating priority leader gives some seats more lead rounds and more early-queue positions than others (N=3: 4/3/3; N=4: 3/3/2/2). Leading is worth about 2-4 points, so seat order alone skews results.): 12 is a multiple of 3 and of 4. Under the rotation, each seat holds every priority position (1st, 2nd, 3rd, 4th) exactly 12/N times: 4 times each at N=3, 3 times each at N=4. Each colour still appears exactly 6 times, so every contract stays equally supplied.
- The priority order each round is a full cyclic rotation starting from seat ((round-1) mod N)+1. It is stated as covering all positions, not just the leader. (fixes: The rest of the priority order is also unbalanced: with 10 rounds, seats do not hold each queue position (2nd, 3rd, 4th) equally often, so the edge extends beyond the lead.): With 12 rounds the rotation is a complete set of cyclic shifts repeated 12/N times, so every seat has an identical distribution of queue positions.
- Restrict the game to 3 or 4 players. (fixes: Allowing 2 players turns the higher-total rule into a pure difference contest, and 5 players cannot be made to rotate evenly through the round count.): With three or more players, one rival's gain is not another's loss, so the higher-total rule does not collapse into a difference contest. 12 rounds rotate evenly for both counts.
- Starting coins stay at 6 and income stays at 2 per round, so pass-only play reaches 30 coins. Limits stay 0-6. (fixes: Seat edge: over 10 rounds the rotating priority leader gives some seats more lead rounds and more early-queue positions than others (N=3: 4/3/3; N=4: 3/3/2/2). Leading is worth about 2-4 points, so seat order alone skews results.): The price scale (1-4) against values (2 or 5) is unchanged, so the tested economics carry over. The 12th-round tie-break remains arithmetic.

## Kept from the original

- Workers queue on revealed goods, the first in the queue is offered the price equal to queue length, and each decline drops the price by 1 for the next worker.
- Secret contract colour: own-colour goods are worth more than others.
- Each player has a limited number of workers per round (2 for 3 lots), so placement is a real choice.
- Coins plus goods value scoring, with the highest total winning.
- A seasonal deck that runs out to end the game.

## The variation's rules

SETUP: There are 6 colours: Red, Blue, Green, Yellow, Purple, Orange. The deck has 36 cards, 6 of each colour, shuffled once at the start. Each player is privately dealt a different contract colour, drawn at random from the 6 without repetition. No one else learns it. Each player starts with 6 coins and no goods. Players are numbered 1 to N (N = 3 or 4) in seating order.

The game lasts exactly 12 rounds. Each round:
1. SUPPLY: Reveal the top 3 cards of the deck as Lot 1, Lot 2 and Lot 3. Each lot is one good of the card's colour.
2. INCOME: Every player gains 2 coins.
3. PRIORITY: This round's priority order starts with player ((round - 1) mod N) + 1 and continues in seat order, wrapping around from N back to 1. It is announced. Over the 12 rounds every player holds each position in the priority order exactly 12/N times.
4. TALK: Everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.
5. QUEUE (secret, simultaneous): Each player submits three whole numbers, one per lot, each from 0 to 6.
   - A 0 means no worker on that lot.
   - A positive number places a worker there, and that number is the highest price the player will pay for that lot.
   - Each player has 2 workers, so at most 2 of the 3 numbers may be positive. If more than 2 are positive, only the positive entries on the two lowest-numbered lots count, and the rest become 0.
6. RESOLVE Lot 1, then Lot 2, then Lot 3:
   - The queue for a lot is every player with a positive number on it, ordered by this round's priority order. Let k be the queue length.
   - The offer starts at price k and goes to the first player in the queue.
   - If that player's limit is at least the current price and they hold at least that many coins, they pay that many coins to the bank and take the good.
   - Otherwise they decline, the price drops by 1, and the offer passes to the next player in the queue. The k-th player is therefore offered price 1.
   - If nobody buys, the card is discarded. A lot with an empty queue is discarded.
   - Coins spent on an earlier lot this round count when checking later lots.
7. ANNOUNCE: For each lot, announce which players queued, who bought it (if anyone) and the price paid. Limits are never revealed. Every player's coins and goods held (with colours) are public at all times.
8. END CHECK: After round 12 the deck is empty and the game ends.

FINAL SCORING: Each player's score is their coins, plus 5 points for each good of their own contract colour, plus 2 points for each good of any other colour. All contract colours are then revealed.

Objective: The player with the highest final score wins. If several tie for highest, the tied player with more goods of their own contract colour wins. If they are still tied, the game is a draw among them. If all players finish equal on both measures, the game is a draw.

Expected effect: Seat order no longer matters: every seat leads, and sits second, third and fourth, equally often, so differences in results come from play. The economics are unchanged from the tested version.
- A good worth 5 to you nets +1 to +4 at prices 4 to 1. A good worth 2 nets +1 at price 1, 0 at price 2, and a loss above that.
- Always pass ends on 30 and loses to any player who buys sensibly.
- Always bidding 6 on two lots overpays for goods worth on average 2.5 (1/6×5 + 5/6×2) and leaves the third lot cheap for others.
- Always bidding 1 only wins goods when last in the queue and is outscored by players who pay 2-4 for their own colour.
With 6 colours and 3-4 players, 2-3 colours belong to nobody. Identifying rivals' colours from their queues and buys, and denying them while hiding your own, is the core reasoning task.
Talk passes both tests. Players disagree because only one can win and each wants short queues on their own colour and long ones on rivals'. A player might claim a colour to scare others off a lot, or feign disinterest to buy cheaply. A player who simply follows a rival's suggestion ('I'll stay off Lot 2 if you stay off Lot 1') can be undercut when the rival queues anyway or was steering them away from the rival's own colour. They can also reveal their contract colour through what they agree to.
There is no endgame unravelling: the game is not about sustaining cooperation, and each round's purchases are independent value decisions.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
