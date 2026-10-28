# Variation: Greek Hold 'em Lite

A fixed-structure poker game for 3–5 players. Each hand has two private cards, a five-card board revealed 3 then 2, and two simultaneous sealed betting stages with call-or-fold. Hand strength is an arithmetic score built from pairing your two hole cards with the board.

Players: 3 to 5, best with 4

## Review of the original

Greek hold 'em is a community-card poker variant. Each player holds two private hole cards, and five shared board cards are revealed in stages with betting rounds between them. At showdown a hand must use exactly both hole cards plus exactly three board cards, and the best standard poker hand takes the pot unless everyone else has folded.

- **non_degenerate**: good. No simple policy wins. Always-fold bleeds blinds. Always-raise is beaten by calling it with above-average hands. Always-call is beaten by value betting without bluffing. Position (the dealer button) gives a real seat edge within a hand, but it rotates, so it evens out over many hands.
- **skill_sensitive**: weak. Over many hands, skill dominates poker. Over the short session a platform can run, the card deal swings single results heavily. Unlimited raising also lets one big all-in pot decide everything.
- **headroom**: good. Hand reading, bluffing, sizing and opponent profiling leave a very high ceiling. A weak player still wins pots with good cards.
- **reasoning_dependent**: good. Hole cards are hidden. Players must infer opponents' holdings from their bets and the board texture, and plan across betting streets.
- **verifiable**: weak. The result is arithmetic in principle. But best-five-card poker evaluation under the exactly-2-plus-exactly-3 constraint (straights, flushes, kickers) is a long rule chain the engine cannot evaluate cheaply. It would lean on a referee to rank hands.
- **fits_platform**: bad. Betting is open-ended sequential raising with a variable number of actions per street, which a flat step list cannot express. There are four betting streets, more than the 4 choice steps allowed per round. Poker hand ranking needs dozens of steps, and side pots add more state.

## Problems

- P1: Open-ended sequential raise/re-raise loops cannot be built in a flat step list, and four betting streets exceed the 4-choice-step limit.
- P2: Standard poker hand ranking (suits, straights, flushes, kickers, best 5 of 7 with the Greek constraint) is far too long a rule chain to compute arithmetically. It would need a referee to decide the winner.
- P3: Unlimited bet sizes let one all-in pot decide a short session, so luck swamps skill in the number of hands the platform can play.
- P4: Acting position within a betting round gives a seat-based edge in any single hand.
- P5: Side pots and all-in handling add state and steps without adding much reasoning.

## Changes

- Two betting stages per hand instead of four: one after the 3-card flop and one after the last 2 board cards. Each stage is a simultaneous sealed bet of 0–4 chips, followed by a simultaneous call-or-fold for everyone who bet less than the highest bet. (fixes: P1: Open-ended sequential raise/re-raise loops cannot be built in a flat step list, and four betting streets exceed the 4-choice-step limit.): This gives a fixed 4 choice steps per hand while keeping betting, raising (bidding high), calling and folding.
- The 52-card deck is replaced by 32 numbered cards (values 1–8, four copies each). Hand strength becomes a single formula: Strength = 20 × min(matches, 3) + 30 × (hole pair ? 1 : 0) + hole1 + hole2, where 'matches' counts board cards equal in value to either hole card. (fixes: P2: Standard poker hand ranking (suits, straights, flushes, kickers, best 5 of 7 with the Greek constraint) is far too long a rule chain to compute arithmetically. It would need a referee to decide the winner.): This keeps the Greek rule that both hole cards always play and at most three board cards count. Pairing the board with your hole cards is what makes a hand strong. It is computable in one calculation.
- Bets are capped at 4 chips per stage and the ante is 1. Stacks start at 40. The session is 15 hands, and the winner is the highest stack. (fixes: P3: Unlimited bet sizes let one all-in pot decide a short session, so luck swamps skill in the number of hands the platform can play.): Each hand can move at most 9 chips per player. Many hands decide the game, so consistent reading and betting beats one lucky deal.
- All betting decisions are simultaneous polls, so there is no button or acting order. (fixes: P4: Acting position within a betting round gives a seat-based edge in any single hand.): No seat ever acts with more information than another.
- There are no side pots. A player who cannot cover a call puts in their whole stack and stays in for the whole pot. A player with 0 chips is eliminated. (fixes: P5: Side pots and all-in handling add state and steps without adding much reasoning.): This removes side-pot bookkeeping. With a 4-chip cap and 40-chip stacks the case is rare and late.

