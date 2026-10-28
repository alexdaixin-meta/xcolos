# 01 design

- time: 2026-10-28T06:10:06+00:00 (60.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 790c00e0ac425e1d, reply sha256 57e103aa5051b9a1

## Sent

````
Original game: Scopa
Players in the original: 2 to 6

Original rules:
Scopa uses 40 cards in 4 suits. Players need even numbers; with 4+ they form pairs sitting opposite. Dealer gives 3 cards to each player and 4 face up to table, deck aside. On your turn play one card from hand. If a table card has same rank, you must take that pair. If not, you may take any set of table cards whose ranks sum to your card's rank, but a single equal rank takes precedence. If no capture is possible you add your card to the table. A capture that clears the whole table is a Scopa and scores 1. When all hands are empty deal 3 more cards each until deck is gone; the last player to capture takes any leftover table cards. Scoring per round: 1 for each Scopa, 1 for most cards captured, 1 for most Coins, 1 for the Seven of Coins, 1 for best Primera - sum of highest Primera value in each suit from your pile. Ties give no point. Teams pool captures. First to 11 wins.
````

## Reply

````
```json
{
  "original_summary": "Scopa is an Italian fishing card game played with a 40-card deck. Players take turns playing one card from a three-card hand to capture table cards of equal rank or of ranks summing to it. Clearing the table scores a Scopa, and each hand ends with points for most cards, most Coins, the Seven of Coins and best Primera, with play continuing until someone reaches 11.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No thoughtless policy wins. 'Always capture the most cards' gives away Scopas by leaving low single cards. 'Always play your lowest card' feeds the opponent. Choices clearly change the outcome. But the dealer plays last in every hand and takes all leftover table cards, which is a built-in seat edge in any single hand. The original evens this out only over many hands."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Expert players beat beginners over a full match, through card counting, refusing to leave capturable sums and protecting sevens. Within one hand the deal (who holds the sevens, which ranks reach the table) swings the result heavily. The original needs many hands to 11 before skill dominates."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A beginner can still score by taking matches and Coins. Strong play keeps improving: tracking which ranks are gone, leaving tables whose sum exceeds 10, baiting captures, and planning the last capture."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Opponent hands and the deck order are hidden. A good player infers which ranks remain from the played cards and predicts what the opponent can capture from a given table. Planning across the hand matters for majorities, sevens and the last capture."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is counting: cards, Coins, the Seven of Coins, Scopas. Primera is a table lookup and a sum. No judge is needed for the result. Only whether a capture is legal needs checking, which is a simple sum or match test."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only with no board. However, playing to 11 takes many hands (often 100+ plays), which exceeds 40 rounds. Primera needs a value lookup per suit, which is costly in steps. Team play for 4 or 6 players adds pooled piles and seating."
    }
  ],
  "problems": [
    "Playing to 11 points needs many hands, far more than 40 rounds.",
    "The dealer plays last and collects the leftover table cards, a seat advantage in any single hand.",
    "Each hand awards only about 5 points and ties award nothing, so short matches end tied or are decided by the deal.",
    "Primera requires a per-suit lookup table of special values, which is too many steps for the engine.",
    "Teams of 2 or 3 pairs add pooled piles and seating rules beyond the attribute budget.",
    "Choosing an arbitrary subset of table cards is hard to resolve arithmetically, and illegal declarations need a defined outcome.",
    "A Scopa on the very last play of a hand is pure luck for the last player."
  ],
  "changes": [
    {
      "what": "The match is exactly two hands (two full passes through the deck), 18 rounds each, 36 rounds total. A round is one card played by each player.",
      "why": "Fits within 40 rounds while giving two deals, so the luck of one deal is partly averaged out.",
      "fixes": "Playing to 11 points needs many hands, far more than 40 rounds."
    },
    {
      "what": "Players swap leader and dealer roles for hand 2, so each player plays last in exactly one hand.",
      "why": "The last-play and leftover-card advantage goes to each player once.",
      "fixes": "The dealer plays last and collects the leftover table cards, a seat advantage in any single hand."
    },
    {
      "what": "The winner is decided by total points over both hands. Ties are broken first by total captured cards, then by total Coins captured, then the result is a draw.",
      "why": "Arithmetic tiebreaks reward the same skills as the main scoring and cut down draws.",
      "fixes": "Each hand awards only about 5 points and ties award nothing, so short matches end tied or are decided by the deal."
    },
    {
      "what": "Primera is replaced by 'most sevens', with ties broken by most sixes, otherwise no point.",
      "why": "Keeps the strategic importance of sevens, which dominate Primera, using simple counts.",
      "fixes": "Primera requires a per-suit lookup table of special values, which is too many steps for the engine."
    },
    {
      "what": "The game is two players only.",
      "why": "Removes team piles and seating while keeping the core duel.",
      "fixes": "Teams of 2 or 3 pairs add pooled piles and seating rules beyond the attribute budget."
    },
    {
      "what": "A player declares the played card and the exact table cards captured. A referee checks the legality rule (match precedence, or an exact sum). An illegal declaration means the card is added to the table and nothing is captured.",
      "why": "Gives a clear yes/no check and a defined, mildly costly outcome for mistakes.",
      "fixes": "Choosing an arbitrary subset of table cards is hard to resolve arithmetically, and illegal declarations need a defined outcome."
    },
    {
      "what": "Clearing the table on the final play of a hand does not count as a Scopa (the traditional rule).",
      "why": "Removes a free point that depends only on position.",
      "fixes": "A Scopa on the very last play of a hand is pure luck for the last player."
    }
  ],
  "keeps": [
    "The 40-card Italian deck with ranks 1 to 10 and four suits including Coins.",
    "Three-card hands, four cards dealt face up to the table, and redeals of three each until the deck is empty.",
    "Capture by equal rank, with equal rank mandatory and taking precedence, or by a set of cards summing to the played card.",
    "Scopa points for clearing the table.",
    "The last capturer takes the leftover table cards.",
    "End-of-hand points for most cards, most Coins, the Seven of Coins, and the importance of sevens."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Scopa (hidden hands, card counting, sum captures, denying Scopas) fits a turn-based text engine. Only match length, Primera, teams and the seat edge need trimming."
  },
  "variation": {
    "name": "Scopa Duel",
    "summary": "A two-hand, two-player Scopa. Players alternate playing cards to capture by match or sum, avoid leaving Scopas, and fight for card, Coin and seven majorities. Each player plays last in one hand.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 40 cards in four suits: Coins, Cups, Swords, Clubs. Each suit has ranks 1 to 10: Ace=1, 2 to 7 at face value, Jack=8, Knight=9, King=10.\n\nSTRUCTURE: The match is 2 hands of 18 rounds each, 36 rounds in total. In each round both players play one card: first the Leader, then the Dealer. In hand 1 (rounds 1 to 18), Player A is Leader and Player B is Dealer. In hand 2 (rounds 19 to 36), the roles swap.\n\nDEALING: At the start of round 1 and round 19, the full 40-card deck is shuffled (the only random event that round). Four cards are dealt face up to the table, and three cards are dealt privately to each player. At the start of rounds 4, 7, 10, 13 and 16 (hand 1) and rounds 22, 25, 28, 31 and 34 (hand 2), both hands are empty and three more cards are dealt to each player from the deck. Each hand uses exactly 4 + 6x3 = 40 cards.\n\nINFORMATION: The table, all played cards and all captures are public. Each player sees only their own hand. The deck order is hidden.\n\nA PLAY: On your turn, choose one card from your hand and declare which table cards you capture: a list, possibly empty. The declaration is legal if:\n(a) some table card has the same rank as your card, and you declare exactly one such card; or\n(b) no table card has the same rank, and you declare either nothing or a set of table cards whose ranks add up exactly to your card's rank.\n\nIf legal, you take your card and the declared cards into your capture pile. If you declared nothing, your card goes face up onto the table. If the declaration is illegal, your card goes face up onto the table and you capture nothing.\n\nSCOPA: If your legal capture leaves the table empty, you score 1 Scopa point. The exception is the final play of a hand (the Dealer's play in round 18 or round 36), which never scores a Scopa.\n\nLAST CAPTURE: The engine records who made the most recent capture. After the Dealer's play in round 18 (and in round 36), every card left on the table goes to that player's capture pile. If nobody captured in that hand, the leftover cards are discarded.\n\nHAND SCORING (after rounds 18 and 36), using only that hand's capture piles:\n- 1 point to the player with more captured cards (none if 20-20).\n- 1 point to the player with more Coins (none if 5-5).\n- 1 point to the holder of the Seven of Coins.\n- 1 point to the player with more sevens. If tied, the player with more sixes gets it. If still tied, no point.\n- Plus each player's Scopa points.\n\nCapture piles are then cleared for hand 2, but each player's running totals of points, captured cards and captured Coins are kept.",
    "objective": "After round 36, the player with more total points across both hands wins. If tied, the player who captured more cards in total across both hands wins. If still tied, the player who captured more Coins in total wins. If still tied, the match is a draw.",
    "expected_effect": "Players must count played cards to infer the opponent's possible captures. They should avoid leaving tables summing to 10 or less, which invites a Scopa, and should weigh taking many cards against grabbing Coins and sevens. They also plan for the last capture. Swapping roles removes the dealer's edge, and two deals plus card-count tiebreaks reduce draws and the impact of a single lucky deal. Simple policies such as 'always capture the largest set' or 'always dump the lowest card' leave Scopas and sevens to a counting opponent and lose. Talk is omitted because there are only two players with strictly opposed interests."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 2,
    "attributes": 17,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
