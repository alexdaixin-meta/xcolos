# Variation: Turn The Tide: Short Seas (revised)

This is a 3-4 player Turn The Tide over P deals of 10 hands. Players hold 11 numbered Weather cards and play one per hand at the same moment. The two highest plays must take the two revealed Tide cards, and whoever is highest on the Tide loses a lifeline. Hands rotate left so everyone plays every hand once, and one card of each hand always stays hidden from rivals.

Players: 3 to 4, best with 4

## Review of the original

Turn The Tide is a 3-5 player card game. Each hand, everyone plays a numbered Weather card at the same moment. The two highest cards are forced to take one of two revealed Tide Level cards, and whoever then shows the highest Tide loses a life preserver. Hands pass around the table over as many rounds as there are players, and the score is preservers kept, minus a penalty for elimination, plus a bonus for the lowest Tide.

- **non_degenerate**: weak. The core is sound. All cards are played at once and no seat has an edge, and hand passing evens out the deal. The tested variation had a hole, though. Everyone started at Tide 11, the median of a 1-20 Tide deck. In 4-player games a player who always plays their lowest card often stays at 11 while others capture High Tides averaging about 14, so pure passivity bled few lifelines. Sunk players also still counted toward 'highest Tide' while losing nothing, so they shielded everyone else.
- **skill_sensitive**: good. Every player plays every original hand once, so luck of the deal cancels out over the game. What separates players is when they spend high cards, reading the two revealed Tides, and predicting which cards rivals will commit. All of these can be learned.
- **headroom**: good. A weak player still keeps some lifelines and can earn the lowest-Tide bonus. A strong player can count which cards are public, track which cards each opponent still holds, and time sacrifices across 10 hands. The game is not solved.
- **reasoning_dependent**: weak. In deal 1 the hands are hidden, so inference matters. In the tested variation every card was eventually played, so from deal 2 on every hand was fully public and the residual uncertainty was only what rivals will choose. Opponent modelling still matters, but the hidden-information component was thin.
- **verifiable**: good. Card comparisons, Tide levels, lifeline losses and end-of-deal scoring are all integer arithmetic on tracked numbers.
- **fits_platform**: bad. The tested variation broke at round 11. Played cards were discarded, so the hands to pass were empty and the stated 'each hand played once' rule was impossible. The 10th hand of each deal was also a forced play with one card left. Otherwise it was turn-based, text-only and within limits.

## Problems

- Fatal contradiction: played Weather cards were discarded, so after 10 hands every hand was empty and the 'pass your 10 cards left' rule passed nothing. Deal 2 could not be played.
- The rules implied hands stay hidden, when in fact every card becomes public once played, so from deal 2 on hands were fully known.
- The last hand of each deal was forced, because only one card remained, which wastes a round.
- The starting Tide level of 11 sat at the median of the Tide deck, so in 4-player games a passive 'always play lowest' policy rarely ended up highest and was hard to punish.
- Sunk players' Tide levels still counted when finding the highest level while they lost nothing, so a Sunk player at a high level shielded everyone else and removed pressure.
- The rules said 'rounds 1, 11, 21, 31' even for 3 players, who only have 3 deals.
- Hidden information after deal 1 was thin, because every card ended up public.

## Changes

