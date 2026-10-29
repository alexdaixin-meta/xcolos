# Variation: Love Letter: Short Hands

Two-player Love Letter on a thinner deck: 5 cards face up out of play and one hidden reserve card. Hands are short, so about 10 are played in 40 turns. Each hand offers one chance to raise the stake to 2, which the opponent may accept or answer by folding. The player with more points wins.

Players: 2 to 2, best with 2

## Review of the original

Love Letter is a 2-4 player card game with a 16-card deck ranked 1 (Guard) to 8 (Princess). Each turn you draw to two cards and discard one, applying its effect (guess, peek, compare, protect, force a discard, swap). A hand ends when one player remains or the deck runs out, and the highest card wins. Winning a hand earns a token, and the first player to a set number of tokens wins the game.

- **non_degenerate**: good. No simple policy dominates. Always discarding the higher card throws away strong showdown cards. Always discarding the lower card walks into Barons and Guards. Always guessing the same rank with a Guard hits about 1 time in 7. In the earlier variation, always raising is punished by an opponent who accepts with strong cards, and always folding gives away every raised hand. Seat order is balanced because the starter alternates.
- **skill_sensitive**: weak. Card counting, Priest information and reading discards improve Guard and Baron play. Many hands are still settled by the deal: being dealt the Princess, a lucky turn-1 Guard, or a Baron comparison fixed at the deal. The earlier variation fit only about 6-8 hands into 40 rounds and could triple the stake, so a skilled player won the match only about 60-65% of the time.
- **headroom**: good. Exact counting, inferring a hand from what an opponent chose to keep, Guard guessing that uses the guesses already announced, and well-timed bluff raises all leave room to improve. A novice still wins hands through the deal.
- **reasoning_dependent**: good. Hands are hidden. The deck and out-of-play cards allow counting. Discards and kept cards reveal likely holdings. A raise is a signal that can be read or bluffed.
- **verifiable**: good. Every effect and the showdown are rank comparisons, and the winner comes from adding up points. No judge is needed.
- **fits_platform**: weak. The game is turn-based text with no board, but the earlier variation sat at every limit (19 steps, 4 choices, about 20 attributes, 3 hidden elements). It also had a blocking bug: hands were never cleared between hands, so the second hand started with 2 cards per player.

## Problems

- P1 Blocking bug: players' hands are not cleared when a new hand is dealt, so the second hand starts with too many cards and contradicts the 16-card count.
- P2 Too few hands fit in 40 rounds (about 6-8), so the deal decides the match far more than skill does.
- P3 The raise triples the stake, so one or two lucky stake-3 hands decide the match.
- P4 It is ambiguous whether the Guard's named rank is public, which changes what can be inferred.
- P5 The design sits at or over the platform limits: 19 steps, about 20 attributes, and 3 hidden elements (hands, deck order, burned card).
- P6 Bookkeeping attributes the rules do not need (raised_this_hand, raiser, hands_won) push the attribute count to the limit.

## Changes

- The new-hand setup step first empties both hands (any card still held returns to the pool), then rebuilds the 16-card deck and deals 1 card to each player. (fixes: P1 Blocking bug): Every hand starts from exactly 16 cards with one card per player.
- Five cards (not 3) go face up out of play. This leaves 9 cards in the deck after the deal, of which 8 can be drawn. (fixes: P2 Too few hands): Hands become shorter (about 3-5 turns), so roughly 9-11 hands fit in 40 rounds. There is also more public information for counting.
- The raise lifts the stake from 1 to 2 only. A fold gives the raiser 1 point. (fixes: P3 Raise variance): A raised hand is worth at most double, so no single hand can swing the match. Bluffing and calling remain worthwhile.
- The Guard's named rank is announced to both players, along with whether it hit. (fixes: P4 Guard ambiguity): A missed guess becomes public information, as in the original game.
- The burned card is replaced by a reserve card: the bottom card of the deck, which is never drawn normally. The hand goes to showdown once only the reserve (or nothing) is left. A Prince redraw may take the reserve. (fixes: P5 Limits): The burn's role (one unknown card, and a card for a late Prince) is kept, but it becomes part of the deck order. Hidden elements drop from 3 to 2.
- Steps are merged (shuffle and deal in one step, pass turn and game end in one step). (fixes: P5 Limits): This brings the count down to 17 steps.
- raised_this_hand, raiser and hands_won are removed. A raise is allowed only while the stake is 1, and a fold always pays the active player, because the response happens in the raiser's own round. Equal points is a draw. (fixes: P6 Bookkeeping attributes): Attributes drop to 17 without changing any decision.

## Kept from the original

- The 16-card Love Letter deck with its original ranks, counts and effects (Guard through Princess, Countess rule, Princess self-elimination).
- Draw one, discard one, and apply the effect even if it hurts you.
- Hands end by elimination or by the deck running out, with the highest rank winning the showdown.
- Hidden one-card hands, face-up discards and public out-of-play cards for card counting (from the 2-player original).
- A short repeated series of hands where hand wins accumulate.

