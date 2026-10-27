# 60 design

- time: 2026-10-27T10:28:45+00:00 (96.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6ada10c5bf167ae7, reply sha256 0a5f06af7efb5499

## Sent

````
Original game: Lost Cities
Players in the original: 2 to 2

Original rules:
Place board with 5 color discard spaces between players. Shuffle 60 cards (9 numbers 2-10 and 3 wagers per color). Deal 8 cards to each player; remaining cards form face-down draw pile. Oldest player starts; turns alternate. On your turn you must first play one card from hand, then draw one. To play to your expeditions: start or extend a column of that color on your side; numbers must be strictly increasing within a column; wager cards can only be played before any number card in that column, multiple allowed. To discard: place a card face-up on its color discard pile, only top visible. Then draw: take top card of draw pile or top card of any discard pile, but not the card you just discarded. Game ends immediately when last card is drawn from draw pile. Score each color: sum numbers, subtract 20 if column exists, multiply result by 1 plus number of wagers (x2,x3,x4), add 20 bonus if column has 8+ cards. No column scores 0. Highest total after three rounds wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: The rules themselves are complete and finite:
- Simultaneous TAKE/LEAVE poll.
- Deterministic resolution and placement.
- Arithmetic scoring.
- Fixed 20 rounds.
Nothing needs a board, clock, judge, trading or binding agreements. Talk is correctly absent: two players, no shared interest to negotiate.

However, the stated complexity is wrong.
- Attributes. The game must track, per player and colour, top value, sum and count: 3 x 3 x 2 = 18. Adding two Burial penalties makes 20. Adding two Backed colours makes 22, and the revealed card's colour and value add 24. The designer states 16. That figure is not credible, and the real count exceeds the attribute limit of 20.
- Steps. Placement needs, for each of 2 possible recipients and 3 colours, a fits/does-not-fit branch: updates to top, sum and count, or burial +4. Together with the reveal, priority and poll steps, this makes 10 steps per round very tight. That figure is also unverified.
- reasoning_over_luck FAILED: With independent Backed colours, the two Backed colours differ with probability 2/3. In that case each player mostly takes cards in its own Backed colour. Contesting a card costs the blocker -4, or forces it into a bad column. Interaction is therefore thin, and each player's score is driven by the random arrival order of its own Backed colour. About 6.7 of that colour's 9 cards are revealed, and 7 deck cards are never seen.

Swing from order alone:
- If the Backed colour's 10 arrives first, the best play is to take it and stop, scoring (10 - 6) x 2 = 8.
- If the colour arrives roughly ascending, for example 4, 6, 8, 9, 10, then 37 - 6 = 31, doubled to 62, plus 10, gives 72.
- In typical orders, an online increasing selection from 6 to 7 random cards gets about 3 cards. Even so, Backed scores spread by roughly 20 to 60 points depending on order.

The remaining decisions are small by comparison: opponent inference about Backed colour, and when to deny a card at -4. Those decisions are worth a few points per game. When both players play well, the winner is mostly whoever's Backed colour happened to arrive in the friendlier order, which is chance and not reasoning. The inference element exists but cannot overcome a variance of this size.
- change: Recount and declare complexity honestly. Cut attributes to at most 20, for example by dropping 'count' and replacing the 4+ bonus with a sum threshold (bonus if sum >= 25), or by dropping the top-value attribute and enforcing a fixed ascending rule another way. Confirm that steps per round stay at or below 20 once placement into 3 colours for 2 possible recipients is written out.
- change: Reduce order luck. Reveal a public row of 2 to 3 cards each round, with the priority player choosing first and the other choosing from the rest (a sequential draft). Alternatively, show the next card as lookahead. Either way, planning around the order replaces passive acceptance of it.
- change: Force interaction so that inference matters. For example, deal both players Backed colours from a pool that guarantees overlap or conflict (e.g., each player has one Backed and one 'Doubted' colour that scores negatively), so that taking and denying cards actually trades off against the opponent's hidden goal.
- change: Alternatively, play duplicate: play the same shuffle twice with seats and Backed colours swapped, and sum the two totals, so that deck order cancels out and only decisions differ.
The variation that was reviewed: Lost Cities: Expedition Draft: SETUP
1. The deck has 27 cards: three colours (Red, Blue, Green), each with one card of every value from 2 to 10. Shuffle it face down. Players may know this composition.
2. Each player is secretly and independently dealt one Backed colour, Red, Blue or Green, each with probability 1/3. The two may be the same. Only its owner sees it.
3. Each player has three expeditions, one per colour. Each starts empty and is tracked by its top value (0 when empty), the sum of its values, and its card count. Each player also has a Burial penalty that starts at 0. All expeditions and Burial penalties are public.

EACH ROUND (20 rounds)
4. Reveal the top card of the deck to both players: its colour and value.
5. Priority belongs to seat 1 in odd rounds and to seat 2 in even rounds. This is announced.
6. Both players choose at the same moment: TAKE or LEAVE.
7. Resolution:
   - If exactly one player chose TAKE, that player gets the card.
   - If both chose TAKE, the player with priority gets it and the other gets nothing.
   - If both chose LEAVE, the card is removed from the game.
8. The player who gets the card does one of two things:
   - If its value is higher than the top value of their expedition in that colour (any value beats an empty expedition), it is added there. Its value is added to the sum, the count rises by 1, and the top value becomes this card's value.
   - Otherwise the card is buried: it is removed from the game and that player's Burial penalty rises by 4.
9. Announce both choices, who got the card, where it went, and all public expedition states.

The 7 cards still in the deck after round 20 are never revealed.

FINAL SCORING (after round 20), for each player and colour
10. If the expedition is empty, it scores 0. If it is empty and is that player's Backed colour, it scores -10.
11. Otherwise its base is sum minus 6.
12. If the colour is the player's Backed colour, the base is doubled. This applies to negative bases as well.
13. Add 10 if the expedition holds 4 or more cards.
14. The player's total is the sum of their three colour scores minus their Burial penalty.
15. Backed colours are then revealed. Winner: After round 20 the player with the higher total wins. Equal totals are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Lost Cities is a two-player card game. Players play cards from a private hand into rising columns of five colours, called expeditions. Each started column costs 20 points, wager cards multiply a column's result, and players draw from a shared deck or from discard piles. The higher total over three rounds wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always discarding scores 0 and loses to any player who builds two good columns. Always playing scatters columns that each cost -20. Seat order alternates over three rounds. The previous variation kept this: always LEAVE scored -10, and always TAKE caused many burials."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, skill matters through hand management, timing and denial, but draw luck is large. In the previous variation the two dealt Backed colours differed with probability 2/3. Each player's score then depended mainly on the arrival order of their own colour, which swung Backed scores by 20 to 60 points. Denial and inference were worth only a few points."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player can still score with one or two columns. A strong player keeps gaining through when to commit, which cards to hold back and what to deny. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The original has hidden hands and an unknown deck, and players infer the opponent's columns from discards. The previous variation reduced this to guessing a dealt colour that played out mostly independently of the opponent."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Scoring is pure arithmetic: sums, a cost per column, multipliers and a bonus."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original needs five colours, 60 cards, hands of 8 and discard piles that can be redrawn, which is far over the attribute limits. The previous variation undercounted its own attributes: it claimed 16 when the real count was 24, over the limit of 20. It also left its step count unverified."
    }
  ],
  "problems": [
    "P1: The previous variation's attribute count (24) exceeded the limit of 20, and its step count was unverified.",
    "P2: Order luck dominated. Each player passively accepted one card at a time in the order it arrived, so the arrival order of their own colour decided their score.",
    "P3: Independently dealt Backed colours usually differed. This made the two players' games nearly separate, so interaction and denial were thin.",
    "P4: The dealt hidden type acted as a lottery. Who got the colour that happened to arrive in the friendlier order decided the winner when both played well.",
    "P5: The 7 deck cards that were never revealed, plus seeing only one card at a time, left planning with little to work on."
  ],
  "changes": [
    {
      "what": "Track only top value and sum per player and colour, and drop the card count. Replace the 4-card bonus with a bonus for a column sum of 25 or more. Store each revealed card as a single attribute such as 'Red 7'.",
      "why": "This brings the attribute count to 19, and the steps per round are written out at 16.",
      "fixes": "P1: The previous variation's attribute count (24) exceeded the limit of 20, and its step count was unverified."
    },
    {
      "what": "Each round, reveal a public row of 2 cards. The priority player picks one card or none, then the other player picks from what is left. There are 12 rounds and 24 of the 27 cards are shown.",
      "why": "A shared draft makes order luck hit both players alike. The question becomes which card to take and which to leave the opponent, not whether one's own colour arrives kindly.",
      "fixes": "P2: Order luck dominated. Each player passively accepted one card at a time in the order it arrived, so the arrival order of their own colour decided their score."
    },
    {
      "what": "Replace the dealt Backed colour with a secret Wager. At the start of round 5, after 8 cards have been seen and drafted, both players choose one colour to double, at the same moment and in secret.",
      "why": "The hidden element becomes a decision made with information, like playing a wager card in Lost Cities. It is no longer a random gift. Each player must also read and hide which colour is doubled.",
      "fixes": "P4: The dealt hidden type acted as a lottery. Who got the colour that happened to arrive in the friendlier order decided the winner when both played well."
    },
    {
      "what": "All colours are open to both players, and denying a card means taking it into your own column or burying it at -3.",
      "why": "Every pick both builds your columns and denies the opponent's. Players compete for the same colours, so guessing the opponent's Wager matters.",
      "fixes": "P3: Independently dealt Backed colours usually differed. This made the two players' games nearly separate, so interaction and denial were thin."
    },
    {
      "what": "Show 2 cards per round and leave only 3 cards unseen. The deck composition is public.",
      "why": "Players can count what remains in each colour and plan their rising sequences.",
      "fixes": "P5: The 7 deck cards that were never revealed, plus seeing only one card at a time, left planning with little to work on."
    }
  ],
  "keeps": [
    "Expeditions are columns of strictly rising values in each colour.",
    "Each started column has a fixed cost, so committing to a colour is a risk.",
    "A wager doubles one colour's result, positive or negative.",
    "A bonus rewards a long, deep expedition.",
    "Denying the opponent cards they need, and inferring their plan from what they take.",
    "Two players and a shared deck."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of rising columns, commitment cost and wager fits inside the limits once the game becomes a 2-card draft with a secret wager chosen during play."
  },
  "variation": {
    "name": "Lost Cities: Wager Draft",
    "summary": "Two players draft from a shared public row of 2 cards into rising Red, Blue and Green expeditions. At round 5 each player secretly wagers on one colour, which doubles that colour's result. Every pick both builds your columns and denies your rival.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "SETUP\n1. The deck has 27 cards: Red, Blue and Green, each with one card of every value from 2 to 10. It is shuffled once, face down. Both players know this composition.\n2. Each player has three expeditions, one per colour. Each starts empty and is tracked by its top value (0 when empty) and its sum. Each player also has a Burial penalty starting at 0. All of these are public.\n\nEACH ROUND (12 rounds)\n3. Priority belongs to seat 1 in odd rounds and to seat 2 in even rounds. This is announced.\n4. The top two cards of the deck are turned face up as Card A and Card B. Their colours and values are shown to both players.\n5. WAGER, at the start of round 5 only, before step 4's cards are revealed:\n   - Both players secretly and at the same moment name one colour: Red, Blue or Green. This is their Wager.\n   - The Wager cannot be changed and stays hidden until the end.\n6. The priority player chooses A, B or NONE.\n7. If they chose a card, they receive it and place it (see step 10).\n8. The other player is told what was chosen. They then choose A, B or NONE. Naming the card already taken counts as NONE.\n9. If they chose a card, they receive it and place it.\n10. Placement is mandatory:\n   - If the card's value is higher than the top value of that player's expedition in its colour (any card beats an empty expedition), it is added. Its value is added to the sum, and it becomes the new top value.\n   - Otherwise the card is buried: it is removed from the game and that player's Burial penalty rises by 3.\n11. Cards in the row that no one took are removed from the game.\n12. Both choices, where each card went, and all expedition states and Burial penalties are announced.\n\nAfter round 12, the 3 cards left in the deck are never revealed.\n\nFINAL SCORING, for each player and each colour\n13. An empty expedition scores 0. However, if the empty expedition is in the player's Wager colour, it scores -15.\n14. Otherwise, the base is the sum minus 10.\n15. If the colour is the player's Wager colour, the base is doubled. Negative bases are doubled too.\n16. Add 10 if the expedition's sum is 25 or more.\n17. A player's total is the sum of their three colour scores minus their Burial penalty.\n18. Wagers are revealed and the totals are compared.",
    "objective": "After round 12, the player with the higher total wins. Equal totals are a draw.",
    "expected_effect": [
      "Order luck becomes shared. Both players see the same 2-card rows and priority alternates 6 and 6, so a lucky run of cards is contested rather than gifted to one player.",
      "Rounds 1 to 4 are positioning. Players decide which colours to open and what to leave the opponent.",
      "The round 5 Wager is a real decision with real information. Players must ask whether to double their strongest column or a colour the rival seems to neglect.",
      "After round 5, each player infers the rival's Wager from their takes and weighs denial against building. A player may bluff interest in a colour at a real cost.",
      "Talk is absent. With two players and only one winner there is nothing to negotiate.",
      "Simple policies all lose to sensible play:",
      "  Always NONE scores -15 from the empty Wager colour.",
      "  Always taking A buries often and opens every colour at its cost.",
      "  Always taking the highest card blocks your own rising sequences."
    ]
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 3,
    "attributes": 19,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 12
  }
}
```
````
