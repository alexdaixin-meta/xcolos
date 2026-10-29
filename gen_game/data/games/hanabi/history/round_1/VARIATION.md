# Variation: Hanabi: Three Fireworks

A cooperative 2 to 4 player Hanabi with a 30-card deck in 3 colours. Players see every hand but their own and communicate only through limited hints. The team must build fireworks worth a target score before the deck runs out or the third fuse burns.

Players: 2 to 4, best with 3

## Review of the original

Hanabi is a cooperative card game for 2 to 5 players. Each player holds a hand they cannot see but everyone else can. The team spends a limited supply of hint tokens to tell teammates about their cards, and tries to play five colour piles in order from 1 to 5 before three failed plays or the end of the deck.

- **non_degenerate**: good. Every simple policy fails. Always playing your oldest card burns the 3 fuses within a few turns, because only 15 of 50 cards are playable 1s at the start. Always discarding scores 0. Always hinting runs out of tokens and builds nothing. There is no seat edge, since everyone shares one outcome. Choices of what to hint, when to discard and when to risk a play decide the score.
- **skill_sensitive**: good. Strong teams reliably score far higher than weak teams on the same deal. They spend hints efficiently, read the intent behind a hint, protect singleton 5s and avoid blind plays. The shuffle sets the ceiling of a deal, but most deals allow a high score with good play.
- **headroom**: good. Perfect scores are rare even for experts, so there is always room to improve. A careful beginner who only plays fully hinted cards still scores a few points.
- **reasoning_dependent**: good. The core of the game is inference. You deduce your own hidden cards from hints, from the public discards and played piles, and from what a teammate's choice of hint implies about what they want you to do. That is opponent modelling in partner form, and it is planned over many turns.
- **verifiable**: good. The score is the sum of the pile tops. Every outcome follows from the card faces and the rules. No judgement is needed.
- **fits_platform**: weak. The game is turn-based and text-only. Problems: the 50-card, 5-colour deck makes games long (often more than 60 turns) and the state large. Hands hidden from their owner but visible to others are the inverse of the supported hidden hands. The result is a score, not a winner. The previous adaptation also overran the limits: it tracked a 15-cell copies table (23 or more numbers) and needed lookup updates that cost far more than 20 steps per turn.

## Problems

- The full game (50 cards, 5 colours, hands of 4 to 5, up to 5 players) is too long and carries too much state for the 40-round, 20-attribute limits.
- The original produces only a score, and the engine can only declare winners or a draw. A cooperative game needs a win threshold.
- Owner-blind hands are the inverse of supported hidden hands, and the mechanism for showing each player the other hands was not stated.
- The previous variation tracked a copies-outstanding table of 15 numbers. That pushed the tracked numbers to at least 23, over the limit of 20.
- Updating a 15-cell colour-by-rank table on every play or discard needs lookup logic the engine lacks, costing roughly 15 to 20 steps by itself.
- The copies table is redundant. It can be derived exactly from the public discard pile and pile values, so it spends budget without adding information.
- The previous step count (12) was understated. Validation, hint resolution, the play test, the pile update, fuses, bonuses, the draw, the final round and the end checks were not all counted.
- Hint matching done card by card, and the play test done as a 3-way colour lookup, would each cost several steps per turn.

## Changes

