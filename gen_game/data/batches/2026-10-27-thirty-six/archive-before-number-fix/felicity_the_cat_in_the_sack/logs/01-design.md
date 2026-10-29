# 01 design

- time: 2026-10-27T16:38:15+00:00 (101.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ad99c1a437419956, reply sha256 ce2e6c65cd67f3f6

## Sent

````
Original game: Felicity The Cat In The Sack
Players in the original: 3 to 5

Original rules:
Each player has 10 cards (cats -8,-5,3,5,8,11,15, rabbit 0, large and small dog) and 15 mice money; one random card is discarded from each hand unseen. 9 rounds: each player places one hand card face down in a row forming the sack. Cards are revealed left to right during the auction. Start player bids mice ( >0 ) or passes; bidding proceeds clockwise, must raise to continue. When a player passes, he takes back his bids and collects the mice on the lowest mouse card still available (2,3,4,6) and is out for the round, then next sack card is revealed. Last remaining player pays his bid to the bank and takes the sack. If exactly one dog is in the final row, it removes a cat: large dog removes highest positive cat (or lowest negative if no positive), small dog removes most negative cat (or lowest positive if none). Dogs then discarded. Winner becomes start player. Next round refill mouse cards from bank if possible. After 9 rounds score won cats plus remaining mice money; rabbit 0, dogs 0. Most points wins, tie broken by cat points.
````

## Reply

````
```json
{
  "original_summary": "Felicity is a 3-5 player auction game. Each round every player secretly adds one card (cats worth -8 to 15, a rabbit, or one of two dogs) to a face-down sack. Players then bid mice in an ascending auction while sack cards are revealed one by one. Each player who drops out collects a growing consolation reward, and the last bidder pays and takes the sack.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Always passing earns only about 15 + 9×2 = 33 points, while players who buy good sacks cheaply gain 10 or more per sack. Always bidding high runs out of mice and gets stuck with sacks of negative cats that opponents dumped into them. The rising pass rewards (2, 3, 4, 6) make staying in tempting but risky. No seat has a lasting edge because the start seat passes to each auction winner."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The only luck is one unseen discarded card per hand. Everything else depends on which card you feed into the sack, how you read others' contributions from their bids, and when you drop out."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still collect pass rewards and the occasional sack. Strong players can keep improving: they track which cards each opponent has already played, time their dumps of negative cats, and bluff by bidding on their own bad cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Some sack cards stay face down until the end. Players must infer them from the remaining hands and the opponents' bidding behaviour, and plan their card contributions across all nine rounds."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Score is cat values plus mice, which is pure arithmetic. The dog removal rules are deterministic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The open-ended clockwise ascending auction, with a reveal after every pass, is a loop of unknown length. The engine's flat step list cannot express that. A limited supply of mouse cards with 'lowest still available' adds further bookkeeping."
    }
  ],
  "problems": [
    "The clockwise ascending auction has unbounded length and interleaves reveals with individual passes, which a flat, fixed step list cannot express.",
    "The mouse-card supply ('lowest available', refilled from a limited bank) is fiddly state tied to the order in which passes happen, and that order does not exist when players choose simultaneously.",
    "The original dog wording ('lowest negative', 'lowest positive') is ambiguous and must be made exact for arithmetic resolution.",
    "In a sealed adaptation, a large reward for finalists could make 'always stay in with the minimum raise' a dominant policy."
  ],
  "changes": [
    {
      "what": "Replace the open auction with exactly three simultaneous sealed bidding stages per round. Before each stage one more sack card is revealed. At each stage, every player still in either passes (bids 0) or bids at least the standing bid + 1.",
      "why": "This keeps the core idea (bid more as you see more, drop out at the right time) inside four choice steps per round with a fixed step list.",
      "fixes": "The clockwise ascending auction has unbounded length and interleaves reveals with individual passes, which a flat, fixed step list cannot express."
    },
    {
      "what": "Pay pass rewards by stage from an unlimited bank: 2 mice for passing at stage 1, 3 at stage 2, 4 at stage 3, and 5 for players still in at the end who do not win.",
      "why": "This keeps the rising incentive to stay in without tracking a mouse-card supply. Several simultaneous passers can each be paid.",
      "fixes": "The mouse-card supply ('lowest available', refilled from a limited bank) is fiddly state tied to the order in which passes happen, and that order does not exist when players choose simultaneously."
    },
    {
      "what": "Add a stuck rule: if every player still in passes at a stage, the leader from the previous stage takes the sack at the standing bid instead of collecting the reward. Keep the final reward for losing finalists modest (5), so minimum raising wins only sacks the others avoided.",
      "why": "Minimum raising becomes exposed to adverse selection: you get stuck with sacks of dumped negative cats. Staying in remains a real gamble.",
      "fixes": "In a sealed adaptation, a large reward for finalists could make 'always stay in with the minimum raise' a dominant policy."
    },
    {
      "what": "Define the dogs exactly. If exactly one dog is in the sack, the large dog removes the highest-valued cat and the small dog removes the lowest-valued cat. If both dogs are in the sack, neither has any effect.",
      "why": "The removal becomes unambiguous arithmetic.",
      "fixes": "The original dog wording ('lowest negative', 'lowest positive') is ambiguous and must be made exact for arithmetic resolution."
    }
  ],
  "keeps": [
    "The same 10-card hand per player (cats -8, -5, 3, 5, 8, 11, 15, rabbit 0, large dog, small dog), with one random card removed unseen.",
    "15 starting mice, 9 rounds, one secret card per player into the sack each round.",
    "Progressive revealing of sack cards during bidding, with some cards still hidden when bidding ends.",
    "Rising consolation rewards for dropping out later, and only the winner pays.",
    "The dog effects, the auction winner becoming start player, and scoring as cats plus mice with ties broken by cat points."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game already rewards hidden-information inference and bluffing. Only its open auction loop needs restructuring into fixed sealed stages to fit the engine."
  },
  "variation": {
    "name": "Cat in the Sack: Sealed Stages",
    "summary": "Each round all players secretly add one card to a sack. In three sealed bidding stages, one more sack card is revealed before each stage. Players who drop out earn growing mouse rewards, and the top bidder pays and takes the sack. Highest cats plus mice after 9 rounds wins.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP\n- Each player gets an identical hand of 10 cards:\n  - cats worth -8, -5, 3, 5, 8, 11 and 15;\n  - a rabbit (worth 0);\n  - a large dog;\n  - a small dog.\n- One random card is removed from each hand and set aside unseen by everyone. Each player then holds 9 cards, and their hand is private.\n- Each player starts with 15 mice, which are public, and 0 cat points, which are also public.\n- Seats are in a fixed order. A random player is the first start player.\n\nEACH ROUND (9 rounds; every player plays exactly one card per round)\n\n1. Fill the sack.\n   - All players at the same moment choose one card from their hand and place it face down. It leaves their hand.\n   - The sack is laid out in seat order beginning with the start player. Sack card 1 is the start player's card, sack card 2 belongs to the next player in seat order, and so on.\n   - Everyone knows which position holds whose card. Only the owner knows its face.\n\n2. Stage 1.\n   - Sack card 1 is revealed to all.\n   - The standing bid is 0.\n   - All players at the same moment write a whole number: 0 means pass; otherwise it is a bid.\n   - A bid must be at least the standing bid + 1 and no more than the player's current mice. An illegal number counts as a pass.\n\n3. Resolve the stage. These rules apply after every stage:\n   - Pass reward: each player who passed at this stage leaves the auction for the round and gains mice from the bank: 2 at stage 1, 3 at stage 2, 4 at stage 3.\n   - Exception (stuck leader): if every player who was still in passed at this stage, the leader from the previous stage takes the sack instead of collecting that pass reward, paying the standing bid. If this happens at stage 1, nobody takes the sack and it is discarded.\n   - New leader: otherwise, the standing bid becomes the highest bid made at this stage. The leader is the player who made it. If several made it, the leader is the first of them in seat order, counting from the player after the start player and with the start player counted last.\n   - Immediate win: if exactly one player is still in, that player wins the sack at their bid, and the remaining stages are skipped.\n\n4. Stage 2.\n   - Played only if two or more players are still in.\n   - Sack card 2 is revealed.\n   - The players still in at the same moment pass (0) or bid at least the standing bid + 1, up to their mice.\n   - Resolve as in step 3.\n\n5. Stage 3.\n   - Played only if two or more players are still in.\n   - Sack card 3 is revealed.\n   - The players still in at the same moment pass or bid, under the same rules.\n   - Resolve as in step 3.\n   - Then, if two or more players are still in, the leader wins the sack at the standing bid. Every other player still in gains 5 mice.\n\n6. Open the sack.\n   - All sack cards are revealed. With 4 or 5 players, cards 4 and 5 stay hidden until this point.\n   - Dog rule: if exactly one dog is in the sack, it removes one cat. The large dog removes the highest-valued cat. The small dog removes the lowest-valued cat. If no cat is present, nothing is removed. If both dogs are present, neither has any effect.\n   - All dogs are then discarded, as are any removed cats.\n\n7. Pay and score.\n   - The sack winner pays their winning bid in mice to the bank.\n   - The winner adds the total value of the cats remaining in the sack to their cat points. The rabbit is worth 0.\n   - The sack cards are then discarded.\n\n8. Next start player.\n   - The sack winner becomes the start player.\n   - If nobody took the sack, the start player passes to the next seat.\n\nEND\nAfter round 9, each player's score is cat points + mice.",
    "objective": "The player with the highest score (cat points + mice) wins. If several tie, the tied player with the most cat points wins. If still tied, the game is a draw among them.",
    "expected_effect": "The tension of the original stays intact. Players dump negative cats or dogs into sacks they hope rivals will buy, and bid on sacks holding their own high cat. They read early bids as signals of what the hidden cards are. They time their exit between the safe 2-mice pass and the 4–5 mice rewards for staying in. The stuck-leader rule and the hidden last cards punish mechanical minimum raising. Always passing (about 33 points) loses to anyone who buys a few good sacks, and all-in bidding bankrupts itself on poisoned sacks. Talk is deliberately left out. The sealed bids and contributions already carry the bluffing, a chat step would push choice steps past the limit, and cheap claims about one's own card would mostly be noise."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 9
  }
}
```
````
