# Variation: Hogwash: Even Rounds

A 3 to 4 player shedding and bluffing game with a 25-card, five-rank deck. Players discard face down claiming the required rank. A sealed challenge poll follows a simultaneous talk step. When someone empties their hand, the cycle of seats is completed so everyone gets equal turns, and ties among finishers go to whoever took the fewest pile cards.

Players: 3 to 4, best with 3

## Review of the original

Hogwash (also known as Cheat or I Doubt It) is a shedding and bluffing card game. Players take turns discarding cards face down while claiming they are the required rank, which rises by one each turn. Any opponent may call a bluff: a caught bluffer takes the whole pile, and a wrong caller takes it instead. The first player to empty their hand wins.

- **non_degenerate**: weak. The previous variation, Sealed Calls, has no dominant pure policy. Always-3 is almost always a bluff and gets caught. Always-pass lets the leader dump cards unopposed. Always-challenge takes the pile from honest plays. But seat order gives a built-in tempo edge: uncontested, P1 goes out on turn 7, P2 on turn 8 and P3 on turn 9 (3 players), and P1 to P4 on turns 5 to 8 (4 players). The starter-card compensation never changes anyone's number of plays. With 6 ranks and 3 players, each seat only ever claims two fixed ranks, so a hand rich in your own ranks is a lasting deal advantage. Challenging a final play was also free, because a true last play ended the game anyway.
- **skill_sensitive**: good. Several skills decide who wins: when to bluff, sizing plays to the pile's risk, tracking which ranks have been publicly revealed and which ranks opponents have taken back into hand, and reading who will call. Two things blur this: the deal (fixed claim ranks per seat) and the tempo edge.
- **headroom**: good. Card counting, pile-size risk management and challenger coordination can be refined without limit. Even a weak player who plays one honest card at a time can survive and score.
- **reasoning_dependent**: good. Hands and pile contents are hidden. Every claim must be judged against what you hold, what has been revealed and the claimant's incentives. The resolving-challenger rule adds a who-calls inference. Without talk, players could only guess at that inference.
- **verifiable**: good. Card checks against the required rank, card counts and a fewest-cards fallback are all arithmetic. No judgement is needed.
- **fits_platform**: weak. The game is turn-based, text-only, has no board and fits within the limits. However, it introduced a second random event (the random starter card) while claiming the shuffle was the only one. It never said whether P3 knew the starter card. It left the zero-card state underspecified and had no talk step, even though the challenger coordination problem calls for one.

## Problems

