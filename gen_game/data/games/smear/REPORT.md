# smear: ready for review

Built from the variation **Pocket Smear** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Keep the compact Pocket Smear core: 24 cards in three suits of ranks 1-8, 4-card hands, 4 tricks per deal, 9 deals (36 rounds), 3 players, and the categories High, Low, Game and Three. (fixes: The original's deck (54 cards, jokers, jick), the stock exchange and discards, and the 6-trick deals make far too much state and too many steps for the engine.): This keeps the game within the step, attribute and round limits while preserving bidding, trump and category scoring.
- The game has a fixed length of 9 deals with rotating dealer and priority. There are exactly 3 players, no teams, and the highest total wins (a tie for highest is a draw). (fixes: The original's open-ended race to 21 with possible teams gives no fixed, buildable length and an unclear winner structure.): This gives a buildable fixed length and a clear arithmetic winner. With three rivals, sandbagging or always passing does not guarantee a result.
- The bid amount and the named suit are submitted together as ONE answer in ONE simultaneous poll (for example '4 Blue' or 'PASS Green'). (fixes: Previous variation, choice-step budget: if the bid and suit are separate submissions, round 1 has 5 choice steps (bid, suit, three card plays), over the limit of 4.): Round 1 then uses exactly 4 choice steps: the bid poll plus three card plays.
- State explicitly that only bid amounts (including PASS) and the pitcher's suit are revealed. Every other named suit stays secret for the whole game. (fixes: Previous variation, bid ambiguity: it did not say whether the suits named by non-winning bidders are revealed. That suit is meaningful hidden information, so players could not know what opponents learn.): Everyone now knows exactly what is public. The hidden suits stay private information, so opponents must infer them from bids and play.
- Every player must name a suit from their own hand even when passing. In an all-pass deal, the dealer's named suit becomes trump. (fixes: Previous variation: the all-pass fallback needs the dealer to have named a suit, but the rules let a passing player's suit seem optional.): The fallback always has a defined trump, and the forced pitcher always holds a trump to lead.
- Track only running state: High trump value and holder, Low trump value and holder, Three captor, and each player's pile card points. Each player's deal points are computed at the scoring step and not stored. (fixes: Previous variation: the attribute count was tight (about 18). Deal points must be computed at scoring time, not stored per player.): This keeps attributes at about 18, under the limit of 20.

Objective: After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. POINTS PER DEAL: High 1 and Low 1 are always awarded. Game 1 is awarded unless the top piles tie. Three is worth 3 but is awarded only if the trump 3 is among the 12 dealt cards (12/24 = 50%). That is about 1 + 1 + ~0.9 + 1.5 = ~4.4 points per deal, split among three players.

PITCHER EDGE: The pitc
- playable: pass. RULES COVERAGE: Every situation is specified:
- bid format, ties (priority order) and the all-pass case (dealer pitches at contract 2 with their named suit, which is guaranteed to be in their hand);
- the forced trump lead, which is always possible;
- the follow rule (follow suit or trump; anything 
- reasoning_over_luck: pass. SOURCES OF CHANCE: The deal is substantial: 4-card hands, a 50% chance that the trump 3 is dealt, and 12 unseen cards. The Three is 3 of a maximum 6 points per deal. I estimate chance at about 40-50% of a single deal's outcome. Over 9 deals, skill should decide most games, perhaps 60%+ of outcomes.


## Complexity

- steps_per_round: designed 14, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 62, limit 20 (built: 80)
- hidden_elements: designed 2, built 20, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 dealer rotation: in deal 9 seat 3 deals, so an all-pass makes seat 3 pitcher
- pass: R1 dealer rotation: in deal 5 seat 2 deals, so an all-pass makes seat 2 pitcher
- pass: R2 deal gives 4 cards each and sets 12 aside (random cards, only counts asserted after the first trick)
- pass: R3 every seat passing is recorded as bid 0 (random hands)
- pass: R4 bid amounts are revealed: everyone bids 6 in deal 2, seat 3 has priority
- pass: R5 the winning bid becomes the contract (deal 3, all bid 6, seat 1 has priority)
- pass: R6 tied top bid in deal 1 goes to dealer+1 = seat 2
- pass: R7 all pass in deal 1: dealer seat 1 pitches with contract 2
- pass: R8 first trick is led by the pitcher (random hands, only pitcher and hand sizes asserted)
- pass: R9 a later trick's leader may lead any card, not only trump
- pass: R10 play goes leader then seat order: seat 3 leads, then seats 1 and 2 follow
- pass: R11 a follower holding the led suit may play only that suit or trump
- pass: R12 a follower void in the led suit may play any card
- pass: R13 a low trump beats the led Red 8: seat 2 takes High, Low and Game, pitcher seat 1 is set
- pass: R14 the trick's cards go to the winner: seat 1's Green 8 capture gives it Game
- pass: R15 High goes to the capturer of the highest trump (seat 2), Low and Game stay with seat 3
- pass: R16 a single trump played is both High and Low: pitcher seat 2 makes 2
- pass: R17 tied most card points means nobody scores Game
- pass: R18 the capturer of the trump 3 scores Three (seat 2 gets 5), pitcher set
- pass: R19 non-pitchers add their deal points to their running scores
- pass: R20 pitcher reaching exactly the contract (6 of 6) adds the deal points
- pass: R21 a set pitcher loses the contract and may go negative (1 - 4 = -3)
- pass: R22 after the 36th trick the highest score wins
- pass: R22 players tied for the highest final score share the win
- pass: R23 a mid-deal trick passes with only card plays and leaves scores unchanged

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seat 3': 7, 'seat 2': 5}, 80-93 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 135.0 decisions, prompts of 266 characters on average (longest 496)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 23, 'seat 3': 22, 'seat 2': 14, 'seats 1 and 2': 1}
- always `first@seat1`: won 49, lost 11, drew 0
- always `first@seat2`: won 50, lost 10, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Choices the rules did not make

- 3 players, fixed: The designer set exactly 3; the priority order, dealer rotation and 12 set-aside cards are all built for 3 seats.
- Card encoding suit*10+rank (Red 1, Blue 2, Green 3): Lets trick winners, trump checks and card points be worked out by arithmetic; players see card names.
- Bid offered as one combined choice such as '4 Blue' or 'PASS Red': The engine takes one answer per question; listing only suits from the seat's own hand enforces that rule.
- PASS stored as bid 0: Allows a numeric comparison for the highest bid and an all-pass test with max(bid) == 0.
- No talk step: The rules forbid table talk; players communicate only through bids and cards.
- Strategy at the table: Players judge their hand's trump strength, bid against two rivals, and decide when to trump in, cash High or protect the 3, reading what is left from the cards played.

## Simplifications

- A tie for the highest final score is a shared win rather than a separate draw: The engine ranks by one expression and players level at the top share the win; this is the same outcome as a draw.
- Deal-start actions (deal, bid, pitcher resolution) are single steps carrying a 'when trick_in_deal == 1' condition: The step list is flat; per-step conditions reproduce the first round of each deal.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (bid_choice, bid_suit, trump_name) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `suit_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_table` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `bid_table` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
