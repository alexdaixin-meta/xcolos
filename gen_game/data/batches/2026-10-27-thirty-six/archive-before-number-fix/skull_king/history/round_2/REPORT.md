# skull_king: needs review

Built from the variation **Skull King: Three-Card Bids** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Use a fixed 3-card hand, 3 tricks per round, 8 rounds, and 3 to 5 players. (fixes: Too big for the engine: 10 hands of growing size, up to 10 tricks per hand, follow-suit rules and an 8-player turn order far exceed the steps-per-round and choice limits.): This keeps every round inside 18 steps and 4 choices while preserving the bid-then-play structure.
- Replace suits with one suitless 18-card deck: numbers 1-12, two Escapes (power 0), a Mermaid (20), Pirate A (30), Pirate B (31) and the Skull King (40). Each trick is played as a simultaneous poll and won by the highest power, except that the Mermaid beats the Skull King. (fixes: Suits and the lead-suit rule add long chains of legality checks that the flat step list cannot express cheaply.): This removes follow-suit legality entirely while keeping the special-card hierarchy and its rock-paper-scissors twist.
- Drop Scary Mary. (fixes: Scary Mary needs an extra declaration choice, which adds a choice step for one card.): Saves a choice step. The two Pirates and two Escapes already supply both of her roles.
- Specify the bid step exactly. It is one simultaneous poll of all players whose options are the whole numbers from table attribute bid_min to table attribute bid_max (0, 1, 2, 3), generated from those attributes rather than typed as literals. Each player's chosen option is written into their own bid attribute, all bids are revealed only after everyone has chosen, and the scoring step reads that stored bid. tricks_won and bonus are reset to 0 at round start; bid is not reset to a literal, because the poll writes it. (fixes: The previous build never actually put the bid to players. Every bid was recorded as 0 and options 0 to 3 were never offered, so the scoring read a bid nobody had made.): The tests were right: the rules require players to choose 0 to 3, and the build never asked them.
- A successful zero bid now scores +20 and a failed zero bid -20, instead of ±30. (fixes: In the previous scoring, a successful zero bid paid 30 against 20 for one trick. That made 'always bid 0 and dump your lowest card' too attractive for a thoughtless policy.): A safe zero bid should be worth no more than one exact trick, so ducking every hand stops being the best thoughtless policy.

Objective: After round 8, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SEATS: Bidding and every trick are simultaneous polls. Deal order is irrelevant because the deck is uniformly shuffled. No seat leads, so neither move order nor information gives any seat an edge.

BID PAYOFF TABLE (rows = bid, columns = tricks won 0/1/2/3, bonus ignored):
- bid 0: +20 / -20 / -20 /
- playable: pass. COMPLETENESS: The rules are complete and unambiguous.
- The 18-card deck covers 5 players (15 cards dealt).
- Ties are impossible: only the two Escapes share a power, and n ≥ 3 guarantees a non-Escape card in every trick.
- The Mermaid–SK override is stated explicitly and applies even if a Pirate is
- reasoning_over_luck: pass. CHANCE: The deal matters. A hand of specials has a ceiling of 60 plus bonuses, while a hand of low numbers is capped at +20 from bid 0. The 50-point Mermaid capture is close to a 1-in-3 timing guess. Estimated luck SD is about 20 per round per player, about 57 over 8 rounds, or about 80 for the diff

## Complexity