## Kept from the original

- Two private hole cards per player and a shared five-card board revealed in stages.
- The Greek constraint: both hole cards always play, and exactly three board cards are used (at most three matches count).
- Betting rounds between board reveals, with folding, calling and raising (bidding above others).
- Winning a pot either at showdown or when everyone else folds, and bluffing and hand-reading as the core skill.

## The variation's rules

SETUP: Each player starts with 40 chips. The deck has 32 cards: values 1 to 8, four copies of each value. The game lasts 15 hands (rounds). There is no dealer or acting order; every decision is made simultaneously.

EACH HAND:
1. Ante and deal. Every player still in the game puts 1 chip into the pot (a player with only 1 chip is then all-in). The deck is shuffled. Each player is dealt 2 hole cards, seen only by that player, and 5 board cards are set face down. Any pot left over from the previous hand stays in the pot.

2. Flop. The first 3 board cards are revealed to everyone.

3. Flop bet. Every player in the hand secretly chooses a bet of 0, 1, 2, 3 or 4 chips (never more than their stack). All bets are revealed together and paid into the pot. Call the largest bet H.

4. Flop call or fold. Each player whose bet was less than H chooses simultaneously:
   - CALL: pay the difference so their bet equals H. If they have fewer chips, they pay their whole stack and stay in.
   - FOLD: they are out of this hand, and chips already put in stay in the pot.
   Players who bet H stay in automatically.

5. If only one player remains in the hand, they take the whole pot and the hand ends (skip to step 10).

6. Turn and river. Board cards 4 and 5 are revealed.

7. River bet. This is the same as step 3: a simultaneous secret bet of 0–4 chips by every player still in the hand.

8. River call or fold. This is the same as step 4.

9. Showdown. If only one player remains, they take the pot. Otherwise every remaining player reveals their hole cards and their Strength is computed:
   - matches = the number of the 5 board cards whose value equals either of the player's hole card values. If both hole cards share a value, a board card of that value counts once.
   - matches counts at most 3, because a hand uses exactly three board cards.
   - pair = 1 if the two hole cards have the same value, else 0.
   - Strength = 20 × min(matches, 3) + 30 × pair + (hole card 1 value) + (hole card 2 value).
   The highest Strength takes the pot. If several players tie for highest, the pot is split equally among them in whole chips, and any leftover chip stays in the pot for the next hand.

10. Elimination. Any player with 0 chips is eliminated and takes no further part.

END: The game ends after hand 15, or earlier if only one player has chips left.

Objective: When the game ends, the player with the most chips wins. If two or more players tie for the most chips, those players draw. If only one player has chips left before hand 15, that player wins.

Expected effect: Play becomes a compact poker duel of inference. A large flop bet after a 6 appears suggests a 6 in hand. A small bet that then calls may be a drawing hand or a trap. Players must size bets to extract value from weaker hands without revealing strength, bluff on boards that look like they hit someone, and fold well. Simple policies all lose to adaptive play: always-4 is called down by better hands, calling stations are value-bet, and always-fold bleeds antes. Capped bets over 15 hands make the deal matter per hand but not for the match, so the stronger reader wins most matches. Simultaneous betting removes positional edge. Talk is deliberately left out. Bets already serve as the signalling and bluffing channel, and a talk phase would cost a choice step beyond the limit without adding a new conflict to reason about.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 15 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