- Played Weather cards stay face up in front of the player who played them. At the end of each deal each player gathers their played cards plus their one unplayed card (11 cards) into one hand and passes it to the player on their left. (fixes: Fatal contradiction: played Weather cards were discarded, so after 10 hands every hand was empty and the 'pass your 10 cards left' rule passed nothing. Deal 2 could not be played.): Hands now exist at every deal, and each player plays each original hand exactly once over P deals.
- Deal 11 Weather cards per player for 10 hands per deal, so one card per hand per deal goes unplayed. (fixes: The last hand of each deal was forced, because only one card remained, which wastes a round.): The 10th hand becomes a real choice between two cards.
- The unplayed card stays face down when the hand is passed, and the set-aside cards stay unseen. A card becomes public only when played. The rules state exactly who knows what. (fixes: Hidden information after deal 1 was thin, because every card ended up public.): Some hidden state survives every deal: rivals know 10 of a hand's 11 cards at most, and they must infer the rest from the unseen pool and the holder's past choices.
- State in the rules that every played card is public and that, from deal 2 on, most of each hand is known. (fixes: The rules implied hands stay hidden, when in fact every card becomes public once played, so from deal 2 on hands were fully known.): Players reason from the correct information.
- Everyone starts each deal at Tide level 15 instead of 11. (fixes: The starting Tide level of 11 sat at the median of the Tide deck, so in 4-player games a passive 'always play lowest' policy rarely ended up highest and was hard to punish.): 15 is above the average High Tide (about 14) and well above the average Low Tide (about 7). A player who never takes a Tide is usually the highest and bleeds lifelines, so dropping requires spending a high card at the right moment.
- Sunk players still play cards and can still take Tide levels, but their level is ignored when finding the highest level. (fixes: Sunk players' Tide levels still counted when finding the highest level while they lost nothing, so a Sunk player at a high level shielded everyone else and removed pressure.): Pressure falls on the players still at risk. Sunk players keep the hand-passing cycle intact and can still affect who takes which Tide.
- Define deal start and end by deal number (deals 1 to P) instead of listing round numbers. (fixes: The rules said 'rounds 1, 11, 21, 31' even for 3 players, who only have 3 deals.): The rules are correct for both 3 and 4 players.

## Kept from the original

- Unique numbered Weather cards played face up at the same moment.
- Two Tide cards revealed per hand: the highest Weather takes the lower Tide and the second highest takes the higher Tide.
- The player showing the highest Tide loses a life preserver (lifeline), with one extra 'last chance' before sinking.
- Hands pass left between deals, with as many deals as players.
- Scoring of 1 per remaining lifeline, -1 if sunk, and +1 for the lowest Tide.

## The variation's rules

SETUP. Let P be the number of players (3 or 4). The Weather deck is the cards 1 to 12xP (1-36 for 3 players, 1-48 for 4), each number once. Shuffle it and deal 11 cards face down to each player as that player's hand. The remaining P cards are set aside face down and stay unseen for the whole game. Each player starts with a game score of 0. The game has P deals of 10 hands each, so 10xP hands in total. One round is one hand.

INFORMATION. You always see your own hand. Every Weather card becomes public the moment it is played and stays face up in front of whoever played it until the end of that deal. Unplayed cards and set-aside cards are never shown. So from deal 2 on, every player knows the cards of a passed hand that were played in earlier deals but not its unplayed card or cards, unless they held that hand themselves.

START OF EACH DEAL (before hand 1 of deals 1 to P):
- Shuffle a Tide deck of the cards 1 to 20.
- Set every player's Tide level to 15.
- Give every player 4 lifelines.
- Clear every player's Sunk status.
- From deal 2 on: each player takes all 10 Weather cards lying face up in front of them, plus the 1 card still in their hand, making 11 cards. They pass these 11 cards as a hand to the player on their left. The face-up rows are now empty. Over the P deals each player plays each of the P original hands exactly once.

EACH HAND (10 per deal):
1. Reveal the next two cards of the Tide deck to everyone. The smaller is Low Tide and the larger is High Tide.
2. Every player secretly chooses one Weather card from their hand. All choices are revealed at the same time and each card is placed face up in front of the player who played it.
3. The player who played the highest Weather card sets their Tide level to Low Tide. The player who played the second highest sets their Tide level to High Tide. All others keep their current Tide level. Weather numbers are unique, so there are no ties. Sunk players take part in this step like anyone else.
4. Among players who are NOT Sunk, find the highest Tide level. Every non-Sunk player at that level loses 1 lifeline. A player who must lose a lifeline while at 0 lifelines becomes Sunk instead. A Sunk player stays Sunk until the next deal, keeps playing cards and is ignored in this step. If every player is Sunk, nothing happens.
5. Announce all Weather cards played, all Tide levels, all lifelines and all Sunk statuses.

END OF EACH DEAL (after hand 10 of each deal), adjust each game score:
- Each player who is not Sunk adds their remaining lifelines (0 to 4).
- Each Sunk player subtracts 1.
- Among players who are not Sunk, the player or players with the lowest Tide level each add 1.
After each deal every player holds exactly 1 card, which is not shown to others.

There is no talk phase.

END. After deal P, the game ends and the winner is decided as in the objective.

Objective: After the last deal, the player with the highest game score wins. If several players tie for the highest score, the tied player with the lowest Tide level at the end of the last deal wins. If that is still tied, the game is a draw.

Expected effect: The fixed hand-passing makes every deal playable. Each player meets each original hand once, so the deal is not a lottery. Starting at Tide 15 makes passivity costly: a player who hoards high cards and dumps low ones stays at 15 and bleeds lifelines. Burning high cards early instead leaves you unable to escape a bad High Tide later. Skill means deciding when a pair of Tides is worth spending a high card on, forcing rivals into the second-highest slot, and predicting their cards from the public record and the one hidden card per hand. Ignoring Sunk players keeps pressure on the live players to the end of each deal. Talk is left out: it cannot bind, and promises about card timing in a game where only one player wins would be empty or simply ignored.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
