# 04 design

- time: 2026-10-28T05:03:29+00:00 (107.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 abc76ee49b0af6b6, reply sha256 ae9ac665869b3e42

## Sent

````
Original game: Masterpiece
Players in the original: 2 to 6

Original rules:
Each player starts with $1,500,000 and one random painting whose hidden value card is clipped face-down to it. Paintings are public, values are private. On your turn roll two dice and move around a circular track. The space landed on triggers an event: Bank Auction of the top deck painting, Private Auction of one of your paintings chosen by the player to your left, optional buy from the bank for a listed price, forced or optional sale to the bank, forced sale to another player for $400,000, or free inheritance of the top painting. Auctions start at $100,000 with $50,000 increments, open to all eligible players in any order. High bidder pays the bank or the owner and takes painting plus new top value card. Play continues until the painting and value decks are exhausted, then cash plus revealed painting values are summed.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Seller's decision. A seller holding a painting of value v who faces a high bid B gets B - v by selling and -B by keeping, because a kept painting costs B paid to the bank. The seller should sell when B > v/2, so the best reserve is v/2: 0, 150, 300 and 600 for v = 0, 300, 600 and 1200. Buyer's decision against that seller, with no information (each v equally likely). A bid B wins only when v < 2B. Table, B : lots won : buyer's average gain when winning. 50 : {0} : -50. 200 : {0, 300} : 150 - 200 = -50. 350 : {0, 300, 600} : 300 - 350 = -50. 650 : all four : 525 - 650 = -125. 1000 : all four : 525 - 1000 = -475. No bid has positive expected value. A profitable bid B needs E[v | v < 2B] > B, and the reserve thresholds rule out every such set. This is a pure lemons market, and bidding 0 is the rational buyer action. Once a value is known, for example after a published reserve, buyers compete the price up to about v, so the trade gains about 0. Equilibrium: everyone bids 0, each seller sets a reserve of about v/2, nothing moves, and every player ends on 1500 + 2100 = 3600. Under the winner rule that is a draw, and no single bidder can profitably deviate. Thoughtless policies, under the winner rule: 'always bid 0' never loses money as a buyer and draws against all-zero opponents; it loses only when other players trade with each other at prices that differ from value, which rational play avoids. 'Always bid 0' is therefore effectively a policy that never loses. 'Always reserve max cash' loses, because others bid their full cash and the seller pays it to the bank. 'Always bid max' loses, because it pays up to 1500 for at most 1200. Sensible play collapses into a universal draw. When trades do happen they are zero-sum between two players, with money burned to the bank, so players cannot realistically win through skill. Seats: each player sells 3 times, which is symmetric; player N sells last and cannot be retaliated against, a small edge. Every player values a painting at the same v, so there are no gains from trade and no reason to transact.
- reasoning_over_luck FAILED: Chance comes from the random value assignment and the left neighbour's lot choice. The neighbour picks blind at first, so the lot is effectively random. When everyone plays well, buyers bid 0 and nothing happens, giving a 3-, 4- or 5-way draw at 3600. Inference therefore has nothing to act on: bidding into the information gap always loses money, and a seller's private knowledge earns nothing because no rational buyer pays. The published reserve, at about v/2, reveals the lot's value to everyone, which destroys the remaining hidden information on any painting that has been auctioned. With imperfect players, the result depends mostly on who makes mistakes, plus which value the blind lot choice happened to hit; roughly half the variance from any trade comes from the random v of a lot bought under uncertainty. There is no opponent type to model and no profitable action that follows from a correct inference. A good reasoner's best play is simply never to bid, which ties.
- change: Create gains from trade so that rational trades exist. For example, give each player a secret collector theme: paintings of one of 3 public styles are worth +50% to that player at scoring. Buyers then value lots differently from sellers, and inferring rivals' themes from their bids becomes the core reasoning.
- change: Remove or soften the rule that a kept painting pays B to the bank, for example by having the seller pay only a fixed fee of 50 when keeping. The seller's reservation price then no longer sits at v/2, which currently makes every buyer bid unprofitable.
- change: Do not publish the reserve. Publish only the bids and whether the lot sold or was kept, so a reserve of v/2 cannot reveal the value to everyone.
- change: Add an arithmetic tie-break, for example most cash and then most paintings, so that the passive equilibrium does not end every game as a draw.
- change: State explicitly how up to 20 paintings, each with an owner and a value, fit within 20 attributes, for example as hidden-hand items. Define seat numbers 1 to N in the setup.
The variation that was reviewed: Masterpiece: Private Sales: MONEY: All amounts are in thousands of dollars ($k). Bids and reserves must be whole multiples of 50.

SETUP:
- Seat players in a fixed circle. Each player starts with 1500 cash. Cash amounts are public.
- Each player receives 4 paintings with public names, unique across the game (for example 'P1-A' to 'P1-D').
- The engine secretly and randomly assigns that player's four paintings the values 0 (a forgery), 300, 600 and 1200, one value each. Every player therefore holds exactly the same total value of 2100.
- Each player is told privately the value of each of their own paintings.
- Who owns which painting is public. Painting values are private: a value is known only to players who have owned that painting.

ROUNDS: The game lasts 3 rounds per player (12 rounds with 4 players, 9 with 3, 15 with 5). The seller of round r is player number ((r-1) mod N)+1, so the role rotates clockwise. Each round:
1. ANNOUNCE: The engine names the seller. If the seller owns no paintings, nothing else happens this round; go to step 8.
2. LOT CHOICE: The player to the seller's left chooses one painting from the seller's current collection. The engine announces it as the lot.
3. TALK: Every player, seller included, writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. SEALED BIDS AND RESERVE: At the same moment:
   - Each non-seller submits a bid between 0 and their current cash.
   - The seller submits a secret reserve between 0 and their current cash.
5. RESOLVE: Let B be the highest non-seller bid. Ties go to the tied bidder nearest the seller going clockwise.
   - If B > reserve: the high bidder pays B to the seller, takes the painting, and is told its value privately. (A painting's value is now known to the seller and the buyer.)
   - If B <= reserve: the seller keeps the painting and pays B to the bank. That money leaves the game. If B is 0, the seller pays nothing.
6. ANNOUNCE: The engine publishes:
   - all bids,
   - the reserve,
   - whether the painting sold or was kept,
   - the money moved and the new cash totals.
   The painting's value is NOT published.
7. A painting bought earlier can be put up again later, whenever its new owner is the seller and their left neighbour chooses it.
8. END CHECK: After the last round, go to scoring.

SCORING: All painting values are revealed. Each player's score = cash + the total value of the paintings they own. Winner: The player with the highest score wins. If two or more players tie for the highest score, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Masterpiece is an art-auction game for 2 to 6 players. Each painting is public but has a private value card. Players move around a track whose spaces trigger bank auctions, private auctions of their own paintings, buys, sales and inheritances, and the winner has the most cash plus painting value at the end. The reviewed variation cut this to a rotating sealed-bid private sale: the left neighbour picks the lot, the seller sets a secret reserve, and a kept painting costs the seller the high bid, paid to the bank.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "Every player valued a painting at the same v, so there were no gains from trade. Keeping a painting cost the seller B, which made the seller's best reserve v/2. A bid B then wins only lots with v < 2B, and the buyer's expected gain is negative at every B (-50, -50, -50, -125, -475). 'Always bid 0' therefore never loses money. Rational play gives no trades and an all-way draw at 3600."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "The best play is never to bid, which ties. Against imperfect players, the result depends on who errs and on the random value of a lot chosen blind. Superior reasoning has no profitable action to exploit."
    },
    {
      "criterion": "headroom",
      "verdict": "bad",
      "evidence": "The game is solved by the passive equilibrium (bid 0, reserve about v/2), and no deviation improves on it. Nothing remains to learn beyond 'do not trade'."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Values are hidden, but the published reserve (about v/2) revealed each auctioned value. There was no opponent type to model, and a correct inference never led to a profitable action."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The score is cash plus painting values, all tracked by the engine, and the highest score wins. The previous version lacked a tie-break, so ties were common draws."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The original's board was already removed. Play is turn-based with sealed bids, simultaneous talk and 9 to 15 rounds. Painting storage was underspecified but buildable as hidden-hand items."
    }
  ],
  "problems": [
    "P1: There are no gains from trade. Every player values a painting at the same v, so any trade is zero-sum between two players and the passive 'bid 0' policy cannot lose.",
    "P2: The keep penalty (the seller pays the full high bid to the bank) pushes the seller's reserve to v/2. That makes every bid unprofitable in expectation, creating a pure lemons market.",
    "P3: Publishing the reserve reveals each auctioned painting's value to everyone, destroying the hidden information.",
    "P4: There is no hidden type, so there is nothing about opponents to infer or model.",
    "P5: There is no tie-break, so the rational outcome is an all-way draw.",
    "P6: Random value deals could hand some players better positions if any value advantage were reintroduced, so a fix must not create a lottery.",
    "P7: The storage of paintings, owners and values was underspecified for the 20-attribute limit."
  ],
  "changes": [
    {
      "what": "There are 4 public styles. Each player gets a secret collector theme, one distinct style per player. Every painting of your theme style is worth +400 extra to you at scoring.",
      "why": "A matching collector values a lot at v+400 while a non-matching seller values it at v. Mutually profitable trades now exist, and buyers who are not the matching collector still face a lemons market and should stay out. Inferring who collects what becomes the core skill.",
      "fixes": "P1, P4"
    },
    {
      "what": "A seller who keeps the painting pays only a flat fee of 50 to the bank, and only if the highest bid was at least 50.",
      "why": "The seller's honest reservation price becomes about v-50 instead of v/2. A matching buyer then has positive expected bids: against an unknown value, bidding 50 gives +87.5 in expectation and bidding 350 gives +100. Sellers in turn shade reserves upward to capture the collector's surplus. The small fee keeps stonewalling from being free.",
      "fixes": "P2"
    },
    {
      "what": "The reserve is never published. Only the bids, sold-or-kept, the money moved and cash totals are announced.",
      "why": "Values stay private to past owners. A 'kept despite a high bid' outcome is only a hint, open to interpretation.",
      "fixes": "P3"
    },
    {
      "what": "Each player holds one painting of each style. Values are dealt by a Latin square: each player holds one each of 0, 300, 600 and 1200, and each style has exactly one painting of each value.",
      "why": "Every player starts at exactly 1500 + 2100 + 400 = 4000, with one theme painting each, so the deal is no lottery. Owning your own painting of a style tells you which values the other three paintings of that style have, which gives a deduction to plan with.",
      "fixes": "P6, P4"
    },
    {
      "what": "The tie-break is most cash, then a draw. The game is fixed at 4 players.",
      "why": "This removes most draws. Four players also means a trade benefits both parties relative to the two bystanders, so trading beats passivity.",
      "fixes": "P5, P1"
    },
    {
      "what": "Paintings are stored as hidden-hand items with three fields: style, value and owner. Seats 1 to 4 are defined at setup.",
      "why": "This states exactly how the 16 paintings fit within the attribute limits.",
      "fixes": "P7"
    }
  ],
  "keeps": [
    "Paintings are public objects with private values, and a forgery is worth 0.",
    "Private auctions are rotated around the table, and the player to the seller's left chooses which painting goes up.",
    "The seller sets a secret reserve against sealed bids, and the buyer learns the value privately.",
    "Paintings can be resold, and the score is cash plus collection value.",
    "Starting cash of 1500 and the value set 0, 300, 600, 1200 are carried over."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Secret collector themes create real gains from trade and a hidden type to infer. With them, the lemons collapse becomes a bargaining-and-inference game within the limits."
  },
  "variation": {
    "name": "Masterpiece: Secret Collectors",
    "summary": "Four collectors each secretly prize one of four styles. They take turns selling paintings in sealed-bid private sales, and must infer who collects what, whether a lot is a forgery, and how much surplus to demand or concede.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "MONEY: All amounts are in thousands of dollars. Bids and reserves are whole multiples of 50.\n\nSETUP:\n1. Seat the players 1 to 4 in a fixed circle. The player 'to the left' of player p is player p+1, and player 4's left is player 1.\n2. Each player starts with 1500 cash. Cash is always public.\n3. There are 4 public styles: Red, Blue, Gold and Green.\n4. Each player receives 4 paintings, one of each style, with public names (for example 'P2-Gold'). Who owns which painting, and each painting's style, are always public.\n5. Secret themes: the engine randomly gives each player a different style as their collector theme. Each player is told only their own theme. Everyone knows that the four themes are all different.\n6. Painting values are dealt as follows.\n   - Start from the pattern value(player p, style s) = [0, 300, 600, 1200][(p + s) mod 4], with players and styles indexed 0 to 3.\n   - Then randomly shuffle which player is which row, which style is which column, and which value is which number.\n   - The result: every player holds exactly one painting each worth 0, 300, 600 and 1200, and every style has exactly one painting of each of those values.\n7. Each player is told privately the values of their own four paintings. A painting's value is known only to players who have owned it.\n\nROUNDS: The game has 12 rounds. The seller in round r is player ((r-1) mod 4) + 1, so each player sells 3 times. Each round:\n1. ANNOUNCE: The engine names the seller. If the seller owns no paintings, skip to step 9.\n2. LOT CHOICE: The player to the seller's left chooses one painting from the seller's current collection. The engine announces it, with its style, as the lot.\n3. TALK: Every player, seller included, writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.\n4. SEALED BIDS AND RESERVE: At the same moment, each non-seller submits a bid from 0 up to their current cash, and the seller submits a secret reserve from 0 to 2000.\n5. HIGH BID: Let B be the highest bid. A tie goes to the tied bidder nearest the seller going clockwise (seller's left first).\n6. RESOLVE:\n   - If B > reserve, the high bidder pays B to the seller, takes the painting, and is told its value privately.\n   - Otherwise the seller keeps the painting. If B is at least 50, the seller pays a fee of 50 to the bank, or all their cash if they have less than 50. Fee money leaves the game.\n7. ANNOUNCE: The engine publishes all bids, whether the lot was sold or kept, the money moved and the new cash totals. The reserve and the painting's value are NOT published.\n8. A painting that was bought can be chosen as a lot again later, when its new owner is the seller.\n9. END CHECK: After round 12, go to scoring.\n\nSCORING:\n1. All values and themes are revealed.\n2. Each player's score = cash + the total value of the paintings they own + 400 for each painting they own whose style is their own theme.",
    "objective": "The highest score wins. If several players tie for the highest score, the one among them with the most cash wins. If they are still tied, the game is a draw.",
    "expected_effect": "Every player starts at exactly 4000. Each lot has at most one collector who gains 400 from it, so for a non-matching buyer bidding is still a losing lemons bet. The matching collector can profit, but bidding reveals their theme. Sellers must guess who the collector is and set a hidden reserve above their honest floor (about v-50) to capture part of the 400. The left neighbour's lot choice is itself strategic: picking a lot of their own style hints at their theme, and picking a lot of the seller's own theme is effectively a block, since nobody else gains from it and it will likely be kept. Owning your own painting of a style tells you which values the other three paintings of that style can have, which sharpens bids. Simple policies lose. 'Always bid 0' never gains the bonus and falls behind players who trade profitably. 'Always bid all cash' pays up to 1500 for lots worth on average 525 plus 400 at most. 'Always reserve the maximum' forgoes surplus and pays fees. 'Always reserve 0' sells 1200-value paintings for 50. Talk passes both tests. Players disagree about prices and about who wins, since only one can. A buyer who believes a seller's claim that the lot is no forgery may overpay, and a seller who believes a bluffed 'I am not your collector' may undercharge."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 12
  }
}
```
````
