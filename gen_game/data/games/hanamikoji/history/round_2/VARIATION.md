# Variation: Hanamikoji: Paired Hands

A two-player Hanamikoji on five Geisha. Hands are played in pairs, each player starts one hand of every pair, and Geisha are won by combined majorities over the pair. At most two pairs (32 rounds) are played.

Players: 2 to 2, best with 2

## Review of the original

Hanamikoji is a two-player card game. Over repeated hands of four alternating turns each, players use four one-shot actions (Secret, Trade-off, Gift, Competition) to commit Item cards to seven Geisha of different Charm values. Gift and Competition force the opponent to choose between offered splits. A player wins by holding the majority on enough Geisha, by count or by Charm.

- **non_degenerate**: weak. The previous variation was tested. No thoughtless policy was undefeated: always the first action, always pick 1, always take the higher-Charm option and always Secret a G5 can all lose to sensible splitting. However, the win was checked after every hand and about 70-80% of games ended after hand 1. In every hand the non-starter acts in round 8 with almost full information and resolves the starter's round-7 offer. So in most games Player 2 had an uncompensated structural edge. That is a seat edge, which this criterion forbids.
- **skill_sensitive**: good. Building Gift and Competition offers so that every pick still leaves you ahead in the Geisha that matter, and choosing well as the picker, are real skills. Timing the Secret and Trade-off actions is also a skill. Each player spends 10 cards over the hand, and the opponent's choices shape about 7 of them, so splitting skill dominates. The deal adds variance, especially when a game is decided by a single hand.
- **headroom**: good. Weak players still win Geisha by pushing majorities. Strong players plan the order of their four actions, bait with Gift offers, read hidden Secret and Trade-off cards from what has been revealed, and count the remaining copies. Play is not solved.
- **reasoning_dependent**: good. Hands, the removed card, the deck and the face-down Secret and Trade-off cards are hidden. Players must infer what the opponent holds and kept from their offers, picks and action order, and plan four actions in advance.
- **verifiable**: good. Majorities are counts per Geisha. Charm is a sum. The win checks are thresholds. Card legality is the check 'the count of each number named is at most the count in hand'.
- **fits_platform**: good. It is turn-based and text-only, with at most three choices per round and no board. Five Geisha keep the state small. The previous version could reach 40 rounds, which is right at the limit.

## Problems

- P1 Seat edge: most games were decided by a single hand, and in every hand the non-starter has a large last-mover information advantage that nothing compensated.
- P2 Starting turns were uneven: Player 1 started hands 1, 3 and 5 and Player 2 only hands 2 and 4.
- P3 Simply alternating the hands and checking only after even hands is not enough if markers carry over hand by hand. The second hand of a pair overwrites the first wherever it decides a Geisha, so one player's last-mover hand would count more than the other's.
- P4 Luck of a single deal decides too much when one hand decides the game.
- P5 The length was 40 rounds, right at the platform limit.
- P6 The card-legality check was worded loosely.

## Changes

- Hands are played in pairs: hands 1 and 2 form pair 1, and hands 3 and 4 form pair 2. Within a pair, Player 1 starts the first hand and Player 2 starts the second. Kept counts add up across both hands of the pair, and Geisha markers move only after the second hand of a pair, by comparing these combined counts. (fixes: P1): Each player gets the last-mover position exactly once in every scored contest, and both hands of a pair weigh the same. Both players play the second hand knowing the full first-hand result, so the extra information is shared.
- There are at most 2 pairs (4 hands, 32 rounds). Each player starts exactly 2 hands. (fixes: P2): The number of starts is equal, and the game is shorter and well inside the limit.
- Markers are updated only from combined pair totals, never from a single hand. At the start of hand 3 the pair totals reset to zero, and markers already placed stay where they are when a later pair ties on that Geisha. (fixes: P3): Neither hand of a pair can overwrite the other, so both last-mover hands count equally.
- At the end of the first hand of a pair, the Secrets are revealed and both players' running pair totals are announced. (fixes: P4): Both players play the second hand with the same full knowledge of where they stand, and the deal's swing is averaged over 32 counted cards instead of 16.
- The win is checked after hands 2 and 4 only. After hand 4 the tiebreak is higher Charm, then more Geisha, otherwise a draw. (fixes: P1): This gives a clean end, and the game always stops at a point where the seats are balanced.
- Legality is stated as 'for each Geisha number, how many times you name it must be at most how many of that number are in your hand'. (fixes: P6): The check becomes pure arithmetic.
- The maximum length is 32 rounds instead of 40. (fixes: P5): This gives margin under the 40-round limit.

## Kept from the original

- The four one-shot actions Secret, Trade-off, Gift and Competition, with the opponent choosing for Gift and Competition.
- Geisha with Charm values equal to their number of Item cards (five Geisha, 3, 3, 4, 5 and 6).
- One card removed unseen each hand, hidden hands of 6 cards, and a deck of 8.
- Majority per Geisha decides its Victory Marker, and ties leave the marker where it is.
- The dual win condition: Charm threshold first, then Geisha count.
- Starting turns alternate between hands.

## The variation's rules

