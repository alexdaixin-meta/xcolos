# Variation: Eleven Takes: Three Piles

A compact, luck-light 11 Nimmt for 3 to 4 players. Players shed hidden hands onto 3 public piles using circular ascending plays. They take piles to reset them with a card of their choice, and use capped bull runs. The lowest ox-head penalty after one deal wins.

Players: 3 to 4, best with 4

## Review of the original

11 Nimmt is a shedding card game for 2 to 7 players. On each turn a player either plays one card onto a pile (higher than its top, within a circular distance of 10) or takes a whole pile into hand. Taking big piles earns bull cards, which allow multi-card runs. A round ends when someone empties their hand, the others score ox-head penalties for the cards they still hold, and the lowest total over several rounds wins.

- **non_degenerate**: good. No simple policy wins outright. 'Always take a pile' never empties the hand and swells it. 'Always play the lowest legal card' leaves you stuck and forced to take big piles when the tops jump. Choosing which pile to feed or block, and when to take a pile, changes who empties first. With 3 or more players one player's gain is not a direct loss for each rival. Two-player games are pure difference games. Seat order gives the first player a small tempo edge in each round.
- **skill_sensitive**: weak. Skill matters: pile blocking, timing takes to earn bulls, and saving runs. But fresh piles are seeded from a random draw deck every time a pile is taken, and the deal of 10 cards from 104 varies a lot. Luck has a large share in any single round.
- **headroom**: good. Weak players still shed cards and score something. Strong players plan bull runs, track which numbers are gone, and take small piles to reset tops in their favour. The game is not solved.
- **reasoning_dependent**: good. Hands are hidden. A player must infer from what opponents play or decline to play which ranges they hold, and plan several turns ahead around bull runs and pile tops.
- **verifiable**: good. Card legality is arithmetic (higher than the top, circular distance at most 10). Penalties are ox-head sums. The lowest total wins. No judge is needed.
- **fits_platform**: bad. The pile count grows without bound, so state is unbounded. Bull runs let a player play an arbitrary number of cards in one turn. Every pile take triggers two random draws. A 104-card deck, 10-card hands and up to 7 rounds of play far exceed the limits of 4 choice steps, 1 random draw per round, 20 attributes and 40 rounds.

## Problems

- The number of piles grows each time one is taken, giving unbounded state that the engine cannot track within 20 attributes.
- Each pile take draws two random cards from the deck, which breaks the limit of one random draw per round and adds luck to every take.
- Bull runs allow an unbounded number of cards in one turn, which exceeds the choice-step limit.
- The 104-card deck, 10-card hands and multi-round match (as many rounds as players) are too long and too large to build and play inside 40 rounds.
- The two-player game is a pure difference game, and seat order gives the first player a tempo edge (they may empty their hand before others have had as many turns).
- Random pile seeding and a large random deal let luck swamp skill in a single deal.

## Changes

- Use exactly 3 piles throughout. A taken pile is immediately restarted, so there are always 3. (fixes: The number of piles grows each time one is taken, giving unbounded state that the engine cannot track within 20 attributes.): This bounds the state to 3 pile lists and keeps the take-or-play pile choice.
- When a player takes a pile, they restart it with a card of their own choosing from their hand (which now includes the taken cards). Nothing is drawn from a deck during play. (fixes: Each pile take draws two random cards from the deck, which breaks the limit of one random draw per round and adds luck to every take.): This removes all in-play randomness and turns the restart into a strategic choice: block opponents or set up your own run.
- Bulls are capped. Each bull held lets a player add one extra card to the same pile in the same turn, with a maximum of 2 extra cards. (fixes: Bull runs allow an unbounded number of cards in one turn, which exceeds the choice-step limit.): This keeps the bull-run idea while fitting within 4 choice steps.
- Use a deck of 1 to 40, circular distance at most 6, 6-card hands, 3 or 4 players, and a single deal of at most 36 or 40 turns. Each engine round is one player's turn. (fixes: The 104-card deck, 10-card hands and multi-round match (as many rounds as players) are too long and too large to build and play inside 40 rounds.): This scales the game to the round and attribute limits while keeping the density of legal plays similar to the original.
- Use 3 or 4 players only. When someone empties their hand, the current cycle is completed so that every player has had the same number of turns. The lowest penalty wins. (fixes: The two-player game is a pure difference game, and seat order gives the first player a tempo edge (they may empty their hand before others have had as many turns).): With 3 or more players the game is not a difference game. Finishing the cycle removes the first seat's tempo edge.
- Make the full contents of every pile public, so that every taken card is known to everyone. The initial deal is the only random event. (fixes: Random pile seeding and a large random deal let luck swamp skill in a single deal.): Hidden information shrinks to the original deal plus the undealt cards. A careful tracker can deduce more and more about opponents' hands, so skill beats luck over a game.

