# Variation: Forehead Poker Match

A 16-hand Indian Poker match for 4 to 6 players. Everyone sees every card but their own. Each hand has one simultaneous public message, one simultaneous bet and one simultaneous call-or-fold decision. Chips carry over, and the most chips after 16 hands wins.

Players: 4 to 6, best with 4

## Review of the original

Indian Poker (Blind Man's Bluff) deals each of 4 to 10 players one card that they hold to their forehead, so each player sees every card but their own. One round of poker betting in turn order follows, and the highest card among players who did not fold wins the pot.

- **non_degenerate**: weak. Folding, calling and raising do change the outcome, and no single action is always best. But betting goes in turn order, so the last seat to act sees everyone else's bets before deciding, which is a built-in positional edge in a single hand. 'Always fold' only ever loses the ante, which is safe but losing. Nothing structurally breaks the game.
- **skill_sensitive**: bad. The original is one hand with one card each. Who holds the highest card decides it almost entirely. A brilliant reader of other players still loses when dealt a 3, and a thoughtless caller wins when dealt an ace.
- **headroom**: weak. There is real depth: you infer your own card from the cards you see and from how others bet against you. But a single hand gives no room for a strong player's edge to accumulate, so improvement barely shows in results.
- **reasoning_dependent**: good. This is the game's core strength. Your own card is the one thing hidden from you. You must estimate it from the distribution of the cards you see and from how opponents, who can see your card, choose to bet. That is classic opponent modelling and inference from limited information.
- **verifiable**: good. The winner is the highest card among players who stayed in (suits break ties), and chip movements are arithmetic. No judge is needed.
- **fits_platform**: weak. Hidden cards, private views and numeric bets are all supported. However, open-ended poker betting (check, bet, raise and re-raise in turn order until everyone has matched) is a loop of unknown length, which the flat step list cannot express. A single hand is also too short to score meaningfully.

## Problems

- A single hand makes the result almost pure card luck; skill cannot show.
- Open-ended sequential betting (raise and re-raise until matched) is an unbounded loop the engine cannot build.
- Turn-order betting gives a fixed positional edge to whoever acts last.
- There is no multi-round planning: no chip management, no reputation, nothing carried between decisions.
- Folding costs only the ante, so very tight play is cheap and the game can stall into everyone folding.
- The table-talk and bluffing that make the game fun in person are informal, so a text platform has no defined channel for them.

## Changes

- Play a match of 16 hands, with chips carried from hand to hand. The winner is the player with the most chips at the end. (fixes: A single hand makes the result almost pure card luck; skill cannot show.): Card luck evens out over 16 hands, while good reading, folding and bluffing accumulate. Chip management and reputation across hands add planning.
- Replace open betting with two fixed simultaneous decisions. First, everyone at the same moment chooses Fold or a bet of 1, 2 or 3 chips. Then the bets are revealed, and every remaining player at the same moment chooses Call (match the highest bet) or Fold. (fixes: Open-ended sequential betting (raise and re-raise until matched) is an unbounded loop the engine cannot build.): This keeps the bet, see and respond structure of poker in a fixed number of steps the engine can build.
- Make all betting decisions simultaneous. (fixes: Turn-order betting gives a fixed positional edge to whoever acts last.): No seat ever acts with more information than another, so position gives no edge.
- If every player folds, or nobody is left to contest the pot, the whole pot carries over to the next hand. (fixes: Folding costs only the ante, so very tight play is cheap and the game can stall into everyone folding.): Mass folding feeds a bigger future pot, which raises the stakes and punishes passive play relative to opponents who contest it.
- Before betting each hand, every player writes one short public message at the same moment, and all messages are then shown. Players may say anything, including true or false claims about other players' cards. (fixes: The table-talk and bluffing that make the game fun in person are informal, so a text platform has no defined channel for them.): This formalises Indian Poker's table talk. You can try to scare a strong player out or lure a weak one in, but the other players see that player's card and know whether you lied. That rewards bluffing, reading and tracking reputation.
- Use a fixed ante, a bet cap of 3 chips and 40 starting chips. A player who has fewer than 4 chips at the start of a hand is eliminated and keeps that total. (fixes: There is no multi-round planning: no chip management, no reputation, nothing carried between decisions.): Losses per hand are bounded, so chip management across the match matters and one hand cannot decide everything.

## Kept from the original

- Each player sees every card except their own.
- You infer your own card from what you see and from how others bet against you.
- Ante, bet, call or fold, then a showdown where the highest card among those still in wins the pot.
- A standard 52-card deck, with suits breaking ties in the order Spades, Hearts, Diamonds, Clubs.
- Table talk and bluffing as part of play.

## The variation's rules

SETUP: Each player starts with 40 chips. The pot starts at 0. The match lasts 16 hands.

CARD STRENGTH: A standard 52-card deck is used. Rank from high to low is A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2. Between equal ranks, suit decides, from high to low: Spades, Hearts, Diamonds, Clubs. No two cards are ever equal.

EACH HAND:
1. ELIGIBILITY: Any active player with fewer than 4 chips is eliminated. They take no further part, and their current chips are their final total.
2. DEAL: The full deck is shuffled and one card is dealt to each active player. Each player is privately told the card of every other active player, but never their own.
3. ANTE: Each active player pays 1 chip into the pot.
4. TALK: Every active player writes one short message (at most 40 words) at the same moment, without seeing the others. All messages are then shown to everyone. Messages may say anything, including claims about anyone's card, and none of them binds anyone.
5. FIRST BET: Every active player, at the same moment, chooses one option: Fold, Bet 1, Bet 2 or Bet 3. A player who bets pays that many chips into the pot immediately. A player who folds is out of this hand and has lost only the ante.
6. REVEAL BETS: Every player's choice from step 5 is shown to everyone. Let H be the highest bet made.
7. CALL OR FOLD: Every player who bet in step 5, at the same moment, chooses Call or Fold. Calling costs H minus that player's own step-5 bet, paid into the pot. A player whose bet was already H calls for free. Folding forfeits everything that player has put in this hand.
8. SHOWDOWN: Find the players who called.
   - Two or more callers: their cards are compared, and the caller with the strongest card wins the whole pot.
   - Exactly one caller: that player wins the whole pot without comparison.
   - No callers: the pot stays and carries over to the next hand.
   All cards are then revealed to everyone, so players can check what was said and bet.
9. Winnings are added to the winner's chips, the pot resets to 0 (unless it carried over), and the next hand begins.

END: The match ends after hand 16, or earlier if only one player is still active. Any pot remaining at that moment is discarded.

Objective: The player with the most chips at the end of the match wins. Eliminated players count with the chips they held when eliminated. If two or more players tie for the most chips, the game is a draw among them.

Expected effect: The game becomes a contest of reading your own invisible card. A player infers their card's strength from the cards they can see (if everyone else holds low cards, yours is probably higher) and from how others bet and talk, since every opponent can see your card exactly.

Simple policies lose:
- Always Fold loses 1 chip per hand and finishes about 16 chips down.
- Always Bet 3 and Call is exploited. Opponents see its card, so they fold when it is high (it wins only the antes) and call when it is low (it loses 4 chips each time).
- Always Bet 1 and Call never pressures anyone and pays to see every losing showdown.
- Random play bleeds chips to anyone who folds when they see the table is strong.

When everyone plays well, card luck still swings individual hands, but over 16 hands the player who folds weak cards cheaply, extracts value with strong ones and bluffs effectively finishes ahead.

Talk passes both tests. On reasoning, players can bluff and bait, for example telling a player holding the 2 'you look strong' to lure them into calling, or telling the player holding the ace 'there is a king out there' to scare them off. Each listener must weigh who gains from the claim and that speaker's past honesty, which can be checked because cards are revealed after each hand. On conflict, only one player can win and every pot is zero-sum, so following another player's advice about your own card is exactly how a credulous player loses: the speaker only says 'call' when your call pays them.

No seat has an edge because all choices are simultaneous. The carry-over pot stops everyone from folding into a stall.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
