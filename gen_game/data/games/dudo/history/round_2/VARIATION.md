# Variation: Short Dudo

A compact Dudo for 2 to 4 players. Each round has a single hidden roll, an opening bid, up to two escalating raises, and a forced Dudo or Calza at the end. Losing all your dice eliminates you. The last player with dice, or the player with the most dice after 30 rounds, wins.

Players: 2 to 4, best with 3

## Review of the original

Dudo (Perudo) is a bluffing dice game for 2 to 10 players. Each player rolls hidden dice, players take turns bidding ever-higher claims about how many dice of a face are on the table (ones are wild), and a challenge ('Dudo') reveals the dice and costs the wrong party a die. The last player with dice wins.

- **non_degenerate**: good. Every simple policy loses. Always calling Dudo loses about half the time against honest openings near T/3, which is the expected count of a face once ones count as wild. Always raising runs into an impossible bid that gets called. The starting seat changes each round because the loser opens.
- **skill_sensitive**: good. Each roll is random, but over many rounds the better player wins by judging probability from their own dice and reading what opponents' bids imply. The ace-conversion rules add skilled edge cases.
- **headroom**: good. Beginners can play to the expected count. Experts track bidding patterns, bluff deliberately and adjust as dice counts shrink. The game is not solved for several players.
- **reasoning_dependent**: good. The core of the game is hidden dice. Players infer opponents' hands from their bids and choose between bluffing and challenging.
- **verifiable**: good. A challenge is settled by counting the revealed dice. Elimination and the winner follow by arithmetic.
- **fits_platform**: weak. Bidding is open-ended, so the number of choice steps per round is unbounded. The ace halving and doubling rules add rule chains. Ten players with five dice each is long and exceeds the attribute limits. Play is turn-based and text-only, which suits the platform.

## Problems

- Unbounded bidding chains exceed the limit of 4 choice steps per round.
- The ace conversion rules (halve or more than double) add complexity without adding much reasoning at small scale.
- Up to 10 players with 5 dice each exceeds the attribute and step budgets, and games can run very long.
- Previous variation: a separate random draw to pick the first opener put hand 1 at two random draws, over the limit of 1.
- Previous variation: it did not say that the dice roll is a single deal operation, so the roll looked like many independent draws, and it did not say that N is a single count.
- Previous variation: with T=2 the opening bound floor(T/3)=0 allowed a Q=0 bid. Such a bid is always true, so it is not a claim, and Dudo against it always loses.

## Changes

- Each round has at most 4 choice steps: an opening bid, up to two responses that can raise by +1 or +2, and a final forced Dudo or Calza. (fixes: Unbounded bidding chains exceed the limit of 4 choice steps per round.): Keeps the round within 4 choice steps while keeping the escalation of bids and the bluff-or-call tension.
- Ones are always wild, and bids may only name faces 2 to 6. There is no switching to aces. (fixes: The ace conversion rules (halve or more than double) add complexity without adding much reasoning at small scale.): Removes a special-case rule chain, while the wild ones still make counting interesting.
- 2 to 4 players with 5 dice each, and a cap of 30 rounds after which the player with the most dice wins. (fixes: Up to 10 players with 5 dice each exceeds the attribute and step budgets, and games can run very long.): Keeps the hidden state within 20 dice and the game short enough to play.
- The separate first-opener draw is removed. Seat 1 opens round 1, and afterwards the loser opens as in the original. (fixes: Previous variation: a separate random draw to pick the first opener put hand 1 at two random draws, over the limit of 1.): Every round, including round 1, then has exactly one random event: the roll. A one-time opening advantage is negligible over many rounds.
- The rules state that each round's roll is one deal operation that produces every player's hidden dice at once, and that N is computed by one count operation over all revealed dice. (fixes: Previous variation: it did not say that the dice roll is a single deal operation, so the roll looked like many independent draws, and it did not say that N is a single count.): Makes random_draws_per_round = 1 true by construction and keeps the step count fixed.
- The opening quantity bound becomes max(1, floor(T/3)) <= Q <= ceil(T/2). (fixes: Previous variation: with T=2 the opening bound floor(T/3)=0 allowed a Q=0 bid. Such a bid is always true, so it is not a claim, and Dudo against it always loses.): Every legal bid is now a real claim of at least one die. At T=2 the only opening quantity is Q=1.

