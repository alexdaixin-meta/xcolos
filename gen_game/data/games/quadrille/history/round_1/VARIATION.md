# Variation: Concealed Quadrille

A 20-card, four-player Quadrille in 8 hands of 5 tricks. Bid for Taker, name trump and secretly call a partner (or secretly go solo), then play tricks under Spadille-Manille-Baste trumps. Defenders must work out who is on the Taker's side.

Players: 4 to 4, best with 4

## Review of the original

Quadrille is a four-player, 40-card trick-taking game descended from Ombre. Bidding decides a Taker, who names trump and either calls a King, making that King's holder a concealed partner, or plays solo against three. The permanent black-Ace trumps (Spadille, Baste) and the trump-dependent Manille top the trump order, and stakes are settled by whether the Taker's side reaches six tricks.

- **non_degenerate**: good. Original and previous variation alike. Always Pass hands the priority seat a forced contract and leaves the passer a defender who loses d whenever a strong Taker makes it. Always bidding 5 gets codille, -5 per side member, on most hands. Always calling the same seat ignores the hand. The priority seat rotates evenly, each seat twice in 8 hands, so no seat has a built-in edge. Four players means one rival's gain is not simply another's loss.
- **skill_sensitive**: good. Card luck exists per hand, but over 8 hands a player chooses when to bid, how high, whom to call, and how to lead and follow. A bad hand can pass and defend, and a good hand can be underbid or squandered. Inferring the concealed partner and counting the 20 cards are both learnable skills.
- **headroom**: good. A weak player still scores by passing and defending sensibly. A strong player can improve indefinitely: bid calibration against remise/codille risk, choosing a call versus a solo (solo pays 3d), reading bids to find who holds the top trumps, signalling to a partner who knows it while opponents do not, and card-counting a fully dealt 20-card pack.
- **reasoning_dependent**: good. Three layers of hidden information must be inferred. Hands are private. In a call, partner identity is known only to the Taker and the partner. Defenders cannot tell whether a hand is a solo. Bids and plays are the only evidence. Planning spans 5 tricks per hand and 8 hands of score race.
- **verifiable**: good. Trick winners follow from card power. Hand results follow from tricks versus contract. Final scores and the winner are pure arithmetic, with tricks won as tiebreak.
- **fits_platform**: bad. The original has 40 cards, 10-card hands, Matador refusals, multiple contract levels and fish stakes, which is far too long. The previous variation was close but failed the build. Trick resolution was specified as six card categories evaluated per card through branching logic, which does not fit a 20-step round without a lookup operation. Its complexity report was also wrong: it declared 2 hidden elements while it had 3 (hands, partner, hidden T). Its claimed 18 steps was not backed by a step list.

## Problems

- P1 Step budget: the previous variation resolved each trick through per-card category branching (Spadille / Manille / Baste / other trump / led suit / other) for 4 cards, plus argmax and side-count updates, which realistically exceeds 20 steps per round once deal, bid, declaration and scoring steps are added.
- P2 Hand scoring was specified as 6 separate cases (made/remise/codille x call/solo), costing extra steps.
- P3 Misreported complexity: a hidden running count T was an extra hidden element (3, declared 2), and no step-by-step list supported the step count.
- P4 Hidden T had to be updated every trick using the hidden partner, adding a conditional hidden-state update every round.

## Changes

- Encode every card as a number: code = 10 x suit + rank, with suits Spades 1, Clubs 2, Hearts 3, Diamonds 4 and ranks A 1, 2 2, J 3, Q 4, K 5. Spadille is 11 and Baste is 21. A card's power is then ONE formula applied to all four played cards in a single step: 30 if code 11; 28 if code 21; 29 if code = 10t+2 (Manille); 20+rank if its suit is trump t; rank if its suit is the led suit; else 0. The winner is one argmax step. (fixes: P1 Step budget): Replaces six-way category branching with a single arithmetic calc. The rank codes double as plain-card power, so no table is needed.
- Score a hand in two steps: one calc for d = B-1 if T>=B, -(B-1) if T=B-1, else -B. Then one update applying +3d (solo Taker) or +d (call side) or -d (others) through per-player if-conditions. (fixes: P2 Hand scoring): Collapses 6 scoring cases into 2 steps.
- Drop the hidden running count T. Each player instead has a public 'hand tricks' count, since who wins each trick is announced anyway. At the end of the hand, T = hand tricks of the Taker plus hand tricks of the partner, with the partner counted only if a different seat. (fixes: P4 Hidden T and P3 Misreported complexity): Removes a per-trick hidden conditional update and one hidden element. The information is unchanged, because defenders still do not know which count belongs to the Taker's side.
- Provide an explicit numbered step list, with each start-of-hand and end-of-hand step guarded by a 'when' condition on the trick number. The total is 18 steps, 4 choice steps, 16 attributes, 2 hidden elements (hands, partner identity) and 1 random draw (the deal, first trick of a hand only). (fixes: P3 Misreported complexity): Makes the budget verifiable and the report honest.

## Kept from the original

- Four players, trick-taking with must-follow-suit and optional trumping when void
- Spadille (A of Spades) as permanent top trump, Manille (2 of trump) second, Baste (A of Clubs) third, always trumps whatever suit is trump
- Bidding for the right to be Taker and name trump
- The call with a concealed partner known only to the Taker and that partner, versus a solo against three, with solo paying more
- Made / remise / codille outcomes graded by how far the Taker's side falls short
- Zero-sum stake settlement among the four players

## The variation's rules

