# Hidden-Pot Ultimatum (Three Players)

Over six rounds each of three players twice proposes how to split a secret pot of 12 or 24. They offer each of the other two 0 to 6 points, and both must accept or the deal fails and the Proposer is penalised.

Players: 3 to 3, best with 3

## Parameters

- `num_players` = 3
- `num_rounds` = 6
- `starting_total` = 0
- `pot_low` = 12
- `pot_high` = 24
- `pot_sum` = 36
- `coin_heads_probability` = 0.5
- `offer_min` = 0
- `offer_max` = 6
- `fail_keep_loss_divisor` = 3
- `reject_penalty` = 1
- `proposer_round_1` = 1
- `proposer_round_2` = 2
- `proposer_round_3` = 3
- `proposer_round_4` = 3
- `proposer_round_5` = 2
- `proposer_round_6` = 1
- `tie_block_margin` = 1000

## Round

1. **update** (all players): round += 1; proposer = the seat for this round from the order 1,2,3,3,2,1; every player's offer = 0 and vote = ''.
2. **tell** (all players): Announce 'Round {round}: the Proposer is seat {proposer}; the other two seats are Responders.'
3. **update** (all players): If second_pot_s{proposer} == 0 (first proposal), flip a fair coin: on heads pot = 12, on tails pot = 24, then second_pot_s{proposer} = 36 - pot. Otherwise pot = second_pot_s{proposer}. Append pot to pot_history.
4. **tell** (seat {proposer}): Privately tell the Proposer: 'The pot this round is {pot}.'
5. **poll** (all players): Broadcast to all: 'Seat {seat} says: {value}'. All messages are shown only after all three are in.
6. **ask** (seat {proposer}): offer of the lower-numbered Responder = answer.
7. **ask** (seat {proposer}): offer of the higher-numbered Responder = answer.
8. **update** (all players): keep = pot - (sum of both Responders' offer), which is always at least 0. Append keep to keep_history.
9. **tell** (all players): Announce both offers: 'Seat X is offered {offer}, seat Y is offered {offer}.' The pot and the keep are not announced.
10. **poll** (the two Responders (every seat except proposer)): Each Responder's vote = answer. Both are chosen simultaneously.
11. **tell** (all players): Announce both votes.
12. **update** (all players): If both Responders' vote == accept: each Responder's total += their offer, and the Proposer's total += keep. Otherwise the Proposer's total -= floor(keep / 3) and no offer or keep is paid. In either case, each Responder with vote == reject has total -= 1.
13. **sync** (all players): Each player is privately sent their own new total.
14. **update** (all players): When round == 6: top_total = the maximum total over all players; top_count = the number of players with total == top_total; every player's total becomes public.
15. **tell** (all players): When round == 6: reveal pot_history, keep_history and every player's total.
16. **check** (all players): If round == 6, end the game; otherwise continue to the next round.

## Ending

- ends when: round == 6
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- min_to_win: `top_total + 1000 * (top_count - 1)` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: Each player's standing is their final total. The single player with the strictly highest total wins. If two or three players tie for the highest total, the bar cannot be reached, nobody wins, and the game is a draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. The proposer schedule (1,2,3,3,2,1) and the two-Responder unanimity rule are built for exactly three seats, so no other size is defined. The minimum is 3 because the schedule needs three seats, and the maximum is not larger because the schedule names only three.
- Keep the simultaneous talk step as a poll with a broadcast: The rules require it. It earns its place because the Proposer's interest (claiming a small pot to justify low offers) conflicts with the Responders' interest (believing the pot is large and demanding more), and Responders can coordinate threats to reject.
- The coin flip is made at each seat's first proposal, and the second pot is stored in hidden table attributes second_pot_s1, second_pot_s2 and second_pot_s3: This matches the source exactly: no seat learns its pot order before its first proposal, so the order stays secret until then.
- The two offers are asked as two consecutive number questions to the Proposer, lower-numbered Responder first: A question takes one whole number. The Proposer answers both before anyone sees them, because the offers are only announced afterwards.
- Strategy at the table: A thoughtful Proposer weighs bluffing about the pot against the risk of a rejection that costs a third of the keep. A thoughtful Responder judges whether an offer is fair given the hidden pot, remembers that rejecting costs 1 point, and uses the reversed schedule (rounds 4 to 6) to reward or punish earlier Proposers.

## Simplifications

- A draw (a tie for the top total) is expressed as 'nobody wins' through min_to_win = top_total + 1000 * (top_count - 1): The engine shares the win among tied leaders by default. Raising the bar out of reach when more than one player holds the top total reproduces the source's 'tie is a draw' with no winner.
- Totals are switched from owner-only to public at the end of round 6: The source reveals every total at the end, so the end-of-game reveal is done by changing visibility as well as by announcement.

## Unsupported (needs engine work)

- none
