# Variation: Jukha Three (revised 2)

Three players pass cards face down around a circle, each with a claimed rank that may be false, racing to be first to start a taking turn holding four of a kind. The game is capped at 30 turns, after which an arithmetic score decides the winner.

Players: 3 to 3, best with 3

## Review of the original

Jukha is a 3-13 player hidden-hand bluffing game. Each player holds 4 cards and the player holding 5 must pass a face-down card, with a claimed rank that may be false, to the next player, who may accept it or ask for another. A player who begins their turn holding exactly four of a kind exits safely, and the last two players left both lose.

- **non_degenerate**: weak. Choices matter: what to request, what to offer, what to claim, whether to accept. But the loss is shared by the last two players, so with many players most decisions barely change one player's fate. With 3 players the first exit decides that the other two lose, so the race is the whole game. A 'never believe, always take the third card' policy turns the exchange into a random draw. The original has no turn limit and no tiebreak, and the Joker can circulate forever.
- **skill_sensitive**: weak. Card tracking and reading false claims help. With 13 players and 52+ cards, though, memory is overwhelmed and the deal dominates. A dealt four of a kind can exit on the first turn with no skill at all.
- **headroom**: good. Several skills can improve: tracking which ranks each player collects from their requests, bluffing claims to keep a rival from completing a set, and timing when to pass on cards a rival needs. A weak player still exits sometimes by luck.
- **reasoning_dependent**: good. Hands are hidden and claims can be false. Requests leak what a player is collecting. The taker must infer from the giver's incentives whether a claim is likely true.
- **verifiable**: weak. An exit is checkable. But there is no turn limit and no rule for endless play, and 'last two lose' gives no single winner the engine can compute.
- **fits_platform**: weak. It is text-only and turn-based. But it scales to 13 players with an unbounded length, and the option to reject twice adds extra branches. It needs a fixed small player count, a turn cap and an arithmetic fallback.

## Problems

- The original has no length limit, so it can loop forever, which the platform cannot run.
- 'Last two lose' does not give the engine a single winner. With many players, individual decisions barely matter.
- With large player counts and big decks, card memory is overwhelmed and luck dominates.
- A dealt four of a kind wins on the first exit check with no decision made. This is a pure lottery.
- The previous variation's turn counter contradicted itself. Its starting value was unstated and 'reached 30' triggered after turn 29, while FALLBACK scored 'the taker of turn 30'. Implementations could end after 29 or 30 turns.
- The previous variation did not say plainly that hand sizes and all requests, claims and choices are public, or exactly what the third player sees.

## Changes

