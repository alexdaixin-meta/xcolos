# Variation: Trischettn Duel

A two-player, two-deal Trischettn without trumps or declarations. A face-up talon card goes to each trick's winner, and the talon-empty endgame rewards exact card counting.

Players: 2 to 2, best with 2

## Review of the original

Trischettn is an Austrian trick-taking game for 2 to 4 players with a 32-card Salzburg deck and no trumps. Cards rank 10, 9, Ace, King, Ober, Unter, 8, 7, and players must follow suit. After each trick both players draw from a talon, winner first. Players score card points, a last-trick point and declaration bonuses (three or four Tens, Nines or Aces, or a Napoli of Ten, Nine and Ace of one suit), playing to 31 or 41 points.

- **non_degenerate**: good. No simple policy wins. 'Always play the highest legal card' throws away Tens and Nines on tricks it cannot win and gives up the lead pointlessly. 'Always play the lowest' hands over every point-bearing trick. The seat that leads first has a small edge in a single deal, but over a match to 31 the lead changes hands constantly.
- **skill_sensitive**: weak. Card play rewards counting and timing, and following suit makes the endgame a counting exercise. But declarations are scored straight from the cards a player is dealt or happens to draw: three Aces is worth 3 of the 11 points in a deal, for no decision at all. That pushes the result toward the deal.
- **headroom**: good. Beginners can follow suit and still win tricks. Strong players count the 32 cards, read the opponent's hand from their follows and draws, decide when to win a trick for a talon card, and play out the talon-empty endgame exactly.
- **reasoning_dependent**: good. Hands and the talon are hidden. Once the talon is empty, a counting player can deduce the opponent's whole hand, so memory and inference decide the endgame.
- **verifiable**: good. Trick winners, card points, the last-trick bonus and declarations are all arithmetic. The one problem is rounding fractions after summing, which is fiddly but deterministic.
- **fits_platform**: weak. A match to 31 needs roughly three deals of 16 tricks, which exceeds 40 rounds. Declarations are gated on winning the previous trick, opt-in, and allow reuse of cards. The previous build attempts failed on exactly these: attributes that never changed, and blank scratch fields. The 4-player variant relies on partnership gestures, and the 3-player variant adds a discard.

## Problems

- Declarations are scored mostly from luck of the deal or draw and outweigh card-play decisions (3-4 of about 11 points per deal).
- The declaration mechanic (only after winning a trick, opt-in, once-per-deal marks, cards reusable) produced attributes that never changed in testing (declared_this_deal, declared_cards_shown, decl_value, decl_cards), so the game could not be built.
- Scratch fields (decl_answer, drawn_hidden_card) and a talon_up field that went blank when the talon ran out appeared empty in the state shown to players.
- Playing to 31 or 41 points takes about 48 or more tricks, beyond the 40-round limit, and an open-ended match length is hard to build.
- Card points in thirds with rounding down after summing are awkward to track and create artificial ties.
- The 3- and 4-player variants add discards and partnership gestures that the engine cannot support cleanly.
- A completely hidden talon makes the decision to win or lose a trick for its draw rather thin.

## Changes

- Remove declarations entirely. (fixes: Declarations are scored mostly from luck of the deal or draw and outweigh card-play decisions (3-4 of about 11 points per deal).): Declarations were mainly a reward for the deal. Removing them makes card play decide the score and deletes every attribute that failed to update.
- Delete the declaration bookkeeping (declared_this_deal, declared_cards_shown, decl_value, decl_cards, decl_answer). No scratch attribute is kept that some step does not change every trick. (fixes: The declaration mechanic (only after winning a trick, opt-in, once-per-deal marks, cards reusable) produced attributes that never changed in testing (declared_this_deal, declared_cards_shown, decl_value, decl_cards), so the game could not be built.): Every remaining attribute changes in normal play.
- Remove drawn_hidden_card from shown state. Every public field starts with a non-empty value: led_card and followed_card start as 'none', and talon_up shows 'none' once the talon is empty. (fixes: Scratch fields (decl_answer, drawn_hidden_card) and a talon_up field that went blank when the talon ran out appeared empty in the state shown to players.): The state shown to players never contains a blank field.
- Fixed match of exactly 2 deals of 16 tricks (32 rounds, one trick per round). Player A leads the first trick of deal 1 and Player B leads the first trick of deal 2. (fixes: Playing to 31 or 41 points takes about 48 or more tricks, beyond the 40-round limit, and an open-ended match length is hard to build.): This fits the round limit, balances the opening lead, and lets a second deal reduce the luck of a single deal.
- Score in whole pips: Ace 3, Ten/Nine/King/Ober/Unter 1, Eight/Seven 0, last trick of a deal 3. This gives 35 pips per deal, the original 11-and-a-bit points times three, with no rounding. (fixes: Card points in thirds with rounding down after summing are awkward to track and create artificial ties.): Integer arithmetic only. Each deal's total is odd, so a single deal cannot tie.
- The game is for 2 players only. (fixes: The 3- and 4-player variants add discards and partnership gestures that the engine cannot support cleanly.): The 2-player form is the base game and the one that fits the engine.
- The top card of the talon lies face up (talon_up). The trick winner takes that visible card and the loser takes the next, hidden card. A new top card is then turned face up. (fixes: A completely hidden talon makes the decision to win or lose a trick for its draw rather thin.): Players must decide whether winning a trick is worth it for the visible card, and the loser's hidden draw is an inference target for the winner.

