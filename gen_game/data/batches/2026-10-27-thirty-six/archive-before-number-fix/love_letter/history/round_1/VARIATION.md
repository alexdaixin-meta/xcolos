# Variation: Love Letter: One Raise

Two-player Love Letter played as a race to 5 points. In each hand, the player whose turn it is may raise the stake from 1 to 2 once before drawing; the opponent accepts or concedes 1 point.

Players: 2 to 2, best with 2

## Review of the original

Love Letter is a 2-4 player elimination card game with a 16-card deck ranked 1 (Guard) to 8 (Princess). On each turn a player holds one card, draws a second and discards one, applying its effect. A hand is won by being the last player standing or by holding the highest card when the deck runs out, and the match is a race to a number of tokens.

- **non_degenerate**: good. No simple policy dominates. 'Always discard the higher card' throws away the Princess and eliminates you. 'Always discard the lower card' keeps you predictable to Guards and Barons. 'Always guess 2 with the Guard' ignores the face-up cards and the discards. The original's winner-starts rule gives a mild snowball, but no seat has a structural edge. In the previous variation, the fixed 4-hand match with a doubling cube created a policy that cannot lose: once the lead exceeds the number of hands left, conceding every double and never doubling locks the match.
- **skill_sensitive**: weak. Card counting, Guard guesses informed by the three face-up cards and the discards, and Priest/Baron timing all matter. A single hand is still very random. A turn-1 Guard hits about 1 time in 6 or 7, and being dealt the Princess against a Guard decides the deck-out comparison. A skilled player wins perhaps 55-60% of hands. Only a long race (7 tokens in 2-player) lets skill show. The previous 4-hand version with stakes up to 8 made one deal decisive.
- **headroom**: good. Weak players still win hands because of luck. Strong players improve by tracking the remaining cards, reading what the opponent's discards say about the card they kept, and bluffing through their own discard order. The game is not solved.
- **reasoning_dependent**: good. The whole game is inference about one hidden card. The evidence is which cards are gone, what the opponent chose to keep, Priest knowledge, and what a King swap transfers. A betting layer adds opponent modelling of confidence.
- **verifiable**: good. Eliminations, the deck-out comparison and token counts are all arithmetic. No judgement is needed.
- **fits_platform**: weak. The game is turn-based and text-only with no board. As previously adapted it needed 4 hidden elements (two hands, the burned card, the deck order) and about 24-27 steps per round, over the limits of 3 and 20. A Prince-forced draw on top of the normal draw would also need two random draws in one turn unless the deck is shuffled once and then read from the top.

## Problems

- P1 Lock: the previous variation's fixed 4-hand length lets a leader concede every double and never lose. Any lead greater than the hands remaining is a guaranteed win, so late hands are dead.
- P2 Variance: stakes up to 8 in a 4-hand match let one lucky deal decide everything. Love Letter hands are already luck-heavy.
- P3 Hidden elements: two hands plus a separate burned card plus the hidden deck order make 4, over the limit of 3.
- P4 Step count: realistic steps per round were 24-27, over 20, and the attribute budget was exhausted.
- P5 Random draws: a Prince on yourself plus the normal draw could mean two random draws in one turn.
- P6 Dead hands: equal cards at deck-out scored nothing, adding zero-score hands and match draws.
- P7 Snowball and seat edge: who starts each hand gives a mild tempo edge that compounds over a short match.

## Changes

- Replace the fixed 4 hands with a race: the first player to reach 5 points wins immediately. Only if the 40-turn cap is reached first does the higher score win, with ties broken by hands won. (fixes: P1 Lock): A conceded double now pays the opponent 1 point toward the target and immediately restarts a hand they may double again. Conceding is a real cost, not a free lock. A lead can only become safe when it exceeds what can be scored in the turns left, which is a genuine endgame.
- Allow at most one double per hand: the stake is 1 or 2 and cannot be redoubled. A concede pays 1. (fixes: P2 Variance): This caps the swing of any single deal at 2 points out of a 5-point race, so several hands decide the match. It keeps the bluff-and-read decision of the cube.
- Shuffle the deck once at hand start, then draw only from the top. The burned card becomes the bottom card of the deck. The hand ends when only that bottom card remains, and that card serves only a late Prince. (fixes: P3 Hidden elements; P5 Random draws): The hidden elements are now exactly Seat 1's card, Seat 2's card and the deck order. The only random event is the hand-start shuffle, so a turn has at most one random draw.
- Merge setup into one step. Fold the forced Countess, Handmaid and Princess into a single post-play bookkeeping step using operation-level ifs. Merge elimination payout and deck-out comparison into one scoring step. Replace per-player eliminated flags with a single 'hand winner' attribute. (fixes: P4 Step count): This brings the honest count to 18 steps, 4 choice steps and 19 attributes.
- At deck-out with equal cards, the higher sum of that hand's own discards wins. If that is also equal, nobody scores. (fixes: P6 Dead hands): It restores Love Letter's own tie-break and removes most dead hands.
- Seat 1 starts hand 1. After that, the player who did not win the previous hand starts the next one; if nobody scored, the seat that did not start last time starts. (fixes: P7 Snowball and seat edge): It gives a small catch-up instead of a winner-keeps-tempo snowball and offsets Seat 1's hand-1 start.

