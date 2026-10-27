# Variation: Three-Card Wizard

A compact Wizard for 3-4 players: 12 rounds of 3-card hands. Players bid exactly how many of the 3 tricks they will take, the dealer cannot let the bids total 3, and exact bids score big.

Players: 3 to 4, best with 3

## Review of the original

Wizard is a trick-taking card game for 3 to 6 players using a 60-card deck (four suits of 1-13, 4 Wizards, 4 Jesters). Hand size grows by one card each round. Players bid exactly how many tricks they will take and score well only for hitting the bid exactly.

- **non_degenerate**: good. Exact-bid scoring defeats every simple policy. Always bidding 0 loses whenever an opponent dumps a trick on you or your cards force wins. Always bidding high loses when the cards are weak. Always playing the highest card wastes winners. The dealer bids last, which gives a small informational edge, but the deal rotates so every seat holds it equally often.
- **skill_sensitive**: good. Card quality matters within a single round, but the scoring rewards accuracy rather than strength: a bad hand that bids 0 and takes no tricks scores 20. Over many rounds, strong players reliably outscore weak ones through bidding judgement, card counting and sabotaging opponents' bids.
- **headroom**: good. A novice can score by bidding conservatively. Expert play still improves through inference from bids, ducking and overtaking, and forcing tricks onto opponents who bid zero.
- **reasoning_dependent**: good. Hands are hidden. Players must infer opponents' holdings from their bids and from cards already played. The play of a round must be planned so that it lands exactly on the bid, which takes planning over several tricks.
- **verifiable**: good. The trick winner follows from fixed card-ranking rules, and the score is simple arithmetic on bid and tricks taken.
- **fits_platform**: bad. Later rounds have up to 20 tricks, meaning up to 20 sequential play steps in one round, far over 4 choice steps per round. The number of rounds varies (10 to 20). When a Wizard is turned for trump the dealer makes an extra choice. The full 60-card deck makes trick resolution long.

## Problems

- Growing hand sizes produce up to 20 tricks in a round, far beyond the limit of 4 choice steps per round.
- Round count and hand size depend on player count, producing long, uneven games that are hard to build.
- The dealer choosing trump when a Wizard is turned adds an extra choice step and an extra branch.
- Bids may total the number of tricks available, so every player can sometimes hit their bid without conflict, weakening the opponent-modelling tension.
- The large deck (60 cards, 4 suits) makes trick resolution and tracking heavy for a text engine with little gain for small hands.

## Changes

- Every round deals exactly 3 cards to each player, so a round has 1 bid step plus 3 trick-play steps. (fixes: Growing hand sizes produce up to 20 tricks in a round, far beyond the limit of 4 choice steps per round.): Keeps choice steps per round at exactly 4 while preserving bidding and multi-trick planning.
- The game always lasts 12 rounds, for 3 or 4 players, with the dealer rotating each round. (fixes: Round count and hand size depend on player count, producing long, uneven games that are hard to build.): 12 is divisible by 3 and 4, so every seat deals and bids last equally often. The length is fixed and short.
- If the turned trump card is a Wizard or a Jester, there is no trump this round. (fixes: The dealer choosing trump when a Wizard is turned adds an extra choice step and an extra branch.): Removes the dealer's extra choice without changing the core trick logic.
- The dealer, bidding last, may not make the total of all bids equal 3 (the number of tricks). (fixes: Bids may total the number of tricks available, so every player can sometimes hit their bid without conflict, weakening the opponent-modelling tension.): Guarantees at least one player cannot be exactly right. Players must read bids and fight to push others off theirs. The burden rotates fairly.
- The deck is reduced to 25 cards: three suits (Red, Blue, Green) of 1-7, plus 2 Wizards and 2 Jesters. (fixes: The large deck (60 cards, 4 suits) makes trick resolution and tracking heavy for a text engine with little gain for small hands.): Small enough for 3-card hands with 4 players while keeping suits, trump, Wizards and Jesters. Card counting becomes feasible and meaningful.

## Kept from the original

- Exact-bid scoring: 20 + 10 per trick if exact, otherwise -10 per trick off.
- Wizards always win (the first one played), Jesters always lose, and both may be played at any time regardless of the follow-suit rule.
- A trump suit set by a turned card.
- Must follow the led suit if able.
- Bidding in turn order with the dealer last, and a rotating dealer.
- Hidden hands and highest total wins.

## The variation's rules

DECK: 25 cards: three suits (Red, Blue, Green), each numbered 1 to 7 (21 cards), plus 2 Wizards and 2 Jesters. Wizards and Jesters have no suit.

SETUP: Seat players in a fixed order. Player 1 is dealer in round 1. The dealer moves one seat along each round. All scores start at 0. The game lasts 12 rounds.

EACH ROUND:
1. Deal: shuffle all 25 cards, deal 3 cards face down to each player (seen only by their owner), then turn the next card face up as the trump card.
2. Trump: if the trump card is a numbered card, its suit is trump for this round. If it is a Wizard or a Jester, there is no trump this round.
3. Bidding: starting with the player after the dealer and ending with the dealer, each player in turn publicly bids a whole number from 0 to 3: the number of tricks they expect to take. Each bidder sees earlier bids. The dealer may not choose a bid that makes the total of all bids exactly 3.
4. Tricks: 3 tricks are played. The player after the dealer leads the first trick; the winner of each trick leads the next. In each trick, starting with the leader, each player in turn plays one card face up from their hand, seeing the cards already played to that trick.
5. Led suit: the led suit is the suit of the first numbered card played to the trick.
   - If a Jester is led, the next numbered card played sets the led suit.
   - If a Wizard is led, there is no led suit for that trick and anything may be played.
6. Following: a player holding a numbered card of the led suit must play either a card of that suit or a Wizard or Jester. Wizards and Jesters may always be played. A player with no card of the led suit may play any card. Only legal cards are offered.
7. Trick winner:
   - the first Wizard played wins;
   - if there is no Wizard, the highest trump card wins;
   - if there is no trump, the highest card of the led suit wins;
   - if every card is a Jester, the first Jester played wins.
   The winner adds 1 to their tricks taken this round.
8. Scoring: each player whose tricks taken equals their bid scores 20 + 10 x tricks taken. Each other player loses 10 x |bid - tricks taken|.
9. Reset bids and tricks taken, and pass the deal to the next seat.

END: after round 12 the game ends.

Objective: After 12 rounds the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

Expected effect: Every round is a small puzzle of inference: read your 3 cards against the trump, read opponents' bids to estimate their hands, then play so that you land exactly on your bid while forcing unwanted tricks onto others or stealing tricks they need. The dealer's restriction guarantees conflict: at least one player must miss, so bids become weapons and signals, and the last bidder must judge whom to squeeze. Exact-bid scoring lets weak hands score by bidding low, so skill outweighs the deal over 12 rounds. Simple policies (always bid 0, always bid 1, always play the highest card) all lose to opponents who exploit them, for example by dumping Wizard-free tricks on a zero-bidder. Talk is left out: bids already carry the public signal, and because only one player can win, open talk would add words without adding decisions.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 11 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
