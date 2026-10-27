# Variation: Lost Cities: Wager Draft

Two players draft from a shared public row of 2 cards into rising Red, Blue and Green expeditions. At round 5 each player secretly wagers on one colour, which doubles that colour's result. Every pick both builds your columns and denies your rival.

Players: 2 to 2, best with 2

## Review of the original

Lost Cities is a two-player card game. Players play cards from a private hand into rising columns of five colours, called expeditions. Each started column costs 20 points, wager cards multiply a column's result, and players draw from a shared deck or from discard piles. The higher total over three rounds wins.

- **non_degenerate**: good. No simple policy wins. Always discarding scores 0 and loses to any player who builds two good columns. Always playing scatters columns that each cost -20. Seat order alternates over three rounds. The previous variation kept this: always LEAVE scored -10, and always TAKE caused many burials.
- **skill_sensitive**: weak. In the original, skill matters through hand management, timing and denial, but draw luck is large. In the previous variation the two dealt Backed colours differed with probability 2/3. Each player's score then depended mainly on the arrival order of their own colour, which swung Backed scores by 20 to 60 points. Denial and inference were worth only a few points.
- **headroom**: good. A weak player can still score with one or two columns. A strong player keeps gaining through when to commit, which cards to hold back and what to deny. The game is not solved.
- **reasoning_dependent**: good. The original has hidden hands and an unknown deck, and players infer the opponent's columns from discards. The previous variation reduced this to guessing a dealt colour that played out mostly independently of the opponent.
- **verifiable**: good. Scoring is pure arithmetic: sums, a cost per column, multipliers and a bonus.
- **fits_platform**: weak. The original needs five colours, 60 cards, hands of 8 and discard piles that can be redrawn, which is far over the attribute limits. The previous variation undercounted its own attributes: it claimed 16 when the real count was 24, over the limit of 20. It also left its step count unverified.

## Problems

- P1: The previous variation's attribute count (24) exceeded the limit of 20, and its step count was unverified.
- P2: Order luck dominated. Each player passively accepted one card at a time in the order it arrived, so the arrival order of their own colour decided their score.
- P3: Independently dealt Backed colours usually differed. This made the two players' games nearly separate, so interaction and denial were thin.
- P4: The dealt hidden type acted as a lottery. Who got the colour that happened to arrive in the friendlier order decided the winner when both played well.
- P5: The 7 deck cards that were never revealed, plus seeing only one card at a time, left planning with little to work on.

## Changes

- Track only top value and sum per player and colour, and drop the card count. Replace the 4-card bonus with a bonus for a column sum of 25 or more. Store each revealed card as a single attribute such as 'Red 7'. (fixes: P1: The previous variation's attribute count (24) exceeded the limit of 20, and its step count was unverified.): This brings the attribute count to 19, and the steps per round are written out at 16.
- Each round, reveal a public row of 2 cards. The priority player picks one card or none, then the other player picks from what is left. There are 12 rounds and 24 of the 27 cards are shown. (fixes: P2: Order luck dominated. Each player passively accepted one card at a time in the order it arrived, so the arrival order of their own colour decided their score.): A shared draft makes order luck hit both players alike. The question becomes which card to take and which to leave the opponent, not whether one's own colour arrives kindly.
- Replace the dealt Backed colour with a secret Wager. At the start of round 5, after 8 cards have been seen and drafted, both players choose one colour to double, at the same moment and in secret. (fixes: P4: The dealt hidden type acted as a lottery. Who got the colour that happened to arrive in the friendlier order decided the winner when both played well.): The hidden element becomes a decision made with information, like playing a wager card in Lost Cities. It is no longer a random gift. Each player must also read and hide which colour is doubled.
- All colours are open to both players, and denying a card means taking it into your own column or burying it at -3. (fixes: P3: Independently dealt Backed colours usually differed. This made the two players' games nearly separate, so interaction and denial were thin.): Every pick both builds your columns and denies the opponent's. Players compete for the same colours, so guessing the opponent's Wager matters.
- Show 2 cards per round and leave only 3 cards unseen. The deck composition is public. (fixes: P5: The 7 deck cards that were never revealed, plus seeing only one card at a time, left planning with little to work on.): Players can count what remains in each colour and plan their rising sequences.

## Kept from the original

- Expeditions are columns of strictly rising values in each colour.
- Each started column has a fixed cost, so committing to a colour is a risk.
- A wager doubles one colour's result, positive or negative.
- A bonus rewards a long, deep expedition.
- Denying the opponent cards they need, and inferring their plan from what they take.
- Two players and a shared deck.

## The variation's rules

SETUP
1. The deck has 27 cards: Red, Blue and Green, each with one card of every value from 2 to 10. It is shuffled once, face down. Both players know this composition.
2. Each player has three expeditions, one per colour. Each starts empty and is tracked by its top value (0 when empty) and its sum. Each player also has a Burial penalty starting at 0. All of these are public.

EACH ROUND (12 rounds)
3. Priority belongs to seat 1 in odd rounds and to seat 2 in even rounds. This is announced.
4. The top two cards of the deck are turned face up as Card A and Card B. Their colours and values are shown to both players.
5. WAGER, at the start of round 5 only, before step 4's cards are revealed:
   - Both players secretly and at the same moment name one colour: Red, Blue or Green. This is their Wager.
   - The Wager cannot be changed and stays hidden until the end.
6. The priority player chooses A, B or NONE.
7. If they chose a card, they receive it and place it (see step 10).
8. The other player is told what was chosen. They then choose A, B or NONE. Naming the card already taken counts as NONE.
9. If they chose a card, they receive it and place it.
10. Placement is mandatory:
   - If the card's value is higher than the top value of that player's expedition in its colour (any card beats an empty expedition), it is added. Its value is added to the sum, and it becomes the new top value.
   - Otherwise the card is buried: it is removed from the game and that player's Burial penalty rises by 3.
11. Cards in the row that no one took are removed from the game.
12. Both choices, where each card went, and all expedition states and Burial penalties are announced.

After round 12, the 3 cards left in the deck are never revealed.

FINAL SCORING, for each player and each colour
13. An empty expedition scores 0. However, if the empty expedition is in the player's Wager colour, it scores -15.
14. Otherwise, the base is the sum minus 10.
15. If the colour is the player's Wager colour, the base is doubled. Negative bases are doubled too.
16. Add 10 if the expedition's sum is 25 or more.
17. A player's total is the sum of their three colour scores minus their Burial penalty.
18. Wagers are revealed and the totals are compared.

Objective: After round 12, the player with the higher total wins. Equal totals are a draw.

Expected effect: ['Order luck becomes shared. Both players see the same 2-card rows and priority alternates 6 and 6, so a lucky run of cards is contested rather than gifted to one player.', 'Rounds 1 to 4 are positioning. Players decide which colours to open and what to leave the opponent.', 'The round 5 Wager is a real decision with real information. Players must ask whether to double their strongest column or a colour the rival seems to neglect.', "After round 5, each player infers the rival's Wager from their takes and weighs denial against building. A player may bluff interest in a colour at a real cost.", 'Talk is absent. With two players and only one winner there is nothing to negotiate.', 'Simple policies all lose to sensible play:', '  Always NONE scores -15 from the empty Wager colour.', '  Always taking A buries often and opens every colour at its cost.', '  Always taking the highest card blocks your own rising sequences.']

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
