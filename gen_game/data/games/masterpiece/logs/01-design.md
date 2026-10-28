# 01 design

- time: 2026-10-28T04:59:57+00:00 (94.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 f6b2f5a84662c198, reply sha256 bf2d2c26ecebf876

## Sent

````
Original game: Masterpiece
Players in the original: 2 to 6

Original rules:
Each player starts with $1,500,000 and one random painting whose hidden value card is clipped face-down to it. Paintings are public, values are private. On your turn roll two dice and move around a circular track. The space landed on triggers an event: Bank Auction of the top deck painting, Private Auction of one of your paintings chosen by the player to your left, optional buy from the bank for a listed price, forced or optional sale to the bank, forced sale to another player for $400,000, or free inheritance of the top painting. Auctions start at $100,000 with $50,000 increments, open to all eligible players in any order. High bidder pays the bank or the owner and takes painting plus new top value card. Play continues until the painting and value decks are exhausted, then cash plus revealed painting values are summed.
````

## Reply

````
```json
{
  "original_summary": "Masterpiece is a 2–6 player roll-and-move auction game. Players buy and sell public paintings whose dollar values are hidden on face-down cards known only to their owners, and the winner has the most cash plus painting value when the decks run out.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Choices matter in auctions, but much of the game is forced by dice: forced sales, free inheritances and bank buys at fixed prices. A player who lands on 'inherit' spaces gains free value no matter what anyone decides. Turn order and track position are not balanced by design."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Dice decide which event fires: free paintings, forced $400,000 sales, auctions. The value deck decides whether an inherited or auctioned painting is a $0 forgery or a $1,000,000 piece. Over a short game, that variance can swamp good bidding."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Valuing paintings from others' bidding behaviour, and deciding when to buy back your own, has real depth. Weak players still score because they always hold some cash and paintings."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Painting values are private to their owners. Buyers must infer value from the owner's behaviour and from who bids what, and owners can bluff. That is genuine hidden-information inference."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The final score is cash plus revealed painting values, which is pure arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "A circular movement track with dice and space effects is a spatial board. Open ascending auctions with players bidding in any order are real-time-like. Several event types and deck exhaustion make the game long, with many steps."
    }
  ],
  "problems": [
    "P1: The roll-and-move circular track is a spatial board and is out of scope.",
    "P2: Dice and the value deck create big luck swings (free inheritances, forced sales, forgery vs masterpiece draws) that swamp skill. This is the lottery trap.",
    "P3: Open outcry auctions in any order cannot be run turn-based without many steps and act like real time.",
    "P4: Too many event types (bank auction, private auction, bank buy, forced sale, forced trade, inheritance) exceed the step limits and dilute the core decision.",
    "P5: Game length depends on deck exhaustion, not a fixed number of rounds.",
    "P6: Starting holdings differ in hidden value (one random painting each), so the deal alone tilts the game."
  ],
  "changes": [
    {
      "what": "Remove the track, dice and all space events. Each round has exactly one Private Auction. The seller role rotates clockwise.",
      "why": "Keeps the signature private-auction mechanic with no board and no dice-driven events.",
      "fixes": "P1"
    },
    {
      "what": "Every player starts with the same hidden portfolio: four paintings worth $0, $300k, $600k and $1,200k, randomly assigned to their four public painting names. There is no value deck and no draws during play.",
      "why": "Every portfolio has the same total, so the deal decides only who knows what, never who is ahead. The forgery-or-masterpiece tension survives because others don't know which of your paintings is which.",
      "fixes": "P2"
    },
    {
      "what": "Same as above: equal starting portfolios.",
      "why": "Removes the unequal hidden value of the original single random painting.",
      "fixes": "P6"
    },
    {
      "what": "Auctions are sealed and simultaneous. Non-sellers submit one bid each. The seller submits a secret buy-back reserve. If the high bid beats the reserve, the high bidder pays the seller and takes the painting. Otherwise the seller keeps the painting and pays the high bid to the bank.",
      "why": "Turn-based and buildable in one poll. The costly buy-back keeps the original 'owner may keep it by paying' tension. It also stops the seller from keeping paintings for free, which would make every winning buyer overpay.",
      "fixes": "P3"
    },
    {
      "what": "Keep the original rule that the player to the seller's left chooses which of the seller's paintings goes up for auction.",
      "why": "This is a faithful hidden-information decision. The chooser must guess which painting is cheap or valuable for the seller to lose.",
      "fixes": "P4"
    },
    {
      "what": "Fixed length of 3 auctions per player (12 rounds with 4 players). Scores are computed at the end.",
      "why": "Gives a predictable length that fits the limits, and every player sells equally often.",
      "fixes": "P5"
    },
    {
      "what": "Add a simultaneous one-message talk phase before bidding each round.",
      "why": "Lets sellers hype or disparage the lot. Former owners, who know a resold painting's value, may tell the truth or lie. Gives bidders claims to test against reputation.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Public paintings with private dollar values known only to whoever has owned them",
    "Private Auction of one of your paintings, chosen by the player to your left",
    "The owner's option to keep the painting by paying the high bid",
    "Forgeries worth $0 mixed with valuable works, and bluffing about which is which",
    "Starting cash of $1,500,000",
    "Final score = cash + revealed painting values"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Masterpiece (auctioning paintings whose value only the owner knows, with a costly buy-back) is a strong hidden-information bluffing game. It fits the limits once the dice track and luck events are removed and portfolios are equalised."
  },
  "variation": {
    "name": "Masterpiece: Private Sales",
    "summary": "Players hold identical hidden portfolios: one forgery and three real works of different worth. Each round one player's painting, picked by their left neighbour, goes to a sealed auction with a secret costly buy-back reserve. Players talk, bluff and infer values from behaviour. Most cash plus painting value wins.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "MONEY: All amounts are in thousands of dollars ($k). Bids and reserves must be whole multiples of 50.\n\nSETUP:\n- Seat players in a fixed circle. Each player starts with 1500 cash. Cash amounts are public.\n- Each player receives 4 paintings with public names, unique across the game (for example 'P1-A' to 'P1-D').\n- The engine secretly and randomly assigns that player's four paintings the values 0 (a forgery), 300, 600 and 1200, one value each. Every player therefore holds exactly the same total value of 2100.\n- Each player is told privately the value of each of their own paintings.\n- Who owns which painting is public. Painting values are private: a value is known only to players who have owned that painting.\n\nROUNDS: The game lasts 3 rounds per player (12 rounds with 4 players, 9 with 3, 15 with 5). The seller of round r is player number ((r-1) mod N)+1, so the role rotates clockwise. Each round:\n1. ANNOUNCE: The engine names the seller. If the seller owns no paintings, nothing else happens this round; go to step 8.\n2. LOT CHOICE: The player to the seller's left chooses one painting from the seller's current collection. The engine announces it as the lot.\n3. TALK: Every player, seller included, writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.\n4. SEALED BIDS AND RESERVE: At the same moment:\n   - Each non-seller submits a bid between 0 and their current cash.\n   - The seller submits a secret reserve between 0 and their current cash.\n5. RESOLVE: Let B be the highest non-seller bid. Ties go to the tied bidder nearest the seller going clockwise.\n   - If B > reserve: the high bidder pays B to the seller, takes the painting, and is told its value privately. (A painting's value is now known to the seller and the buyer.)\n   - If B <= reserve: the seller keeps the painting and pays B to the bank. That money leaves the game. If B is 0, the seller pays nothing.\n6. ANNOUNCE: The engine publishes:\n   - all bids,\n   - the reserve,\n   - whether the painting sold or was kept,\n   - the money moved and the new cash totals.\n   The painting's value is NOT published.\n7. A painting bought earlier can be put up again later, whenever its new owner is the seller and their left neighbour chooses it.\n8. END CHECK: After the last round, go to scoring.\n\nSCORING: All painting values are revealed. Each player's score = cash + the total value of the paintings they own.",
    "objective": "The player with the highest score wins. If two or more players tie for the highest score, the game is a draw.",
    "expected_effect": "Every portfolio is worth the same, so the outcome depends only on trading well.\n\nRational sellers set a reserve near half the lot's value: selling at B gives B − V relative to keeping, while buying back costs B. A forgery's owner therefore wants to sell at any price, and the owner of a 1200 painting will not let it go below about 600.\n\nBuyers profit only when they win at a price between the painting's hidden value and that threshold. So they must read the seller's talk, the seller's earlier reserves, the left neighbour's choice of lot, and claims by former owners who know a resold painting's value.\n\nThe left neighbour reasons too: forcing the seller to auction their masterpiece invites a costly buy-back, while picking the suspected forgery gives everyone a cheap trap to avoid.\n\nTalk passes both tests. Players disagree because the seller wants a high price, bidders want a low one, and only one player can win. A bidder who simply believes 'this is my 1200 piece' loses heavily if it is the forgery. A seller who always hypes becomes unreadable and sells nothing above value.\n\nSimple policies lose:\n- Always bidding 0 never buys bargains and ends level at best, so any player who profits from one good purchase beats it.\n- Always bidding all your cash wins the forgery for everything you have.\n- Always setting the reserve at 0 sells masterpieces cheaply to a sharp bidder.\n- Always setting the reserve at maximum pays the high bid to the bank every time.\n\nThe end has no trust to unravel, because every round is a fresh auction with conflicting interests."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 15
  }
}
```
````