## Kept from the original

- The 16-card deck with eight ranks and all eight original effects
- Holding one hidden card, drawing to two, and discarding one with its effect applied even if harmful
- The 2-player setup of three face-up out-of-play cards and one unseen burned card
- Winning a hand by elimination or by the highest card at deck-out, with the discard-sum tie-break
- A race to a points target across several hands
- The confidence-reading double from the earlier variation, now bounded

## The variation's rules

CARDS (16): five 1-Guard, two 2-Priest, two 3-Baron, two 4-Handmaid, two 5-Prince, one 6-King, one 7-Countess, one 8-Princess.

PLAYERS: Seat 1 and Seat 2. Each starts with 0 points and 0 hands won.

ROUNDS: Each round is one turn by one player, the active player. The match lasts at most 40 turns.

STARTING A HAND (done at the start of a turn whenever a new hand is due, including turn 1):
- Shuffle all 16 cards into a deck. This is the only random event of the turn.
- Remove the top 3 cards face up as out of play and announce them to both players.
- Deal the next card face down to the starting player and the next to the other player. Each player sees only their own card.
- The remaining 11 cards stay as the deck in shuffled order, unseen. The bottom card of the deck is the burned card: it is never drawn normally.
- Stake = 1, no raise has been made, nobody is protected, and every player's discard sum for the hand = 0.
- Seat 1 starts hand 1. Afterwards, the player who did not win the previous hand starts. If nobody scored in the previous hand, the seat that did not start it starts.
- The starting player takes the first turn of the hand, which is this turn.

A TURN:
(1) RAISE: if no raise has been made in this hand, the active player, holding their one card, chooses 'raise' or 'no raise'.
(2) RESPONSE: if they raised, the opponent chooses 'accept' or 'concede'.
(3) RESOLVE:
- On 'concede', the active player wins the hand and gains 1 point. The hand ends and the rest of the turn is skipped; go to step 11.
- On 'accept', the stake becomes 2. No further raise is possible this hand.
(4) DRAW: the active player loses any Handmaid protection and takes the top card of the deck. They now hold two cards, seen only by them.
(5) PLAY: the active player chooses one of their two cards to discard face up.
(6) BOOKKEEPING:
- If they hold the Countess together with the King or a Prince, the Countess is discarded instead, whatever they chose.
- Add the discarded card's rank to their discard sum.
- If the discard is the Handmaid, they are protected until the start of their next turn.
- If the discard is the Princess, they are eliminated.
(7) DETAIL:
- If the discard is a Guard, the active player names a number from 2 to 8.
- If it is a Prince, they choose a target, themselves or the opponent. If the opponent is protected, they must target themselves.
(8) EFFECTS. The Guard, Priest, Baron and King do nothing if the opponent is protected.
- Guard: if the opponent's card equals the named number, the opponent is eliminated.
- Priest: the opponent's card is shown privately to the active player.
- Baron: both players privately see each other's cards. The lower card's holder is eliminated; on equal cards nothing happens.
- Prince: the target discards their card face up without effect and adds its rank to their discard sum. If it was the Princess, they are eliminated. Otherwise they take the top card of the deck; this may be the burned card if it is the only card left.
- King: the two players swap their cards.
- Countess, Handmaid, Princess: no further effect.
(9) ANNOUNCE to both players: the card discarded, any Guard number or Prince target, any card discarded by a Prince, any elimination together with the eliminated player's revealed card, the stake, both scores, and the number of cards left in the deck.
(10) HAND END CHECK:
- If a player is eliminated, the other player wins the hand and gains points equal to the stake.
- Otherwise, if the deck now holds 1 card or fewer, both players reveal their cards. The higher card wins the hand and gains the stake. On equal cards, the higher discard sum for this hand wins and gains the stake. If both are equal, nobody scores.
- The winner of a hand adds 1 to their hands won.
(11) MATCH CHECK AND NEXT TURN:
- If a player has 5 or more points, they win the match immediately.
- Otherwise, if this was turn 40, the match ends (see objective).
- Otherwise, if the hand ended, the next turn starts a new hand. If it did not, the other player becomes active.

Objective: The first player to reach 5 points wins; only one player can score per hand, so two players never reach 5 at once. If 40 turns pass with neither at 5, the player with more points wins. If points are equal, the player with more hands won wins. If those are also equal, the match is a draw.

Expected effect: Each hand is still classic Love Letter inference: counting cards against the three face-up cards and the discards, guessing with the Guard, timing the Priest and Baron, and bluffing through discard order. The raise adds a recurring read of the opponent's confidence while they hold a single card. Raising on a weak card can make the opponent concede for 1, but an accepted raise doubles the loss. Conceding is never a free lock, because every concede gives the opponent 1 point of the 5 needed and the next hand can be raised again. With swings capped at 2 and roughly 6-8 hands per match, no single deal decides the result. Simple policies fail. 'Always raise' loses 2-point hands whenever the opponent accepts on strength. 'Always concede' hands the opponent about a point per hand. 'Always accept' gets raised on every Princess and Countess. Luck within a hand remains real, so skill shows through over the series of hands. Talk is omitted: in a 2-player zero-sum race any message is pure cheap talk with nothing to bargain over.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