COMPONENTS
- 5 Geisha, G1 to G5, with Charm G1=3, G2=3, G3=4, G4=5, G5=6 (total 21).
- 21 Item cards: three of G1, three of G2, four of G3, five of G4 and six of G5. A card is written as its Geisha number, 1 to 5.
- 5 Victory Markers, one per Geisha. Each is on Player 1's side, on Player 2's side, or neutral. All start neutral.
- Each player has four action markers: Secret, Trade-off, Gift and Competition.
- Each player has pair totals: five counts, one per Geisha, of the cards they have kept during the current pair of hands.

STRUCTURE
- There are at most 4 hands of 8 rounds each (32 rounds).
- Hands 1 and 2 form pair 1. Hands 3 and 4 form pair 2.
- Player 1 starts hands 1 and 3. Player 2 starts hands 2 and 4.
- In each hand, the starting player is active in rounds 1, 3, 5 and 7, and the other player is active in rounds 2, 4, 6 and 8. The player who is not active is the opponent.

START OF EACH HAND (before its round 1)
- Shuffle all 21 Items.
- Remove the top card face down. Nobody sees it, and it plays no part this hand.
- Deal 6 cards to each player as a private hand. Each player sees only their own hand, as a sorted list of numbers.
- The other 8 cards form the face-down deck.
- Both players' four actions become unused, and both Secrets are emptied.
- At the start of hands 1 and 3 only, both players' pair totals are reset to 0 0 0 0 0.
- Victory Markers always stay where they are.

EACH ROUND
1. The game announces the hand, the round, the active player, each player's unused actions, both players' pair totals and the marker positions.
2. The active player draws the top deck card and is privately shown their hand.
3. Choice 1: the active player names one unused action: Secret, Trade-off, Gift or Competition.
4. Choice 2: the active player writes the cards the action uses, as space-separated numbers with repeats written out (for example '5 5 2'). The cards are legal if, for each Geisha number, the number of times it is written is at most the number of that card in the player's hand.
   - Secret: exactly 1 number. That card is set face down as their Secret.
   - Trade-off: exactly 2 numbers. Those cards are discarded face down and do not count.
   - Gift: exactly 3 numbers, revealed in the order written as offer 1, 2 and 3.
   - Competition: exactly 4 numbers, all revealed. The first two form pair A and the last two form pair B.
   The named cards leave the active player's hand.
5. Choice 3, only for Gift or Competition: the opponent writes one digit.
   - Gift: 1, 2 or 3. The opponent adds that card to their pair totals, and the active player adds the other two to theirs.
   - Competition: 1 for pair A or 2 for pair B. The opponent adds the chosen pair to their pair totals, and the active player adds the other pair to theirs.
6. The action becomes spent. The game publicly announces the action, and for Gift or Competition the revealed cards and the split. For Secret and Trade-off it announces only that the action was used.

DEFAULTS
- Illegal or missing action: the first unused action in the order Secret, Trade-off, Gift, Competition is used.
- Illegal card answer (wrong count, unreadable or not in hand): the required number of lowest-numbered cards in hand are used, in ascending order. For Competition, the first two of them form pair A.
- Illegal or missing pick: counts as 1.
- Cards always work out: each player holds 6 + 4 = 10 cards and spends 1 + 2 + 3 + 4 = 10.

END OF EACH HAND (after round 8)
- Each player's Secret is revealed and added to their pair totals.
- The game announces both Secrets and both players' pair totals.

END OF EACH PAIR (after hands 2 and 4, following the end-of-hand step)
- For each Geisha, compare the two players' pair totals. A strictly higher total moves that Geisha's marker to that player's side. A tie leaves the marker where it is (neutral, or on a side from pair 1).
- Charm is the sum of the Charm values of the Geisha on a player's side. Geisha count is the number of markers on a player's side.
- The game announces all markers, Charm and Geisha counts.
- Win check:
  - If a player has 11 or more Charm, they win.
  - Otherwise, if a player has 3 or more Geisha, they win.
  - Otherwise, after pair 1 the game continues with hand 3.
  - After pair 2 with no winner, the higher Charm wins. If Charm is equal, the higher Geisha count wins. If both are equal, the game is a draw.

Objective: After hand 2 and after hand 4: a player with 11 or more Charm from markers on their side wins. Otherwise a player with 3 or more markers on their side wins. Total Charm is 21 and there are 5 Geisha, so at most one player can meet each condition, and Charm is checked first. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count, and otherwise the game is a draw.

Expected effect: Every scored contest now contains one hand where each player is the starter and one where each is the last mover, so the move-order edge cancels. Both hands count equally, and the second is played with both players fully informed of the first, which turns the pair into a two-stage plan. In hand 1 players build a lead or a position. In hand 2 they defend or chase specific Geisha with known deficits, and offers can be targeted. The swing from the deal is spread over 32 counted cards, so splitting skill and reading hidden Secrets matter more. Most games should end after pair 1, and a stalemate goes to a second pair in which earlier markers hold on ties. Thoughtless policies still lose: a player who always picks 1 receives the worst offer, and fixed action orders reveal intent and waste high cards. No talk phase is used, since this is a two-player game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 19 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
