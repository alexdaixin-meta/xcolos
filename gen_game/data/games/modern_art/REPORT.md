# modern_art: needs review

Built from the variation **Modern Art: Four Seasons** (design round 3); see VARIATION.md.

## What was changed from the original, and why

- Use one auction type only: a simultaneous sealed first-price bid in which every player, including the auctioneer, bids. (fixes: P1): One poll per auction fits the engine and keeps valuation as the core skill.
- Use 16 auctions in 4 seasons of 4. The auctioneer order rotates each season: S1 seats 1,2,3,4; S2 seats 2,3,4,1; S3 seats 3,4,1,2; S4 seats 4,1,2,3. Deal 5 cards each from 24, leaving each player one spare card. (fixes: P2): Every seat auctions exactly once in every value tier, so expected auctioneer income is equal.
- Add a season-end nomination. After the 4th auction of a season, every player secretly and simultaneously names one artist, and each nomination adds 1 to that artist's season count before ranking. The 4 nominations weigh as much as the 4 cards played that season. (fixes: P3): The last card no longer settles the ranking. The last painting is bought without knowing the final ranking. The power to decide the ranking is shared by all four players at once, so they must predict each other's nominations.
- Make the bid tie-break explicit. Tied highest bidders are ordered auctioneer+1, auctioneer+2, auctioneer+3 (seat numbers, with 5 wrapping to 1, 6 to 2, 7 to 3), with the auctioneer last. (fixes: P4): This gives an arithmetic, unambiguous result. It rotates with the auctioneer, so it is symmetric over a season.
- After each sale, announce only the artist and the buyer. The price is told privately to the buyer and the auctioneer only. (fixes: P5): Money becomes genuinely hidden, so players must infer rivals' wealth and standing from their behaviour and their talk.
- Break artist ranking ties by higher cumulative value, then by a priority that rotates each season (S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G). (fixes: P6): No artist is favoured over the whole game, and established artists keep a natural edge.
- Starting money becomes 100, and a player must buy at least 3 paintings to be eligible to win. (fixes: P1): Players can afford Season 3-4 prices, and the 'never buy' policy stays losing over 16 auctions.

Objective: Only players who bought at least 3 paintings during the game are eligible. Among eligible players, the one with the most money wins. If two or more eligible players tie for most money, the game is a draw. If no player is eligible, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PAINTING VALUE TABLE. A placed painting pays its artist's cumulative value after the season's increment. An artist can gain at most 30 per season. Upper bounds per painting: S1 30/20/10 for 1st/2nd/3rd; S2 up to 60; S3 up to 90; S4 up to 120. An unplaced artist pays 0.

