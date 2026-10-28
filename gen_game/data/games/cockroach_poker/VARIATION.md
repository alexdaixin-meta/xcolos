# Variation: Cockroach Poker: Straight Calls

This is a three-player game. A sender hands one face-down card to a chosen rival and claims its creature. The rival calls TRUE or FALSE, and whoever is wrong takes the card face-up. The game ends as soon as one player loses, and the other two are ranked by fewest face-up cards.

Players: 3 to 3, best with 3

## Review of the original

Cockroach Poker is a bluffing card game. Players slide a face-down card to another player and name its creature, truthfully or not. The receiver either calls the claim true or false, or peeks and passes the card on. Whoever is wrong takes the card face-up, and a player loses on collecting four of one creature or on having to start a turn with an empty hand.

- **non_degenerate**: good. The previous build showed simple policies losing heavily. first@seat1 went 4-53-3, first@seat2 2-55-3, last@seat1 20-31-9 and last@seat2 21-36-3. Always calling FALSE, always telling the truth and always targeting one player can all be read and punished, because the sender adapts the true-claim rate to the receiver's habit. One weakness: seat 2 won 20 of 60 against random seats and seat 3 won 11, a seat skew probably caused by the fixed first sender.
- **skill_sensitive**: good. Results come from reading lies, tracking which creatures are already face-up and choosing whom to target. The deal changes what each player can claim believably, but card-counting and opponent modelling decide most rounds.
- **headroom**: good. Weak players still win some rounds on calls that are right by chance. Strong players improve by modelling each opponent's lying frequency, using face-up information and steering cards toward the player closest to three of a kind.
- **reasoning_dependent**: good. Each player's hand and the removed cards are hidden. Every call is an inference about the sender's honesty. Every send is a plan about the receiver's likely call and about the elimination race.
- **verifiable**: good. A call is checked by revealing the card, and losses are counts of face-up cards or an empty hand. The only weak point is the previous non-loser ranking, which produced many shared wins: 18 of 60 games against random play ended with two seats sharing the win.
- **fits_platform**: bad. The previous build had 7 choice steps per round against a limit of 4, because passing adds a peek, a pass-or-call decision, a new receiver and a new claim. Variable-length pass chains are also a conditional block the flat step list cannot express.

## Problems

- The PASS mechanic pushes choice steps per round to 7, over the limit of 4, and needs a conditional sub-sequence the engine lacks.
- Seat imbalance against random play (seat 2 won 20, seat 3 won 11, seat 1 won 11 outright), most likely from a fixed first sender and fixed seat order.
- Many shared wins between the two non-losers (18 of 60 random games), so the ending often fails to separate players.
- A 64-card, 8-creature deck makes hands large and card-counting too diffuse for a short text game. With few creatures face-up, the inference is weak until very late.

## Changes

- Drop PASS entirely. Each round the sender chooses a card, chooses a claimed creature and chooses a receiver, and the receiver calls TRUE or FALSE. That is exactly 4 choice steps. (fixes: The PASS mechanic pushes choice steps per round to 7, over the limit of 4, and needs a conditional sub-sequence the engine lacks.): This keeps the core bluff-and-call duel inside the limit, and the step list becomes flat.
- Choose the first sender at random during setup instead of always seat 1. After that, whoever takes a card sends next, as in the original. (fixes: Seat imbalance against random play (seat 2 won 20, seat 3 won 11, seat 1 won 11 outright), most likely from a fixed first sender and fixed seat order.): This removes the built-in seat advantage while keeping the original's rule that the loser of a card starts the next round.
- Shrink the deck to 4 creatures x 6 copies (24 cards). Deal 7 to each of 3 players and set 3 aside unseen. A player loses on 3 face-up cards of one creature. (fixes: A 64-card, 8-creature deck makes hands large and card-counting too diffuse for a short text game. With few creatures face-up, the inference is weak until very late.): Fewer creatures make face-up information and card-counting meaningful and the game short. The 3 hidden cards keep counting from becoming certain.
- Use a chain of arithmetic tie-breaks among non-losers. First, fewest face-up cards. Then fewest cards of their single most common face-up creature. Then most cards still in hand. Only after that is it a draw. (fixes: Many shared wins between the two non-losers (18 of 60 random games), so the ending often fails to separate players.): Outright winners become far more common, and every tie-break is a count the engine tracks.

