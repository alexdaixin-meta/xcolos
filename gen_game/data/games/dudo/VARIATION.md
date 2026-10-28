# Variation: Four-Bid Dudo

Two-player Dudo with wild ones, a four-action cap on bidding each round, an alternating opener and elimination at 0 dice. When the current bid is the maximum (T sixes), the player to act must call Dudo.

Players: 2 to 2, best with 2

## Review of the original

Dudo (Perudo) is a bluffing dice game for 2 to 10 players. Each player hides a cup of dice, players make rising claims about how many dice of a face exist across all cups (ones are wild), and anyone may call 'Dudo' to challenge the standing claim. The loser of each challenge loses a die, and the last player holding dice wins.

- **non_degenerate**: good. Simple policies all lose. 'Always call Dudo' loses to an opener who bids near the expected count. 'Always raise by the minimum' walks into a challenge on an impossible bid. 'Always bid high' is caught. Seat advantage from bidding first is balanced by rotating who starts. Every choice moves the probability of losing a die.
- **skill_sensitive**: good. Each roll is random, but losing a die needs a misjudged bid or call. A player who conditions on their own dice and reads the opponent's bids as evidence beats one who does not, over many challenges. In the 2-player cut, the game ends only after 5 lost dice, which averages out the luck of single rolls.
- **headroom**: good. Basic play is easy to learn: bid about a third of the table plus your own matches. Strong play is not solved within a few rounds. It needs Bayesian updating on bids, bluffing about which face you hold, adjusting as dice counts shrink, and exploiting the opponent's calling tendencies. A weak player still wins some challenges.
- **reasoning_dependent**: good. Every die is hidden from the opponent. Each bid is a signal that may be honest or a bluff. Deciding to raise or challenge requires inferring the opponent's dice from their bids and modelling whether they bluff.
- **verifiable**: good. A challenge is settled by counting the dice showing the bid face plus ones against the bid quantity. Elimination follows from dice counts. No judge is needed.
- **fits_platform**: weak. The original has up to 10 players and 50 dice. Its bidding chain is unbounded within a round, so the round has no fixed step count. Ace-switching (halve, or more than double) adds rule branches. A long multi-player elimination can exceed the step and round limits. The previous 2-player, four-bid cut fits the limits, but it left the 'T sixes' dead end undefined at steps 3 and 4.

## Problems

- The unbounded bidding chain gives a round no fixed number of steps, which the engine needs (at most 20 steps and 4 choices per round).
- With up to 10 players the game is long and has a large hidden state, and players knocked out early sit idle.
- Ace-switching rules (halve rounded up, or more than double) add branches that models misapply and that cost steps.
- Gap in the previous variation: the highest possible bid, T sixes, can be the current bid at step 3 (after an opening of T sixes) or at step 4 (after the responder raises to T sixes). No raise exists there, so the rule 'an illegal raise is replaced by the lowest higher bid' is undefined. Forced Dudo was stated only for step 5.
- Gap in the previous variation: the rule for an unreadable response did not say what happens when no legal raise exists, and did not say whether an unreadable response could be read as Dudo.

## Changes

- Two players only, 5 dice each, with the opener role alternating every round. (fixes: With up to 10 players the game is long and has a large hidden state, and players knocked out early sit idle.): This keeps the hidden state small and the game short (at most 9 rounds, since exactly one die is lost per round). Alternation removes any seat edge.
- Each round is capped at four bidding actions: opening, answer, answer, and a final answer. A final raise is resolved immediately as if the opener had challenged it. (fixes: The unbounded bidding chain gives a round no fixed number of steps, which the engine needs (at most 20 steps and 4 choices per round).): Every round then has a bounded, flat step list within 4 choice steps, using per-step 'when' conditions only.
- Ones are wild but can never be bid as a face. Bid order is quantity first, then face. The opening quantity floor is Q0 = ceil(T/3) and the cap is T. (fixes: Ace-switching rules (halve rounded up, or more than double) add branches that models misapply and that cost steps.): This removes ace-switching while keeping the wild ones that make Dudo recognisable. The floor stops trivially safe openings.
- Forced Dudo at every answer step. At steps 3, 4 and 5, if the current bid is quantity T and face 6, the player to act must call Dudo, and any other response counts as Dudo. Opening or raising to T sixes stays legal. (fixes: Gap in the previous variation: the highest possible bid, T sixes, can be the current bid at step 3 (after an opening of T sixes) or at step 4 (after the responder raises to T sixes). No raise exists there, so the rule 'an illegal raise is replaced by the lowest higher bid' is undefined. Forced Dudo was stated only for step 5.): This defines the only dead end in the bid order. It keeps the real tactic of a 'T sixes' bid that forces the opponent to challenge, which is true with probability 1/3 at T=2 when you hold a 1 or a 6.
- Explicit default rule. An unreadable or illegal opening becomes Q0 twos, which always exists. An unreadable or illegal answer becomes the lowest legal raise if one exists, and otherwise Dudo. The response is counted as Dudo only if it clearly says Dudo, or if no raise exists. Every replacement is announced. (fixes: Gap in the previous variation: the rule for an unreadable response did not say what happens when no legal raise exists, and did not say whether an unreadable response could be read as Dudo.): Every response then has exactly one defined outcome.

