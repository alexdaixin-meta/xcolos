# skull_king: ready for review

Built from the variation **Skull King: Three-Card Raids** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Fix the game at 3 players, every hand 3 cards, 9 hands, so each round of the engine is one trick (27 rounds). (fixes: Too long and too large: 10 hands of growing size means 55 tricks, and with up to 8 players each trick needs more than the 4 choice steps allowed per round.): One trick per round needs at most 4 choice steps (one bid poll plus 3 plays). 27 rounds is within the 40 limit.
- Use a 25-card deck: Green 1-7, Yellow 1-7, Black 1-5, 2 Pirates, 2 Escapes, 1 Mermaid, 1 Skull King. Drop Scary Mary and the second Mermaid. (fixes: The 70-card deck with many special cards inflates the dealing and resolution steps beyond what the engine builds reliably.): This keeps every type of interaction (following suit, black trump, escapes, the pirate/mermaid/king triangle) with a deck small enough to deal in one random draw. 9 of 25 cards are dealt, so the unseen remainder still creates uncertainty.
- Remove Scary Mary entirely. (fixes: Scary Mary needs an extra declaration choice when played, which adds a choice step for little strategic value.): This removes the extra declaration choice.
- Flat bid scoring: an exact bid of k (k at least 1) scores 20k; an exact zero bid scores 20; a missed zero bid scores -20; any other miss scores -10 per trick of difference. Bonuses (+30 per Pirate captured by the Skull King, +40 for a Mermaid capturing the Skull King) count only if the bid was exact. (fixes: The zero-bid payoff (hand number x 10) grows with hand number rather than with difficulty, which distorts late-hand bidding.): The zero bid is now worth the same as bid 1. It is chosen for weak hands, not as a late-game jackpot. All four bids are live options for a 3-card hand.
- Rotate the first leader of each hand among the 3 seats. 9 hands means each seat leads first exactly 3 times. (fixes: With growing hand sizes and an uneven count of hands per seat, the first-leader seat is not equalised.): This equalises any first-lead advantage.
- The engine offers each player only their legal cards when they play. (fixes: Too long and too large: 10 hands of growing size means 55 tricks, and with up to 8 players each trick needs more than the 4 choice steps allowed per round.): This keeps the game playable without a judge and prevents rule-breaking moves.

Objective: After 9 hands the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw among the tied players.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Hit payoffs: bid 0 = +20, bid 1 = +20, bid 2 = +40, bid 3 = +60, plus bonuses on a hit. Miss payoffs: bid 0 = -20; bid k>0 = -10 per trick of difference. With 3 players and 3 tricks, each player averages 1 trick per hand. ALWAYS BID 1: this hits only when the player takes exactly 1 trick, roughly 40
- playable: pass. Deck and structure: 7+7+5+2+2+1+1 = 25 cards. 9 hands × 3 tricks = 27 rounds, so the game is finite. The deal happens only on trick 1 of a hand (a `when` step), giving 1 random draw per round. Choice steps: the bid poll plus 3 card plays makes 4 on the first trick of a hand and 3 on the others, with
- reasoning_over_luck: pass. Chance: the 3-card deal decides whether a player can bid 2-3 (40-60 points) or only 0-1 (20 points). Over 9 deals this evens out partly. I estimate 35-45% of the result is card luck. Skill drives the rest. Bid estimation must account for 16 unseen cards and how strong a card is given 6 opposing card

## Complexity

- steps_per_round: designed 12, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 13, built 51, limit 20 (built: 80)
- hidden_elements: designed 2, built 12, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 27, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Deal: each seat gets 3 cards, 16 stay in deck (after one trick each hand holds 2)
- pass: Each player holds their own dealt hand (hand sizes only, deal is random)
- pass: All seats bid 0-3 and the bids are recorded
- pass: Hand 2 is led by seat 2 (all-Escape deal, so the leader wins the trick)
- pass: Play goes clockwise from the leader: the first Pirate (seat 1, after leader 3) wins
- pass: A suited card played after an Escape sets the lead suit, so seat 3 must follow Yellow
- pass: No suited card played: no lead suit, the Mermaid wins
- pass: Holding the lead suit, seat 2 is offered only Green and special cards
- pass: The leader and a player void in the lead suit are offered every card
- pass: Mermaid beats the Skull King
- pass: Skull King beats a Pirate when there is no Mermaid
- pass: The first Pirate played wins
- pass: Mermaid wins without Skull King or Pirate
- pass: The highest Black card wins over the lead suit
- pass: The highest card of the lead suit wins and an off-suit card does not
- pass: All Escapes: the first card played (the leader, seat 2) wins
- pass: The trick winner gains a trick and leads the next trick (shown by the all-Escape last trick)
- pass: Skull King capturing two Pirates adds 60 bonus, paid on an exact bid
- pass: Mermaid capturing the Skull King adds 40 bonus
- pass: After a trick the winner is recorded for everyone (tricks_won)
- pass: An exact bid of 2 scores +40 and an exact bid of 1 scores +20
- pass: Bid 0 and won 0 scores +20
- pass: Bid 0 but won a trick scores -20 and loses the Skull King bonus
- pass: A missed bid scores -10 per trick of difference and loses the bonus
- pass: At the end of a hand scores are applied and tricks_won resets to 0
- pass: The game ends after round 27 is scored; the highest score wins
- pass: Seats tied for the highest final score share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 4, 'seat 1': 9, 'seat 2': 6, 'seats 1 and 2': 1}, 71-77 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 108.0 decisions, prompts of 159 characters on average (longest 207)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 14, 'seat 1': 26, 'seat 2': 19, 'seats 1 and 2': 1}
- always `first@seat1`: won 14, lost 42, drew 4
- always `first@seat2`: won 13, lost 45, drew 2
- always `last@seat1`: won 3, lost 57, drew 0
- always `last@seat2`: won 2, lost 58, drew 0

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the game at 3 seats, and the 25-card deck, the 3-card deal and the clockwise leader rotation are all built for 3. Minimum and maximum are both 3.
- No free-talk step before bids or plays: The source has no talk. Strategy comes from reading the revealed bids and the cards played (whether to win or duck a trick to land your own bid, or to spoil a rival's), so added talk would only add words.
- One trick per round, with the deal, bid and scoring steps run only when trick_in_hand is 1 or 3: The source sets each round to one trick (27 rounds). Single-step 'when' conditions keep the step list flat.
- Ties at the top share the win: The source calls a top tie a draw among the tied players, which is exactly a shared win.

## Simplifications

- The 16 undealt cards stay in the deck list rather than a separate set-aside pile: They are unseen and unused until the next hand's reshuffle, so a separate list adds nothing.
- Card play uses ask in seat order starting from the leader: Tricks are sequential in the source; each later player must see the earlier cards to follow suit.
