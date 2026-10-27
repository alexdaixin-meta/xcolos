# Variation: Coyote: Around the Fire

Each player sees every feather but their own. Declarations of the feather total climb by at least 1 around the table, lap after lap, until someone calls Coyote. A wrong declarer or a wrong caller takes a token. The opener rotates every hand, three tokens eliminate a player, and the last survivor wins.

Players: 3 to 4, best with 4

## Review of the original

Coyote is a bluff-and-deduction game. Each player wears a feather card they cannot see but everyone else can. Players take turns declaring ever-higher estimates of the total of all feathers, until someone calls 'Coyote'. If the true total is below the last declaration, the declarer takes a token; otherwise the caller does. Three tokens eliminate a player, and the last survivor wins. The previous variation capped each hand at 4 turns, used a 33-card deck, forced an opening floor of 3×players and a +3 minimum raise, and made the loser open the next hand.

- **non_degenerate**: bad. The previous variation has a structural seat edge. Testing gave these loss rates per hand: opener ≈ 0.43, turn 2 ≈ 0.12, turn 3 ≈ 0.31, turn 4 ≈ 0.14, against a fair share of 0.25. The opener is hurt by the forced floor F = 3N, which sits near the median total. Turn 3 is hurt because R9 punishes a true claim when turn 4 declares truthfully. 'Loser opens' then puts the last loser into the worst seat, so tokens snowball onto whoever lost first. No simple policy is unbeatable: always calling at turn 2 loses ≈57% and always raising the minimum at turn 4 loses ≈70%. The imbalance comes from move order, not play.
- **skill_sensitive**: bad. Under sensible play the loser is fixed by which band the true total falls in: below 12 the opener loses, 12–14 turn 2, 15–17 turn 3. Inside a band the stuck player loses whatever they choose, because their uncertainty is one card with SD 5.7 against a forced step of 3. About 60–70% of hand outcomes are set by the deal plus seat. The 4-turn cap stops the real Coyote contest of creeping toward the true total and judging when to stop.
- **headroom**: weak. Skill matters only near band edges, roughly 2 decisions per hand. Little can be learned beyond 'declare the minimum when likely true, call when likely false'. Weak players are not shut out, but strong players cannot pull away.
- **reasoning_dependent**: weak. The hidden information is genuine: you see everyone's card but your own, and others' declarations leak information about yours. However, the +3 step, the 4-turn cap and the huge card spread (−10 to 20) leave too few turns for that leaked information to be used before the band decides the hand.
- **verifiable**: good. The true total, the comparison with the last declaration, the token and elimination are all arithmetic. No judge is needed.
- **fits_platform**: good. The game is turn-based, text-only, has one hidden card per player and one shuffle per hand, and has no board. It fits the limits, though the 4-turn hand cap was a workaround that damaged the game.

## Problems

- P1: The forced opening floor (3 × players) sits near the median total, so the opener's claim is false about 43% of the time before anyone thinks.
- P2: 'Loser opens next hand' sends the loser into the worst seat, so tokens snowball onto the first unlucky player.
- P3: The 4-turn cap with a turn-4 showdown (R9) punishes a TRUE claim by turn 3 and puts the end-of-hand burden on fixed seats instead of on whoever misjudges the total.
- P4: The +3 minimum raise creates 3-wide 'stuck' bands in which the player to act loses whatever they choose.
- P5: Card variance is too high (SD ≈ 5.7, values −10 to 20). One unseen card swamps everything that can be inferred from others' declarations.
- P6: Too few decisions per hand. Reasoning acts on about 2 choices, so the deal decides most hands.

## Changes

- Remove the hand turn cap. A hand passes around the table lap after lap, one lap per engine round, until someone calls Coyote. A new hand can begin only at the start of a round, and once Coyote is called the remaining turns of that round are skipped. (fixes: P3): This restores real Coyote. Nobody is forced to end the hand by seat. The loss lands on whoever misjudges the total, or is caught when the declaration reaches it. It also keeps choice steps at no more than 4 per round and one deal per round.
- Abolish the R9 showdown. Every hand ends with a Coyote call: the declarer loses if the true total is below the declaration, otherwise the caller loses. (fixes: P3): A true claim is never punished, so the only ways to lose are overclaiming or calling a true claim.
- The opener may declare any whole number from −3 to 20. (fixes: P1): The floor of −3 is below almost every possible total, so the opener is no longer forced into a false claim. The opener chooses how aggressive to be.
- The opener rotates one surviving seat clockwise every hand, whoever lost. (fixes: P2): Every player opens equally often and there is no snowball.
- The minimum raise is +1. (fixes: P4): The 'stuck' situation shrinks to the single case where the declaration equals the true total exactly. Aiming at that exact value, and avoiding it, becomes the skill.
- Use a new 20-card deck: values −2 to 5 plus one Max→0. The card SD is about 2.0 and the 4-player total has mean ≈ 5.7. (fixes: P5): Your own-card uncertainty (about ±4) becomes comparable to what others' declarations reveal. Inference can narrow it, and totals are small, so hands last 1–3 laps.
- Each hand has many +1-sized decisions near the true total, made over several laps, with the full declaration history visible. (fixes: P6): Players can read jumps and hesitations, which carry information about their own card. They can jump to pin the next player or creep safely. This gives many reasoned decisions per hand.

