# 01 design

- time: 2026-10-28T06:00:05+00:00 (59.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b9f508cca101657a, reply sha256 38175baec1f67527

## Sent

````
Original game: Cockroach Poker
Players in the original: 2 to 6

Original rules:
Shuffle 64 cards (8 types x 8 copies) and deal face-down evenly. On your turn, slide one card from your hand face-down to another player and declare its creature (truthfully or falsely). The receiver may: 1) Accept - say 'true' or 'false' about your claim. If correct, you must take the card face-up in front of you; if wrong, receiver takes it. 2) Pass - peek secretly at the card, then slide it to a different player who hasn't seen it, either repeating or changing the claim. A card may be passed until all players have seen it; the last player must accept. Whoever ends up with the card starts the next round. In 2 players, remove 10 unseen cards and no passing. Lose if you collect four of the same creature in front of you or you must start a round with no cards in hand.
````

## Reply

````
{
  "original_summary": "Cockroach Poker is a bluffing card game. Players slide face-down cards to each other with a claimed creature. The receiver either calls the claim true or false or, after peeking, passes the card on with a new claim. Whoever judges wrongly, or whose claim is caught out, takes the card face-up. Collecting four of one creature, or running out of cards to send, loses.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. If a receiver always says 'true', senders bluff every time and the receiver collects cards. If a sender always tells the truth, receivers always say 'true' and the sender collects them. If a player always passes, they give away information and still end up holding cards. Always picking the same target lets that target predict and exploit you. The only built-in edge is that the first sender has a forced move, which matters little."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The deal decides only which cards you can send. The outcome comes from reading bluffs, choosing claims, and steering cards toward players who are close to losing. Card counting from the face-up piles also gives better players a real edge."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Mixing truth and lies, reasoning about which creatures are still in hand, and targeting the player nearest a losing set all reward deeper play. A weak player still gets about half their calls right by chance."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and the card in play is hidden. Every call means modelling the sender's incentive to lie and using the public face-up counts to judge how likely the claim is. Passing creates second-order bluffs."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card identities are tracked, and whether a call was right is a direct comparison. The loss conditions are counts."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. However, the open-ended pass chain (up to five passes with 6 players) needs a variable-length subsequence. 64 cards across 6 players is long. Only one loser is named, with no single winner. The 2-player mode with no passing loses the second-order bluffing."
    }
  ],
  "problems": [
    "The unbounded pass chain needs a variable number of choice steps per round. The engine cannot branch into repeating blocks.",
    "64 cards with 8 creatures and four-of-a-kind to lose makes games too long, with too much state for the step and attribute budgets.",
    "The game names only one loser. The engine must declare a winner or a draw, so the outcome among the survivors is undefined.",
    "The 2-player variant removes passing and plays almost like a pure guessing game. Wide player counts (2–6) make balancing hard."
  ],
  "changes": [
    {
      "what": "At most one pass per card. A receiver who passes peeks, then sends the card with a new claim to a player who is neither the original sender nor themselves. That final receiver must call true or false.",
      "why": "This keeps the peek-and-pass double bluff but fits into a flat list of 4 choice steps, using `when` conditions on the pass steps.",
      "fixes": "The unbounded pass chain needs a variable number of choice steps per round. The engine cannot branch into repeating blocks."
    },
    {
      "what": "Use 24 cards: 4 creatures (Roach, Rat, Fly, Toad), 6 copies each. Collecting three of one creature face-up loses.",
      "why": "Games last about 8–20 rounds and the state stays small. Card counting stays tractable but non-trivial.",
      "fixes": "64 cards with 8 creatures and four-of-a-kind to lose makes games too long, with too much state for the step and attribute budgets."
    },
    {
      "what": "When a player loses, the game ends immediately. Among the other players, the one with the fewest face-up cards wins. If several tie for fewest, the game is a draw.",
      "why": "The winner is decided by arithmetic. Players must avoid cards all game, not just avoid the losing set, which rewards consistent good calls throughout.",
      "fixes": "The game names only one loser. The engine must declare a winner or a draw, so the outcome among the survivors is undefined."
    },
    {
      "what": "Restrict play to 3–4 players and drop the 2-player mode.",
      "why": "With at least 3 players, passing is always possible and targeting has meaning. Fewer counts are easier to balance.",
      "fixes": "The 2-player variant removes passing and plays almost like a pure guessing game. Wide player counts (2–6) make balancing hard."
    }
  ],
  "keeps": [
    "Sliding a face-down card with a declared creature that may be a lie.",
    "The receiver's choice to call true or false, or to peek and pass with a new claim.",
    "The loser of the judgement takes the card face-up and becomes the next sender.",
    "Losing by collecting a set of one creature or by having no card to send."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core bluff-and-call loop is strong strategic material. It needs only a bounded pass, a smaller deck and an arithmetic winner rule to fit the engine."
  },
  "variation": {
    "name": "Roach Bluff",
    "summary": "This is a compact Cockroach Poker for 3–4 players. Players send face-down creature cards with claims that may be lies. Receivers call the claim or peek and pass it once. Wrong judges and exposed liars collect cards face-up. Three of one creature loses, and the cleanest survivor wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP: The deck has 24 cards: 6 Roach, 6 Rat, 6 Fly and 6 Toad. Shuffle it once and deal it all face-down. With 4 players each gets 6 cards; with 3 players each gets 8. Each player's hand is private. Every player has a face-up pile, which starts empty; all face-up piles are public. Seat 1 is the first sender.\n\nEACH ROUND:\n1. The engine announces every player's face-up counts per creature and every player's hand size.\n2. SEND: The sender privately picks one card from their hand. They declare a creature (Roach, Rat, Fly or Toad), which may be true or false. They also pick one other player as receiver. The card leaves the sender's hand and becomes the card in play. The claim and the receiver are announced to all; the card's identity is not.\n3. RESPOND: The receiver chooses TRUE, FALSE or PASS.\n   - TRUE or FALSE: Go to step 5.\n   - PASS: Go to step 4.\n4. PASS (only when the receiver chose PASS):\n   - The receiver privately sees the card and becomes the passer.\n   - The passer declares a creature, which may be true or false. They pick a new receiver who is neither the original sender nor the passer.\n   - The new claim and new receiver are announced.\n   - The final receiver must choose TRUE or FALSE; passing again is not allowed.\n5. RESOLVE: The claim being judged is the latest one; the claimer is whoever made it (the sender, or the passer if there was a pass).\n   - If the judge's call is correct (TRUE and the card matches the claim, or FALSE and it does not), the claimer takes the card face-up.\n   - Otherwise the judge takes the card face-up.\n   - The card's identity is revealed to everyone, and the player who took the card becomes the next sender.\n6. CHECK:\n   - If any player now has 3 face-up cards of one creature, that player loses and the game ends.\n   - Otherwise, if the next sender has no cards in hand, that player loses and the game ends.\n\nThe game cannot last more than 24 rounds. There is no table talk: the claims are the only communication.",
    "objective": "When the game ends, the player who triggered the end (three of one creature face-up, or no card to send) loses. Among all other players, the one with the fewest total face-up cards wins. If two or more of them tie for fewest, the game is a draw.",
    "expected_effect": "Players must mix truthful and false claims unpredictably. They count the public face-up piles and their own hand to judge how likely a claim is. They steer cards at whoever is nearest a losing set while watching their own total, because the winner is the cleanest survivor. The single pass adds a second layer: the passer knows the truth and can relay or twist it. A separate talk phase is left out because the claims already are the communication and adding messages would only lengthen rounds. Every simple policy loses to a player who exploits it: always-TRUE is bluffed, always-truthful is called, always-PASS hands opponents information and still has to make a claim that can be caught."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 24
  }
}
````