## The variation's rules

CARDS (16, stored once as full_deck): 5 Guard (rank 1), 2 Priest (2), 2 Baron (3), 2 Handmaid (4), 2 Prince (5), 1 King (6), 1 Countess (7), 1 Princess (8).

STATE
- Each player has: hand (private, seen only by its owner), discards (public list), points (start 0), protected (public, 0/1) and eliminated (public, 0/1).
- The table shows: out_of_play (public list), deck_count (public, always the number of cards in the deck), stake, active seat, starter seat (starts as seat 1) and round number.
- Hidden bookkeeping: deck order, new_hand (starts 1), folded, current_discard and guard_guess.
- The bottom card of the deck is the RESERVE. It is never drawn at the start of a turn.

ROUND: one round is one turn by the active player. The game lasts exactly 40 rounds. The steps run in order every round. A step marked 'when' runs only if its condition holds.

1. NEW HAND (when new_hand = 1):
- Empty both players' hands and discards, and clear out_of_play.
- Copy full_deck into the deck and shuffle it. This is the only random event in a round.
- Move the top 5 cards face up into out_of_play.
- Deal 1 card to each player's hand. The deck now holds 9 cards.
- Set protected = 0 and eliminated = 0 for both players, stake = 1 and folded = 0.
- The active seat becomes the starter seat. Set new_hand = 0.

2. START OF TURN: set the active player's protected to 0. The active player draws the top card of the deck, so they hold 2 cards.

3. DISCARD (choice, active player): 'Choose one of your two cards to discard.'

4. RESOLVE DISCARD: if the active player holds the Countess together with a King or a Prince, the Countess is discarded whatever was chosen. The card goes onto the player's discards and becomes current_discard. Everyone is told 'Seat X discards CARD'.

5. GUARD GUESS (choice, when current_discard is a Guard and the opponent is not protected): the active player names a rank from 2 to 8. The named rank is announced to both players.

6. GUARD CHECK (when step 5 ran): if the opponent's card has the named rank, the opponent is eliminated and everyone is told 'Hit: CARD'. Otherwise everyone is told 'Miss'.

7. PRIEST (when current_discard is a Priest and the opponent is not protected): only the active player is told the opponent's card.

8. BARON (when current_discard is a Baron and the opponent is not protected): the two hand cards are compared. The holder of the lower rank is eliminated and their card is announced. On equal ranks nothing happens and nothing is revealed.

9. HANDMAID (when current_discard is a Handmaid): the active player becomes protected (until their next turn starts).

10. PRINCE DISCARD (when current_discard is a Prince): the target is the opponent, or the active player if the opponent is protected. The target discards their hand card face up with no effect, and it is announced. If it is the Princess, the target is eliminated.

11. PRINCE REDRAW (when step 10 ran and the target is not eliminated): the target takes the top card of the deck. This may be the reserve if it is the only card left.

12. KING (when current_discard is a King and the opponent is not protected): the two players swap hand cards.

13. PRINCESS (when current_discard is the Princess): the active player is eliminated.

14. RAISE (choice, active player; only when stake = 1, nobody is eliminated, deck_count >= 2 and the opponent has at least one card in their discards): 'Raise this hand's stake to 2, or pass?'

15. RESPONSE (choice, opponent; when a raise was just made): 'Accept (the stake becomes 2) or fold?' On accept, stake = 2. On fold, folded = 1.

16. HAND END. Apply the first of these that holds:
- (a) If folded = 1, the active player gains 1 point.
- (b) Otherwise, if a player is eliminated, the other player gains points equal to the stake.
- (c) Otherwise, if deck_count <= 1 or this is round 40, there is a showdown. Both hand cards are revealed and the higher rank gains points equal to the stake. On equal ranks nobody scores.
If (a), (b) or (c) applied, set new_hand = 1 and switch the starter seat to the other seat.

17. PASS TURN AND GAME END:
- If new_hand = 1, the active seat becomes the starter seat. Otherwise the opponent becomes the active player.
- After round 40 the game ends.

DECK CHECK: after the deal the deck holds 9 cards. A hand goes to showdown whenever 1 or 0 cards remain at the end of a turn. So every turn starts with at least 2 cards in the deck, the draw always leaves at least the reserve, and a Prince redraw always has a card to take.

Objective: After exactly 40 rounds (a hand still running in round 40 is settled by showdown in that round), the player with more points wins. Equal points is a draw.

Expected effect: With 8 drawable cards and 5 known out of play, hands last about 3-5 turns, so about 9-11 hands are played instead of 6-8. More hands and a stake capped at 2 should let a counting, discard-reading player win noticeably more often, an estimated 65-72% of matches against a naive player. Fewer unknown cards make counting and Guard guessing sharper. The raise stays as a bluff-and-call decision. Showdown luck within a hand remains, but no single hand decides the match. No talk phase: this is a two-player game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 17 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
