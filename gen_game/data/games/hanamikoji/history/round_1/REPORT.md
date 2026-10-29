# hanamikoji: needs review

Built from the variation **Hanamikoji: Compact Build** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- State is packed into 17 named attributes. Each player's placed counts are one 7-entry list. All seven markers are one 7-entry list. Each player's unused actions are one list. Charm held and Geisha held for both players are one 4-entry 'standing' list. One 'offer' list, one 'chosen action' and one 'pick' hold the current turn. (fixes: Attribute count exceeded the limit.): This replaces 14 count attributes and 7 marker attributes with 3, and keeps every tracked number within 20.
- Start-of-hand work is two conditioned steps: one shuffle, then one update that sets aside, deals, builds the deck and resets actions and counts. End-of-hand work is one step that adds the secrets, one calculation that compares the two count lists, updates the marker list and computes the standing list, one announcement, and one winner step that holds the win check and the hand-4 tiebreak. The fallback and the placement each become one step. (fixes: Steps per round exceeded the limit.): This brings the flat step list to 17 per round with 2 choice steps.
- The rules name exactly three hidden elements. (1) The hidden pile: the deck order plus the out-of-play pile, which holds the removed card and Trade-off cards. (2) The two private hands. (3) The two secret cards. (fixes: Hidden elements were not listed explicitly.): This makes the information structure explicit and verifiably within 3.
- Hand order is defined. Dealt cards are kept in deal order, each drawn card is added at the end, and removing cards keeps the order of the rest. The fallback uses the first cards in this order. The rules also show that a legal fallback always exists, because hand size always covers the remaining actions. (fixes: Hand order for the illegal-choice fallback was unspecified.): This removes the ambiguity in the illegal-choice rule.
- The complexity block is restated from an explicit count of steps and attributes, both listed in the rules. (fixes: The declared complexity block was not credible.): This makes the declared numbers match the build.

Objective: At the end of each hand, a player whose markers total 11 or more Charm wins. Otherwise, a player holding 4 or more Geisha markers wins. If neither has happened after hand 4, higher Charm held wins, then more Geisha held, and if both are equal the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. ARITHMETIC: Charm 2+2+2+3+3+4+5 = 21, and Items per Geisha equal Charm, so there are 21 cards. Per hand: 1 card to the pile, 6+6 dealt, 8 in the deck. Each player draws 4 (one per own turn), so each holds 10 cards in total. Each uses 1+2+3+4 = 10 cards. This is exact. Because total Charm is 21, only
- playable: pass. COMPLETENESS: every step names its trigger (turn 1 only / after turn 8 only), its actor and its effect. Deal positions are fixed: card 1 to the pile, 2–7 to the first player, 8–13 to the second, 14–21 to the deck. Hand order rules make the fallback deterministic. Duplicate naming is handled by 'coun
- reasoning_over_luck: pass. WHAT DECIDES: the order of actions (when to Secret or Trade-off versus give cards away), how Competition pairs are balanced, which Gift card is taken, and which Geisha to contest given persistent markers. INFERENCE: the 21-card composition is known. Each player can deduce the unseen set: opponent ha

## Complexity

