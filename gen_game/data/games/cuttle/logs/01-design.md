# 01 design

- time: 2026-10-27T17:25:15+00:00 (67.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 58611d933c86134c, reply sha256 40b061cce35ec940

## Sent

````
Original game: Cuttle
Players in the original: 2 to 2

Original rules:
Two players share a standard 52-card deck. Deal 6 cards to dealer and 5 to opponent, rest is draw pile; scrap pile is face-up discard showing top only. On your turn do exactly one: draw one card, or play one card from hand. Number cards A,2-10 can be point cards worth their value (A=1) placed on your side; first to 21+ points wins, but kings reduce requirement to 14/10/7/5 for 1-4 kings you control. A point card can also scuttle: play a higher rank, or equal rank with higher suit C<D<H<S, to discard both cards. Cards  A,2-7,9 can be one-offs discarded after use for effects like wipe points, destroy permanents, recover from scrap, force opponent discard 2, draw 2, play top of deck immediately, bounce a permanent. 8,J,Q,K are permanents staying on table: 8 forces opponent to reveal hand, J stacked on a point card steals it, Q protects your other points/permanents from single-target effects, K lowers win threshold. 2 can be played on opponent's turn to counter a one-off. If draw pile empty you may pass; three passes ends game with no winner.
````

## Reply

````
```json
{
  "original_summary": "Cuttle is a two-player combat card game played with a standard 52-card deck. Players race to 21 points (fewer if they hold Kings) by laying number cards as points, and they use scuttles, one-off effects and permanents (8, Jack, Queen, King) to destroy, steal or protect cards, all from a hidden hand.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always drawing never scores, and it loses to the first opponent who reaches 21. Always laying the highest point card loses to scuttles and Jacks. Always scuttling runs out of cards and never scores. The dealer's sixth card roughly offsets the opponent's first move, so seat advantage is small. The one degenerate case is the empty-deck pass rule: three passes end the game with no winner, so a player who is behind can stall for a no-result."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Expert Cuttle play is known to beat novices reliably. The skill lies in timing (drawing versus committing points), tracking which cards are gone, holding a 2 to counter, and choosing scuttle targets. The draw matters, but hand management outweighs it over a game."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "The game is not solved. Beginners score points easily but lose to tempo and to removal they did not see coming. Strong players keep improving through card counting and reading the opponent's hand."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and deck order are hidden. Players must infer whether the opponent holds a scuttler, a Jack or a counter from the cards already gone and from what the opponent declines to do, and must plan several turns of tempo."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "The point totals and threshold are arithmetic. However, the deck-out rule ends the game with no winner. The many interacting effects (Queen protection, Jack stacks, 2 counter chains, the 7's immediate play) also make exact resolution error-prone without a large rule engine."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Thirteen ranks carry distinct effects, including counter windows on the opponent's turn (interrupt chains), recursive one-offs (a 7 plays the top card, which can trigger another effect), Queen protection checks, Jack stacks that can be stolen back, and an 8 that reveals a hand. This far exceeds the limits of 20 steps and 4 choices per round, and the engine cannot run conditional sub-sequences or interrupts."
    }
  ],
  "problems": [
    "There are too many distinct card effects (about 10 one-offs and 4 permanents), many needing their own resolution blocks, which breaks the step and attribute limits.",
    "The 2-counter is an interrupt on the opponent's turn and can chain. The engine's flat, turn-based step list cannot run it.",
    "The 7 (play the top of the deck immediately) and the 3 (recover from scrap) trigger recursive effects that need conditional sub-sequences.",
    "Jack stacking (stealing a point card, then stealing it back) and Queen protection need per-card ownership layers and target-legality checks that are too complex to build reliably.",
    "The deck-out rule ends the game with no winner after three passes, so a losing player can stall for a non-result and the game may not be decided by arithmetic.",
    "The game has no fixed length, so a game could run beyond the platform's round limit."
  ],
  "changes": [
    {
      "what": "Cut the deck to 48 cards: point cards 1–10 in four colours (40), 4 Jacks and 4 Kings. Remove suits; ties in a scuttle go to the attacker (equal or higher rank scuttles).",
      "why": "This keeps the core of points, scuttle, steal and threshold while dropping most of the special-effect resolution blocks. Without suits, no suit-order lookup is needed.",
      "fixes": "There are too many distinct card effects (about 10 one-offs and 4 permanents), many needing their own resolution blocks, which breaks the step and attribute limits."
    },
    {
      "what": "Remove the 2-counter and every effect played on the opponent's turn. All actions happen on your own turn.",
      "why": "Interrupts cannot be run. The bluff element survives because Jacks and scuttlers in hand are still hidden threats.",
      "fixes": "The 2-counter is an interrupt on the opponent's turn and can chain. The engine's flat, turn-based step list cannot run it."
    },
    {
      "what": "Remove the 3, 7, 4, 5, 6, 8, 9 and Queen effects. Number cards are only points or scuttlers.",
      "why": "These effects need recursive or conditional blocks. The dual use of number cards (points versus removal) is the decision that matters most in Cuttle, and it remains.",
      "fixes": "The 7 (play the top of the deck immediately) and the 3 (recover from scrap) trigger recursive effects that need conditional sub-sequences."
    },
    {
      "what": "Make the Jack a one-off. It moves one opponent point card of rank 7 or less permanently to your point pile, and the Jack goes to the scrap. A stolen card can still be scuttled. The Jack cannot steal 8, 9 or 10.",
      "why": "This keeps stealing without stacks or ownership layers. The rank cap stops a single Jack swinging 20 points, which would let the draw dominate.",
      "fixes": "Jack stacking (stealing a point card, then stealing it back) and Queen protection need per-card ownership layers and target-legality checks that are too complex to build reliably."
    },
    {
      "what": "Fix the length at 30 rounds, where each round is one turn for each player. If the deck is empty, Draw becomes Pass. If nobody has reached their threshold after round 30, the player needing fewer points to reach it wins; equal shortfalls are a draw.",
      "why": "Every game ends and is decided by arithmetic. Stalling no longer secures a non-result, because the player who is behind on shortfall loses.",
      "fixes": "The deck-out rule ends the game with no winner after three passes, so a losing player can stall for a non-result and the game may not be decided by arithmetic."
    },
    {
      "what": "Set a hand limit of 8. If a Draw would take you to 9 cards, you may not draw and must play a card instead.",
      "why": "This bounds the game state and stops endless drawing to hoard answers, which keeps games short.",
      "fixes": "The game has no fixed length, so a game could run beyond the platform's round limit."
    }
  ],
  "keeps": [
    "A race to a point threshold, with Kings lowering it in the original steps: 21, 14, 10, 7, 5.",
    "Each turn you do exactly one thing: draw or play a card.",
    "Number cards have a dual use: lay them as points or spend them to scuttle an opponent's point card of equal or lower rank, with both cards going to the scrap.",
    "Stealing an opponent's point card with a Jack.",
    "Hidden hands, an uneven deal (6 cards to the second player, 5 to the first) and a public scrap pile that can be used for card counting.",
    "Tempo tension between building your hand and committing points."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Cuttle's core (dual-use cards, scuttling, King thresholds, hidden hands) fits within the limits once the interrupt and recursive effects are removed. The cut-down game still rewards card counting, reading the opponent's hand and tempo planning."
  },
  "variation": {
    "name": "Scuttle Race",
    "summary": "A two-player Cuttle variant. Players race to a point threshold that Kings lower, using number cards either as points or to scuttle the opponent's points, and Jacks to steal small point cards, all from hidden hands over at most 30 rounds.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 48 cards. There are 40 point cards: ranks 1 to 10, four copies of each, with no suits. There are 4 Jacks and 4 Kings. Shuffle the deck.\n\nSETUP: Randomly pick the First player. Deal 5 cards to the First player and 6 to the Second player. Hands are private. The rest of the deck is the draw pile, face down. The scrap pile is face up, and all of it is public. Each player has a public point pile and a public King count, both starting empty or zero.\n\nTHRESHOLD: A player's threshold depends on how many Kings they have played. 0 Kings: 21. 1 King: 14. 2 Kings: 10. 3 Kings: 7. 4 Kings: 5. A player's points are the sum of the ranks in their point pile. Their shortfall is threshold minus points, with a minimum of 0.\n\nROUND: Each round the First player takes a turn, then the Second player takes a turn. At the start of each turn the engine shows everyone the public state: both point piles, both point totals, both King counts and thresholds, the scrap pile, the size of the draw pile, and both hand sizes. Only the acting player sees their own hand.\n\nTURN: The acting player chooses exactly one action.\n(a) DRAW: Take the top card of the draw pile into your hand. This is not allowed if your hand already holds 8 cards or the draw pile is empty.\n(b) POINTS: Put one point card from your hand into your point pile.\n(c) SCUTTLE: Choose one point card from your hand and one card in the opponent's point pile whose rank is equal to or lower than it. Both cards go to the scrap pile.\n(d) JACK: Play a Jack from your hand and choose one card of rank 7 or less in the opponent's point pile. That card moves to your point pile, and the Jack goes to the scrap pile.\n(e) KING: Put a King from your hand on the table. Your King count rises by 1 and your threshold falls accordingly.\n(f) PASS: Allowed only if you cannot draw, either because the draw pile is empty or because you hold 8 cards. A player with 8 cards who holds a point card should play instead; passing is allowed but wastes the turn.\nAn illegal or unparseable choice counts as PASS.\n\nWIN CHECK: Immediately after every turn, if either player's points are at or above their threshold, that player wins at once. A steal can push the acting player over; only the acting player's action can change totals, so at most one player can cross on a turn.\n\nEND: The game stops after round 30. If nobody has won by then, the player with the smaller shortfall wins. Equal shortfalls are a draw.",
    "objective": "You win immediately if, after any turn, your point total (the sum of the ranks in your point pile) is at least your threshold (21, 14, 10, 7 or 5 for 0 to 4 Kings played). If nobody has done so after 30 rounds, the player with the smaller shortfall (threshold minus points, minimum 0) wins. Equal shortfalls are a draw.",
    "expected_effect": "Every simple policy can lose. Always-draw never scores, and it loses to anything that lays points. Always laying the highest card is beaten by an opponent who holds scuttlers and Jacks and strikes once a big card is exposed. Always-scuttle burns its hand and loses on shortfall or to a King rush. Always-King with no points cannot reach even 5. Good play means counting the public scrap to judge whether the opponent still holds high scuttlers or Jacks. It also means deciding when to commit points, since a small card of 7 or less invites a Jack and a big one invites a scuttle. Players must also time their Kings against their opponent's hand size and keep score with an eye on the round-30 shortfall tiebreak. Luck in the draw remains, but over a 30-round game with removal on both sides, decisions about tempo and targets outweigh it. The second player's extra card offsets the first player's tempo. The game has no talk, since it is a two-player game."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 2,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
