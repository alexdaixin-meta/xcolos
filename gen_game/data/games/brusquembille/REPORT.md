# brusquembille: ready for review

Built from the variation **Mirror Brusquembille** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Step 1 now says both players see only the NUMBER of cards left in each pile (always equal), the fixed starting composition, and every card played so far. They never see the cards in either pile. A sentence spells out what can and cannot be inferred. (fixes: P1): Hands become genuinely private. Each player knows the opponent's remaining cards as a set but not which of them are in hand, and that gap is the inference the game rewards.
- A 'Hidden information' section lists exactly three hidden elements: Player 1's hand (seen by its owner only), Player 2's hand (seen by its owner only), and the order of both piles (hidden from both players, fixed by setup shuffles). It also lists everything that is public. (fixes: P2): The engine and the playing models can then tell precisely what is public and what is private, and the reported count is correct.
- Kept from the previous variation: each player has an identical private 16-card pile (one Ace, Ten, King and Seven of each suit, worth 100 points). (fixes: P3): Both players get equal total card strength. Only the draw order is random, and timing can overcome it.
- Kept: two players only, no chips, pot, side-payments or trump exchange, and the winner is the higher point total. (fixes: P4): This fits what the platform can decide and removes steps that add no reasoning.
- Kept: Queens and Jacks removed, and a 1-point bonus for the last trick, giving 201 points in total. (fixes: P5): An odd total makes a draw impossible.

Objective: After 16 tricks, the player with the higher score wins. Since 201 points are shared, a draw is impossible.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. ARITHMETIC: each suit is 11+10+4+0 = 25, so a pile is 4×25 = 100. Two piles give 200, plus the 1-point last-trick bonus gives 201. The total is odd, so the higher-total WINNER RULE can never draw. The game is zero-sum, so there is no cooperation and no 'safe option' problem.

SEATS: the piles are id
- playable: pass. RULES COMPLETE: the winner order (a)-(c) covers every case:
- one trump;
- same suit, including trump vs trump and identical cards, where the leader wins;
- different suits with no trump, where the leader wins.

DRAW COUNT: 13 cards per pile are drawn after tricks 1-13, so the piles empty exactly af
- reasoning_over_luck: pass. THE MIRROR DESIGN REMOVES THE ORIGINAL'S BIGGEST LUCK SOURCE. There is no competition for a shared stock, and both players hold identical 100-point resources over the game. Chance remains in two places:
- Arrival timing: for example, drawing trumps late, or holding Aces when you have no trump cover.

## Complexity

- steps_per_round: designed 12, built 11, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 11, built 29, limit 20 (built: 80)
- hidden_elements: designed 3, built 5, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Each pile holds 13 cards after the 3-card deal from the 16-card pile
- pass: Each seat draws 3 cards and pile_count is 13
- pass: Random trump and leader: only the facts chance cannot change are checked (nothing played yet)
- pass: Game starts with both scores 0 and trick 1
- pass: Leader plays a chosen card; it is led and recorded
- pass: Trick 1: follower may discard off-suit while holding the led suit
- pass: Trick 14: follower holding the led suit must follow
- pass: Trick 14: follower void in the led suit may play any card
- pass: Trump H: follower's 7H beats the led AS
- pass: Same suit: follower's TS beats the led KS
- pass: Identical cards: the leader wins
- pass: Different suits, no trump: the led 7S beats AH
- pass: Winning AS and TS adds 21 to the existing score
- pass: Trick 16 winner gets 11 card points plus a 1-point bonus
- pass: Follower wins the trick and becomes leader
- pass: Trick 13: both seats draw their last pile card and hands are back to 3
- pass: Trick 14: no draw, hands drop to 2, pile_count stays 0
- pass: After trick 16 the game ends and the scores total 201
- pass: Higher final score wins even after losing the last trick
- pass: Each seat is offered only the cards in its own hand

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 12, 'seat 1': 8}, 28-30 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 32.0 decisions, prompts of 119 characters on average (longest 164)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 28, 'seat 1': 32}
- always `first@seat1`: won 32, lost 28, drew 0
- always `first@seat2`: won 29, lost 31, drew 0
- always `last@seat1`: won 29, lost 31, drew 0
- always `last@seat2`: won 30, lost 30, drew 0

## Choices the rules did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer set 2. The game is a two-player duel of mirrored piles, and every rule (leader/follower, the 201-point total that rules out ties) assumes two seats.
- No talk step: The source has no communication, and in a zero-sum two-player duel talk adds nothing to reason about.
- Card codes as rank letter plus suit letter (A/T/K/7 with S/H/D/C): A compact text form for list membership and suit/rank tests.
- Same-suit comparison by point value: The point values 11 > 10 > 4 > 0 are strictly ordered like the ranks, so comparing points is the same as comparing ranks.
- The follower is asked after the leader, with ask: The rules are sequential: the follower sees the led card before choosing.
- Strategy at this table: A thoughtful player tracks the cards played to infer which cards the opponent still has between hand and pile, saves trumps and high cards for valuable tricks, and plans for the forced-follow endgame of tricks 14 to 16.

## Simplifications

- Drawing the 'top card' of a shuffled pile is a random draw from the pile list: The order is hidden from everyone and fixed by a random shuffle, so a seeded random draw is equivalent.
- Each pile is a hidden table attribute (pile_1, pile_2) rather than a player attribute: The rules hide a pile even from its owner, and a player attribute cannot be hidden from its owner. Each pile is still drawn only by its own seat, and its public size is kept in that player's pile_count.
- Card points and the trick winner are worked out by conditional arithmetic over the card codes: The engine has no lookup table, so the 4 rank values and the suit/trump tests are written as if-chains in the update steps.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (follow_card, led_card) in `your_view`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (follow_card, led_card) in `your_view`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