## Kept from the original

- Each turn you either play one card onto a pile or take a whole pile into your hand.
- A play must be higher than the pile top within a circular distance, with wraparound past the highest card.
- If you cannot or do not play, you must take a pile.
- Taking a pile of 3 or more cards earns a bull, which allows multi-card runs onto one pile. When the supply runs out, you steal a bull from the player who has the most.
- The deal ends when a player empties their hand. Others score ox-head penalties for the cards left in hand, and the lowest penalty wins.
- Hands are hidden, and you must read opponents from what they play and decline.

## The variation's rules

SETUP
1. Use a deck of cards numbered 1 to 40.
2. Ox-heads per card: 3 if the number is a multiple of 10; 2 if it is a multiple of 5 but not of 10; 1 otherwise. The whole deck holds 52 ox-heads.
3. Shuffle once. This is the only random event in the game. Deal 6 cards face down to each player as a private hand. Turn 3 cards face up to start Pile A, Pile B and Pile C, one card each. The remaining cards (13 with 4 players, 19 with 3) are set aside unseen for the rest of the game.
4. Place a supply of bull tokens equal to the number of players minus 1 (3 with 4 players, 2 with 3 players).
5. Seats are numbered 1 to N. Seat 1 moves first, and play proceeds in seat order.

WHAT IS PUBLIC
- The full ordered contents of every pile.
- Each player's hand size and bull count.
- Every action taken.
Only the contents of hands and the set-aside cards are hidden.

LEGAL PLAY
6. A card c may be played on a pile whose top card is t if (c - t) mod 40 is between 1 and 6. Examples: on 12 you may play 13 to 18; on 37 you may play 38, 39, 40, 1, 2 or 3.

A TURN (one engine round)
7. The active player privately chooses one action:
   (a) PLAY card X onto pile P, where X is in their hand and legal on P; or
   (b) TAKE pile P.
   A player may take even when a legal play exists. If the chosen action is illegal, or the player has no legal play and chose PLAY, they instead TAKE the smallest pile (ties: A before B before C).
8. If the player PLAYED: card X goes on top of pile P. If they hold at least 1 bull, they may then add one more card legal on the new top of the same pile. If they hold 2 or more bulls, they may add a second extra card the same way. They may stop at any point. An illegal extra card is ignored and ends the run. Bulls are not spent by using them.
9. If the player TOOK pile P:
   - All cards of P go into their hand.
   - They must then choose any one card from their hand to place face up as the single card of the restarted pile P.
   - If P held 3 or more cards before it was taken, the player gains a bull from the supply. If the supply is empty, they instead take one bull from the opponent holding the most bulls; ties go to the first such player in seat order after the taker. If no opponent has a bull, nothing happens.
10. If the active player's hand is now empty, the game will end at the end of the current cycle, that is, after the player in seat N has finished their turn. Every player therefore gets the same number of turns.
11. Pass the turn to the next seat.

END OF GAME
12. The game ends at the end of the cycle in which any player emptied their hand. It also ends after 10 full cycles (40 turns with 4 players) or 12 full cycles (36 turns with 3 players), whichever comes first.
13. Each player's penalty is the total ox-heads of the cards in their hand. A player with an empty hand scores 0.

Objective: The player with the lowest penalty wins. If two or more players tie for lowest, the game is a draw among them (an engine draw).

Expected effect: All randomness is in the opening deal, and the full contents of every pile are public. Strong players track every card that has been seen and deduce which numbers opponents can hold. They restart taken piles with cards that block a rival's likely ranges or set up their own bull runs. They also time takes of piles with 3 or more cards to gain bulls, or to steal one from the leader. Taking a 1-card pile becomes a tempo move that does not grow your hand: you swap a card into a better position. Mindless policies lose. 'Always play the lowest legal card' gets stuck behind high tops. 'Always take the smallest pile' never empties a hand and is limited by the cycle cap. 'Always take the biggest pile' piles up ox-heads. Finishing the cycle removes the first seat's edge. A talk phase is left out: talk would add a message to every one of up to 40 sequential turns. In a sequential game where every action is already public, informal ganging up on the leader can be done through play itself, so talk would add words without adding a decision.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
