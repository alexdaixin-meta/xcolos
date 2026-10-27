# Variation: Coyote: Open Circle

Each player sees every card but their own and bids on the total of all cards. Bids strictly rise until someone calls Coyote. The loser of each round takes a token, three tokens eliminate a player, and the last player alive wins. Each round's turns run as a bounded loop of at most 16 turns that always ends in a call.

Players: 3 to 4, best with 4

## Review of the original

Coyote is a bluff-and-bid elimination game. Each player sees every feather card except their own. Players take turns raising a declared total of all cards in play until someone calls 'Coyote'. If the true total falls short of the last declaration, the declarer loses; otherwise the caller loses. Three losses eliminate a player, and the last survivor wins.

- **non_degenerate**: good. Simple policies can lose. 'Always call at once' loses whenever the opening bid is at or below the true total, and a low opening bid usually is. 'Always raise by 1' eventually overshoots the true total and loses as declarer. 'Always open high' loses when it is called. The opener seat rotates, so no seat keeps an edge. Winning means surviving, not having the highest total, so there is no safe option that cannot lose.
- **skill_sensitive**: good. Each player sees all cards but one, so a good player can estimate the total tightly from the known deck composition and from other players' bids. A weak player who ignores the distribution of their own unseen card, or who reads nothing from the bids, overshoots or calls too early. The deal randomises information, not advantage. Everyone has exactly one unknown card.
- **headroom**: good. A basic player can survive by bidding near the visible sum plus the expected value of their own card. Strong play adds several layers: inferring one's own card from what others bid, pushing a dangerous bid onto the next player, and timing calls. The Max→0 card makes totals uncertain in a way that needs real reasoning. The game is not solved and not hopeless.
- **reasoning_dependent**: good. Every player has hidden information, their own card. Bids leak information about that card because other players can see it. Doing well requires inference from limited information and modelling opponents.
- **verifiable**: good. The true total, the comparison with the last declaration, token counts and elimination are all arithmetic. No judge is needed.
- **fits_platform**: weak. The game is turn-based, text-only and has no board. However, the original has an open-ended deck with chained blue specials, and the reviewed variation had two build defects. First, its 15-turn cap could cut off the forced 16th call and leave a round with no caller. Second, its open 'lap after lap' turn loop gave no bounded repetition and no exit condition.

## Problems

- The original's blue special cards (draw from the deck, discard the highest, negate, double, reshuffle) form a long chain of rules that the engine cannot build reliably.
- The original's deck has no fixed composition here, so players cannot reason about the distribution of their unseen card.
- Turn cap defect: the reviewed variation capped a round at 15 turns. Declarations 1 to 15 can use all 15 turns, so the forced Coyote call on turn 16 could be cut off. That leaves caller = none and a round with no loser, which breaks the token rule.
- Turn loop defect: the reviewed variation's 'lap after lap' loop was not specified as a bounded counted repetition of one choice step with an exit condition. The build is ambiguous and the claim of one choice step per round was unsupported.

## Changes

