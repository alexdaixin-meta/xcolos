# 01 design

- time: 2026-10-28T05:14:40+00:00 (63.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 40931d736ad4ceac, reply sha256 3390a406e6a91b53

## Sent

````
Original game: Skull
Players in the original: 3 to 6

Original rules:
Each player has 3 roses and 1 skull as a hidden hand and a mat. Rounds: each player in turn must place one card face-down on their own stack if able. At any time on your turn instead of placing you may announce a bet: number of cards you claim you can flip showing only roses. Betting then goes around: raise or pass. Once all but one pass, the challenger resolves: first flip all their own placed cards, then flip others' top cards in any order, one by one. If they reveal exactly their bet in roses with no skull, they win the round and mark their mat; two marks wins the game. If they reveal a skull, they lose: the owner of that skull chooses one card at random from challenger's hand to discard permanently. A player with no cards left is eliminated. Last player standing also wins.
````

## Reply

````
```json
{
  "original_summary": "Skull is a 3–6 player bluffing game. Each player secretly stacks roses and a skull face-down, then players bid how many roses they can reveal. The highest bidder must flip that many cards without hitting a skull, starting with their own stack. Two successful challenges win, and each failure costs a random card.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. 'Always rose and bid high' gets caught by skulls. 'Always pass' never scores, while others collect marks or force it into challenges. 'Always skull' can never complete a challenge, because the challenger flips their own stack first. Seat order matters a little through who places first, but it rotates."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Reading who is likely holding a skull, sizing bids and choosing which stacks to flip are what decide the game. Luck enters only through the random discard after a failed challenge."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Bluffing depth is open-ended: feigning a skull, baiting a raise, catching the leader. Weak players still win challenges against careless tables."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "All placed cards are hidden, so every bid and flip is an inference about opponents' likely placements given their incentives and bidding."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Marks, eliminations and a failed or successful flip are all mechanical."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Several things exceed the step limits: interleaved place-or-bet turns, an open-ended raise/pass auction, multi-card stacks per player and a free-order flipping sequence. The game has no fixed length either."
    }
  ],
  "problems": [
    "Interleaved turns where each player may place another card or open bidding create an unbounded, branching turn structure the flat step list cannot express.",
    "The open raise/pass auction around the table takes an unbounded number of choice steps.",
    "Multi-card stacks per player, flipped top-down in any order, need many hidden attributes and long reveal sequences.",
    "There is no round cap, so a cautious table could stall indefinitely.",
    "If everyone passes or nobody can be forced to bid, nothing happens."
  ],
  "changes": [
    {
      "what": "Each hand, every player places exactly ONE card face-down, all at the same moment.",
      "why": "This collapses the interleaved place-or-bet loop into one simultaneous choice and keeps one hidden card per player.",
      "fixes": "Interleaved turns where each player may place another card or open bidding create an unbounded, branching turn structure the flat step list cannot express."
    },
    {
      "what": "Bidding becomes one sealed simultaneous bid from 0 (pass) up to the number of other active players. The highest bid challenges, and ties go to the tied player nearest the start player in seat order. The bid counts only OTHER players' cards, while the challenger's own card is still flipped first and fails them if it is a skull.",
      "why": "This keeps 'bid high to win the right, but risk more' in one step. Counting only others' cards stops 'play rose, bid 1' from being automatic, because every challenge must trust at least one opponent.",
      "fixes": "The open raise/pass auction around the table takes an unbounded number of choice steps."
    },
    {
      "what": "The challenger names exactly as many other active players as they bid. All named cards plus the challenger's own are revealed at once.",
      "why": "This keeps the core choice of whose card to trust while avoiding multi-card stacks and step-by-step flipping.",
      "fixes": "Multi-card stacks per player, flipped top-down in any order, need many hidden attributes and long reveal sequences."
    },
    {
      "what": "If every player bids 0, the start player must challenge with a bid of 1.",
      "why": "Every hand has a challenge, so passivity is not free.",
      "fixes": "If everyone passes or nobody can be forced to bid, nothing happens."
    },
    {
      "what": "Cap the game at 30 hands. Most marks wins, then most cards left; a remaining tie is a draw.",
      "why": "This bounds the length with an arithmetic tiebreak.",
      "fixes": "There is no round cap, so a cautious table could stall indefinitely."
    },
    {
      "what": "Add one simultaneous message per hand after placement and before bidding.",
      "why": "Bluffing about what you placed is the soul of Skull. Only one player can win, so claims conflict and must be read, not trusted.",
      "fixes": "The open raise/pass auction around the table takes an unbounded number of choice steps."
    }
  ],
  "keeps": [
    "A hand of 3 roses and 1 skull, placed face-down.",
    "Bidding a number of roses to reveal; the highest bidder must deliver.",
    "The challenger's own card is revealed first and counts against them if it is a skull.",
    "The challenger chooses whose cards to flip.",
    "Failure costs a card chosen at random from the challenger's hand, and the loss stays hidden.",
    "Two marks wins; losing all cards eliminates; last player standing wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The bluff-bid-flip core survives intact once placement and bidding are made single simultaneous steps."
  },
  "variation": {
    "name": "Sealed Skull",
    "summary": "Each hand, every player secretly plays a rose or their skull, talks, then seals a bid. The top bidder must reveal their own card plus that many chosen opponents' cards, all roses, to earn a mark. Two marks win.",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "rules": "SETUP: Each player starts with a private hand of 4 cards: 3 Roses and 1 Skull. Each player has 0 marks. Seat order is fixed, and the start player for hand 1 is seat 1. A player's number of cards is public. Whether a player still holds their Skull is private to that player.\n\nEACH HAND (at most 30 hands), among active (non-eliminated) players:\n1. PLACE: All active players at the same moment secretly choose one card type from their hand to place face-down: Rose (if they hold at least one) or Skull (if they still hold it).\n2. TALK: Every active player writes one short message at the same time without seeing the others. Then all messages are shown to everyone. Talk is not binding.\n3. BID: All active players at the same moment submit a whole-number bid from 0 to K, where K is the number of OTHER active players. A bid of 0 means pass.\n4. CHALLENGER: The highest bid wins the challenge. If several players tie for the highest bid, the challenger is the tied player who comes first in seat order starting from the start player. If every bid is 0, the start player becomes challenger with a bid of 1.\n5. TARGETS: The challenger names exactly B distinct other active players, where B is the winning bid.\n6. REVEAL: The challenger's own placed card and the placed cards of the named players are revealed to everyone. Unnamed players' cards stay hidden.\n7. RESOLVE: If every revealed card is a Rose, the challenge succeeds and the challenger gains 1 mark. If any revealed card is a Skull, including the challenger's own, the challenge fails. One card is then removed permanently from the challenger's hand, chosen uniformly at random from the cards they hold. Only the challenger learns whether it was a Rose or the Skull. Everyone sees that the challenger's card count dropped by 1.\n8. All placed cards return to their owners' hands.\n9. ELIMINATION: A player with 0 cards is eliminated.\n10. END CHECK: The game ends immediately if a player has 2 marks (that player wins), or if only one player remains active (that player wins).\n11. The start player passes to the next active player in seat order.\n\nAFTER HAND 30, if no one has won: the player with the most marks wins. If tied, the tied player with the most cards left wins. If still tied, the game is a draw.",
    "objective": "The first player to 2 marks wins, or the last active player. After 30 hands, the most marks wins, then the most cards; any remaining tie is a draw.",
    "expected_effect": "Each hand turns on a small poker-like inference: who would play their Skull here? The leader is the natural target for Skulls, so trailing players coordinate implicitly to catch them, and a player near 2 marks must bid carefully and pick the opponents least motivated to Skull them. Bidding high wins the right to challenge but forces trusting more opponents. Players disagree because only one can win. A player wants the challenger to flip their card when they hold a Skull, and to avoid it when they hold a Rose. Talk therefore consists of competing claims ('I'm on a rose, flip me') that may be bluffs. A player who simply follows another's claim flips a Skull, loses a card and may drift toward elimination. The random discard only matters after a failed challenge, so careful bidders control their exposure to luck. Hidden Skull loss adds inference about who can no longer catch anyone."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
