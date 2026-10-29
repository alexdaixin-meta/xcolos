# Variation: Love Letter Duel: Long Courtship

A two-player Love Letter played over exactly 40 turns. Each hand sets aside 1 hidden and 5 face-up cards, any hand still running at turn 40 is settled by showdown, and the player with more tokens wins, with ties broken by total ranks discarded across the game.

Players: 2 to 2, best with 2

## Review of the original

Love Letter is a 2–4 player deduction card game played with 16 ranked cards. Each turn a player draws one card and discards one of their two, triggering its effect (guess, peek, compare, protect, force a discard, swap, or eliminate themselves). The last player standing, or the highest hand when the deck runs out, wins a token, and the first player to a set number of tokens wins.

- **non_degenerate**: good. No fixed policy is safe. 'Always discard the lower card' gives away predictable hands that Guards and Barons punish. 'Always discard the higher card' throws away Princesses and loses Barons and showdowns. 'Always guess 2' with a Guard misses most of the time. The seat edge is small because the loser of a hand starts the next one. In the reviewed duel variation the main defect was not degeneracy but the short first-to-3 race.
- **skill_sensitive**: weak. Chance decides roughly 40–50% of individual hands even between equal players: blind Guard hits, forced Princess or Countess draws, the burned card. A skilled player wins perhaps 60–65% of hands. First to 3 tokens turns that into only about 72% of games, and the 40-turn cap with unfinished hands discarded adds draws and stale leads.
- **headroom**: good. There is a lot to improve at: card counting over the live cards, Guard guess selection, Baron timing, Handmaid timing, Countess bluffs, and using King or Prince after a Priest peek. A weak player still wins hands through the deal.
- **reasoning_dependent**: good. Hands, deck order and the burned card are hidden. Each discard leaks information about the card kept, so a player must infer the opponent's card from the visible cards and the pattern of their choices.
- **verifiable**: good. Eliminations, showdown comparisons, tokens and tiebreaks are all arithmetic on tracked cards and sums.
- **fits_platform**: weak. The game is turn-based and text-only with no board. However, the reviewed duel variation had broken gating on Priest, Baron and King, so the protected message could never fire. It also threw away the hand in progress at round 40, and it listed hidden elements unclearly.

## Problems

- P1: First to 3 tokens is too short a race. The deal decides about 28% of games even when one player is clearly better.
- P2: A hand still unfinished at round 40 scores nothing. This produces draws and stale leads that depend on how many turns the deck happened to give.
- P3: Equal final tokens is a plain draw, which happens often over an even number of hands.
- P4: The Priest, Baron and King steps were gated on 'opponent not protected', so the protected announcement could never fire. Their effects also lacked a clear branch for a protected opponent.
- P5: Hands are long (up to 9+ draws), so few hands are played in 40 turns and per-hand luck is poorly averaged. With only 4 face-up cards, early Guard guesses are close to blind.
- P6: Hidden elements were not stated, and the private hand message did not say which card was newly drawn.
- P7: Constant parameters used up attribute slots needed for a tiebreak attribute.

## Changes

- Remove the 3-token immediate win and play all 40 turns. The winner is decided by tokens at the end. (fixes: P1): About 8 or more hands are averaged instead of a best-of-five, so the better player wins more reliably.
- On turn 40, if the hand is still running after the turn's effects, hold a showdown immediately and award the token. (fixes: P2): No hand is wasted, and the last turns carry real decisions.
- Add a career_sum player attribute: the cumulative total of all ranks each player has discarded over the game. It breaks equal tokens before declaring a draw. (fixes: P3): Draws become rare. The tiebreak also creates a small real trade-off, because discarding high cards helps the tiebreak but weakens a player's showdown hand.
- Gate Priest, Baron and King only on which card was discarded. Inside each step, check whether the opponent is protected: if so, announce protected; if not, apply the effect. (fixes: P4): Handmaid protection is reported correctly and the effects are unambiguous.
- Set aside 6 cards per hand instead of 5: 1 face down (burned) and 5 face up. The deck after the deal is then 8 cards, not 9. (fixes: P5): Hands are shorter, so more hands fit in 40 turns. More public information also makes Guard guesses and counting depend on inference rather than blind luck.
- State the hidden elements as three: hands, deck order and the burned card. The private message names which card was kept and which was just drawn. (fixes: P6): Gives a clear build and clear information for players.
- Write constants (16, 6, 8, guess range 2–8, 40) as literals in the steps rather than as attributes. (fixes: P7): Frees attribute slots for career_sum and keeps the total at 14.

## Kept from the original

- The 16-card deck and the eight card effects, including the Countess rule and Princess self-elimination
- Draw one, discard one, apply the effect even if it hurts you
- A burned card, face-up set-aside cards in the two-player game, and the Prince drawing the burned card when the deck is empty
- Last player standing or highest card at showdown wins the hand, with ties broken by discard sum
- Tokens of affection across several hands, and the loser of a hand starts the next one

