# Variation: Nyet! Duplicate Lone (Open Reserve)

Three players take turns as the Lone against a Pair in 4-trick deals. Within each set of three deals, every player plays the same Lone hand against the same 10 opposing cards. The Pair vetoes colours and sets the supertrump, the Lone picks trump, and the player with the most tricks won as Lone wins.

Players: 3 to 3, best with 3

## Review of the original

Nyet! is a trick-taking card game for 2 to 5 players. Each round, players take turns placing veto tokens to fix the round's rules: first player, discard rule, trump, supertrump and points per trick. The first player then forms uneven teams, and the teams score tricks and captured 1s ('Loot') over 8 to 10 rounds.

- **non_degenerate**: weak. Original: the veto phase and team choice give real decisions, and no single veto policy wins. However, the first player both picks the teams and hands out the doubling Bonus card, which is a strong seat edge each round. The previous 3-player variation was worse: in Nyet the Pair's 2 names against the Lone's 1 let the Pair alone fix supertrump and push trump onto the Lone's short colour. 'Pair names the Lone's long colours' was then close to a dominant policy, and the Lone's choices barely mattered.
- **skill_sensitive**: weak. Original: card play rewards skill, but full random deals of 60 cards plus team composition make single rounds very noisy. Previous variation: the testers estimated 60-70% of the result came from each player's single blind Lone deal. An informed Pair held the Lone to about 0-0.5 tricks, against 1-2 for a blind Pair. So the winner was whoever got the best blind hand.
- **headroom**: good. Trick play has deep headroom: counting cards, reading voids, timing the supertrump 1, choosing when to lead trump. A weak player still wins some tricks with good cards.
- **reasoning_dependent**: good. Hands are hidden. Players infer voids from what is followed, and the veto phase reveals preferences. Previous variation: there was something to infer, but information was unequal between seats, so inference could not overcome the leak.
- **verifiable**: good. Trick winners and scores follow arithmetically from colour and number. No judge is needed.
- **fits_platform**: weak. Original: a 5-line veto board, team selection, Bonus cards, discard/pass rules and 60 cards with 8-10 long rounds exceed the step limits. Previous variation: it fit the limits (36 one-trick rounds, 24 cards) but needed fixes for fairness.

## Problems

- P1 Information leak: in the 2nd and 3rd deals of a set, Pair members already know the Lone Hand L card for card. The three plays of L therefore happen under different information, so the duplicate comparison is unfair.
- P2 Nyet shut the Lone out: with 2 names against 1, the Pair fixed supertrump and blocked the Lone's best trump colours. The Lone's one decision outside card play was meaningless.
- P3 Deal luck in the Pair hands: the 19 non-L cards were reshuffled each deal with 9 set aside unseen, so trump length against the same L varied widely between the three plays.
- P4 Any fix that fixes the set-aside cards but keeps them hidden creates a new leak: after deal 1, players have seen most of the Pair's cards. So the later Lones would know the Pair's card pool and the first Lone would not.
- P5 The PairTricks tie-break was largely decided by the draw (random splits), so ties were settled by luck.
- P6 Simultaneous talk added little: Pair members were already informed, and talk let them share the leaked L.

## Changes

- The Lone's 5 cards are face up to all players in every deal, including the first of each set. (fixes: P1 Information leak): All three plays of L now happen with everyone knowing L, so they are identical in information.
- At the start of each set, the deck is shuffled once into L (5 cards), a Reserve of 9 cards that stays out all set, and a Pair Pool of 10 cards. The Reserve is shown face up to everyone. Each deal of the set, only the Pair Pool is reshuffled and split 5/5 between the two Pair members. (fixes: P3 Deal luck in the Pair hands; P4): Every Lone faces the same 10 opposing cards, so trump length against L is identical across the set. Making the Reserve public tells every Lone, including the first, exactly which cards oppose them. Deal 1 therefore leaks nothing that later Lones lack. Only the 5/5 split is hidden from the Lone.
- New Nyet. The two Pair members secretly and at the same moment each name one colour, and the names are revealed. Supertrump is the colour they named; if they named different colours, it is the one earlier in the set's priority order. Both named colours are barred. The Lone then chooses trump from the unnamed colours, of which there are always 2 or 3. (fixes: P2 Nyet shut the Lone out): The Pair still vetoes, which keeps the Nyet idea. The Lone now has real control: they weigh L against the known Pair Pool and against what the Pair's names suggest about the hidden split.
- The winner is decided by total LoneTricks alone. Equal highest totals are a draw. PairTricks is still recorded but does not decide anything. (fixes: P5 The PairTricks tie-break): Each player is Lone exactly once per set with the same L, so comparing LoneTricks is already a duplicate comparison. Subtracting a set average would change nothing, because the same average is subtracted from everyone. Removing the tie-break removes the luck it carried.
- The talk phase is removed. (fixes: P6 Simultaneous talk added little): Each Pair member knows their own 5 cards, L and the Reserve, so they can work out their partner's hand. They have nothing to coordinate by talk. Anything they say is seen by the Lone and serves only to mislead, so a rational Lone ignores it. Talk fails the reasoning test. The Pair's Nyet names already serve as costly, informative signals.

