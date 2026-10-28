# Variation: Da Bai Fen Lite

Four players in two facing partnerships play four short hands of single-card trick-taking. In each hand a declarer names trumps and the defenders try to capture 40 of the 100 points in play. The declarer role rotates so each team declares twice.

Players: 4 to 4, best with 4

## Review of the original

Da Bai Fen is a four-player partnership trick-taking game of the Sheng Ji / Tractor family. Trumps are declared during the deal, the leader buries a kitty, and multi-card leads are allowed. Teams fight over 100 points in point cards, and that total decides whether the declarers keep the lead and climb levels.

- **non_degenerate**: good. No simple card-play policy wins. 'Always play your highest card' wastes trumps and gives point cards to opponents. 'Always play lowest' never captures. Seat order matters, but the declarer role moves between teams.
- **skill_sensitive**: weak. Over many deals, good card play wins clearly. In a short session the deal decides a lot: trump length, jokers and kitty contents. The voluntary race to expose a trump card also turns partly on the order of the deal.
- **headroom**: good. There is much to master: counting trumps, inferring voids, partnership signalling through discards, and timing point cards. A weak player can still win tricks with strong cards.
- **reasoning_dependent**: good. Hands and kitty are hidden. Players must infer holdings from follows and discards, model the partner's intentions, and plan trump control over a whole hand.
- **verifiable**: good. Trick winners and point totals follow from card ranks. The level outcome is a table lookup on points.
- **fits_platform**: bad. Several rules exceed the engine limits: card-by-card dealing with interruptible trump exposure, kitty exchange, multi-card leads with a legality check against all hidden hands, and void-hand redeals. A 54-card, 12-trick deal with a level race from 2 to Ace is far too long and has too many steps.

## Problems

- Trump declaration during a one-by-one deal, where any holder may interrupt, is a real-time-like race that the engine cannot run in a few steps.
- Multi-card leads require checking that no card in any hidden hand beats them; this is a long, error-prone rule chain.
- The kitty exchange (take 6, discard 6) and void-hand redeals add choice steps and conditional blocks the flat step list cannot support.
- 54 cards, 12 tricks per deal and a level race from 2 to Ace make the game far too long for the 40-round cap.
- A short session is dominated by deal luck (jokers, trump length), and the declaring role does not rotate evenly, so one team can gain a structural edge.

## Changes

- The deck shrinks to 30 cards: four suits of 5, 8, 10, J, Q, K, A plus two jokers. Each player gets 7 cards and 2 go to a face-down kitty. Point cards stay K=10, 10=10, 5=5, still 100 in total. (fixes: 54 cards, 12 tricks per deal and a level race from 2 to Ace make the game far too long for the 40-round cap.): Keeps the 100-point fight while making each deal 7 tricks long.
- There is no level system or trump rank. Trumps are the two jokers plus a trump suit that the hand's declarer names after seeing their own 7 cards. (fixes: Trump declaration during a one-by-one deal, where any holder may interrupt, is a real-time-like race that the engine cannot run in a few steps.): One single choice step replaces the interruptible exposure race. The declarer still reads their hand to choose trumps, as in the original.
- Only single-card leads are allowed. A player must follow suit if able, and trumps count as their own suit. (fixes: Multi-card leads require checking that no card in any hidden hand beats them; this is a long, error-prone rule chain.): Removes the multi-card legality check while keeping follow-suit inference and the value of being void in a suit.
- The kitty is never exchanged. Its points go to whichever team wins the last trick, and its cards are revealed only then. There are no redeals. (fixes: The kitty exchange (take 6, discard 6) and void-hand redeals add choice steps and conditional blocks the flat step list cannot support.): Keeps a hidden element and a reason to fight for the last trick, without extra choice steps.
- The match has 4 hands. The declarer rotates through all four seats, so each team declares twice. Each hand pays match points from a threshold table on the defenders' points. The higher match total wins, with card points as the tie-break. (fixes: A short session is dominated by deal luck (jokers, trump length), and the declaring role does not rotate evenly, so one team can gain a structural edge.): Balances the seats and spreads deal luck over four deals. The threshold table keeps the original's stay-or-flip character on the 40-point line.
- The winning card in each trick is decided by a numeric strength: rank, plus 10 if the card is in the led suit, plus 20 if it is a trump. The jokers have fixed top values. (fixes: 54 cards, 12 tricks per deal and a level race from 2 to Ace make the game far too long for the 40-round cap.): Lets the engine find the trick winner in one calculation step with no lookup table.

