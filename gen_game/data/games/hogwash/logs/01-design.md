# 01 design

- time: 2026-10-28T03:40:44+00:00 (51.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6769cb6abc24d296, reply sha256 e6f8fdc1446663a6

## Sent

````
Original game: Hogwash
Players in the original: 2 to 8

Original rules:
Deal the 13-rank deck evenly face down. The player left of dealer starts a central pile by playing 1-4 cards face down claiming them as 1s. Play goes clockwise, each turn the required rank increases by 1, wrapping from 13 to 1. The player must discard 1-4 cards face down claiming the required quantity and the required rank. If they lack that rank they must bluff with other cards. After any discard, any opponent may call Hogwash! to challenge the last play. Flip those cards: if they match the claim, the challenger takes the entire central pile into their hand; if they do not match, the bluffer takes the entire pile. First player to empty their hand wins.
````

## Reply

````
```json
{
  "original_summary": "Hogwash is the bluffing shedding game also known as Cheat or I Doubt It. Players take turns discarding 1-4 cards face down while claiming they are the next rank in sequence. Any opponent may challenge, and whoever is proved wrong takes the whole central pile. The first player to empty their hand wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every simple policy can lose. 'Never challenge' lets opponents dump bad cards freely. 'Always challenge' picks up the pile every time a play is honest, which is often when ranks have several copies. 'Always bluff the maximum' gets caught and takes the pile. 'Always play honestly' stalls on missing ranks. Seat order gives only a small edge to the first player, who sheds first."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading bluffs, counting cards and timing bluffs matter. With up to 8 players, a 52-card deck and free-for-all challenges, the deal and turn order add a lot of noise. Whoever happens to challenge first, or whoever happens to be dealt the needed ranks, can decide a game more than reasoning does."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player can still shed honest cards and win sometimes. A strong player can improve through card counting (holding 3 of a rank exposes a claim of 2), modelling each opponent's bluff rate, and planning which cards to keep for future required ranks."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, and claims are unverifiable unless challenged. Good play needs inference from one's own hand, from claim history and from opponent tendencies, plus planning around the known rank sequence."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Whether a claim is true is checked by comparing card ranks. The winner is the first player with an empty hand. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. However, 'any opponent may call at any moment' is a real-time race. A 52-card deck with 1-4 card plays and up to 8 hands exceeds the attribute budget. Games have no length cap and can run very long."
    }
  ],
  "problems": [
    "The challenge window is a real-time race ('any opponent may call'), which the turn-based engine cannot run.",
    "When several players want to challenge, the rules do not say who takes the pile.",
    "The full 13-rank deck, 1-4 card plays and up to 8 players create too much state for the attribute and step limits, and add noise that swamps skill.",
    "There is no length cap, so games can drag on far beyond a playable number of rounds.",
    "Turn order gives the first player a small head start in shedding."
  ],
  "changes": [
    {
      "what": "After each play, all other players choose Challenge or Pass in one simultaneous secret poll.",
      "why": "This replaces the real-time race with a turn-based step and makes every opponent decide independently.",
      "fixes": "The challenge window is a real-time race ('any opponent may call'), which the turn-based engine cannot run."
    },
    {
      "what": "If several players challenge, the challenger who sits soonest after the active player in clockwise order is the one who resolves the challenge.",
      "why": "This gives a deterministic, arithmetic tie-break. It also creates a positional stake: challenging is riskier when you sit next after the active player.",
      "fixes": "When several players want to challenge, the rules do not say who takes the pile."
    },
    {
      "what": "Use 3 or 4 players, a 24-card deck (ranks 1-6, four copies each), and plays of 1-3 cards.",
      "why": "This keeps state within limits. The small deck also makes card counting powerful (seeing 2 of a rank in your own hand says a lot), which shifts weight from luck to inference.",
      "fixes": "The full 13-rank deck, 1-4 card plays and up to 8 players create too much state for the attribute and step limits, and add noise that swamps skill."
    },
    {
      "what": "Cap the game at 36 turns. If no one has emptied their hand by then, the fewest cards wins, and equal fewest is a draw.",
      "why": "This bounds game length and gives an arithmetic fallback winner.",
      "fixes": "There is no length cap, so games can drag on far beyond a playable number of rounds."
    },
    {
      "what": "The last seat in turn order starts with one card fewer, which goes face down as the first card of the pile.",
      "why": "This offsets the first player's shedding head start and seeds the pile, so challenges matter from turn one.",
      "fixes": "Turn order gives the first player a small head start in shedding."
    }
  ],
  "keeps": [
    "Face-down discards with a claimed rank that rises in a fixed wrapping sequence.",
    "Forced bluffing when you lack the required rank.",
    "Challenge resolution: whoever is wrong takes the whole central pile.",
    "The first player to empty their hand wins.",
    "The bluffing and bluff-calling identity of Cheat / I Doubt It."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of hidden hands, unverifiable claims and costly challenges is excellent reasoning material. It only needs a turn-based challenge poll, a smaller deck and a length cap."
  },
  "variation": {
    "name": "Hogwash: Sealed Calls",
    "summary": "A compact Cheat for 3-4 players. On each turn the active player discards 1-3 cards face down, claiming they are the required rank. The other players then secretly and simultaneously decide whether to call Hogwash. Whoever is wrong takes the pile. The first player to an empty hand wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "SETUP\n- Deck: 24 cards, ranks 1 to 6, four copies of each.\n- Shuffle once at the start of the game; this is the only random event.\n- Seat order is Player 1, Player 2, Player 3 (and Player 4 if present). Clockwise means increasing seat number, wrapping from the last seat back to Player 1.\n- With 3 players: deal 8 cards each. Then the last seat (Player 3) places one of their own cards, chosen at random, face down as the first card of the central pile. They hold 7.\n- With 4 players: deal 6 cards each. Then Player 4 places one random card of their own face down to start the pile. They hold 5.\n- Hands are private. Everyone always knows how many cards each player holds and how many are in the pile.\n- The required rank starts at 1. Player 1 is the first active player.\n\nEACH TURN (one turn per round)\n1. Announce the turn number, the active player and the required rank.\n2. Play. The active player secretly chooses 1, 2 or 3 cards from their hand (never more than they hold). The cards go face down onto the top of the central pile. It is announced publicly: 'Player X plays N cards, claiming N cards of rank R', where R is the required rank. The claim is always exactly the required rank and exactly the number of cards played. The cards may be anything; playing other ranks is a bluff.\n3. Challenge poll. Every other player simultaneously and secretly chooses CHALLENGE or PASS.\n4. Resolution.\n   - If nobody challenged, the cards stay in the pile.\n   - If one or more challenged, the resolving challenger is the challenger who comes soonest clockwise after the active player.\n   - Reveal only the cards just played. If every one of them is rank R, the claim was true and the resolving challenger takes the entire central pile into their hand.\n   - If any revealed card is not rank R, the claim was a bluff and the active player takes the entire central pile into their hand.\n   - The pile is then empty, and the result (true or bluff, and who took how many cards) is announced. Other challengers suffer nothing.\n5. Win check. If any player now holds 0 cards, that player wins immediately. A player who emptied their hand with a bluff that was caught has taken the pile back, so does not win.\n6. Advance. The required rank increases by 1, wrapping from 6 to 1. The active player passes to the next seat clockwise.\n\nEND\n- The game ends when a player empties their hand, or after turn 36.\n- After turn 36, the player holding the fewest cards wins. If two or more tie for fewest, the game is a draw.",
    "objective": "The first player to hold 0 cards after a turn's resolution wins. If nobody has done so after 36 turns, the single player with the fewest cards wins. A tie for fewest is a draw.",
    "expected_effect": "Simultaneous sealed challenges force each opponent to judge alone whether a claim is credible. They use their own hand (if you hold 3 fives, a claim of 2 fives must be a lie), past claims and the bluffer's history. The rule that the challenger soonest after the active player resolves the challenge adds a positional bet: you can hope a neighbour challenges for you, but if you challenge and the claim is true, you may be the one who eats the pile. The 6-rank deck makes counting decisive and the rank cycle short, so players plan which cards to hold for their coming required ranks and when to spend a bluff. Every simple policy loses to adaptive play: never challenging invites free dumping, always challenging eats honest piles, and always bluffing gets caught. Talk is deliberately left out. The public claim is already the bluffing channel, and free chat would mostly add noise without creating a new decision."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 2,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 36
  }
}
```
````