## Kept from the original

- Each player's own feather is hidden from them and visible to everyone else.
- Strictly increasing declarations of the total of all feathers, ended by a 'Coyote!' call.
- The liar-or-caller rule: the declarer loses if the total is below the declaration, otherwise the caller loses.
- The special Max→0 card that cancels the highest feather.
- Coyote tokens, elimination at 3 tokens, and last survivor wins.

## The variation's rules

R1 Setup. Seats are numbered 1 to N clockwise (N is 3 or 4). Every player starts with 0 tokens and is alive. opener_seat = 1, hand_active = no, round = 1.

R2 Deck. The deck has exactly 20 cards:
- one −2
- two −1
- three 0
- three 1
- three 2
- three 3
- two 4
- two 5
- one special card, Max→0

R3 Start of a round. If hand_active is no, a new hand begins:
- The deck is restored to all 20 cards and shuffled.
- Each alive player is dealt exactly 1 card face-down.
- Each player is privately told the card of every other alive player, never their own.
- current_declaration is set to none and hand_active to yes.
- Everyone is told that a new hand begins and who opens it.
If hand_active is already yes, the hand in progress simply continues.

R4 Turn order. In every round the alive players take exactly one turn each:
- The first turn goes to the player in opener_seat, then each next alive player clockwise, so a round has as many turns as there are alive players (at most 4).
- The order is the same in every round of a hand, so a hand passes around the table lap after lap.
- If Coyote is called, the hand ends and any remaining turns of that round are skipped.
Before each turn, all players are shown the current declaration, who made it, and every declaration made so far this hand.

R5 A turn.
(a) If there is no declaration yet this hand, the player must declare a whole number from −3 to 20.
(b) Otherwise the player either declares a whole number at least current_declaration + 1 and at most 20, or calls Coyote. If current_declaration is 20, the player must call Coyote.
(c) A declaration makes that player the current declarer and the number the current declaration.

R6 True total. All cards are revealed to everyone.
- Add all card values, counting Max→0 as 0.
- If Max→0 was dealt, the single highest other dealt card counts as 0 instead, provided its value is positive. If several cards tie for highest, only one of them is cancelled.

R7 Resolving Coyote. Compute the true total.
- If the true total is less than the current declaration, the current declarer loses the hand.
- Otherwise the caller loses the hand.
The loser gains 1 token. All cards, the true total and the loser are announced to everyone. hand_active becomes no.

R8 Elimination. A player with 3 tokens is eliminated. They receive no more cards and are skipped in turn order.

R9 Next opener. After every hand, opener_seat moves to the next alive player clockwise from the current opener, whoever lost. If the current opener was just eliminated, it moves to the next alive player clockwise from their seat.

R10 End. The game ends immediately when only one player is alive, and that player wins. If round 40 ends first, any unfinished hand is discarded without a token. The alive player with the fewest tokens then wins; if two or more alive players tie for fewest, the game is a draw.

There is no table talk: declarations and calls are the only communication.

Objective: Be the last player not eliminated (3 tokens eliminate). If 40 rounds pass with more than one player alive, the alive player with the fewest tokens wins, and a tie for fewest is a draw.

Expected effect: Losses now fall on whoever misjudges the total, not on a seat. Every player opens equally often, a true claim is never punished, and the only 'stuck' case is the declaration equalling the total exactly.

Your own card (SD ≈ 2) is the only unknown, and everyone else's jumps, creeps and calls are evidence about it. The reasoning in play includes:
- inferring your own card from how far others dared to raise;
- jumping to exactly the likely total so the next player is pinned;
- creeping by +1 when unsure;
- calling when the declarer has stretched past what the visible cards support;
- opening with deliberately uninformative numbers so others learn less about their cards.

Simple policies all lose:
- Always calling loses to any true opening.
- Always raising by +1 eventually overclaims and is called.
- Always opening at 20 is called at once.

Luck remains in which player is facing the declaration when it reaches the true total. However, with +1 steps, many laps and visible histories, accurate inference shifts that risk onto weaker estimators.

Talk is left out. Only one player can win, so any message would be an unverifiable claim about another player's card, which careful players would ignore. Declarations already serve as the costly, informative signal.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