- Keep a fixed 15-card deck that is reset and shuffled every round, with a single special card, Max→0, whose effect is fully specified with tie rules and examples. (fixes: The original's blue special cards (draw from the deck, discard the highest, negate, double, reshuffle) form a long chain of rules that the engine cannot build reliably.): This replaces the chained blue specials with one buildable rule. It also gives players a known distribution to reason about.
- Publish the deck list in the rules, so every player knows which cards could be their own. (fixes: The original's deck has no fixed composition here, so players cannot reason about the distribution of their unseen card.): This allows probabilistic inference about one's own card.
- Raise the cap to at most 16 turns per round: up to 15 declarations (1 to 15), then a forced Coyote call. Add a safety fallback: if 16 turns pass with no call, the next alive player after the current declarer is recorded as the caller and the round resolves normally. (fixes: Turn cap defect: the reviewed variation capped a round at 15 turns. Declarations 1 to 15 can use all 15 turns, so the forced Coyote call on turn 16 could be cut off. That leaves caller = none and a round with no loser, which breaks the token rule.): Every round now always has exactly one declarer, one caller and one loser.
- Specify the turns as a counted repetition of ONE choice step, at most 16 iterations, with a turn counter that picks the acting player. The repetition exits as soon as coyote_called = yes. When current_declaration = 15, the only legal option is Coyote. The first turn of a round may not call. (fixes: Turn loop defect: the reviewed variation's 'lap after lap' loop was not specified as a bounded counted repetition of one choice step with an exit condition. The build is ambiguous and the claim of one choice step per round was unsupported.): This makes the loop buildable on a flat step list and justifies counting one choice step per round.

## Kept from the original

- Each player sees every card but their own.
- Declarations must strictly rise until someone calls Coyote.
- Resolution: the declarer loses if the true total is below the declaration, otherwise the caller loses.
- One token per loss, three tokens eliminate, and the last player alive wins.
- A special card that alters the total (Max→0, the descendant of the blue cards).
- No talk phase: declarations are the only communication, because interests already conflict and the bids carry the information.

## The variation's rules

SETUP. Seats are numbered 1 to N clockwise, with N = 3 or 4. Every player starts with tokens = 0 and alive = yes. Set opener_seat = 1 and round = 1.

DECK. At the start of every round the deck is reset to exactly these 15 cards and shuffled:
- one -2;
- two -1;
- three 0;
- two 1;
- two 2;
- two 3;
- one 4;
- one 5;
- one Max→0 card.
Every player knows this list.

EACH ROUND:

1. RESET AND ORDER. Set current_declaration = none, current_declarer = none, coyote_called = no, caller = none and turn_count = 0. The turn order starts at opener_seat and goes clockwise through the alive seats, skipping eliminated seats. After the last alive seat it wraps around to opener_seat again.

2. DEAL. Deal one card face down to each alive player.

3. PRIVATE VIEW. Each alive player is told privately the card of every other alive player, but never their own card.

4. TURNS (one choice step, repeated at most 16 times). Repeat the following until coyote_called = yes, or until it has been done 16 times:
- Add 1 to turn_count. The acting player is the player in position turn_count of the turn order: position 1 is the opener, position 2 is the next alive seat clockwise, and so on, wrapping around.
- If current_declaration is none, the acting player must declare a whole number from 1 to 15. Calling Coyote is not allowed on the first turn.
- If current_declaration is a number d from 1 to 14, the acting player either declares a whole number from d+1 to 15 or calls Coyote.
- If current_declaration is 15, the acting player's only option is to call Coyote.
- A declaration is announced to all players at once. It sets current_declaration to that number and current_declarer to the acting player.
- Calling Coyote sets caller to the acting player and coyote_called = yes, which ends the repetition.
A player may declare again on each of their later turns. Because declarations strictly rise from at least 1 to at most 15, there are at most 15 declarations, and the call comes on turn 16 at the latest. Safety fallback: if the repetition ends with coyote_called = no, the next alive player in the turn order after current_declarer becomes the caller.

5. TRUE TOTAL.
- If the Max→0 card was dealt, it counts 0. Exactly one other dealt card with the highest positive value also counts 0. If two or more cards tie for highest, only one of them counts 0. If no other dealt card is positive, nothing further changes. All remaining dealt cards are added.
- If the Max→0 card was not dealt, the true total is the plain sum of the dealt cards.
Examples:
- {1, 2, -1}, no Max→0: total 2.
- {Max→0, 5, 2, -1}: the 5 counts 0, total 1.
- {Max→0, 3, 3, 0}: one 3 counts 0, total 3.
- {Max→0, -1, 0}: total -1.

6. RESOLUTION. If the true total is less than current_declaration, the current_declarer loses. Otherwise, when the total is equal to or greater than the declaration, the caller loses.

7. TOKENS. The loser gains 1 token. A player who reaches 3 tokens is eliminated (alive = no) and takes no further part.

8. NEXT OPENER. opener_seat becomes the next alive seat clockwise after the seat number of the current opener_seat, whoever lost. This works even if the current opener was just eliminated.

9. ANNOUNCEMENT. Reveal to everyone: all dealt cards, the true total, the final declaration, the declarer, the caller, the loser and everyone's tokens.

10. END CHECK. If only one player is alive, the game ends. Otherwise round increases by 1 and a new round begins. Exactly one player loses each round, so the game ends within 8 rounds with 3 players (3+3+2) and within 11 rounds with 4 players (3+3+3+2).

There is no talk phase. Declarations are the only communication.

Objective: The last player still alive, with fewer than 3 tokens, wins. Exactly one token is given out every round, so the game always ends with a single survivor and there are no draws.

Expected effect: Play is unchanged from the reviewed variation, but every round now resolves cleanly with exactly one caller and one loser. Players estimate the total from the visible cards plus the known distribution of their own card, which has an expected value of about 1.2, and adjust for the Max→0 risk. They also infer their own card from others' bids and try to leave a dangerous bid to the next player. No talk is added. Interests conflict, since exactly one player loses each round, and the bids already carry the information worth reasoning about.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 11 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