PACK AND CARD CODES: 20 cards. Each suit has A, 2, J, Q, K. Suits are numbered Spades 1, Clubs 2, Hearts 3, Diamonds 4. Ranks are numbered A 1, 2 2, J 3, Q 4, K 5. A card's code is 10 x suit + rank: for example K of Hearts = 35, A of Spades = 11 (Spadille), A of Clubs = 21 (Baste). Cards are always shown to players by name and code.

SEATS AND PUBLIC RECORDS: Seats 1-4 sit clockwise. Each player has a public score (starts 0), a public 'tricks won' total for the game (starts 0) and a public 'hand tricks' count (reset to 0 at the start of each hand).

STRUCTURE: 8 hands of 5 tricks, 40 rounds. One round is one trick. Hand h covers rounds 5h-4 to 5h. The priority seat of hand h is seat ((h-1) mod 4)+1, so the order is 1, 2, 3, 4, 1, 2, 3, 4.

START OF EACH HAND (first trick of the hand only):
1. DEAL: Shuffle the 20 cards and deal 5 privately to each player. Set every player's hand tricks to 0.
2. BID: All players at the same moment choose Pass, 3, 4 or 5: the number of tricks out of 5 their side promises to win. All bids are announced.
3. TAKER: The highest bid wins. Ties go to the tied player who comes first clockwise starting from the priority seat (that seat itself first). If all four pass, the priority seat is Taker with contract 3. The winning bid is the contract B.
4. DECLARATION: The Taker privately chooses a trump suit (Spades, Clubs, Hearts or Diamonds) and a partner seat (any of seats 1-4, including their own): 16 options. The trump suit is announced to all. If the partner seat is another player, the hand is a CALL and that player alone is privately told 'you are the Taker's partner'. If the Taker names their own seat, the hand is a SOLO and nobody is told anything beyond the trump suit. Nobody else learns the partner seat until the hand ends.

TRUMPS: The trumps are every card of the trump suit plus Spadille (code 11) and Baste (code 21), whatever the trump suit. Spadille and Baste count as trump-suit cards and as no other suit. Manille is the 2 of the trump suit. With red trump there are 7 trumps, and Spades and Clubs each have 4 non-trump cards. With black trump there are 6 trumps.

PLAY OF A TRICK:
- On the first trick of a hand the Taker leads. Afterwards the winner of the previous trick leads.
- The leader chooses any card from their hand. It is removed from the hand and shown to all.
- The led suit L is the trump suit if the led card is Spadille, Baste or any trump-suit card. Otherwise it is the led card's suit.
- The other three players then each choose a card from their hand at the same moment. A player holding any card of suit L (counting Spadille and Baste as trump suit) must play one. A player holding none may play any card. Illegal choices are not accepted.

CARD POWER: For each of the four played cards, with t the trump suit number:
- Spadille (11): 30.
- Manille (code 10t+2): 29.
- Baste (21): 28.
- Other card of the trump suit: 20 + rank (K 25, Q 24, J 23, red A 21).
- Non-trump card of the led suit: its rank (K 5, Q 4, J 3, 2 2, red A 1).
- Any other card: 0.
The highest power wins the trick. Ties cannot occur. All four cards and the winner are announced, and the winner adds 1 to their tricks won and their hand tricks.

HAND SCORING (after the fifth trick of a hand):
- T = the Taker's hand tricks, plus the partner's hand tricks if the hand is a call.
- d = B-1 if T >= B (made). d = -(B-1) if T = B-1 (remise). d = -B if T <= B-2 (codille).
- CALL: the Taker and the partner each gain d; the other two each lose d.
- SOLO: the Taker gains 3d; each of the other three loses d.
- Every hand sums to zero. The partner seat (or the fact that it was a solo), T, d and all scores are then announced.

NO TALK: There is no discussion phase. All communication is through bids and cards.

END: After round 40 the game ends and the winner is decided as in the objective.

STEP LIST PER ROUND (for building):
(1) [first trick of hand] deal 5 cards to each player.
(2) [first trick] reset hand tricks to 0.
(3) [first trick] simultaneous bid poll.
(4) [first trick] announce bids, compute Taker and B with key = bid x 10 + (4 - ((seat - priority) mod 4)), Pass = 0; all pass gives the priority seat and B = 3.
(5) [first trick] Taker's declaration choice.
(6) [first trick] store t and the hidden partner, announce trump.
(7) [first trick, when call] privately notify the partner.
(8) set leader = Taker on the first trick, else the last winner.
(9) leader's lead choice, remove the card, announce.
(10) compute L.
(11) simultaneous follow poll of the other three, with the legality check.
(12) compute power for all four played cards with the one formula.
(13) argmax: set last winner.
(14) announce the cards and winner, add 1 to the winner's tricks won and hand tricks.
(15) [fifth trick of hand] compute T and d.
(16) [fifth trick] update all scores with call/solo conditions.
(17) [fifth trick] announce partner or solo, T, d and scores.
(18) [round 40] decide the winner.

Objective: After round 40, the player with the highest score wins. If several tie for the highest score, the one among them with the most tricks won over the whole game wins. If that also ties, the game is a draw.

Expected effect: Play should be identical in spirit to the previous variation, now buildable inside the step limit. Bidding becomes a risk judgement, because remise and codille punish overbidding, while passing leaves you paying a strong Taker. The Taker must choose between a solo (3d, all risk) and calling a partner, picking the seat whose bid suggests complementary strength. Defenders must infer from bids and cards who the hidden partner is, or whether one exists, while the partner can play to help a Taker who knows them. Over 8 hands, card-deal luck is diluted and good bidding, inference and card counting decide the winner. Talk is left out deliberately, because public talk would let the partner reveal themselves and dissolve the concealed-partnership inference that is the game's reasoning content.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
