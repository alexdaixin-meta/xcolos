# modern_art: needs review

Built from the variation **Modern Art: Private Collections** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Deal all 20 cards out, 5 hidden cards to each player. Each round the auctioneer chooses which card from their own hand to put up for sale. Only auctioned cards raise market counts, and each player auctions exactly 3 of their 5 cards, so 8 cards never reach the market. (fixes: P3): This restores the original's core decision of which artist to push, and makes hidden hands the hidden state to infer: what others still hold and what they will play.
- Make bids any whole number from 0 up to the bidder's current money, with no fixed cap. (fixes: P1): Prices are found by bidding, and no cap sits below value. Whole-number bids make exact ties rare.
- Resolve ties among highest non-auctioneer bids by giving the painting to the tied player with the least current money. If they are still tied, the painting is discarded unsold and nobody pays, though the market count still rises. (fixes: P2): No seat is favoured, and a full tie benefits no one, which discourages tying on purpose.
- Replace the hot artist and its clues with hidden hands as the single strong hidden element. Talk is about holdings and intentions ('I am sitting on C, it will top the market'). (fixes: P4): The hidden hand is the original game's real hidden information, and it drives both planning and bluffing. One strong hidden element is preferred over a weak extra one, and dropping the clues keeps the game inside the attribute limit.
- Draw the round-1 auctioneer at random at setup. Auctioneers then rotate clockwise, so each seat auctions exactly 3 times. (fixes: P5): The seat that makes the last, best-informed sale is no longer fixed. It is also no longer known before the game starts.
- Set painting values to 60 for an artist ranked 1st, 40 for 2nd, 20 for 3rd, and 0 for 4th and 5th, with starting money of 100. Rank ties are broken alphabetically, which is known in advance. (fixes: P6): This follows the original's top-three payout and narrows the top-artist jackpot. A known tie rule is something players can plan around rather than luck.

Objective: After round 12, the player with the highest score (money plus collection value) wins. If two or more players tie for the highest score, the game is a draw between them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF SCALE. 12 of the 20 cards are offered, each artist at most 4. A typical spread is 4/3/3/1/1. Painting value is then about 4x60 + 3x40 + 3x20 = 420, set against 400 starting money, so paintings matter as much as cash. Money only changes hands between players, except when an auctioneer buys the
- playable: pass. The game is finite: 12 rounds. Bids, money, market counts and collections are all kept numbers. The ranking and scoring are arithmetic and need no judge, board or clock.

Limits against the stated complexity:
- steps_per_round 13 (limit 20)
- choice_steps_per_round 3 (limit 4): offer, talk, bid
- at
- reasoning_over_luck: pass. CHANCE. The deal decides which artists each player can push. That is real luck, but each player chooses 3 of their 5 cards, and every card is priced by bidding. A player dealt a strong hand still has to buy paintings at a sensible price. I estimate chance at about 25-35% of the result.

WHAT CAN BE 

## Complexity

- steps_per_round: designed 13, built 12, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 19, built 50, limit 20 (built: 80)
- hidden_elements: designed 1, built 12, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup deals 5 cards to each seat and empties the 20-card deck (after one offer the auctioneer holds 4)
- pass: Setup gives money 100, empty collections and zero market counts (checked after one free round)
- pass: Random first auctioneer: whoever it is offers one painting (only chance-independent facts asserted)
- pass: Offering a card removes it from hand and raises that artist's market count
- pass: Discarded unsold painting keeps its market +1
- pass: Talk round happens and the round still resolves normally
- pass: Every seat including the auctioneer bids from 0 up to its own money
- pass: All bids 0: auctioneer takes the painting free
- pass: Auctioneer strictly highest at 30 buys from the bank
- pass: Auctioneer tying at 30 loses to the non-auctioneer, who pays the auctioneer
- pass: Single highest non-auctioneer bid 40 wins and pays the auctioneer
- pass: Tied non-auctioneers: the one with strictly least money wins
- pass: Tied non-auctioneers sharing the least money: painting discarded, nobody pays
- pass: Won painting is appended to an existing collection
- pass: Auction result is resolved and public (winner pays its price)
- pass: Auctioneer passes from seat 4 to seat 1
- pass: Game ends after round 12; unplayed cards in hand score nothing
- pass: Market ties broken alphabetically (B over C over D over E)
- pass: Painting values 60/40/20 for ranks 1-3 and 0 for ranks 4-5
- pass: Score is money plus collection value; tied top scores share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 2': 1, 'seat 3': 7, 'seat 1': 4, 'seat 4': 8}, 106-108 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 108.0 decisions, prompts of 171 characters on average (longest 197)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 2 wins 88% of decided matches against random seats
- random seats: {'seat 2': 6, 'seat 3': 19, 'seat 1': 15, 'seat 4': 20}
- always `first@seat1`: won 49, lost 11, drew 0
- always `first@seat2`: won 53, lost 7, drew 0
- always `last@seat1`: won 5, lost 55, drew 0
- always `last@seat2`: won 7, lost 53, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file works as specified, but the design lets a thoughtless policy dominate. Always taking the first option, in practice bidding 0 and never spending, wins about 98% of decided matches. Always taking the last option, bidding everything, loses about 90%. Holding cash beats competing for paintings, which is a flaw in the economy, not in the code.
- round 2: revise_rules: The game file works as specified, but the rules make passive play dominant. The 'first' policy, almost certainly always bidding the minimum of 0, wins about 88% of decided games: it keeps all 100 starting money and still collects payments as auctioneer, while paintings are capped at 60 and are often worth 0. The 'last' policy, bidding everything, loses badly, so in practice there is no real auction tension.

## Choices the rules did not make

- Exactly 4 players (min, max and suggested all 4): The designer fixes the game at 4 seats. The 12 rounds and the 3 auctions per seat depend on that count.
- Keep the simultaneous talk step as a poll, broadcast to all: The rules require simultaneous messages. Players disagree about prices and about which artists to push, so bluffing about values and hands gives the talk real strategic content.
- When two or more of the tied non-auctioneers share the least money, the painting is discarded: The source says 'if the tied players also have equal money'. This reading is applied to the least-money players among those tied, so that the least-money rule decides whenever it can.
- Alphabetical tie-break encoded as key = market*10 + (4 - index): Market counts never exceed 4 per artist, so this key orders artists by count and then alphabetically using plain arithmetic.
- The per-artist coll_* counters mirror the collection list: Collection value needs arithmetic per artist. The public list remains the stated collection.
- Strategy at the table: A thoughtful player judges which artists will reach the top three from the public market counts and their own hidden hand, offers cards to steer the rankings, bids up to a painting's expected value, and uses talk to mislead. Auctioneers weigh selling to rivals for cash against buying back from the bank.

## Simplifications

- A bid above the player's money cannot be entered; the bid range is capped at current money: The source treats an over-bid as all of the player's money. Capping the range has the same effect.
- 'Clockwise' rotation is implemented as the next seat number, wrapping from 4 to 1: The engine has no table geometry, and seat order stands in for clockwise.
- The step that offers the auction card is shown with the auctioneer's letter options taken from their hand list: Options come from a list attribute, and duplicates collapse into one option per artist, which does not change the choice.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 4 players: the match crashed: CalcError: 'min(players, 1 + int(uniform(0, players)))': unsupported operand type(s) for -: 'list' and 'int'
- 2: passed
