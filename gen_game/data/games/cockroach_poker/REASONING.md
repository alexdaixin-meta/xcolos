# Reasoning and planning: Cockroach Poker: Straight Calls

**Verdict: strong.** Winning rewards reading opponents' call tendencies, counting cards and thinking about the tie-break, and the best moves showed real inference and kingmaking awareness. Many calls still fell back on naive base rates. The game would demand more if senders had stronger reasons to build and later break truth patterns, for example longer games or scoring that punishes predictable calling.

From 3 play(s): 188 choices, 188 with a reason given (about 52.3 words each); results {'seat 2': 1, 'seat 1': 1, 'seat 3': 1}.

## Reasoning: 2 of 3

Most calls rest on card counting, on the sender's past honesty, and on asymmetric risk, which matters most when a player already holds two of a creature. Several of these inferences are sharp: a claim that would sink the sender is read as a bluff, and calls are weighed against the tie-break. But many calls treat the sender's card as a random draw from all unseen cards and ignore how often that sender had told the truth, so players kept losing to honest claims.

- match 1, turn 32, seat 2: "Seat 1 already has 2 Cockroaches face-up. If this card really were a Cockroach and I called TRUE, seat 1 would take it and lose at once. A sensible sender wouldn't take that risk" (Correctly infers a bluff from the sender's incentives given visible face-up cards.)
- match 1, turn 48, seat 1: "I lose only if the card is the last Cockroach, about 1 in 11 (9%)." (Accurate count of unseen cards, comparing the risk of elimination under each call.)
- match 2, turn 64, seat 3: "All 6 Cockroaches are accounted for: 4 are face-up and 2 are in my hand. The 7 unseen cards are 2 Rats, 3 Stinkbugs and 2 Toads" (Full deck tracking feeds an outcome-by-outcome evaluation of each call.)

## Planning: 2 of 3

Senders link card choice, claim and receiver into one plan, keep dangerous or useful cards for later, and in the endgame refuse to eliminate a player when that would hand the win to a rival. Plans seldom run beyond the next one or two sends, and players rarely build a deliberate truth pattern now in order to exploit it later.

- match 2, turn 51, seat 3: "If seat 2 wrongly took this Rat, they would have three Rats and lose at once. The game would end with seat 1 and me both at 4 face-up cards. Seat 1's most common creature count is 1 and mine is 2, so seat 1 would win the tiebreak." (Picks the receiver to avoid ending the game on a tie-break it would lose, as the designer intended.)
- match 3, turn 62, seat 2: "Seat 1 already has 2 Cockroaches, so a TRUE call would knock them out. But then only seat 3 and I would be ranked" (Declines to sink the weakest player because that would make the leader the winner.)
- match 2, turn 61, seat 2: "I already have 2 Rats face-up, so keeping it as my last card would be the bigger danger later." (Manages the hand for the coming rounds and the empty-hand rule.)
- match 1, turn 45, seat 2: "I keep my second Toad for later." (Keeps a threatening card for a later send.)

## Luck: 1 of 3

The deal shapes options; some hands collapsed to a single creature and forced the card. Many early calls were near coin-flips with no read. Still, outcomes mostly followed exploitable calling habits (seats that always called FALSE were fed true claims), so choices drove the results.

- match 2, turn 65, seat 3: "My only cards are Cockroaches, so I will claim the truth and send to seat 2." (The deal left only one card type to send, so the card choice was forced.)
- match 2, turn 4, seat 1: "With no read yet on how often seat 3 bluffs, calling FALSE is the better bet." (Early calls are made on base rates alone, close to a guess.)

## Weak spots

- match 1, turn 30, seat 1: Claimed Cockroach while holding 2 Cockroaches face-up, which is a transparent bluff: an honest Cockroach claim would risk the sender's own loss, and seat 2 saw through it. Claiming Rat or Stinkbug would have been believable.
- match 1, turn 28, seat 1: Called FALSE using a base rate that treats the card as a random draw from all unseen cards. It ignored that seat 2 had been honest every time and that seat 1 itself always called FALSE, which made it an obvious target for a true claim.
- match 3, turn 28, seat 1: Said seat 3 'told the truth on both of its claims', but seat 3 had made only one claim. Calling TRUE also went against a 3/13 base rate. FALSE was better supported.
- match 2, turn 44, seat 2: Kept calling FALSE on base rates after opponents had clearly begun feeding it true claims. It never adjusted to its own exploitable pattern and kept taking cards.