## Kept from the original

- Hidden dice, with each player seeing only their own.
- Bids are claims about the whole table, and ones are wild.
- Bids must escalate, and players choose between raising and calling Dudo.
- The Calza (exact) call, which can win a die back.
- Losing a die for being wrong, elimination at zero dice, the loser opening the next round, and the last player with dice winning.

## The variation's rules

SETUP. 2 to 4 players sit in a fixed seat order: seat 1, seat 2, and so on. Each player starts with 5 dice. Seat 1 is the opener for round 1. There is no random draw before play.

EACH ROUND.
1. ROLL. In one deal operation, every player still in the game receives a fresh random roll of as many six-sided dice as they currently hold. This single operation produces all hands at once and is the only random event of the round. Each player is shown only their own dice. T is the total number of dice still in play, and every player is told T and every player's dice count.
2. OPENING BID (choice 1). The opener chooses a face from 2 to 6 and a quantity Q with max(1, floor(T/3)) <= Q <= ceil(T/2). The bid means 'at least Q dice among all players show this face, with every 1 counting as this face'. The bid is announced to all.
3. RESPONSE 1 (choice 2). The next player in seat order who is still in the game chooses one of four options:
   (a) Raise +1: the new quantity is the current quantity + 1, with any face from 2 to 6 the player chooses.
   (b) Raise +2: the new quantity is the current quantity + 2, with any face from 2 to 6 the player chooses.
   (c) Dudo: challenge the current bid as false.
   (d) Calza: claim the count is exactly the current quantity.
   A raise is illegal if the new quantity would exceed T. If both raises are illegal, only Dudo or Calza may be chosen. The choice is announced. A player who raises becomes the current bidder.
4. RESPONSE 2 (choice 3). This step happens only if response 1 was a raise. The next player in seat order who is still in the game makes the same kind of choice against the current bid. With 2 players, this is the opener again.
5. FINAL RESPONSE (choice 4). This step happens only if response 2 was a raise. The next player in seat order who is still in the game must choose Dudo or Calza. Raising is not allowed.
6. REVEAL. All dice are shown. N is the number of dice showing the current bid face plus the number showing 1, computed as one count over all dice.
7. SETTLE. If the call was Dudo: when N >= the current quantity, the caller loses 1 die; otherwise the current bidder loses 1 die. If the call was Calza: when N equals the current quantity exactly, the caller gains 1 die, up to a maximum of 5; otherwise the caller loses 1 die.
8. ELIMINATION. A player with 0 dice is out and is skipped in seat order from then on.
9. NEXT OPENER. The player who lost a die opens the next round. After a successful Calza, the caller opens. If that player was eliminated, the next player in seat order who is still in the game opens.
10. END CHECK. If only one player remains, the game ends. If 30 rounds have been played, the game ends. Otherwise a new round begins.

There is no talk phase. Bids and calls are the only communication.

Objective: If only one player has dice left, that player wins. If 30 rounds are completed with two or more players still in, the player holding the most dice wins. If two or more players tie for the most dice, the game is a draw.

Expected effect: Players must judge the likely count from their own dice and the expected one-third of the other dice, then read each raise as evidence about the bidder's hand. Bluffs that are too large get called, and calls made too eagerly lose against honest bids near T/3. Always calling Dudo, always raising and always calling Calza all lose to sensible play. The new opening floor guarantees every bid is a real claim, and each round has exactly one random event. Talk is left out: bids already carry the signalling, and there is no shared plan anyone could propose that others would gain by following.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
