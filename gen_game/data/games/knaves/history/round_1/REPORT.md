# knaves: needs review

Built from the variation **Knaves' Wager** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Shrink the deck to 20 cards (A, K, Q, J, 10 in each suit). Deal 6 cards to each player. Turn the 19th card up for trump and leave the 20th face down, out of play. (fixes: Scale: a 52-card deck with 17-card hands is far more state than needed to keep the game's decisions.): This keeps the original's structure of three equal hands, one turned-up trump card and leftover cards out of play, at a size the engine can track. Each hand becomes 6 tricks.
- Play exactly 6 hands (36 tricks, one trick per round). The highest total wins, and a tie for highest is a draw. (fixes: Length: 17 tricks per hand, played to 20 points, exceeds the 40-round limit and has an unpredictable length.): This gives a fixed length inside 40 rounds and a complete winner rule. Endgame unraveling does not apply, because this is not a cooperation game.
- Rotate the dealer every hand. The player left of the dealer (eldest) leads the first trick. Over 6 hands, each player is dealer twice and eldest twice. (fixes: Seat edge: the rules never rotate the deal or the first lead.): This removes any built-in seat advantage.
- Add a secret simultaneous bid at the start of each hand. Each player predicts how many tricks they will take (0 to 6). Bids are revealed before the first lead, and an exact bid earns +4. (fixes: Lottery: hand strength largely decides trick count, and nothing in the scoring rewards playing a weak hand well, so the deal often decides the winner.): A weak hand can now score well by bidding low and ducking accurately, so the deal changes what to do rather than who wins. Revealed bids give opponents a target to read and disrupt: they can force tricks on a player who bid low, or refuse tricks to one who bid high.
- Make each trick worth 2 points and keep the Jack penalties unchanged (spades -1, clubs -2, diamonds -3, hearts -4). (fixes: Lottery: hand strength largely decides trick count, and nothing in the scoring rewards playing a weak hand well, so the deal often decides the winner.): With only 6 tricks per hand, worth 1 each, the -10 of Jack penalties would swamp trick-taking. At 2 points per trick (12 per hand), tricks and Jacks keep roughly the original balance against each other.

Objective: After 6 hands, the player with the highest total wins. If two or three players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF ARITHMETIC PER HAND: 6 tricks x 2 = 12 trick points in total. The four Jacks carry -10 in penalties, but on average 18 of the 20 cards are in play, so about -9 is assessed. That leaves about +3 net from tricks, roughly +1 per player per hand. The exact-bid bonus is +4. Bidding accuracy theref
- playable: pass. COMPLETENESS: the deck (20 cards), ranks, deal (6/6/6, 19th card face-up for trump and out of play, 20th hidden), simultaneous bid 0-6, follow-suit rule, trick winner (highest trump, else highest card of the led suit), leader rule, scoring and draw rule are all specified. All cards are distinct, so 
- reasoning_over_luck: pass. CHANCE: the deal strongly shapes how many tricks a hand can take. However, the scoring rewards accurate prediction (+4) more than strength (about +1 net per hand from tricks). A weak hand that bids 0 or 1 accurately scores comparably to a strong hand. Over 6 hands with rotating lead, single-deal luc

## Complexity

