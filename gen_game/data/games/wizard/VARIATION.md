# Variation: Wizard Duel of Three

Three players play 6 hands of 5 tricks with a 32-card Wizard deck. They seal-bid the exact number of tricks they will take, play one trick per round, and score 20 + 10 per trick for an exact bid or -10 per trick missed. The highest total after 30 tricks wins.

Players: 3 to 3, best with 3

## Review of the original

Wizard is a 3-6 player trick-taking game with a 60-card deck: four suits of 1-13, four Wizards that always win and four Jesters that always lose. Each round the hand size grows by one, a turned card sets trump, each player bids exactly how many tricks they will take, and only an exact bid scores well; the highest total wins.

- **non_degenerate**: good. Simple policies lose. Always bidding 0 fails whenever you are dealt Wizards or high trumps. Always bidding high misses often at -10 per trick. Always playing your highest card throws away the control that exact bids need. The deal rotates, so no seat has a lasting edge. Bid and play choices decide whether a bid is met exactly.
- **skill_sensitive**: good. Exact-bid scoring rewards accurate hand evaluation and careful card play: ducking, forcing tricks, and reading what opponents still need. Card luck matters within one hand, but over many hands better bidders win reliably, because a weak hand can still be bid low and made.
- **headroom**: good. Beginners score by making small bids. Strong players keep improving at counting played cards, inferring hands from bids, and manipulating tricks to break opponents' bids.
- **reasoning_dependent**: good. Hands are hidden and the undealt cards are unknown. Bids reveal partial information about opponents' hands. Play needs inference about who holds the remaining trumps and Wizards, and planning across the tricks of a hand.
- **verifiable**: good. Trick winners and scores follow mechanically from the cards played and the bids made.
- **fits_platform**: weak. The game is text-only and turn-based, but it has three build problems. Up to 20 rounds with up to 20 tricks each and one play per player per trick is far too long. Growing hand sizes need a variable number of choice steps. The follow-suit rule needs per-seat legal-option lists, and the previous build failed on these five times: 'Blue 5' and 'Green 2' were offered and then refused, internal fields leaked into the displayed state, attributes went unused, and broadcast placeholders were left unfilled.

## Problems

- Length: many rounds of growing hand sizes produce hundreds of play decisions, beyond the 40-round and 4-choice-steps-per-round limits.
- Variable hand size means a variable number of plays per round, which the flat step list cannot express.
- Follow-suit legality: the previous build repeatedly offered cards that were then refused ('Blue 5' in lead_a_card, 'Green 2' in second_card), because the legal list had to be rebuilt per seat from the trick state.
- Sequential bidding plus the dealer's forbidden-total rule costs three choice steps and a dynamic option list (the unused bid_options attribute) on top of three plays.
- Bookkeeping leaked into the displayed state: blank played_card copies appeared in your_hand.
- Unused attributes (full_deck, bid_options) were never changed by any step.
- Broadcasts used unfillable placeholders ({bid}, {tricks}, {score}).
- The dealer choosing trump on a turned Wizard adds an extra choice step for little reasoning value.
- A 60-card deck with up to 6 players and 13-card suits gives a large state for little added reasoning at 3 players.

## Changes

