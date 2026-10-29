# Variation: Row Yaniv

A simultaneous-round Yaniv for 2 to 4 players. Each player holds up to three private cards. A hand uses one shuffled deck, with a public offer row of last round's discards and a public dead pile. Each round, every player at once either calls Yaniv or sheds a card (or a set) and replaces it, either by taking a card from the row or by drawing blind. The lowest penalty total after 24 rounds, or when someone reaches 50, wins.

Players: 2 to 4, best with 3

## Review of the original

Yaniv is a shedding card game. Players discard singles, sets or runs and draw from a blind pile or from the previous discard, trying to bring their hand total low enough to call Yaniv. A caller who is not strictly lowest takes a penalty (Asaf), penalties build up across hands, and players are eliminated past a total. The reviewed predecessor, Slot Yaniv, turned it into simultaneous rounds with three private card slots and a bid for one upcard.

- **non_degenerate**: good. The Asaf penalty punishes always calling. Never calling lets a low-handed opponent take 0 while you pay your hand total. Always shedding the highest card is sensible but does not decide when to call. In the predecessor, the tie-break priority over 15 rounds gave the seats 8/7 or 4/4/4/3 shares, a small built-in seat edge.
- **skill_sensitive**: weak. The predecessor re-shuffled a full deck every round, and held cards stayed in it. Every draw was therefore an independent card with mean 6.3. With only 2 to 4 showdowns in 15 rounds, about 60-70% of results between competent players came from the draw.
- **headroom**: weak. Shed highest, take a low upcard, bid 0 or 1 and call at a low total was close to optimal. Little remained for a stronger player to discover beyond Yaniv timing.
- **reasoning_dependent**: weak. Hands are hidden, but with no persistent deck there was no card counting. Taking had only one public option, so taking revealed and denied little. The real inference left was reading an opponent's total from their public sheds and card count.
- **verifiable**: weak. Scoring is pure arithmetic. However, rule 8 left three of a kind undefined: 'that card' is singular. That case arises in about 2.6% of fresh deals alone, and it changes hand size and the showdown result.
- **fits_platform**: good. 17 steps, 1 random draw per round, 15 rounds and about 16 attributes, all within the limits. Text-only, with no board.

## Problems

- P1: Three of a kind on shedding is undefined. One or two matching cards might be removed, so the outcome is ambiguous.
- P2: The deck is re-shuffled full every round with held cards included. Card counting and discard tracking, the core inference of Yaniv, are gone.
- P3: Only one public takeable card exists. Taking is an obvious threshold decision that reveals little and denies little.
- P4: Hands last too long relative to the match: threshold 7 on 3 cards, 15 rounds, about 2 to 4 showdowns. A few lucky draws decide the match, and the end total of 60 is rarely reached.
- P5: When everyone plays the obvious heuristic, the shuffle alone decides the winner. This is the lottery trap.
- P6: The tie-break priority is shared unequally between seats over 15 rounds.
- P7: The bid sub-game adds steps but mostly reduces to bidding 0 or 1. It is complexity without much reasoning.

## Changes

- When a shed card matches other slots, every other slot with the same value is also shed and stays empty. A triple sheds all three. (fixes: P1: Three of a kind on shedding is undefined.): Gives one unambiguous rule for pairs and triples.
- Shuffle once per hand, not every round. Deal from a running draw pile. Keep a public dead pile of every card that has left play this hand. If the draw pile cannot serve every player, that round's showdown is forced. (fixes: P2: The deck is re-shuffled full every round with held cards included.): Players can count the 54-card deck. They can infer what remains in the pile and what opponents hold from what they kept. There is still at most one random event per round, and no mid-hand reshuffle is needed.
- Replace the single upcard with an offer row. It holds all cards shed in the previous round, numbered in order. Each player may TAKE one card from it by position. Conflicts are resolved in rotating priority order, and a player who loses a conflict draws blind. Unclaimed offer cards go to the dead pile. (fixes: P3: Only one public takeable card exists.): Taking becomes a public, informative choice. It shows what you are collecting, for example pairs or low cards. It can deny an opponent the card they need, and it forces guesses about who else wants the same card.
- Raise the Yaniv threshold to 10. Extend the match to 24 rounds. End early when any total reaches 50 after a showdown. (fixes: P4: Hands last too long relative to the match.): Hands end in about 3 to 5 rounds, giving roughly 5 to 7 showdowns. Luck averages out, and the end total actually comes into play.
- Remove the bid. Rotate priority every round. Allow only 2 to 4 players with 24 rounds, a number divisible by 2, 3 and 4. (fixes: P6: The tie-break priority is shared unequally between seats; P7: The bid sub-game adds steps but mostly reduces to bidding 0 or 1.): Over a full match every seat gets priority equally often. Removing the bid frees steps for the offer row.
- The overall combination: counting, a choice of takeable cards, readable sheds and more showdowns. (fixes: P5: When everyone plays the obvious heuristic, the shuffle alone decides the winner.): Among heuristic players the draw still matters. A player who counts low cards, tracks what opponents took and times Yaniv against an opponent's likely total beats a fixed heuristic over 5 to 7 showdowns.