- Use a 30-card deck in 3 colours (three 1s, two each of 2, 3 and 4, one 5 per colour), 2 to 4 players, hand size 5 with 2 players and 4 with 3 or 4 players, and a cap of 40 turns. (fixes: The full game (50 cards, 5 colours, hands of 4 to 5, up to 5 players) is too long and carries too much state for the 40-round, 20-attribute limits.): This keeps the structure of Hanabi (scarce 5s, duplicated low cards, the hint economy) while making a game fit in 40 turns and a handful of tracked numbers.
- Add a team target: the team wins if the final fireworks score is at least 10 (2 or 3 players) or 9 (4 players). Losing the last fuse sets the team score to 0. Every player's total equals the team score, and the engine's target rule declares everyone a winner or nobody. (fixes: The original produces only a score, and the engine can only declare winners or a draw. A cooperative game needs a win threshold.): The engine can only declare winners. A threshold turns the cooperative score into a shared win or loss, and it needs real coordination to reach.
- At the start of each turn, the engine sends the active player, through a private channel, the faces of every other player's hand plus only the IDs of their own hand. (fixes: Owner-blind hands are the inverse of supported hidden hands, and the mechanism for showing each player the other hands was not stated.): This states the supported mechanism for owner-blind hands. Only the active player needs the view, so one step per turn is enough.
- Remove the copies-outstanding table entirely. Players work it out themselves from the public discard pile and the three pile values, both shown every turn. (fixes: The previous variation tracked a copies-outstanding table of 15 numbers. That pushed the tracked numbers to at least 23, over the limit of 20.): This removes 15 attributes and all the lookup updates. The information is still fully available, and doing the counting is part of the reasoning.
- No colour-by-rank cell is ever updated. Cards are strings such as 'R3' in game lists (deck, hands, discard pile), and only the three pile values change. (fixes: Updating a 15-cell colour-by-rank table on every play or discard needs lookup logic the engine lacks, costing roughly 15 to 20 steps by itself.): Without a table there is nothing to look up, so plays and discards cost a few list operations.
- Keep only: piles R, G and B; hint tokens; fuses; deck count; turns played; final-round counter; team score; target; the action this turn; a play-success flag; the deck, discard and hint-log lists; and each player's hand list and score. That is 17 in all. (fixes: The copies table is redundant. It can be derived exactly from the public discard pile and pile values, so it spends budget without adding information.): This is an honest attribute budget under 20.
- Recount the turn as 18 explicit steps, each with a `when` condition. The 4 ordered end checks are merged into 2 steps that use `or`. The final round is handled by one counter, decremented before it is triggered. (fixes: The previous step count (12) was understated. Validation, hint resolution, the play test, the pile update, fuses, bonuses, the draw, the final round and the end checks were not all counted.): This gives an honest step count within the 20-step limit, with every rule accounted for.
- Resolve the validity check, hint matching and the play test each as a single referee rule check. Examples: 'list the IDs in the named hand whose card has the named colour or rank'; 'the revealed card's rank equals its colour's pile value plus 1'. The pile is then raised by one step with three `if` operations. (fixes: Hint matching done card by card, and the play test done as a 3-way colour lookup, would each cost several steps per turn.): Each of these replaces several per-card or per-colour comparison steps with one step.

## Kept from the original

- Fully cooperative play: one shared outcome for the whole team.
- Owner-blind hands: you see everyone's cards but your own.
- The three actions (hint, discard, play) and the economy of 8 hint tokens and 3 fuses.
- Hints must point to all matching cards of one colour or one rank, and so give negative information about the other cards.
- Discarding regains a hint token; completing a pile to 5 regains one.
- The deck mix of three 1s, two each of 2 to 4, and a single 5 per colour, so 5s must be protected.
- The final round after the deck empties, and losing everything on the last fuse.
- No table talk: all communication goes through hints.

## The variation's rules

CARDS. The deck has 30 cards in three colours: Red, Green and Blue. Each colour has three 1s, two 2s, two 3s, two 4s and one 5. A card is written as colour letter plus rank, for example R1 or B5. At the start, the deck is shuffled once and each card gets a permanent ID from #1 to #30 in shuffled order. An ID never reveals a card's face.

SETUP. With 2 players each hand has 5 cards; with 3 or 4 players each hand has 4 cards. Deal from the top of the deck in seat order. Each hand is an ordered list of card IDs, oldest first. The rest form the face-down deck: 20 cards with 2 players, 18 with 3, 14 with 4. The team starts with 8 hint tokens (never more than 8) and 3 fuses. There are three piles, Red, Green and Blue, each starting at 0. The target is 10 with 2 or 3 players and 9 with 4 players. Turns played starts at 0. The final-round counter starts at -1, meaning not started.

