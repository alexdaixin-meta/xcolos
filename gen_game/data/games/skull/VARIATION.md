# Variation: Skull Gambit

A simultaneous Skull played as a race to 6 points. Each hand, everyone secretly places a Rose or their Skull, talks, then bids. The unique top bidder names that many rivals to reveal. All Roses scores big for the challenger and +1 for each named Rose. Any Skull costs the challenger a card and pays +1 to each Skull that caught them. A Skull that nobody reveals costs its owner a point.

Players: 3 to 5, best with 4

## Review of the original

Skull is a 3-6 player bluffing game. Players secretly stack Roses or their single Skull, bid on how many Roses they can flip, and the winning bidder flips cards, starting with their own. Succeeding twice wins. Hitting a Skull costs a card, and a player with no cards is eliminated.

- **non_degenerate**: weak. In the tabletop original, open sequential bidding and permanent card loss make choices matter. In the tested simultaneous adaptation it collapsed. Placing was free and a revealed card only ever hurt the challenger, so 'always Skull, bid 0' was a best response for every non-start player. The forced all-pass challenge then cost the start player a card every hand, and the last seat in rotation won with certainty.
- **skill_sensitive**: weak. The original rewards reading the table. In the tested version, equilibrium play scored no marks and elimination followed the start-player rotation, so skill did not change the winner.
- **headroom**: weak. Reading bluffs and tracking who lost their Skull has depth in principle. Under the passive equilibrium that depth was never used.
- **reasoning_dependent**: good. Placements and hand contents are hidden, and bids are signals to interpret. The inference is real whenever deviation pays. The tested version made deviation unprofitable.
- **verifiable**: good. Marks, card counts and eliminations are all arithmetic on tracked state.
- **fits_platform**: weak. The open-ended raise/pass bidding loop and choosing flips one card at a time do not fit a flat step list. Simultaneous polls fit, but the tested version had an ambiguous RESOLVE clause, where 'Then' could be read as removing a card after any challenge, and a seat-order tie-break.

## Problems

- P1: Placing Skull was free and weakly dominant for non-challengers. A revealed Rose only helped an opponent, and Roses were never rewarded for their owner.
- P2: If every bid was 0, the start player was forced to challenge, so universal passing punished the start player every hand and made elimination follow seat rotation.
- P3: Bid ties broken by seat order gave earlier seats a built-in edge, and with rotation the last seat won the equilibrium outright.
- P4: Under intended good play no marks were scored, so the winner was fixed by seat (lottery-like, with no reasoning involved).
- P5: The end tie-break 'most marks, then most cards' rewarded stalling.
- P6: The RESOLVE wording was ambiguous about whether a card is removed after a successful challenge.
- P7: Cooperation, such as two players placing Rose and bidding to set each other up, did not pay, because the mark went to the earlier seat and the partner got nothing.

## Changes

- An unrevealed placed Skull costs its owner 1 point at the end of the hand. Scores may go negative. (fixes: P1: Placing Skull was free and weakly dominant for non-challengers.): Skull becomes a gamble: +1 if named, -1 if ignored. 'Always Skull' now bleeds points.
- A named player whose Rose is revealed in a successful challenge gains 1 point. A named player whose Skull catches the challenger gains 1 point. (fixes: P1, and P7: cooperation did not pay because the partner got nothing.): Being named is worth +1 either way, so the placement choice is really 'help or hurt the challenger' against 'risk being ignored'. Roses now have value for their owner.
- Points replace marks. A successful challenger gains B+1 points, and the first hand that ends with anyone at 6 or more ends the game. (fixes: P4: under good play no marks were scored and seat decided the winner.): This is a target race in which challengers outpace helpers. Bigger bids are riskier but worth more, so passivity cannot win.
- If every bid is 0 there is no challenge. If two or more players tie for the highest bid there is also no challenge. (fixes: P2 (forced all-pass challenge) and P3 (seat-order tie-break).): No forced challenger and no seat tie-break. Bidding becomes a guessing duel: be the unique top bidder, or spoil a rival by matching their bid.
- Remove the start player and rotation entirely. All choices are simultaneous. (fixes: P3: earlier and later seats had built-in edges.): Every seat is identical, so no seat has any edge.
- If no one reaches 6 points by the end of hand 24, the game is a draw. The 'most cards' tie-break is dropped. (fixes: P5: the end tie-break rewarded stalling.): Stalling can at best draw. It cannot win.
- RESOLVE now states explicitly that a card is removed only when a challenge fails. (fixes: P6: the RESOLVE wording was ambiguous.): Removes the ambiguity a model could misread.