## Kept from the original

- Card values: Ace 1, 2-10 face value, J/Q/K 10, Joker 0, in a 54-card deck
- Shedding a single card or a matching set
- Choosing between a known discard and a blind draw
- Calling Yaniv below a threshold; lowest hand scores 0, others score their hand total
- The Asaf penalty for a caller who is not strictly lowest
- Penalty totals built up across hands, with a match-ending total and lowest total winning

## The variation's rules

DECK: 54 cards, used only for their values: two Jokers worth 0; four each of values 1 to 9 (Ace = 1); sixteen cards worth 10 (the 10s, Jacks, Queens and Kings). Only values matter; suits are ignored.

STATE: Each player has three private slots c1, c2 and c3. Each slot holds one card value or is empty. A player's hand total H is the sum of their non-empty slots. Each player has a public penalty total, starting at 0.
Public table state:
- the round number (1 to 24);
- the priority seat (seat 1 in round 1);
- a 'new hand' flag (on at the start);
- the draw pile, whose order is hidden and whose size is public;
- the OFFER ROW, an ordered public list of cards;
- the DEAD PILE, a public list of every card that has left play this hand.

EACH ROUND:
1. NEW HAND. If the 'new hand' flag is on: shuffle all 54 cards to form the draw pile. This is the only random event in any round. Empty all slots, empty the dead pile, and deal 3 cards from the top of the draw pile to each player in seat order, into c1, c2 and c3, told privately. Then turn the next card face up as the offer row (one card at position 1). Switch the flag off.
2. ANNOUNCE the offer row with its positions and values, the dead pile, the draw pile size, the priority seat, and each player's number of cards.
3. CHOICES. All players answer at the same moment, privately, three things:
   (a) action: YANIV, DRAW, or TAKE;
   (b) take position: a number from 1 to the length of the offer row (used only for TAKE);
   (c) shed slot: 1, 2 or 3. It must be a non-empty slot; if it is not, the lowest-numbered non-empty slot is used.
4. YANIV CHECK. A YANIV is valid only if the player's H is 10 or less. An invalid YANIV is announced as invalid, and that player is treated as DRAW for the rest of the round.
5. If at least one valid YANIV was made, no cards move this round. Go to step 10.
6. SHED. Each player removes the card in their shed slot. Every other slot of theirs holding the same value is also removed, so a pair sheds two cards and a triple sheds three. Those extra slots stay empty for the rest of the hand. Announce every player's shed card values.
7. TAKE. Go through the TAKE players in seat order, starting at the priority seat and wrapping around. Each one receives the offer-row card at their take position if no earlier player has claimed it, and places it in their shed slot. Announce who took which card. A TAKE player whose card was already claimed becomes DRAW.
8. DRAW. In the same order (from the priority seat), each DRAW player takes the top card of the draw pile into their shed slot, told privately. The drawn value is never announced.
9. ROW UPDATE. All offer-row cards not taken go to the dead pile. The new offer row is every card shed in step 6, listed in seat order from seat 1, and within a player in the order of their slots. Announce each player's card count and the draw pile size.
10. SHOWDOWN. A showdown happens in any of three cases:
   - a valid YANIV was made this round;
   - after step 9 the draw pile holds fewer cards than there are players;
   - this is round 24.
   All hands are revealed.
   If there were valid callers: let M be the lowest H among the callers, and N the lowest H among the non-callers (N = 99 if everyone called).
   - A caller scores 0 if their H equals M and M is less than N. Otherwise they score H + 20 (Asaf).
   - A non-caller scores 0 if their H is less than or equal to M. Otherwise they score H.
   With no valid caller: every player with the lowest H scores 0, and the others score their H.
   Add the scores to the penalty totals and announce all totals. Then switch the 'new hand' flag on, so the next round begins a fresh hand and a fresh shuffle.
11. The priority seat passes to the next seat in order.
12. END CHECK. The match ends after any showdown that leaves some player's penalty total at 50 or more, or after round 24.

There is no discussion phase.

Objective: When the match ends, the player with the lowest penalty total wins. If two or more players share the lowest total, the match is a draw among them.

Expected effect: Hands end in about 3 to 5 rounds, so a match has roughly 5 to 7 showdowns and the 50 limit is often reached. Players can count Jokers and low cards in the dead pile and the row, and estimate what remains in the draw pile. They can read opponents: a player who takes a 4 from the row probably holds or wants another 4, and a player who keeps shedding 10s still holds high cards. Taking a low card from the row signals your plan but denies it to others, and with conflicts each player must guess whether a rival with priority wants the same card. Calling Yaniv is a risk judgement: with H of 8 to 10, the caller must estimate from opponents' sheds, takes and card counts whether anyone is lower, against the 20-point Asaf. A fixed 'shed highest, take lowest, call when valid' heuristic loses to a player who times calls on opponents' likely totals and denies key cards. Talk is left out: it is a free-for-all where every rival wants you to call badly, so messages would be pure noise with no shared plan to test.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