- steps_per_round: designed 17, built 20, limit 20
- choice_steps_per_round: designed 2, built 7, limit 4
- attributes: designed 17, built 41, limit 20 (built: 80)
- hidden_elements: designed 3, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 32, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: the deal puts 1 card in the pile, 6 in each hand and 8 in the deck; seat 1 then draws 1 and hides 1 as Secret
- pass: R2: a new hand resets counts, actions and secrets but keeps markers, charm and geisha
- pass: R3: in hand 1 seat 1 acts on odd turn 3
- pass: R3: in hand 2 seat 2 acts on odd turn 3
- pass: R4: the active seat draws the first deck card to the end of its hand
- pass: R5: Secret moves one card from hand to secret and places nothing
- pass: R6: Trade-off moves two cards from hand to the pile and places nothing
- pass: R7: Gift takes 3 cards from hand and the opponent is offered card 1 to card 3
- pass: R8: the picked Gift card goes to the opponent, the other two go to the giver
- pass: R9: Competition takes 4 cards from hand and the opponent is offered Pair 1 or Pair 2
- pass: R10: the picked Competition pair goes to the opponent, the other pair to the active seat
- pass: R13: a used action is removed, so seat 1's later turn can only use Trade-off
- pass: R14: after turn 8 both secrets are added to their owners' counts
- pass: R15: strictly more cards takes a marker, a tie leaves the marker where it was
- pass: R16: charm sums the Charm of a player's markers and geisha counts them
- pass: R17: 11+ charm at the end of a hand wins, even against 4 geisha
- pass: R18: 4 geisha without anyone at 11 charm ends the game and wins
- pass: R19: at the end of hand 4 equal charm is broken by more geisha
- pass: R19: equal charm and equal geisha after hand 4 is a shared win
- pass: R20: after hand 1 ends without a win, hand 2 starts with a fresh deal and seat 2 acts first

## Does the file follow the spec's shape? (flags for a person)

- the spec declares game attribute `charm_values` but the game file does not: a piece of state the rules need is missing
- rule R11 has no scenario: nothing checks it
- rule R12 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 9, 'seat 2': 11}, 26-109 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 74.7 decisions, prompts of 154 characters on average (longest 293)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 29, 'seat 2': 30, 'seats 1 and 2': 1}
- always `first@seat1`: won 28, lost 32, drew 0
- always `first@seat2`: won 27, lost 33, drew 0
- always `last@seat1`: won 35, lost 25, drew 0
- always `last@seat2`: won 32, lost 28, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built and behaves as specified, and its balance is acceptable (about 29-30 wins per seat against random play, no thoughtless policy dominates). The flaw is structural: each round needs 7 choice steps against a limit of 4. Four action types each take a different number of cards, the active seat alternates, and a second-player pick follows Gift and Competition, so the choices cannot be expressed in so few steps.

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer's size is kept. The game is a two-sided split-and-choose duel: every Gift and Competition is offered by one player to the single opponent, and each marker is won by comparing two counts.
- Seat 1 is Player A and seat 2 is Player B: The source names the players A and B; markers 'A' and 'B' refer to seats 1 and 2.
- No talk step: The source has no talk. In a two-player zero-sum duel, talk would only add words, and bluffing already lives in the offers.
- Strategy at the table: A thoughtful player builds Gift and Competition offers so that either answer suits them, saves Secret and Trade-off to hide or deny key Geisha, and tracks the 21-card composition and the spent actions to infer the opponent's hand.
- rank_by = charm * 10 + geisha: Geisha never exceeds 7, so charm decides first and geisha breaks ties. The 11-Charm and 4-Geisha wins always coincide with the top of this ranking, as explained under decided_by.

## Simplifications

- The single choice 'name an action and its cards' is split into one action question plus 1 to 4 card questions, each chosen from the current hand list: Choices from a game list make a held card automatic and count duplicates correctly. The source fallback is kept for invalid answers, though it is rarely reached.
- standing is stored as each player's charm and geisha attributes instead of one 4-number table list: Ranking is an expression over you.<attribute>; the values are identical to standing [A charm, B charm, A geisha, B geisha].
- hand_A/hand_B, secret_A/secret_B, counts_A/counts_B and actions_A/actions_B become per-player attributes hand, secret, counts and actions: Per-player attributes with ally or public visibility give each player the same view as the source.
- Turn-1-only and after-turn-8-only steps are ordinary steps carrying a 'when' condition, and the after-turn-8 steps test turn_number = 9 after the increment: The step list is flat; single conditioned steps express it without block branching.
- The multi-step winner check is folded into one end condition plus the ranking: The engine ends on an arithmetic condition and ranks by one expression; the outcomes are unchanged.