- steps_per_round: designed 18, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 36, limit 20 (built: 80)
- hidden_elements: designed 2, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every score is 0 and the round counter is 0
- FAIL: Round start: round goes from 3 to 4 (cards are chance, only the counter is asserted) | rule R2 is broken: When a round starts, then round increases by 1, and every player's tricks_won is 0, bonus is 0 and hand is empty.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Round start resets tricks_won to 0: an old count of 50 would wreck seat 2's bid of 3, but with the reset seat 2 (at least 470) still beats seat 1 (at most 320) | rule R2 is broken: When a round starts, then round increases by 1, and every player's tricks_won is 0, bonus is 0 and hand is empty.; seat 2 bid: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- pass: Deck holds 18 cards before any deal
- FAIL: Deck is refilled to 18 at round start even if emptied, so 18 - 3x3 = 9 remain after the deal | rule R3 is broken: When a round starts, then the deck holds all 18 cards: powers 1 to 12, two 0s (Escapes), 20 (Mermaid), 30 (Pirate A), 31 (Pirate B) and 40 (Skull King).; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: With 4 players the deal leaves 18 - 12 = 6 cards in the deck | rule R3 is broken: When a round starts, then the deck holds all 18 cards: powers 1 to 12, two 0s (Escapes), 20 (Mermaid), 30 (Pirate A), 31 (Pirate B) and 40 (Skull King).; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: With 5 players each gets 3 cards, which leave the deck (3 remain) | rule R4 is broken: When cards are dealt, then each player receives exactly 3 random cards from the deck into their hand, and those cards are removed from the deck.; Dara: the rule for 3 was never matched (the game never put that option to this seat); Eli: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Hands are private and the deck is hidden: only counts are checked, 9 cards stay undealt with 3 players | rule R5 is broken: When cards are dealt, then a player's hand is visible only to that player, and the undealt deck is visible to no one.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Bids 0, 1, 2 and 3 are offered and stored for each seat | rule R6 is broken: When bidding, then every player at the same time chooses a whole number from 0 to 3, stored as bid, and no player sees another's bid before all are in.; seat 2 bid: expected 1, got 0; seat 3 bid: expected 2, got 0; seat 4 bid: expected 3, got 0; seat 1 was never offered 2, but should have been; seat 1 was never offered 3, but should have been; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: All bids are announced and kept: every seat bids 3 | rule R7 is broken: When all bids are in, then every bid is announced to everyone.; seat 1 bid: expected 3, got 0; seat 2 bid: expected 3, got 0; seat 3 bid: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Each trick removes the played card: after 3 tricks every hand is empty (cards are chance) | rule R8 is broken: When a trick is played, then every player at the same time chooses one card from their own current hand, that card is removed from the hand, and all played cards are revealed.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Mermaid over Skull King: who holds them is chance, so only round and bids are asserted | rule R9 is broken: When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick.; seat 1 bid: expected 1, got 0; seat 2 bid: expected 1, got 0; Dara: the rule for 3 was never matched (the game never put that option to this seat); Eli: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Highest power wins: the deal is chance, so only round and bids are asserted | rule R10 is broken: When the Mermaid and the Skull King are not both played in a trick, then the player of the highest-power card wins it (for example, 31 beats 30, and 12 beats 0).; seat 1 bid: expected 2, got 0; seat 2 bid: expected 1, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Trick winners gain tricks_won: who wins is chance, only bids and empty hands are asserted | rule R11 is broken: When a player wins a trick, then their tricks_won increases by 1.; seat 1 bid: expected 1, got 0; seat 2 bid: expected 1, got 0; seat 3 bid: expected 1, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Skull King pirate bonus: captures are chance, so only round and bids are asserted | rule R12 is broken: When the Skull King wins a trick, then its player's bonus increases by 30 for each Pirate (30 or 31) in that trick: 30 for one Pirate, 60 for both.; seat 1 bid: expected 1, got 0; Dara: the rule for 3 was never matched (the game never put that option to this seat); Eli: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Mermaid captures Skull King bonus: captures are chance, so only round and bids are asserted | rule R13 is broken: When the Mermaid wins a trick in which the Skull King was played, then the Mermaid's player's bonus increases by 50.; seat 1 bid: expected 1, got 0; Dara: the rule for 3 was never matched (the game never put that option to this seat); Eli: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: After 3 tricks the round is scored and ends: all hands empty, round 1 complete | rule R14 is broken: When 3 tricks have been played in a round, then the round's scoring happens.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Exact or missed bid of 3 keeps seat 1 at 170 or more from 200, above the others' maximum of 20 (outcome is chance, winner is not) | rule R15 is broken: When a player bid 1, 2 or 3 and tricks_won equals the bid, then their score increases by 20 times the bid plus their bonus (for example, a bid of 2 with 2 tricks and a bonus of 30 gains 70).; seat 1 bid: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Missed bid of 3 costs at most 30: seat 1 from 100 stays at 70 or more, above the others' 20 | rule R16 is broken: When a player bid 1, 2 or 3 and tricks_won differs from the bid, then their score decreases by 10 times the difference, and the bonus is not scored (for example, a bid of 3 with 1 trick loses 20).; seat 1 bid: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Bid 0 scores +20 or -20: seat 1 from 50 ends at 70 or 30, above the others (from 0, at most 20) | rule R17 is broken: When a player bid 0 and won 0 tricks, then their score increases by 20.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Bid 0 moves the score by exactly 20 either way: seat 2 from 45 ends at 25 or 65, above the others (from 0, at most 20) | rule R18 is broken: When a player bid 0 and won 1 or more tricks, then their score decreases by 20.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Starting from round 7 the game plays round 8 and ends there | rule R19 is broken: When the round counter reaches 8 after scoring, then the game ends.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Highest score after round 8 wins: seat 3 from 300 cannot be caught by seats from 0 that bid 0 | rule R20 is broken: When the game ends, then the player with the highest score wins, and players tied for the highest share the win.; Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `repeat` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 11, 'seat 1': 6, 'seats 1 and 2': 1, 'seat 3': 11, 'seats 1 and 3': 2, 'seat 5': 5, 'seat 4': 4}, 71-120 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 128.0 decisions, prompts of 175 characters on average (longest 179)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 18, 'seat 1': 20, 'seats 1 and 2': 3, 'seat 3': 16, 'seats 1 and 3': 2, 'seats 2 and 3': 1}
- always `first@seat1`: won 13, lost 43, drew 4
- always `first@seat2`: won 4, lost 56, drew 0
- always `last@seat1`: won 1, lost 58, drew 1
- always `last@seat2`: won 3, lost 57, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: The failing assertions check `deck` and `hand`, which are the coder's own bookkeeping and not part of the interface. The deck is legitimately refilled to 18 for the next round's shuffle, so expecting 9 or 3 left after the round misreads the rules. The bid and 'rule never matched' failures come from the tests' choice scripting: they expect bids to be offered as a fixed menu containing 1, the game never offered such a menu, so the default choice of 0 was entered and the bid checks failed.
- round 1: fix_game: The trace shows only 12 moves in round 1. That is exactly three simultaneous card plays of 4 seats, so the game never polls a bid: `bid` stays at its starting 0, and seats are never offered 0-3. The tests correctly expect the bid each seat enters to be recorded, and the rules do not reset bids at round end.
- round 1: fix_game: The tests correctly expect each player to be offered the bids 0, 1, 2 and 3 and to have the chosen value recorded in `bid`. In the game file, the bid step never offered those options (not even 0), so every seat's bid stayed at the default 0 and the bid-0 scoring followed from that.
- round 2: fix_tests: The R6 trace shows the game working as the rules say. The deck is refilled to 18 and 3 cards are dealt to each seat. A bid poll offering 0–3 stores the bids (all 0 here). Three tricks are played and resolved correctly, with seat 3 winning two and seat 2 one, and scoring applies the zero-bid +20/−20 rule. R2–R5 did not fail on what they assert (round counter, deck size, hands). They failed only on a test-side scripted rule ('option 0 offered exactly once to each seat') that the harness never matched under a 'decline' default.
- round 2: fix_game: The bid poll did not offer every seat the options 0 to 3. Seat 1's rule matched, but seats 2 and 3 were never offered option 3 and fell back to the default 0, so seat 2's bid of 3 could not be entered. The rules require one simultaneous poll in which every player chooses from bid_min to bid_max, so the game file is at fault.
- round 2: fix_game: The rules say the bid poll offers exactly 0, 1, 2 and 3, and the tests rightly answer 3 whenever that option is offered. The game never offered 3 to any seat, so every bid fell back to the default 0 (seat 2's expected bid of 3 came out as 0), which means the file builds the bid options wrongly.

## Choices the rules did not make

- 3 to 5 players, 4 suggested: The designer's table size of 4 is kept. The minimum is 3 because, with fewer, one player could hold both Escapes and a trick could end in a tie, and bids would have no rivals to read. The maximum is 5 because 5 x 3 = 15 cards fit an 18-card deck with some cards left unseen, and more seats would leave no uncertainty about the undealt cards.
- Strategy at the table: A thoughtful player bids from the strength of their hand and from how many high cards are still unseen. After the announced bids, they time their strong cards against the tricks rivals need, and they spend Escapes to avoid unwanted wins. Simultaneous play rewards predicting when others will commit their Pirates and the Skull King.
- No talk step: The source states there is no discussion phase.
- Table attributes mermaid_played, skull_king_played, pirates_in_trick, max_power and trick: The engine cannot compare one player's attribute against another's directly, so the trick resolution is computed through table attributes. The three tricks are counted with trick.
- The played attribute resets to -1 each round: This is a sentinel meaning no card played yet, so it cannot be confused with an Escape (power 0).

## Simplifications

- Shuffling is modelled as random draws from the freshly refilled deck list: The engine draws at random from a list, which is equivalent to shuffling and dealing.
- The three tricks use a repeat over the play, reveal, resolve and award steps, counted by trick: The engine runs a flat step list, so repetition happens through repeat with a counter.

## Encoding attempts

- 1: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered 31 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 4 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