## Kept from the original

- Each player has a secret hand of 3 Roses and 1 Skull, and secretly places one card each hand.
- The challenger's own card is revealed first, so challenging while on your own Skull fails.
- Bidding a number of cards to reveal, with bigger bids harder and worth more.
- A failed challenger loses a random card permanently, and only they learn which one.
- Elimination at 0 cards, with the last player standing winning.
- Bluffing about whether you placed a Rose or a Skull, and tracking who has lost their Skull.

## The variation's rules

SETUP: Each player has a private hand of 4 cards: 3 Roses and 1 Skull. Each player starts with 0 points. Points and card counts are public. Which cards a player still holds is private to that player. There is no start player; all players are equal.

EACH HAND (at most 24 hands). Only active (non-eliminated) players take part.

1. PLACE: All active players at the same moment secretly choose a placed card. They may choose Rose only if they hold at least one Rose, and Skull only if they still hold their Skull. Placing does not remove the card from the hand.

2. TALK: Every active player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Talk is not binding.

3. BID: All active players at the same moment submit a secret whole-number bid from 0 to K. K is the number of OTHER active players.

4. BIDS SHOWN: All bids are announced to everyone.

5. CHALLENGER: If every bid is 0, there is no challenge this hand; go to step 10. If two or more players share the highest bid, there is no challenge this hand; go to step 10. Otherwise the unique highest bidder is the challenger, and their bid is B.

6. TARGETS: The challenger names exactly B distinct other active players.

7. REVEAL: The challenger's placed card and the placed cards of the named players are shown to everyone. Other placed cards stay secret.

8. SUCCESS: If every revealed card is a Rose, the challenge succeeds. The challenger gains B+1 points. Each named player gains 1 point. No card is removed from anyone.

9. FAILURE: If any revealed card is a Skull, the challenge fails. Each named player whose revealed card is a Skull gains 1 point. A Skull placed by the challenger themselves earns nothing for anyone. Only when a challenge fails, one card is removed permanently from the challenger's hand (all cards they hold), chosen uniformly at random. Only the challenger is told whether it was a Rose or their Skull. Everyone sees their card count drop by 1. A player who has lost their Skull can never place Skull again. A player with only their Skull left must place Skull.

10. HIDDEN SKULL COST: Every active player who placed Skull and whose card was NOT revealed this hand loses 1 point. This also applies in hands with no challenge. Scores may go below 0.

11. ELIMINATION: A player with 0 cards is eliminated and takes no further part. Their points no longer count.

12. END CHECK: If only one active player remains, that player wins. Otherwise, if any active player has 6 or more points, the game ends. The active player with the most points wins. If two or more active players tie for the most, the game is a draw.

13. If the game has not ended and fewer than 24 hands have been played, start the next hand.

AFTER HAND 24: If no one has won, the game is a draw.

Objective: The game ends after the first hand in which any active player has at least 6 points. The active player with the most points then wins; a tie for the most is a draw. A player also wins if they are the last active player. If 24 hands pass without either ending, the game is a draw.

Expected effect: Neither card dominates. Skull pays +1 if you are named but costs 1 if you are ignored. Rose costs nothing, pays +1 if named in a success, and is required for anyone who wants to challenge. Each player must therefore predict whether they will be named.

Challengers must infer who placed Rose. A positive bid reveals the bidder's own Rose, so losing bidders become safe targets who still earn +1. Bidding 0 hides your card but forfeits the challenge. Tie-voiding turns bidding into a duel: a player can spoil a leader's challenge by matching their bid, at the risk of becoming challenger themselves.

No seat order exists. Simple policies all lose to sensible play:
- Always Skull, bid 0 bleeds a point every unnamed hand and is never named once read.
- Always Rose, bid 0 earns only +1 per success while challengers earn at least 2.
- Always the top bid ties into voids or gets caught by Skulls and loses cards.
- Always Skull, top bid fails every challenge it wins and is eliminated.
If everyone passes forever, it is only a draw.

Talk passes both tests. Players disagree because only one can win. A named Rose helps a rival by B+1 while gaining only 1, so a player who promises 'name me, I'm Rose' may be laying a Skull trap, and a challenger who follows such a claim can lose a card. A player who trusts a proposed alternating partnership can be betrayed with a Skull, or watch the partner pull ahead by more each time. After a betrayal, cooperating again still pays, because the +1 for being named and the target race keep partnership worthwhile against the third player.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 24 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