- Kept 3 players, a 13-card deck (four each of A, B and C plus one Joker) and a 30-turn cap with an arithmetic fallback score. (fixes: The original has no length limit, so it can loop forever, which the platform cannot run.): This bounds the length. It makes hands trackable so that memory and inference pay. It gives a single computed winner.
- The first player to exit wins outright and the other two lose. If no one exits, there is a fallback score with one top scorer winning and any tie for top a draw. (fixes: 'Last two lose' does not give the engine a single winner. With many players, individual decisions barely matter.): This gives one arithmetic winner. Each decision now affects one's own chance of winning, and blocking a rival who is close to a set matters.
- Kept the small deck and the 3-player limit. (fixes: With large player counts and big decks, card memory is overwhelmed and luck dominates.): Twelve rank cards plus one Joker can be tracked, so card counting and reading claims beat luck.
- Added a setup redeal: if either 4-card player is dealt four cards of one rank, the whole deck is reshuffled and redealt until neither is. (fixes: A dealt four of a kind wins on the first exit check with no decision made. This is a pure lottery.): No one can win before making a single decision. The 5-card first giver must still give a card and wait for a later taking turn.
- Rewrote the counter. It starts at 1 on turn 1. In Advance, if the turn just completed was turn 30, go to FALLBACK; otherwise add 1 and begin the next turn. (fixes: The previous variation's turn counter contradicted itself. Its starting value was unstated and 'reached 30' triggered after turn 29, while FALLBACK scored 'the taker of turn 30'. Implementations could end after 29 or 30 turns.): This makes it exactly 30 turns. The turn-30 taker is then the 5-card holder at FALLBACK, matching the FALLBACK wording.
- Stated an explicit information rule. Hand sizes, who gives and who takes, requests, claims and the taker's choice are all public. Only the giver and the taker know the identity of the passed card. (fixes: The previous variation did not say plainly that hand sizes and all requests, claims and choices are public, or exactly what the third player sees.): This removes guesswork for both the implementer and the playing models.

## Kept from the original

- A face-down card is passed from the 5-card holder to the next player, with a claimed rank that may be a lie.
- The taker can refuse the first offer and seek another, ending with a forced blind take.
- A non-binding request naming the rank the taker wants.
- A player exits by holding exactly four of a kind at the start of their own turn; four of a kind plus an extra card does not count.
- The Joker is a dead card that never completes a set and is a liability to hold.
- Play passes clockwise, and the player who just took becomes the next giver.

## The variation's rules

CARDS. 13 cards: four each of ranks A, B and C, plus one Joker. Suits do not exist.

SETUP. Assign the 3 players at random to seats 1, 2 and 3. Play passes 1 -> 2 -> 3 -> 1. Pick one seat at random to be the first giver. Shuffle and deal 5 cards to the first giver and 4 to each of the other two. If either 4-card player holds four cards of one rank, collect all cards, reshuffle and redeal, repeating until neither 4-card player does. Hands are private.

INFORMATION. Public: every player's hand size, who is giver and taker each turn, every request, every claim and every take choice. Private: a player's own hand. The giver knows which card left their hand; the taker sees the card they received. The third player never sees the passed card.

TURN ORDER. Each turn has a giver, who holds 5 cards, and a taker, the next seat in play order, who holds 4. On turn 1 the giver is the first giver. After each turn, that turn's taker becomes the next giver and the seat after them becomes the next taker.

TURN COUNTER. The turn counter starts at 1 on turn 1.

EACH TURN:
1. Exit check. If the taker's 4 cards are all the same rank (four A, four B or four C), the taker shows them and wins immediately, and the other two players lose. The Joker never counts toward a set.
2. Request (public). The taker names one rank they want (A, B or C) or says 'none'. The request binds no one.
3. Offer (public claims). The giver chooses two different cards from their 5-card hand; the two may be of the same rank. The giver places them face down as Offer 1 and Offer 2 and publicly claims a rank for each (A, B, C or Joker). Claims may be true or false.
4. Take (public choice). The taker announces exactly one of 'Offer 1', 'Offer 2' or 'blind'. Blind gives the taker one card chosen uniformly at random from the giver's three cards that were not offered. Offered cards that are not taken return to the giver's hand unrevealed.
5. Pass. The received card moves from the giver's hand to the taker's hand. Record it privately as the taker's 'last received' card. The taker now holds 5 cards and the giver holds 4.
6. Advance. If the turn just completed was turn 30, go to FALLBACK. Otherwise add 1 to the turn counter and begin the next turn.

FALLBACK (reached only after turn 30 is completed with no exit). Reveal all hands and score each player:
- Group count: the largest number of cards of one rank (A, B or C) among that player's scored cards, at most 4. For the two players holding 4 cards, the scored cards are their whole hand. For the player holding 5 cards (the taker of turn 30), the scored cards are their 5 cards minus their 'last received' card, which are the 4 cards they held at turn 30's exit check.
- Joker penalty: the player physically holding the Joker subtracts 2, even if it is their last received card.
- Score = group count minus any Joker penalty.
If exactly one player has the highest score, that player wins and the other two lose. If two or three players tie for the highest score, the game is a draw.

There is no free talk. The only public statements are requests, claims and take choices.

Objective: The first player who, at the exit check of a turn in which they are the taker, holds exactly four cards of one rank (A, B or C) wins, and the other two lose. If no one has done so when turn 30 is completed, each player scores their largest same-rank group (at most 4) among their scored cards, minus 2 if they hold the Joker. The 5-card holder's scored cards exclude the card they received on turn 30. A single top scorer wins and the other two lose. Any tie for the top score is a draw.

Expected effect: Players must infer which rank each rival is collecting from their requests and from which offers they take. Givers bluff claims to keep the next player from completing a set and to unload the Joker. Takers weigh whether a claim is credible given the giver's interest, and use 'blind' to escape suspected traps. The third player watches public choices to judge who is close to winning. The redeal removes instant dealt wins. The exact 30-turn counter makes the end, the 5-card holder at FALLBACK and the fallback score unambiguous. Talk is left out because the only player able to block a near-winner on a given turn is the giver, who already wants to; requests and claims already serve as the bluffing channel.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