- steps_per_round: designed 12, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 14, built 46, limit 20 (built: 80)
- hidden_elements: designed 2, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: totals are 0, hand 1, full 20-card deck, no hand dealt yet
- pass: Same suit ranks A K Q J 10: KS beats QS and 10S
- pass: Game ends after round 36: starting at round 35, two tricks are played and the game ends
- pass: Hand 1 starts with all totals at 0 (dealer and eldest are not observable)
- pass: End of a hand dealt by seat 3 moves on to the next hand
- FAIL: After a hand ends, a new hand is dealt and its first trick is played (only chance-free counts asserted) | rule R6 is broken: When a hand begins, eldest is the seat to the dealer's left: dealer mod 3 + 1.; the match crashed: CalcError: 'deck[int(uniform(0, len(deck)))]': list index out of range
- FAIL: Each seat is dealt 6 cards and holds 5 after the first trick (chance: counts only) | rule R7 is broken: When a hand begins, all 20 cards are shuffled and each player is dealt 6 cards into their hand, which only the owner can see.; game deck: expected 0 items, got 3; Ada: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Turned card is out of play: deck is empty after the deal and hands hold 5 after one trick (chance: counts only) | rule R8 is broken: When a hand is dealt, the 19th card is turned face up into turned_card, trump_suit becomes its suit, and that card is out of play.; game deck: expected 0 items, got 3; Ada: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Hidden card is out of play: no card is left in the deck after the deal (chance: counts only) | rule R9 is broken: When a hand is dealt, the 20th card goes face down into hidden_card, is out of play, and is never revealed during the hand.; game deck: expected 0 items, got 3; Ada: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Bids 0 to 6 are stored for each seat | rule R10 is broken: When a hand has been dealt, all players bid at the same moment a whole number from 0 to 6, and no bid is seen until all three are in.; seat 1 bid: expected 3, got 0; seat 3 bid: expected 6, got 0; seat 1 was never offered 6, but should have been; seat 2 was never offered 0, but should have been; Ada: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: All three bids are revealed after bidding | rule R11 is broken: When all three bids are in, all three are revealed to everyone.; seat 1 bid: expected 2, got 0; seat 2 bid: expected 5, got 0; seat 3 bid: expected 1, got 0; Ada: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 5 was never matched (the game never put that option to this seat)
- pass: Eldest (seat 2) leads; the others must follow its suit
- pass: The previous trick's winner (seat 3) leads the next trick
- pass: All three seats play one card each in the trick
- pass: Leader may lead any card in hand
- pass: Followers holding the led suit must follow it
- pass: A follower void in the led suit may play anything, including a trump that then wins
- pass: Highest trump wins: AD beats KD
- pass: Without trump, off-suit aces cannot beat the led 10C
- pass: Winning a trick adds 1 trick and 2 points
- pass: Winner taking JH and JC scores 2 - 4 - 2 = -4
- pass: Winner (trumping with JD) taking JS and JD scores 2 - 1 - 3 = -2
- pass: After a trick, its winner and every seat's tricks taken are public
- pass: Exact bid earns +4 at the end of the hand
- pass: End of hand: hand_score added to total, then reset to 0
- pass: Each seat plays one card in the trick and the trick is scored
- pass: Game ends after round 36 and the highest total wins
- pass: Tie for the highest total is shared by both seats

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 9, 'seat 1': 6, 'seat 3': 3, 'seats 1 and 3': 1, 'seats 1 and 2': 1}, 77-92 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 126.0 decisions, prompts of 128 characters on average (longest 191)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 19, 'seat 1': 19, 'seat 3': 17, 'seats 1 and 3': 1, 'seats 1 and 2': 3, 'seats 1, 2 and 3': 1}
- always `first@seat1`: won 10, lost 48, drew 2
- always `first@seat2`: won 15, lost 40, drew 5
- always `last@seat1`: won 8, lost 51, drew 1
- always `last@seat2`: won 10, lost 47, drew 3

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are sound and the platform can express them, but the game file mishandles its deck. After the first trick the three played cards (JD, 10D, QD) reappear in the table deck instead of leaving play. When a new hand begins the deck is not refilled with all 20 cards, so the deal draws from an empty list and crashes.
- round 1: fix_game: Dealing works: each seat holds 5 cards after one trick, the deck is empty, and the turned and hidden cards are set. But the bid step never offers the options 0 to 6. In every failing scenario the seats were never offered 0 (or 6), and the stored bid stayed at 0 when the test chose 3 and 6, so the bid is not implemented as the rules and interface require.
- round 1: fix_game: Cards played to a trick are put back into the table deck (the deck holds 10D, QD and JD after trick 1), and the deck is never rebuilt at the start of a new hand. So when hand 2 is dealt, the game draws from a nearly empty list and crashes with an index out of range. The rules deal all 20 cards each hand, and trick cards simply leave play.

## Choices the rules did not make

- Exactly 3 players (min, max and suggested 3): The designer fixed 3. The 20-card deck is built for it: 3 x 6 dealt cards plus the turned trump card and the hidden card make 20, so no other count works without changing the deck.
- No talk phase: The source has no table talk, and adding one would add a mechanic. The strategy is already in the exact bid (balancing taking tricks against hitting the bid), in dumping or avoiding Jacks, and in reading the revealed bids.
- Cards are written as rank plus suit letter (AS, 10H, ...), with rank values A=14, K=13, Q=12, J=11, 10=10: This lets the trick winner be worked out by arithmetic comparison.
- Seat to the left means the next seat number, with seat 1 after seat 3: The source says 'left' but gives no numbering, and a direction is needed for dealer rotation, eldest and play order.
- The first-round-of-hand steps (deal, bid, reveal) and the end-of-hand step carry a when condition on trick_in_hand: This keeps the step list flat while running those steps only on tricks 1 and 6 of each hand.

## Simplifications

- A tie for the highest total is a shared win rather than a separately named draw: The engine has no separate draw outcome; players level at the top share the result, which matches the source's draw.
- Dealing is done by random draws from the deck list rather than by a physical shuffle and dealing in order: Drawing at random is equivalent to shuffling, so the 19th and 20th cards are simply the two left after the 18 dealt cards.
- The order of play within a trick is three ask steps addressed relative to leader: The engine has no seat-order rotation, so the leader, the next seat and the third seat are each named by arithmetic on leader.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (played_card, played_card, played_card, led_suit) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `trump_weight` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `led_weight` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