- One engine round equals one trick. The game is 6 hands of 5 tricks each, so exactly 30 rounds. (fixes: Length: many rounds of growing hand sizes produce hundreds of play decisions, beyond the 40-round and 4-choice-steps-per-round limits.): Each round then has a constant structure with one bid poll and three plays. This fits 4 choice steps and stays within 40 rounds while keeping several hands so bidding skill averages out card luck.
- Fixed hand size of 5 cards in every hand instead of 1, 2, 3, and so on. (fixes: Variable hand size means a variable number of plays per round, which the flat step list cannot express.): The number of plays per hand is constant, so no block of steps has to switch on or off depending on hand size.
- Remove the obligation to follow suit. Any card in hand may be played. The led suit still matters, because off-suit non-trump cards can never win. (fixes: Follow-suit legality: the previous build repeatedly offered cards that were then refused ('Blue 5' in lead_a_card, 'Green 2' in second_card), because the legal list had to be rebuilt per seat from the trick state.): Each seat's options become exactly its own hand, so nothing is ever offered and then refused. Trick tactics (ducking, trumping, saving Wizards) and the inference about hidden cards remain.
- Bids become one sealed simultaneous poll on the first trick of each hand. The options are the fixed list 0, 1, 2, 3, 4, 5, written into the step. Bids are revealed after the poll. There is no forbidden dealer total. (fixes: Sequential bidding plus the dealer's forbidden-total rule costs three choice steps and a dynamic option list (the unused bid_options attribute) on top of three plays.): This uses one choice step instead of three and needs no dynamic option list. Players must infer from their own hand alone, then read opponents' revealed bids during play.
- Mark the player scratch attribute played_card as hidden and never store it inside hand. The playing step removes the card from hand directly, and played_card is cleared at the start of each trick. (fixes: Bookkeeping leaked into the displayed state: blank played_card copies appeared in your_hand.): Players see only their real hand, the public trick, and the scores.
- Drop the full_deck and bid_options attributes. The deal step rebuilds deck from the constant 32-card list written into the step, and the bid poll carries its fixed options. Every remaining attribute is changed by a step that runs. (fixes: Unused attributes (full_deck, bid_options) were never changed by any step.): No attribute stays untouched.
- Every broadcast uses only {seat} and {value}, with one value per message: a separate message for each bid, each trick winner, each trick count, and each score. (fixes: Broadcasts used unfillable placeholders ({bid}, {tricks}, {score}).): No literal placeholder ever reaches players.
- A turned Wizard or Jester both mean no trump for that hand. (fixes: The dealer choosing trump on a turned Wizard adds an extra choice step for little reasoning value.): This removes the dealer's extra trump choice step.
- Exactly 3 players and a 32-card deck: four suits of 1-7, 2 Wizards and 2 Jesters. 15 cards are dealt, 1 is turned for trump and 16 stay unseen. (fixes: A 60-card deck with up to 6 players and 13-card suits gives a large state for little added reasoning at 3 players.): The state is small enough to build, and enough cards stay unseen that card counting and inference still matter. With three players, one rival's broken bid is not automatically your gain.

## Kept from the original

- Wizards always win (the first Wizard played takes the trick) and Jesters always lose (they win only if every card in the trick is a Jester).
- A turned card sets trump each hand.
- Each hand starts with a bid of the exact number of tricks a player will take.
- Exact-bid scoring: 20 + 10 per trick if exact, otherwise -10 per trick off.
- The led suit and trump decide tricks; the trick winner leads next.
- Hidden hands, inference from bids and played cards, and highest total wins.

## The variation's rules

DECK (32 cards). Four suits, Red, Blue, Green and Yellow, each numbered 1 to 7 (28 cards), plus 2 Wizards and 2 Jesters.

STRUCTURE. The game has 6 hands. Each hand has 5 tricks, and each trick is one game round, so the game lasts exactly 30 rounds. Seats are 1, 2 and 3. The dealer of hand 1 is seat 1, and the dealer moves to the next seat (1, then 2, then 3, then 1) each hand.

START OF A HAND (first trick of each hand only).
(a) The deck is rebuilt from all 32 cards and shuffled. This is the round's single random event.
(b) Each player receives 5 cards, kept privately.
(c) The next card is turned face up and announced. If it is a numbered card, its suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.
(d) The 16 remaining cards are not used this hand and nobody sees them.
(e) Each player's bid and tricks taken are reset to 0.
(f) All three players, at the same moment and without seeing each other's choice, bid how many of the 5 tricks they will take: 0, 1, 2, 3, 4 or 5. The bids need not add up to 5.
(g) All bids are then announced, one message per player.
The player after the dealer leads the first trick.

EACH TRICK.
(1) The led suit is reset to none and the trick is empty.
(2) The leader plays any one card from their hand, face up.
(3) The next player in seat order plays any one card from their hand.
(4) The third player plays any one card from their hand.
There is no obligation to follow suit: any card in hand may always be played.
The led suit is the suit of the first numbered card played in the trick. A Jester played before it does not set the suit. If a Wizard is the first card played, the trick has no led suit, and that Wizard wins.

WHO WINS THE TRICK.
- If any Wizard was played, the first Wizard played wins.
- Otherwise, if any trump was played, the highest trump wins.
- Otherwise, the highest card of the led suit wins.
- If all three cards are Jesters, the first Jester played wins.
Numbered cards not of the led suit and not trump can never win. Every card is unique, so there are no ties.
The winner's tricks taken increases by 1 and is announced, and the winner leads the next trick.

END OF A HAND (after the fifth trick).
Each player's score changes:
- If tricks taken equals the bid exactly, the player gains 20 + 10 x tricks taken.
- Otherwise, the player loses 10 x |bid - tricks taken|.
Each player's trick count and new score are announced in separate messages, then the dealer moves to the next seat.

INFORMATION. You see your own hand, the turned trump card, all revealed bids, every card played so far, and all scores. You never see other players' hands or the unused cards.

No discussion phase.

END. After the 30th trick (the end of hand 6), the game ends.

Objective: After 6 hands (30 tricks), the player with the highest score wins. If two or three players tie for the highest score, those players share the win and the game is a draw.

Expected effect: Players must judge a 5-card hand against 16 unseen cards and two unknown hands, then bid without seeing rivals' bids. During play the revealed bids tell everyone who needs tricks and who needs to avoid them, so good players duck, force and save Wizards or trumps to make their own bid and break a rival's. Removing follow-suit makes trumps and Wizards playable at will, so timing them matters even more. Card luck in a single hand is offset by exact-bid scoring and six hands. Talk was left out: it would only add cheap claims about hands that cannot be checked, while sealed bids already give the signal that matters, so talk would not add reasoning.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