## Kept from the original

- Four players in fixed facing partnerships.
- Point cards K=10, 10=10, 5=5 totalling 100, with the 40-point line deciding whether declarers or defenders profit.
- Two jokers as the top trumps (red/big above black/small), and a trump suit chosen from the declarer's hand.
- A hidden kitty whose points matter at the end of the hand.
- Follow-suit trick play, anticlockwise order, and trick winners leading the next trick.
- Partnership inference and signalling purely through which cards are played.

## The variation's rules

SEATS AND TEAMS. Seats 1, 2, 3 and 4 sit in anticlockwise order. Seats 1 and 3 are Team North-South (NS). Seats 2 and 4 are Team East-West (EW). Partners cannot see each other's cards. There is no talk; the only communication is the cards played.

DECK. The deck has 30 cards. Each of four suits (Spades, Hearts, Clubs, Diamonds) has seven cards: 5, 8, 10, J, Q, K, A, with rank values 5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7. There are also two jokers: the Big Joker and the Small Joker. Point cards: each K is worth 10 points, each 10 is worth 10 points, each 5 is worth 5 points. All other cards and both jokers are worth 0. The deck holds 100 points in total.

MATCH STRUCTURE. The match has 4 hands of 8 rounds each, 32 rounds in total. The declarer is seat 1 in hand 1, seat 2 in hand 2, seat 3 in hand 3 and seat 4 in hand 4. The declarer's team is the Declaring Team for that hand; the other team is the Defending Team.

ROUND 1 OF EACH HAND (DEAL AND TRUMPS). The 30 cards are shuffled (the only random draw of the round). Each player privately receives 7 cards. The remaining 2 cards form the face-down kitty, which no one sees. The declarer then names one suit as the trump suit, and it is announced to all. Trumps are the Big Joker, the Small Joker and the 7 cards of the trump suit, 9 cards in all. For following purposes all trumps form one suit, the Trump suit. The declarer will lead the first trick.

ROUNDS 2 TO 8 OF EACH HAND (ONE TRICK EACH).
(a) The leader plays any one card face up. The suit of that card is the led suit; if the card is a trump, the led suit is Trump.
(b) The other three players then each play one card face up, one after another, in anticlockwise order from the leader. Each sees the cards already played. A player holding a card of the led suit must play one. A player holding none may play any card. An illegal play is rejected and the player must choose again.
(c) Strength of each played card. Big Joker = 40. Small Joker = 39. A trump-suit card = 20 + its rank value. A non-trump card of the led suit = 10 + its rank value. Any other card = its rank value.
(d) The card with the highest strength wins the trick. Ties cannot occur. The winner's team adds the point values of the four cards to its hand points, and the winner leads the next trick.
(e) In round 8 (the 7th and last trick), the kitty is also revealed after the trick, and its points are added to the hand points of the team that won that trick.

END OF HAND SCORING. Let P be the Defending Team's hand points, always a multiple of 5 from 0 to 100.
- P from 0 to 15: Declaring Team +3 match points.
- P from 20 to 35: Declaring Team +2.
- P from 40 to 55: Defending Team +1.
- P from 60 to 75: Defending Team +2.
- P from 80 to 100: Defending Team +3.
In addition, each team adds its hand points to its running card-point total. Hand points then reset to 0 for the next hand.

Objective: After hand 4, the team with more match points wins, and both its players win. If match points are equal, the team with the higher card-point total over all four hands wins. If that is also equal, the match is a draw.

Expected effect: Play becomes a compact trick-taking duel. Strong play counts trumps (9 per hand), infers voids from failures to follow, protects or feeds point cards to the partner when the partner is winning the trick, and plans for the last trick and its hidden kitty. The trump choice rewards reading one's own hand: a long suit versus spreading the risk across suits. Rotating the declarer gives each team two declaring hands and each seat one, so no seat has a built-in edge, and four deals reduce card luck. The match-point bands cap the reward for one lucky deal, so consistent play across hands matters most. Simple policies lose: 'always highest legal card' burns trumps early and loses the last trick and kitty; 'always lowest' concedes points; 'always lead points' feeds the opponents. Talk is left out on purpose. Any message would be public, so it either reveals hands to opponents or adds noise. The partnership-inference challenge is to read the partner's cards from play alone.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