- P1: Move-order tempo edge. Earlier seats reach zero cards turns earlier, and winning immediately on emptying rewards seat position rather than play.
- P2: The starter-card compensation is cosmetic (it changes no seat's play count) and adds a second random event whose knowledge status is unstated.
- P3: With 6 ranks and 3 players (or 4), each seat claims only a fixed subset of ranks, so being dealt your own ranks is a deal-lottery advantage.
- P4: Challenging a final play is free, because a true last play ends the game regardless, so that challenge carries no decision.
- P5: No talk step, although the resolving-challenger rule gives players opposed interests over who calls.
- P6: The zero-card state is underspecified: whether a player with no cards takes turns, votes in polls or can receive the pile.

## Changes

- When any player empties their hand, the current cycle of seats is finished, so every seat has had exactly the same number of turns before the game ends. Every player then at zero cards is a finisher. Ties among finishers are broken by fewest total cards taken from the pile over the game, otherwise a draw. (fixes: P1): Equal turns remove the tempo edge. The uncontested race now ends with all seats out together, a draw, so seat order alone wins nothing. The tiebreak rewards accurate challenging and well-judged bluffing over the whole game.
- Use a 25-card deck: ranks 1 to 5, five copies of each. Deal 8 each with 3 players or 6 each with 4. The one leftover card goes face down as the first pile card, seen by nobody. There is no player-placed starter card. (fixes: P2): The shuffle and deal is the only random event, everyone is dealt the same hand size, and nobody has special knowledge of the starter card.
- Use 5 ranks instead of 6. (fixes: P3): 5 shares no factor with 3 or 4, so over five cycles every seat must claim every rank. A hand rich in one rank helps every seat equally often, and no seat is locked to fixed ranks.
- Because the game no longer ends on the spot, a challenger who calls a true final play takes the whole pile. (fixes: P4): Calling a last play now has a real cost, so it becomes a judgement rather than an automatic call.
- Add a simultaneous talk step after the claim and before the challenge poll. Every player still holding cards, including the active player, writes one short message. All messages are shown, then the poll happens. (fixes: P5): The first challenger clockwise carries all the risk and later challengers carry none, so non-active players disagree about who should call. The active player can bluster or bait. Talk gives players promises to test and bluffs to read.
- State the zero-card rules explicitly. A player with zero cards is finished. They take no further turns (their turn slot passes with no play), do not talk, are always counted as PASS in polls, and can never receive the pile. (fixes: P6): Removes ambiguity so the engine can build the game correctly.

## Kept from the original

- Face-down discards claimed as the required rank, which rises by one each turn and wraps around
- Bluffing when you lack the rank
- Calling a bluff: a caught bluffer takes the whole pile, and a wrong caller takes it instead
- Shedding race: emptying your hand is the goal
- Hidden hands with public card counts
- The resolving-challenger rule from Sealed Calls, now paired with talk

## The variation's rules

SETUP
- Deck: 25 cards, ranks 1 to 5, five copies of each rank.
- Shuffle once at the start. This shuffle and the deal are the only random events in the game.
- Seats are Player 1, Player 2, Player 3 (and Player 4 with four players). Clockwise means increasing seat number, wrapping from the last seat to Player 1.
- With 3 players, deal 8 cards to each player. With 4 players, deal 6 cards to each player.
- The one remaining card is placed face down as the first card of the central pile. Nobody sees it.
- Hands are private. Everyone always knows how many cards each player holds and how many cards are in the pile.
- Each player has a public 'taken' counter, starting at 0. It counts the total number of cards that player has picked up from the pile during the game.
- Turn 1: the required rank is 1 and Player 1 is the active player.
- A cycle is one turn for each seat in order, from Player 1 to the last seat. Turns 1 to 3 are cycle 1 with 3 players; turns 1 to 4 are cycle 1 with 4 players; and so on.

FINISHED PLAYERS
- A player holding 0 cards is finished.
- A finished player takes no turns: when their turn comes, it passes with no play, and the rank and turn still advance.
- A finished player writes no messages and is always counted as PASS in challenge polls.
- A finished player can never receive the pile.

EACH TURN
1. Announce the turn number, the active player and the required rank R.
2. Play. The active player secretly chooses 1, 2 or 3 cards from their hand (never more than they hold) and puts them face down on top of the pile.
   - It is announced: 'Player X plays N cards, claiming N cards of rank R.'
   - The claim is always exactly rank R and exactly the number of cards played.
   - The cards may be anything. Playing any card that is not rank R is a bluff.
3. Talk. Every player who still holds cards, including the active player, writes one short message at the same moment, without seeing the others. All messages are then shown to everyone.
   - Messages are not binding. Players may promise, threaten, bluff or lie.
4. Challenge poll. Every non-active player who holds cards simultaneously and secretly chooses CHALLENGE or PASS.
5. Resolution.
   - If nobody challenged, the cards stay in the pile.
   - Otherwise, the resolving challenger is the challenger who comes soonest clockwise after the active player.
   - Reveal only the cards just played.
   - If all of them are rank R, the claim was true: the resolving challenger takes the entire pile into their hand.
   - If any revealed card is not rank R, the claim was a bluff: the active player takes the entire pile into their hand.
   - Whoever took the pile adds the number of cards taken to their taken counter.
   - The pile is now empty. The result is announced: true or bluff, who took the pile, and how many cards.
   - Other challengers lose nothing.
6. Finish check. Any player now holding 0 cards is finished.
   - The first time any player becomes finished, the game is marked to end at the end of the current cycle.
   - A bluff that was caught never finishes the bluffer, because they have taken the pile back.
7. End check. The game ends if the turn just played was the last seat's turn and either of these is true:
   - the game has been marked to end; or
   - this was turn 36.
8. Advance. The required rank increases by 1, wrapping from 5 back to 1. The next seat clockwise becomes the active player.

NOTES
- Because 5 ranks share no factor with 3 or 4 seats, every seat is required to claim every rank over the course of five cycles.
- Because 36 turns is a whole number of cycles for both 3 and 4 players, every seat always gets the same number of turns.

Objective: When the game ends, every seat has had the same number of turns. Find the smallest hand size held by any player; this is 0 if anyone is finished. Among the players holding that many cards, the one with the lowest taken counter wins. If two or more of them tie on the lowest taken counter, the game is a draw.

Expected effect: Seat order no longer wins anything. If nobody challenges, all players go out in the same cycle with zero taken, a draw (in 3 players, 3+3+2 plays each; in 4 players, 3+3). Winning therefore requires catching others' bluffs while avoiding pickups yourself.

Simple policies each lose:
- Always-3 bluffs constantly and takes piles.
- Always-challenge takes the pile from true claims and racks up its taken counter.
- Always-pass lets bluffers dump cards and can lose the tiebreak race.
- Always-1-honest-when-possible is too slow to finish.

Calling a final play now costs the challenger the pile if the claim is true, so last plays become real reads.

Talk passes both tests:
- Players disagree about who should call, because only the first challenger clockwise risks the pile. The seat right after the active player wants a later seat to carry the risk, and each wants the other's taken counter to rise.
- The active player wants to bait a call on a true play, or bluff confidence on a false one.
- A player who simply follows another's 'you call, I'll back you' can end up as the resolving challenger on a true claim, swallowing the pile while the advisor loses nothing.
- A player who believes 'I'll call' and passes can let a bluffer finish.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