## Kept from the original

- Face-down card handed over with a claim that may be a lie.
- The receiver calls TRUE or FALSE, and whoever is wrong takes the card face-up.
- Losing by collecting too many of one creature, or by having to send with an empty hand.
- The loser of a card sends next, so being caught creates pressure to act.
- The sender chooses whom to target, which creates ganging-up and elimination-race dynamics.

## The variation's rules

SETUP
- The deck has 24 cards: 4 creatures (Cockroach, Rat, Stinkbug, Toad), 6 copies of each.
- Shuffle. Deal 7 cards face-down to each of the 3 players as their private hand. Set the remaining 3 cards aside face-down, unseen by anyone, for the whole game.
- Each player starts with no face-up cards.
- Choose the first sender uniformly at random.

EACH ROUND (at most 24 rounds)
1. Announce the round number, the sender, and every player's face-up cards (counts per creature) and hand size.
2. The sender privately chooses one card from their own hand.
3. The sender chooses a claim: one of the 4 creatures. It may be true or false.
4. The sender chooses a receiver: either of the other two players.
5. The receiver, who sees the claim but not the card, calls TRUE (the card is the claimed creature) or FALSE (it is not).
6. Reveal the card to everyone.
   - The receiver is correct if they called TRUE and the card matches the claim, or called FALSE and it does not.
   - If the receiver is correct, the sender takes the card face-up.
   - If the receiver is wrong, the receiver takes it face-up.
   - Either way, the card has left the sender's hand.
7. The player who took the card face-up becomes the sender for the next round.
8. Loss check: if the player who took the card now has 3 face-up cards of the same creature, that player LOSES and the game ends.
9. Empty-hand check: if the next sender has no cards in hand, that player LOSES and the game ends.
10. If round 24 has finished without a loser, the game ends with no loser.

TALK
There is no separate talk phase. The claim is the only message.

ENDING
When the game ends, the losing player (if any) cannot win. The players who did not lose are ranked by these tests in order:
(a) fewest total face-up cards;
(b) if tied, the smaller count of their single most common face-up creature;
(c) if still tied, the most cards remaining in hand.
The player ranked first wins. If the top players are tied on all three tests, the game is a draw between them.

Objective: Avoid being the loser, who ends the game with 3 face-up cards of one creature or must send with an empty hand. Among the players who did not lose, the one with the fewest face-up cards wins. Ties are broken by the smaller count of their most common face-up creature, then by more cards left in hand. Players tied on all three draw.

Expected effect: Every round is a two-player lie-detection duel with a third player watching and keeping score. Senders must vary their truth rate per receiver, because a receiver who always calls FALSE is beaten by honest claims and one who always calls TRUE is beaten by lies. Face-up counts and the shrinking 24-card deck let players reason about what a sender can still hold, and claiming a creature the receiver already has two of becomes a pointed threat. A random first sender removes the seat skew, and the three-step tie-break should turn most shared non-loser wins into outright wins.

Talk is left out deliberately. The claim already is the communication, and a free chat would mostly repeat claims or let two players openly coordinate against the third. That second effect already arises tacitly through the choice of receiver, which keeps it a matter of reading rather than of announcing.

Because the winner is the non-loser with the fewest face-up cards, nobody can safely coast. Pushing cards onto the leader matters as much as sinking the weakest player, so a player who blindly piles onto whoever is nearly eliminated can end the game while holding more face-up cards than the other survivor, and lose.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