## The variation's rules

CARDS (16): rank 1 Guard x5, rank 2 Priest x2, rank 3 Baron x2, rank 4 Handmaid x2, rank 5 Prince x2, rank 6 King x1, rank 7 Countess x1, rank 8 Princess x1.

ZONES: deck (hidden order); out_of_play (6 cards: position 1 is the face-down burned card, positions 2-6 are face up); each player's hand (hidden, seen only by its owner); each player's discards (public). Every card is always in exactly one zone, so the zones total 16.

HIDDEN ELEMENTS: hands, deck order, burned card.

GAME STATE: deck, out_of_play, deck_count, active_seat (starts 1), hand_over (starts 1), discard_choice, guess.

PLAYER STATE: hand, discards, discard_sum (reset each hand), career_sum (whole game, starts 0), tokens (start 0), protected, eliminated.

The game lasts exactly 40 rounds. Each round is one turn of the active player:
1. NEW HAND (only if hand_over = 1). Return all cards to the deck and shuffle it; this is the round's only random draw. Move the top 6 cards to out_of_play (the first one to position 1, face down). Deal 1 card to each player's hand. Set deck_count = 8. Set protected, eliminated and discard_sum to 0 for both players. Set hand_over = 0.
2. If a new hand was just dealt, announce: 'The face-up out-of-play cards are ranks a, b, c, d, e' (positions 2-6).
3. START TURN. Set the active player's protected to 0. They take the top deck card, and deck_count goes down by 1. Privately tell them: 'You kept rank X and just drew rank Y.'
4. CHOICE. The active player chooses which of their two ranks to discard; store it in discard_choice.
5. COUNTESS. If they hold rank 7 together with rank 5 or rank 6, set discard_choice = 7.
6. DISCARD. Move the chosen card to their discards. Add its rank to their discard_sum and career_sum. Announce 'Seat s discards rank r (name).'
7. GUARD GUESS (if discard_choice = 1). The active player names a rank from 2 to 8; store it in guess.
8. GUARD RESOLVE (if discard_choice = 1). If the opponent is protected, announce that the card has no effect. Otherwise, if the opponent's card equals guess, set the opponent's eliminated = 1 and announce a hit; if not, announce a miss.
9. PRIEST (if discard_choice = 2). If the opponent is protected, announce no effect. Otherwise, privately tell the active player the opponent's rank, and announce publicly that Seat s looked at Seat o's card.
10. BARON (if discard_choice = 3). If the opponent is protected, announce no effect. Otherwise compare the two hand cards: the owner of the lower one gets eliminated = 1, and the result is announced with the losing rank. If the cards are equal, announce a tie and nobody is out.
11. HANDMAID (if discard_choice = 4). Set the active player's protected = 1 and announce it.
12. PRINCE (if discard_choice = 5). The target is the opponent, or the active player if the opponent is protected. The target moves their hand card to their discards, adds its rank to their discard_sum and career_sum, and the rank is announced. If that card was rank 8, the target's eliminated = 1. Otherwise the target draws the top deck card if deck_count > 0 (deck_count goes down by 1), or else takes the burned card from out_of_play position 1.
13. KING (if discard_choice = 6). If the opponent is protected, announce no effect. Otherwise the two players swap hand cards, and the swap is announced.
14. PRINCESS (if discard_choice = 8). The active player's eliminated = 1; announce it.
15. SHOWDOWN (if nobody is eliminated and (deck_count = 0 or this is round 40)). Announce both hand ranks. The owner of the lower card gets eliminated = 1. If the cards are equal, the owner of the lower discard_sum gets eliminated = 1. If those are also equal, announce that the hand is tied and set hand_over = 1.
16. AWARD (if exactly one player is eliminated). The other player gains 1 token; announce the new total. Set hand_over = 1. The eliminated player becomes active_seat for the next hand.
17. PASS (if no token was awarded this round). active_seat switches to the other seat.
18. END CHECK. After round 40 the game ends.

Objective: After round 40, the player with more tokens wins. If tokens are equal, the player with the higher career_sum (total ranks they discarded over the whole game, including cards a Prince forced them to discard) wins. If both are equal, the game is a draw.

Expected effect: About 8–10 short hands are averaged, instead of a race to 3 that a lucky start can decide. With 5 face-up cards and only 8 deck cards, Guard guesses and Baron or King timing rest on counting and reading the opponent's discards rather than blind odds, so I estimate a skilled player wins 75–80% of games against a heuristic one. The final turn always matters because the open hand is settled. Simple policies all lose: 'always discard the lower card' is read and punished by Guards and Barons; 'always discard the higher card' loses showdowns and discards Princesses; a fixed Guard guess misses most of the time. When both players play well, deal luck still decides some individual hands, but not the game. Talk is not used because there are only 2 players.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
