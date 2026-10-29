# 01 design

- time: 2026-10-27T17:03:57+00:00 (89.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 81d7b944f8329f07, reply sha256 bc852ddb5351cf7f

## Sent

````
Original game: Jaipur
Players in the original: 2 to 2

Original rules:
Two players compete for Seals of Excellence. Setup 5 cards: 3 camel cards form the market center, plus 2 face-up goods from the deck; each player gets 5 cards, camels go to their herd. Goods tokens are sorted by type descending; bonus tokens are shuffled by size (3,4,5 cards). On your turn do one action: TAKE or SELL. Take options: take 1 goods card from market to hand; OR take all camels from market to your herd; OR exchange 2+ cards: take any number of goods from market then return same number of cards from hand and/or herd. Hand limit 7. Market refills to 5 from deck after taking. SELL: discard 1 type of goods from hand. For diamonds, gold, silver you must sell at least 2. Take that many top tokens of that type, plus one random bonus token if you sold 3+ cards. Round ends when 3 goods token piles are empty or deck runs out while refilling market. Most camels gets 5 rupee camel token. Sum tokens including hidden bonus values; highest total wins a Seal. First to 2 Seals wins.
````

## Reply

````
```json
{
  "original_summary": "Jaipur is a two-player trading card game. Players take goods and camels from a shared five-card market and sell sets of one goods type for tokens whose values fall as the pile is used up. Selling three or more cards at once earns a random bonus token. Highest rupee total wins a Seal, and two Seals win the match.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. 'Always sell immediately' gets no bulk bonuses and dumps cheap single cards. 'Always hoard' loses the high early tokens to the opponent. 'Always take camels' gives up goods. Seats are close to symmetric, and every take or sell changes what the opponent can do next."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skill matters: timing sales against falling token values, and denying the market. But luck is heavy. Every take refills the market from a shuffled deck, so one player may be handed three diamonds. Bonus tokens are random (a 5-card sale gives 8 to 10). The starting deal is random. Much of a single round's result depends on the deck."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Strong play keeps improving: tracking cards, setting up the market for the opponent, and timing camel majorities. A weak player still scores by selling sets."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and the deck is unknown. Players infer what the opponent holds from their takes and sales, guess when they will sell, and plan the race for the high tokens over several turns."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The result is a sum of token values plus the camel bonus. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "It is turn-based and text-only. But each turn can trigger several random refill draws (the limit is 1 per round). It has six goods types with separate token piles plus three bonus piles, which is far more than 20 attributes. The multi-card exchange is complex, and a best-of-three match triples the length."
    }
  ],
  "problems": [
    "Market refills draw up to several random cards per turn, which exceeds one random draw per round and makes the market a lottery.",
    "Random bonus tokens (different values for the same 3/4/5-card sale) add pure luck to the payout.",
    "Six goods types, each with an explicit token pile, plus three bonus piles need far more state than the 20-attribute limit.",
    "The open-ended exchange action (take any goods, return any mix of goods and camels) is hard to state and check as one choice.",
    "The best-of-three Seals structure triples the length without adding new decisions.",
    "If the market became fully public and deterministic, nothing would be hidden: hands would be fully inferable from public takes. A hidden element must therefore be kept deliberately."
  ],
  "changes": [
    {
      "what": "The market is restocked by exactly one card per round from a fixed, published 16-round schedule instead of random refills.",
      "why": "This keeps the shared-market race while removing refill luck. Players can plan around upcoming arrivals, such as the diamond due in round 5.",
      "fixes": "Market refills draw up to several random cards per turn, which exceeds one random draw per round and makes the market a lottery."
    },
    {
      "what": "The only random draw is one private card per round from a 20-card goods deck (5 Diamond, 7 Silver, 8 Cloth). It goes to that round's first player, and the first player alternates.",
      "why": "This keeps Jaipur's hidden hand: the opponent knows you drew but not what, and must infer it from your later behaviour. Draws are split evenly, 8 each, and the deck composition is public.",
      "fixes": "If the market became fully public and deterministic, nothing would be hidden: hands would be fully inferable from public takes. A hidden element must therefore be kept deliberately."
    },
    {
      "what": "Bulk bonuses are fixed: 3 cards earn +3, 4 cards earn +5, and 5 or more earn +8.",
      "why": "This keeps the incentive to wait for large sets, without random payouts.",
      "fixes": "Random bonus tokens (different values for the same 3/4/5-card sale) add pure luck to the payout."
    },
    {
      "what": "The goods are cut to three types (Diamond, Silver, Cloth). Each token pile becomes one price number: a sale of k cards pays k times the current price, then the price drops by k, to a minimum of 1.",
      "why": "This keeps the falling-token-value race in three numbers instead of dozens of tokens.",
      "fixes": "Six goods types, each with an explicit token pile, plus three bonus piles need far more state than the 20-attribute limit."
    },
    {
      "what": "The exchange is folded into TAKE. You take n cards of one goods type and return n minus 1 camels from your herd to the market.",
      "why": "This keeps camels as the currency that buys several market cards at once, and gives a one-line, checkable action.",
      "fixes": "The open-ended exchange action (take any goods, return any mix of goods and camels) is hard to state and check as one choice."
    },
    {
      "what": "The match is a single game of 16 rounds (32 turns), and the highest total wins.",
      "why": "This gives one complete trading game at a playable length.",
      "fixes": "The best-of-three Seals structure triples the length without adding new decisions."
    }
  ],
  "keeps": [
    "A two-player race over a shared market of goods and camels.",
    "One action per turn: take goods, take all camels, or sell one goods type.",
    "Falling sale values, so the first seller of a type earns more.",
    "Bulk-sale bonuses for 3, 4 and 5 or more cards, creating the sell-now-or-wait tension.",
    "Diamonds and Silver must be sold at least two at a time.",
    "A 7-card hand limit, and camels that do not count toward it.",
    "Camels as currency for taking several cards, with a +5 bonus for the camel majority.",
    "Hidden hands inferred from the opponent's behaviour."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Jaipur fits the limits once refills, bonus tokens and token piles become fixed numbers: a timing race on falling prices, market denial, and a hidden hand. One private draw per round keeps the hidden information."
  },
  "variation": {
    "name": "Jaipur Bazaar",
    "summary": "A two-player, 16-round trading race. Players take goods and camels from a shared market restocked on a public schedule, and sell sets of Diamond, Silver or Cloth at prices that fall with every card sold. Each player also receives private draws that the opponent must infer.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS AND STATE\n- There are three goods types (Diamond, Silver, Cloth) and camels.\n- Each player has a hidden hand, recorded as counts of Diamond, Silver and Cloth, a public camel herd, and a public score.\n- The market is public and holds counts of Diamond, Silver, Cloth and Camel.\n- Each goods type has a public price. The starting prices are Diamond 7, Silver 5, Cloth 3.\n- A private deck of 20 goods cards is shuffled once at the start: 5 Diamond, 7 Silver, 8 Cloth. Its composition is public knowledge.\n\nSETUP\n- The market starts with 2 Camel, 1 Silver and 1 Cloth.\n- Each player starts with 1 Silver and 1 Cloth in hand, 1 camel in herd, and score 0.\n- Player A is the first player in odd rounds. Player B is the first player in even rounds.\n\nEACH ROUND (16 rounds)\n1. Restock: add one card to the market according to the public schedule.\n   - Round 1 Cloth, 2 Camel, 3 Silver, 4 Cloth, 5 Diamond, 6 Camel, 7 Cloth, 8 Silver.\n   - Round 9 Camel, 10 Cloth, 11 Diamond, 12 Silver, 13 Camel, 14 Cloth, 15 Silver, 16 Diamond.\n2. Private draw: the round's first player draws the top deck card into their hand. Only they see it. Both players are told that a draw happened.\n   - If the hand already holds 7 goods, the drawn card is discarded, and only the drawing player learns its type.\n3. The first player takes one turn, which is announced publicly.\n4. The second player takes one turn, which is announced publicly.\n\nA TURN: choose exactly one action.\n- TAKE <good> <n>: take n cards (n at least 1) of one goods type from the market into your hand. Three conditions apply:\n  - the market must hold at least n of that type;\n  - you must return n minus 1 camels from your herd to the market, so you must own at least n minus 1 camels;\n  - your hand must hold at most 7 goods afterwards.\n- CAMELS: take all camels from the market into your herd. The market must hold at least 1 camel.\n- SELL <good> <n>: discard n cards of one goods type from your hand.\n  - Diamond and Silver require n of at least 2. Cloth requires n of at least 1.\n  - You score n times that good's current price.\n  - If n is 3 you also score +3. If n is 4 you also score +5. If n is 5 or more you also score +8.\n  - Then that good's price drops by n, but never below 1.\n- An illegal or missing choice counts as a pass: nothing happens.\n\nThe actions announced publicly are the action type, the good and n. The opponent can therefore track your takes and sales, but not your private draws.\n\nEND\n- After round 16, the player with strictly more camels in their herd scores +5. If camels are tied, nobody gets the bonus.\n- Cards still in hand score nothing.",
    "objective": "After the camel bonus, the player with the higher score wins. Equal scores are a draw.",
    "expected_effect": "Players face Jaipur's timing dilemma. Selling early captures the high price but forfeits bulk bonuses. Waiting risks the opponent selling first and dropping the price. Because selling k cards drops the price by k, a large Diamond or Silver sale sharply devalues the opponent's holdings, so guessing what they hold matters. Their private draws (8 each, from a known 5/7/8 deck) and their takes are the evidence. The public restock schedule rewards planning: hoard camels to buy the round-5 and round-11 diamonds in bulk, or take a card just to deny it. Thoughtless policies lose to a planner. Always-sell-at-once misses bonuses and sells Cloth at low prices. Always-take never scores. Always-camels secures +5 but little else. Random draws are split evenly and only shape information and options; skilled play decides the winner. Talk is omitted: with two strictly opposed players it adds nothing that the public actions do not."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 2,
    "attributes": 19,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 16
  }
}
```
````