WHAT PLAYERS SEE. At the start of every turn the engine announces to everyone:
- the three pile values;
- the hint tokens and fuses remaining;
- the number of cards left in the deck;
- the turns played so far;
- the full discard pile, with faces;
- the full hint log.
The engine then sends the active player, privately, the colour and rank of every card in every other player's hand, together with the IDs only (never the faces) of the active player's own hand. A player never sees the faces of their own cards until those cards are played or discarded. How many copies of a card remain unseen can be worked out from the discard pile and the piles; the engine does not track it. There is no talk phase and no other communication.

TURN ORDER. Players take turns in seat order, starting with seat 1. On a turn, the active player gives exactly one answer, in one of these three forms.

(a) HINT <player> <colour or rank>. This needs at least 1 hint token. The named player must be someone else, and at least one card in their hand must match. The team spends 1 token. The engine announces to everyone which IDs in that hand match, and that every other ID currently in that hand does not match. The hint is added to the public log.

(b) DISCARD <ID>. The ID must be in your own hand. Remove it, reveal its face to everyone and put it face up in the discard pile. The team gains 1 hint token, up to a maximum of 8.

(c) PLAY <ID>. The ID must be in your own hand. Remove it and reveal its face to everyone.
- If its rank is exactly 1 more than the current value of its colour's pile, the play succeeds and that pile rises to the card's rank. If the pile has just reached 5, the team gains 1 hint token, up to a maximum of 8.
- Otherwise the play fails: the card goes face up to the discard pile and the team loses 1 fuse.

INVALID ANSWERS. An answer is invalid if it:
- has an unreadable form;
- is a hint given with 0 tokens;
- is a hint to yourself;
- is a hint that matches no card;
- names an ID not in your own hand.
An invalid answer is replaced by DISCARD of the oldest ID in the active player's hand.

DRAW. After a discard or a play, if the deck is not empty, the active player takes the top card into the end of their hand. Its ID is announced to everyone. Its face is visible only to the other players, through their private views.

FINAL ROUND. When the last card of the deck is drawn, the final-round counter is set to the number of players. On each later turn it drops by 1 at the end of that turn. So every player, starting with the next seat and ending with the player who drew the last card, gets exactly one more turn. No draws happen during these turns.

SCORE. After every turn, the team score is the sum of the three pile values (0 to 15). If the fuses are at 0, the team score is 0 instead. Every player's total is set to the team score.

END OF GAME. After every turn, the game ends if any of these is true:
- fuses are 0;
- the team score is 15;
- the final-round counter has reached 0;
- 40 turns have been played.

Objective: When the game ends, every player's total equals the team score: the sum of the three pile tops, or 0 if the last fuse was lost. If that total is at least the target (10 with 2 or 3 players, 9 with 4 players), every player wins together. Otherwise no player reaches the target, the team has lost, and the engine records the result as no winner (a shared draw). No player can ever win alone.

Expected effect: Play stays as hard as Hanabi on a smaller scale. Players must read hints for intent ('why did they point at that card now?'), count unseen copies themselves from the discard pile, protect the three singleton 5s, and time discards against the hint economy. Simple policies lose: blind playing burns 3 fuses and ends at 0, always discarding or always hinting builds nothing, and random play fails. The target of 10 out of 15 (9 with 4 players, who get smaller hands and a shorter deck) leaves slack for an unlucky shuffle, so the deal limits the ceiling but does not decide the result. Talk is deliberately left out: every player wants the same outcome, so there is nothing to disagree about, and free talk would let players simply state each other's cards and destroy the hint economy that is the game. Endgame unraveling does not apply, because the game is fully cooperative and judged against a target.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