## Kept from the original

- Concealed dice: each player sees only their own.
- Rising bids of 'at least Q dice show face F' across the whole table.
- Ones are wild.
- Calling Dudo to challenge. A true bid costs the caller a die and a false bid costs the bidder a die.
- Losing dice shrinks your information and the table total.
- The last player with dice wins (elimination).

## The variation's rules

SETUP: There are two players, each starting with 5 six-sided dice. Seat 1 is the opener in round 1. After that the opener role alternates every round. The other player in a round is the responder.

TERMS: A bid is two whole numbers: a quantity Q and a face F, where F is 2, 3, 4, 5 or 6. It claims that at least Q dice on the whole table show F. Every die showing 1 also counts as showing F (ones are wild). 1 can never be bid as a face. T is the total number of dice in play this round. Q must be between 1 and T. Bid B is higher than bid A if B's quantity is larger, or if the quantities are equal and B's face is larger. A raise must be higher than the current bid. The highest possible bid is 'T sixes'.

DEFAULTS: If the opening is illegal or unreadable, it is replaced by 'Q0 twos'. If an answer is illegal or unreadable, it is replaced by the lowest legal raise: the current quantity with the next higher face, or, if the face is 6, quantity plus 1 with face 2. If no legal raise exists, the answer is replaced by Dudo. Every replacement is announced.

FORCED DUDO: At steps 3, 4 and 5, if the current bid is quantity T and face 6, the player to act must call Dudo. Any other response from them counts as Dudo.

EACH ROUND:
1. Roll. All dice in play are rolled. Each player privately sees only their own dice. Both players are told T, Q0 = ceil(T/3) and each player's dice count. Examples: T=10 gives Q0=4, T=9 gives 3, T=4 gives 2, T=2 gives 1.
2. Opening (opener). The opener bids with quantity at least Q0 and at most T, with face 2 to 6. The bid is announced and becomes the current bid.
3. Answer (responder). The responder either calls Dudo or raises. A raise is announced and becomes the current bid. If Dudo is called, the opener is the bidder and the responder is the challenger; go to Resolution.
4. Answer (opener; only if no Dudo yet). The opener either calls Dudo or raises. A raise is announced and becomes the current bid. If Dudo is called, the responder is the bidder and the opener is the challenger; go to Resolution.
5. Final answer (responder; only if no Dudo yet). The responder either calls Dudo or makes a final raise. If Dudo is called, the opener is the bidder and the responder is the challenger. A final raise is announced and resolved immediately, with the responder as bidder and the opener as challenger. The opener makes no further choice.

RESOLUTION: All dice are revealed. Count the dice showing the bid face plus all dice showing 1. If the count is at least the bid quantity, the bid is true and the challenger loses one die. Otherwise the bid is false and the bidder loses one die. The count, the result and both dice counts are announced.

END OF ROUND: If a player has 0 dice, they are eliminated and the other player wins. Otherwise the opener role passes to the other player and a new round begins. Exactly one die is lost each round, so the game ends after at most 9 rounds.

Objective: Elimination. As soon as a player's dice count reaches 0, the other player wins. Exactly one die is lost per round, so the game always ends within 9 rounds and draws cannot occur.

Expected effect: Play centres on judging the bid against the expected count: a third of the opponent's dice plus your own matches, including ones. Players read the opponent's bids as evidence about their dice and bluff about which face they hold. Because a bid of T sixes forces Dudo at any answer step, a player can push the opponent into a challenge at the maximum, which matters most late in the game when T is small and every bid is a sharp probability call. The responder's last word (the final raise, resolved as a challenge by the opener) is offset by the opener's control of the opening and by alternating roles. Simple policies lose: always calling Dudo, always raising minimally, and always bidding the maximum are each beaten by a player who bids near the expected count. No talk is used, since with two players talk would only be cheap bluffing already captured by the bids.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 9 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
