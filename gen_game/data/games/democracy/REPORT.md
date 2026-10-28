# democracy: ready for review

Built from the variation **Democracy: Three Tribes** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Fix the game at 3 players with a 24-card deck: 3 suits of 8 cards (5,4,3,A,K,Q,J,6), each suit worth 20 points, with a tribe at 11+ points. (fixes: Too many tracked numbers: per-suit point tallies for 4 suits across up to 6 players exceed the 20-attribute limit.): Per-suit tallies become 3 players × 3 suits = 9 attributes. The deck divides evenly into 6-card hands plus a 6-card voting pool. With three players, one rival's gain is not another's loss, so blocking and spoiling matter.
- Remove jokers and the player-count deck variants. (fixes: Variable deck construction (jokers depending on player count) and joker special rules add rule branches with little strategic value.): Fewer rule branches; the core trump/majority tension is untouched.
- Play exactly 4 deals of 6 tricks each (24 rounds), one deal per 'day', and end the match after the 4th deal. (fixes: Two 'days' of dealing per hand plus an open-ended 'first to an agreed total of tribes' match make length undefined and possibly long.): Gives a fixed, buildable length.
- Score tribes across 4 separate deals and add them up. (fixes: A single deal's hand quality and the random trump order can decide a match, so luck is not damped.): Over four deals, a bad hand in one deal can be outweighed by better reasoning in the others, which damps hand luck.
- Add one simultaneous message per trick before cards are chosen. (fixes: With 2 players, majorities become a zero-sum race in which the higher capture total almost always also takes the majorities, which reduces the reasoning.): With three players and only one winner, players can propose 'you take Hearts, I take Spades' deals to stop the leader. They can bluff about their holdings or betray a pact. Promises do not bind, so trust must be read.
- Most tribes wins. Tie-break: the highest total captured points in the final deal. If still tied, the tied players draw. (fixes: The winner rule has no tie-break, so tied tribe counts are unresolved.): Resolves ties by arithmetic on numbers the engine already tracks. Tallies are reset at the start of each deal, so final-deal tallies remain available at the end.

Objective: The player with the most tribes after 4 deals wins. If two or more players tie for most tribes, the tied player with the highest sum of their three suit tallies in the 4th deal wins. If they are still tied, the game is a draw among the tied players.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Arithmetic check. Suit points are 5+4+3+3+2+2+1+0 = 20, as labelled. The tribe threshold of 11 is more than half of 20, so at most one player can win each suit. All 24 cards are used every deal (18 in hands + 6 in the pool). Each trick consumes 3 hand cards + 1 pool card, so 6 tricks empty the deal 
- playable: pass. Rules are complete.
- Ranking: 5 > 4 > 3 > A > K > Q > J > 6.
- Trump: the trump suit beats all other suits. The Six of trump beats the Five of trump only when both appear, and there is only one trump suit per trick, so the exception is unambiguous.
- Ties: a tie is possible only when no trump is pl
- reasoning_over_luck: pass. Sources of chance:
- The 6-card deal (the share of Fives, Fours and trump-Sixes).
- The hidden pool order, which sets the trump sequence.

Rough estimate: hand strength explains perhaps 40–50% of a single deal's result. Aggregating four independent deals lowers that to about 25–35% of the match resu

## Complexity

- steps_per_round: designed 13, built 10, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 18, built 47, limit 20 (built: 80)
- hidden_elements: designed 2, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: the deck holds all 24 cards before any deal
- pass: Match ends after trick 24: last trick played from trick 23, seat 1 keeps the most tribes
- pass: First deal: each hand gets 6 cards and the pool 6, deck empty (only counts asserted, the deal is random)
- pass: A new deal keeps tribes (tallies come from a random deal, so they are not asserted)
- pass: The first pool card becomes the prize and its suit is trump
- pass: The talk poll each trick does not stop the trick from being played
- pass: Each seat plays a chosen card from its own hand and the card leaves the hand
- pass: Highest trump wins: 4H beats KH and the off-suit 5S
- pass: The 6 of trump beats the 5 of trump when both are played
- pass: With no trump played, the highest rank wins whatever its suit
- pass: With no trump and a tie at the top, nobody wins: each seat scores its own card and the prize scores for nobody
- pass: The trick winner takes all 3 played cards and the prize, each into its own suit's tally
- pass: Tallies carry over between tricks in a deal and played cards are public
- pass: End of deal: a tally of 11 or more in a suit gains a tribe
- pass: End of deal: suits where nobody reaches 11 award no tribe
- pass: Tribe scoring after trick 24 counts before the game ends: seat 2 wins with it
- pass: Tie on tribes is broken by the highest sum of 4th-deal tallies
- pass: Seats level on tribes and tallies share the win

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `sync` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 7, 'seat 3': 6, 'seat 1': 7}, 132-132 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 144.0 decisions, prompts of 154 characters on average (longest 170)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 23, 'seat 3': 17, 'seat 1': 20}
- always `first@seat1`: won 17, lost 43, drew 0
- always `first@seat2`: won 25, lost 35, drew 0
- always `last@seat1`: won 15, lost 45, drew 0
- always `last@seat2`: won 15, lost 45, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The rules are sound and fit the platform. The failures come from the file's step order: it shows players a 'your_new_hand' prompt before the prize and trump are set, and while played_card is still blank. A different order fixes this without changing any rule.

## Choices the rules did not make

- 3 players, fixed: The designer set 3. The game needs exactly three tribes contested by three players, and the 24-card deck splits exactly into three hands of 6 plus a pool of 6. Fewer or more seats would break the deal.
- Talk kept as a simultaneous poll broadcast to all: The rules say messages are written at the same moment and then shown. Talk matters because players compete for suits and can propose non-binding splits ("you take Hearts, I take Spades") that may be betrayed.
- Card encoding as rank+suit text (e.g. '5H', 'AS'): This gives the hand, pool and revealed lists a concrete, checkable form.
- Trick resolution by a strength number (rank 1 to 8, +100 for trump, 200 for the 6 of trump when the 5 of trump is played) with a unique maximum required: This makes the winner arithmetic. Trump ties cannot occur within one suit, so a tie at the top only happens with no trump played, which is the no-winner case.
- Tie-break folded into rank_by as tribes*1000 + the three tallies: Tallies are reset each deal, so at the end they are the 4th-deal tallies. A sum of at most 60 never overtakes a tribe.
- Draw expressed as a shared win: The engine has no separate draw: players level at the top share the win.

## Simplifications

- Deal-start and deal-end steps run inside the round with a `when trick % 6 == 0` condition: The engine repeats a single flat round. These steps are single conditional steps, not a separate block.
- Each deal restores all 24 cards to the deck before dealing: This models 'shuffle all 24 cards'. Drawing at random is the shuffle.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Deal 1, trick 1: the voting card is KS; trump is S. Your hand: {hand}. Write one short mes'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Deal 1, trick 1: the voting card is KS; trump is S. Your hand: {hand}. Write one short mes'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Deal 1, trick 1: the voting card is KS; trump is S. Your hand: {hand}. Write one short mes'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: passed