## Kept from the original

- The Nyet idea: players veto colours, and what is left becomes the round's trump and supertrump.
- Trump plus a supertrump whose 1 beats every trump.
- Following the led colour, and highest trump, otherwise highest of the led colour, wins.
- The uneven 1-against-2 team structure (the small team against the larger team) that rotates every deal.
- Duplicate structure: each player plays the same Lone hand once per set, so the hand's quality cancels out.

## The variation's rules

PLAYERS AND CARDS: There are 3 players in seats 1, 2 and 3, sitting clockwise. The deck has 24 unique cards in four colours (Red, Yellow, Green, Blue), each colour numbered 1 to 6. Each player has two counters, LoneTricks and PairTricks, both starting at 0.

STRUCTURE: There are 9 deals of 4 tricks each, 36 rounds in all, and each round is one trick. The deals form 3 sets: set 1 is deals 1-3, set 2 is deals 4-6 and set 3 is deals 7-9.

LONE ORDER: The Lone for deals 1 to 9 is seat 1, 2, 3, 2, 3, 1, 3, 1, 2. The other two players form the Pair. The Pair member to the Lone's left (clockwise) is Pair-Left; the other is Pair-Right.

COLOUR PRIORITY: Set 1 uses Red, Yellow, Green, Blue. Set 2 uses Yellow, Green, Blue, Red. Set 3 uses Green, Blue, Red, Yellow.

START OF A DEAL (before the first trick of each deal only):
(a) DEAL. In the first deal of a set: shuffle all 24 cards. The first 5 become this set's Lone Hand L. The next 9 become this set's Reserve. The last 10 become this set's Pair Pool, dealt 5 to Pair-Left and 5 to Pair-Right. In the second and third deals of a set: the Lone receives exactly the cards of L, the Reserve is unchanged, and only the 10 Pair Pool cards are shuffled and dealt 5 to Pair-Left and 5 to Pair-Right.
(b) OPEN CARDS. The Lone's 5 cards and the 9 Reserve cards are shown face up to all players for the whole deal. Reserve cards are never played. Each Pair member's hand is seen only by that Pair member. Everyone therefore knows which 10 cards the Pair holds together, but only the Pair knows how they are split.
(c) NYET. Pair-Left and Pair-Right at the same moment each secretly name one colour. Both names are then revealed.
(d) SUPERTRUMP. If both named the same colour, that colour is supertrump. If they named different colours, supertrump is the named colour that comes first in the set's priority order. Every named colour is barred from being trump.
(e) TRUMP. The Lone chooses trump from the colours nobody named, of which there are 3 or 2. Trump and supertrump are therefore always different colours.
(f) Trump and supertrump are announced. Pair-Left leads the first trick.

EACH TRICK:
(1) The leader plays any one card from hand face up. Its colour is the led colour.
(2) The other two players then each choose one card at the same moment, seeing the led card but not each other's choice. Both cards are then revealed.
(3) FOLLOWING: a player holding a card of the led colour must play one. Otherwise they may play any card.

WINNING A TRICK:
- If the 1 of the supertrump colour was played, it wins. Other supertrump cards are ordinary cards of their colour.
- Otherwise, if any trump was played, the highest-numbered trump wins.
- Otherwise, the highest-numbered card of the led colour wins.
- Ties cannot occur, because every card is unique.
- The winner leads the next trick of the same deal.

SCORING EACH TRICK: If the Lone wins the trick, the Lone's LoneTricks rises by 1. If a Pair member wins it, that member's PairTricks rises by 1.

ANNOUNCEMENT: After each trick, all three cards, the winner and every player's counters are shown to everyone.

END OF DEAL: After the 4th trick, each player's remaining card is discarded unseen. Reserve cards stay out until the set ends.

END OF GAME: The game ends after trick 36.

Objective: The player with the highest LoneTricks total wins. If two or three players share the highest LoneTricks, the game is a draw among them. PairTricks does not affect the result.

Expected effect: Each player is Lone exactly once per set, holding the same L against the same 10 Pair cards, with the same public knowledge. Seats differ only by the hidden 5/5 split and by skill, so hand quality cancels out. The Pair still vetoes: they name colours to grab a supertrump 1 they hold, or to block the Lone's long colour. Every veto spends their choice of supertrump. The Lone reads the split from the names: a Pair naming Green may hold the Green 1, or may be protecting a Green void. The Lone then picks trump against the known pool, and in play reads voids, counts the 10 known cards and judges when the supertrump 1 is still out. Simple policies lose. A Lone who always picks the first allowed trump falls behind one who matches trump to L. A Pair that always names the first priority colour leaves the Lone a free choice of 3. A player who always plays their highest card wastes trumps. The play order rotates by set, so each seat is first, second and third Lone once and no seat gains from watching others play L first. Talk is omitted because the Pair is fully informed and talk could only be cheap bluffing that the Lone would rightly ignore.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