## Kept from the original

- 32-card Salzburg deck in four suits, no trumps
- Rank order 10, 9, Ace, King, Ober, Unter, 8, 7 within each suit
- 8 cards each and a 16-card talon; trick winner draws first, then the loser; trick winner leads next
- Must follow suit if able; highest card of the led suit wins
- Play out the hands after the talon is empty
- Original relative card values (Ace worth three times a Ten/Nine/court card) and the last-trick bonus

## The variation's rules

DECK. The deck has 32 cards in four suits: Hearts, Bells, Leaves, Acorns. Each suit holds these ranks, from strongest to weakest: Ten, Nine, Ace, King, Ober, Unter, Eight, Seven (strength 8 down to 1). There are no trumps.

CARD VALUES (pips).
- Ace: 3 pips.
- Ten, Nine, King, Ober and Unter: 1 pip each.
- Eight and Seven: 0 pips.
- Winning the 16th (last) trick of a deal: 3 extra pips.
Each deal therefore contains 35 pips in total.

MATCH. The match is exactly 2 deals of 16 tricks each, 32 rounds in all. Each round is one trick.

START OF A DEAL (in round 1 and round 17 only).
1. Shuffle all 32 cards.
2. Deal 8 cards face down to each player as a private hand.
3. The remaining 16 cards form the talon, face down. Its top card is turned face up as the 'talon up' card, visible to both players.
4. Both players' deal pips are set to 0.
5. The leader of the first trick is Player A in deal 1 and Player B in deal 2.

EACH TRICK.
1. The leader plays any one card from their hand face up.
2. The follower then plays one card. If they hold any card of the led suit, they must play a card of that suit. Only legal cards are offered. If they hold none, they may play any card.
3. Winning the trick: if both cards are of the led suit, the one of higher strength wins. Otherwise the leader wins.
4. The trick winner adds the pips of both cards to their deal pips. If this was the 16th trick of the deal, the winner adds 3 more.
5. If the talon is not empty:
   - the winner takes the face-up 'talon up' card into their hand, so both players know it;
   - the loser takes the next talon card face down, so only the loser sees it;
   - if any talon cards remain, the new top card is turned face up as 'talon up'; otherwise 'talon up' becomes 'none'.
   The 16-card talon empties after exactly 8 tricks. The last 8 tricks are played from hand with no drawing.
6. The trick winner leads the next trick.

END OF A DEAL (after trick 16). Each player adds their deal pips to their match total.

PUBLIC INFORMATION. Both players see:
- the deal number and trick number;
- who leads;
- both cards of the current trick (shown as 'none' before they are played);
- the 'talon up' card, or 'none';
- the number of cards left in the talon;
- both players' deal pips and match totals.
Each player privately sees only their own hand.

END OF MATCH. After round 32, the player with the higher match total wins. Equal totals are a draw.

Objective: After 2 deals (32 tricks), each player's match total is the sum of their pips from both deals, out of 70 pips available. The higher total wins. If both totals are 35, the match is a draw.

Expected effect: Without declarations, every pip comes from card play, so counting and timing decide the match. The face-up talon card creates a real trade-off on each of the first 8 tricks: spend a strong card to win the trick and take a visible Ten or Ace, or duck cheaply and accept a hidden card. The winner must then infer what the loser drew. Once the talon is empty, a player who has tracked every played and visible card can deduce the opponent's whole hand and play the last 8 tricks perfectly. That final phase, worth over a third of the deal including the 3-pip last trick, separates strong from weak players. Alternating the first lead and playing two deals balances the seats and dampens the luck of a single deal. Simple policies lose to thoughtful play: always-highest wastes Tens and Nines, always-lowest concedes the Aces, and random play loses the endgame. Talk is omitted because there are only two players.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
