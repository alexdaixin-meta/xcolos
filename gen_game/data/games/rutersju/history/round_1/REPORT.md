# rutersju: needs review

Built from the variation **Rutersju Twelve** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Play exactly 12 deals. The highest total after 12 deals wins; a tie for the top is a draw. (fixes: No number of deals and no winner rule: a single 3-card deal is mostly luck, and the game never ends by arithmetic.): Gives the game an arithmetic end and averages hand luck over many deals, so bidding and defending skill decide the result.
- The first bidder rotates one seat clockwise each deal. 12 deals divides evenly by 3 and by 4, so every seat bids first, and last, equally often. (fixes: The tie rule (last tied bidder wins) hands a permanent edge to a fixed seat unless the bidding order rotates, and no rotation is stated.): The tie-goes-to-last advantage is shared equally among all seats.
- A declarer who takes exactly the bid scores the bid plus 1. Failure is unchanged: each opponent scores the number of tricks of difference. (fixes: A declarer who makes a 0 bid scores 0, so a 0 contract is worthless. When everyone bids 0, the last bidder is forced into a pointless contract.): A 0 contract is now worth 1 point, so every contract has value. Failure still feeds every opponent, so a reckless high bid is punished.
- Limit the game to 3 or 4 players. Keep the 36-card pack, so 9 or 12 cards are dealt and the rest stay unseen. (fixes: Player counts up to 12 make rounds too long and exhaust the deck, which changes the game's character by player count.): Keeps each round short and inside the step limits. Leaves undealt cards, so nobody knows whether the diamond 7 is in play, which keeps inference alive.
- No discussion phase. The only signals are bids and cards played. (fixes: Talk among the defenders would let them announce their cards (for example 'I hold the diamond 7'), which would remove the hidden-hand inference that drives the defence.): The defenders share an interest only against the declarer. Talk would let them reveal their hands outright, and the game's reasoning is inferring hands from bids and play.

Objective: After 12 deals, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Declarer payoff for contract c, where p is the chance of taking exactly c tricks: +(c+1) if made. If missed, the declarer gets 0 and every opponent gets |c - t|. Relative swing of declaring against each opponent = (c+1)p - (1-p)E|c-t|. Table, using rough 3-card estimates with opponents defending aga
- playable: pass. The rules are complete: ranks and suits, the diamond 7 rule (it wins any trick, and when led it is a diamond lead that must be followed), follow suit, the trick winner leads next, the first bidder rotates, ties go to the last tied bidder, the forced 0 contract when all bid 0, absolute-difference sco
- reasoning_over_luck: pass. Chance is substantial: 3-card hands vary a lot, and the diamond 7 is a big swing. I estimate 40-55% of a single deal's outcome is chance, and over 12 deals the hands average out a fair amount. If everyone plays the intended strategy (bid your realistic exact trick count, defend to push the declarer 

## Complexity

- steps_per_round: designed 14, built 23, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 10, built 37, limit 20 (built: 80)
- hidden_elements: designed 1, built 12, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Every score starts at 0 and no deal has been played
- pass: 3 cards each are dealt and all of them are played, so hands end empty and the deck keeps 36-12 (cards are random, only counts asserted)
- pass: With 3 players, 36-9 = 27 undealt cards stay in the deck for the whole deal (random deal, only counts asserted)
- pass: Deal 1: seat 1 bids first, so when all bid 2 the last bidder, seat 4, is declarer
- pass: Deal 2: seat 2 bids first, so when all bid 2 the last bidder, seat 1, is declarer
- pass: Deal 3 with 3 players: seat 3 bids first, so when all bid 1 the last bidder, seat 2, is declarer
- pass: Each seat bids once from 0 to 3, and no pass is offered
- pass: Every bid is public: all bids are visible after bidding
- pass: Highest bid of 3 makes seat 2 declarer with contract 3
- pass: Bids 2,2,1,0 make the second bidder, seat 2, declarer
- pass: Declarer seat 3 is set before play and the deal is played out (who leads cannot be observed; random cards)
- pass: Following suit when possible still lets every card be played (random cards, only counts asserted)
- pass: Playing any card when void still empties every hand over 3 tricks (random cards, only counts asserted)
- pass: A deal with the diamond 7 possibly in play resolves all 3 tricks (random cards, only what chance cannot change asserted)
- pass: Tricks are resolved by the led suit and the deal finishes (random cards, only counts asserted)
- pass: Trick winners lead on until all 3 tricks are played (random cards, only counts asserted)
- pass: Exactly 3 tricks per deal: each 3-card hand is emptied and the deck is untouched (random cards)
- pass: Contract 3 is set for the declarer before scoring (made or missed depends on random cards, so score is not asserted)
- pass: Declarer seat 3 with contract 2 is scored (outcome random, so only the contract is asserted)
- pass: Scoring keeps the declarer recorded (opponents' tricks are random, so only the declarer is asserted)
- pass: After a deal is scored the game moves on to deal 2 (scores random, not asserted)
- pass: Deal 12 ends the game: seat 1 at 50 cannot be caught by at most 4 more points
- pass: Deal 12 ends the 3-player game: seat 3 at 40 wins
- pass: Play runs on bids and cards only: no option other than a bid or a card is needed to finish a deal

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 2': 12, 'seat 3': 13, 'seat 1': 4, 'seats 2 and 3': 2, 'seat 4': 6, 'seats 1 and 2': 2, 'seats 1 and 3': 1}, 85-127 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 168.0 decisions, prompts of 280 characters on average (longest 296)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 18, 'seat 3': 20, 'seat 1': 16, 'seats 2 and 3': 3, 'seats 1 and 2': 2, 'seats 1 and 3': 1}
- always `first@seat1`: won 34, lost 21, drew 5
- always `first@seat2`: won 34, lost 22, drew 4
- always `last@seat1`: won 10, lost 47, drew 3
- always `last@seat2`: won 16, lost 39, drew 5

## Triage (whose problem each failure was)

- round 1: fix_game: The game plays only one trick per round. After round 1 every hand still holds 2 cards and trick_number is 1, and after round 2 deal_number is still 1, so a 12-deal game cannot fit the 12 rounds the rules imply. The tests rightly treat one round as one complete deal (deal, bid, three tricks, score), and the platform's counted repetition can express all three tricks inside one round.
- round 1: revise_rules: The game is built correctly, but the design has two flaws. It needs 23 steps per round, over the limit of 20. And a thoughtless policy (always bid lowest and play the first legal card) wins well over half its games, while always bidding high loses badly.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The source allows 3 to 4 and the designer chose 4. Three is the smallest table with more than one opponent to set the contract against. More than 4 would exceed the 36-card pack's balance and make each trick too crowded for a 3-card hand to steer.
- No talk step: The rules forbid discussion; players communicate only through bids and cards.
- Card codes such as 'AS', '10H', '7D': A text code per card lets the engine check suits and ranks arithmetically.
- Declarer tie-break done by updating on bid >= high_bid in bidding order: This makes the last of the tied highest bidders the declarer, exactly as the rules require, using only arithmetic.
- Strategy at the table: A thoughtful player bids from hand strength and from the bids already made, since bidding last wins ties. Opponents cooperate to break the contract, either by taking tricks from the declarer or by giving tricks away when the declarer bid low.

## Simplifications

- The source's draw on a tied top total is represented as a shared win among the tied players: The engine has no separate draw; players level at the top share the result.
- The 3-trick play loop is expressed as a repeat over two steps: The engine runs flat step lists and repeats them until a condition holds.

## Encoding attempts

- 1: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 3 was offered '9D' in `play_a_card`, picked it, and was asked again without it (round 2): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 'JH' in `play_a_card`, picked it, and was asked again without it (round 3): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 2: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 3 was offered '9D' in `play_a_card`, picked it, and was asked again without it (round 2): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 'JH' in `play_a_card`, picked it, and was asked again without it (round 3): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 3: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `rank_table` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