MAIN DECISION (sealed first-p
- playable: pass. COMPLETENESS.
- Every phase is specified: card choice, count increment, simultaneous talk, sealed bid bounded by current money, sale or no sale at a top bid of 0, a deterministic tie order relative to auctioneer seat A, payment split with floor, and what is announced to whom.
- Season end is specifi
- reasoning_over_luck: pass. WHERE CHANCE ENTERS. The only randomness is the initial 5-card deal from 6 of each of 4 colours, plus 4 hidden cards.
- A skewed hand (e.g. 3 of one colour) gives some influence over season counts.
- But each player plays only 1 card per season. Nominations add as many counts as auctions do.
- Every

## Complexity

- steps_per_round: designed 15, built 16, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 18, built 50, limit 20 (built: 80)
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup deals 5 cards to each seat, leaves the deck empty and sets 4 cards aside
- pass: Setup gives 100 money, 0 paintings and all artist values at 0
- pass: Season 2 auction 1: seat 2 is auctioneer and receives half of seat 3's bid of 20
- pass: Season 4 auction 2: seat 1 is auctioneer and receives half of seat 2's bid of 40
- pass: The auctioneer chooses among its distinct artists and the chosen card leaves its hand
- pass: An unsold Yellow painting still counts for Yellow, so Yellow places 2nd behind Blue's 4 nominations
- pass: After the talk poll every seat is still asked for a sealed bid, and an all-zero auction changes no money
- pass: A bid ranges from 0 to the seat's money and the auctioneer may bid all of its 40
- pass: When the highest bid is 0 the painting is unsold and no money or paintings change
- pass: Auctioneer 2 with seats 1 and 4 tied at 30: seat 4 buys
- pass: Auctioneer 1 tied with seat 3 at 20: seat 3 buys, because the auctioneer comes last
- pass: Seat 3 buys for 25: it pays 25 and auctioneer 1 receives 12
- pass: The auctioneer buys its own painting for 25: it pays 25 and receives nothing
- pass: A sale raises the buyer's paintings_bought from 2 to 3
- pass: Only the winning bid is charged; seat 3's losing bid of 20 costs nothing
- pass: Four Yellow nominations outrank one auctioned Green: Yellow gains 30 and Green 20
- pass: Equal season counts are broken by higher cumulative value (Green 20 > Yellow 10 > Blue 0)
- pass: Season 2 priority B>G>Y>R breaks equal counts and values: Blue 2nd, Green 3rd, Red 4th
- FAIL: Artists with season count 0 do not place: high-value Red and Green stay unchanged and only Blue gains | rule R15 is broken: Artists are ranked by season count, higher first; ties are broken by higher cumulative value, then by the season priority (S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G), and an artist with season count 0 cannot place.; game value_red: expected 50, got 70
- pass: Season-end gains are 30, 20, 10 and 0 for 1st to 4th (Red, Blue, Green, Yellow)
- pass: Paintings pay their artist's value after the increase; a 4th-placed Yellow pays 0
- FAIL: A held Green painting pays the public Green value of 30 when Green places 1st | rule R18 is broken: Each player's payout is told only to them, while the artists' cumulative values are public.; game value_red: expected 0, got 20
- pass: Collections and season counts are cleared after the payout: seat 1's old Red pays nothing in season 2
- pass: The game ends after the 16th auction and Season 4 payout; seat 3 is richest but ineligible, so seat 2 wins
- pass: Eligible seats 1 and 2 tied at 150 share the win over ineligible seat 3 with 300
- pass: With no seat holding 3 paintings, nobody wins
- pass: Seat 3 buys its own painting in the last auction, reaches 3 paintings, and wins with 320

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 2': 5, 'seat 1': 7, 'seat 4': 3, 'seat 3': 5}, 154-160 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 160.0 decisions, prompts of 130 characters on average (longest 158)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 16, 'seat 1': 18, 'seat 4': 16, 'seat 3': 10}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 9, lost 51, drew 0
- always `last@seat2`: won 14, lost 46, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file works as specified, but the design lets a thoughtless policy dominate. Always taking the first option, in practice bidding 0 and never spending, wins about 98% of decided matches. Always taking the last option, bidding everything, loses about 90%. Holding cash beats competing for paintings, which is a flaw in the economy, not in the code.
- round 2: revise_rules: The game file works as specified, but the rules make passive play dominant. The 'first' policy, almost certainly always bidding the minimum of 0, wins about 88% of decided games: it keeps all 100 starting money and still collects payments as auctioneer, while paintings are capped at 60 and are often worth 0. The 'last' policy, bidding everything, loses badly, so in practice there is no real auction tension.
- round 3: fix_tests: In the failing scenario seat 4 nominated Red, which raises Red's season count to 1. With Blue and Yellow at 0, Red ranks 2nd and correctly gains 20 cumulative value, so the game's value_red of 20 follows the rules and the test's expected 0 is wrong.
- round 3: fix_tests: In the first scenario seat 4 nominated 'Red', which by rule (a) gives Red a season count of 1. Red then legitimately placed second (+20, 50 to 70), so the game is right and the test's premise of a count-0 Red is false. The second failure (value_red expected 0, got 20) has the same cause: an uncontrolled nomination, probably the default first option 'Red', gave Red a season count.
- round 3: fix_tests: In the season-count-0 scenario the game's log shows seat 4 nominated Red. By rule (a) that gives Red a season count of 1, so Red rightly places 2nd and gains 20 (50 to 70). The game followed the rules, and the test wrongly assumed Red stayed at count 0. The Green payout scenario fails the same way: value_red went 0 to 20, consistent with an uncontrolled Red nomination placing Red.

## Choices the rules did not make

- 4 players (min 4, max 4, suggested 4): The designer fixed the table at 4. The auctioneer rotation, the tie-break order and the card counts (4 auctions per player plus 1 unused card each, with 4 cards set aside) all depend on exactly 4 seats.
- Talk kept as a simultaneous poll each auction, broadcast to all: The rules specify it. Players have opposing interests (an auctioneer wants high bids, a bidder wants a cheap buy, and nominations push artists up or down), so non-binding talk gives them something to bluff and reason about.
- Ranking and the bid tie-break are computed as numeric keys: This puts the stated tie-break orders into plain arithmetic without changing them.
- The ranking expression adds 1 to money and requires a value of at least 1: An eligible player with 0 money still beats every ineligible player, and if nobody is eligible nobody wins.
- Strategy at the table: Players balance spending against later payouts, use nominations to steer which artists place, read whose talk is a bluff, and make sure they buy 3 paintings to stay eligible.

## Simplifications

- The source's 'draw' among eligible players tied for most money becomes a shared win: The engine has no separate draw; players level at the top share the win, which is the equivalent outcome. 'No eligible player' becomes no winner through min_to_win.
- Each auction is one round; the season-end steps carry a when-condition (auction_in_season == 4): The step list is flat, so each season-end step is a single conditional step rather than a separate block.
