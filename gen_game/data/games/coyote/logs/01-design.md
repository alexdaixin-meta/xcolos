# 01 design

- time: 2026-10-27T08:36:20+00:00 (115.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 9845bad6c31efc1d, reply sha256 22851eb4a2427a7e

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.
````

## Reply

````
```json
{
  "original_summary": "Coyote is a bluffing and bidding game in the style of Indian poker. Each player sees every feather card except their own. Players take turns declaring ever-higher estimates of the total of all cards until someone calls 'Coyote'. The cards are then revealed: an over-declarer loses, otherwise the caller loses, and three losses eliminate a player.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies all lose. Always calling at once loses to any opener who declares low. Always raising by 1 is eventually caught over the true total. Always declaring very high is always caught. Every choice decides who takes the token. The only seat effect is who starts, and the starting rule ('the player who did not lose starts') ties the starting seat to past results."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The core reads (your hidden card from others' bids, the spread of the total) reward skill. But the blue specials add a lot of luck: 'add top of deck' and the reshuffle card can swing the total by up to 20 after all bidding is done, and nobody could have reasoned about it."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player can still survive by bidding the visible sum plus the average card. A strong player keeps improving by reading what each opponent's bid implies about their own card, and by choosing between raising and calling depending on who acts after them."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player's own card is hidden from them and visible to everyone else, so the opponents' declarations are the only evidence about it. Doing well means inferring your card from bids and predicting whether later players will call."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The total is a sum with mechanical modifiers, and the loser follows by comparing it with the last declaration. Some blue-card rules ('discard highest positive' when ties exist, chains of specials) are underspecified and would need clarifying."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Bidding goes round the table an unbounded number of times, which breaks the limit of 4 choice steps per round. The five chained blue-card rules (including drawing extra cards and forced reshuffles) add several random draws in one round and long rule chains. With elimination at 3 tokens and up to 6 players, the game has no fixed length."
    }
  ],
  "problems": [
    "P1: Bidding can circle the table any number of times, which exceeds the platform's limit of 4 choice steps per round.",
    "P2: The five blue special cards (extra draw from the deck, discard highest, flip highest to negative, double positives, forced reshuffle) add post-bidding luck and extra random draws. They also form a long, partly ambiguous rule chain.",
    "P3: Who starts depends on who lost, and elimination makes seats unequal: players do not hold the opening and closing positions equally often.",
    "P4: The length is open-ended (elimination at 3 tokens with up to 6 players), and the game gets thin once few players remain.",
    "P5: With up to 6 players, the number of hidden cards and turns per hand exceeds what fits in one round."
  ],
  "changes": [
    {
      "what": "Each hand is one round with exactly one lap of bidding. The opener declares, then each other player in clockwise order either raises or calls Coyote, once each. If nobody calls, the opener is automatically treated as calling Coyote on the final declaration.",
      "why": "This bounds a hand at 4 choices while keeping the declare-or-call tension. The last responder can still dump the risk on someone else by raising only when confident, which keeps the late-position decision meaningful.",
      "fixes": "P1"
    },
    {
      "what": "The blue specials are replaced by one special card, 'Max→0': if it is in play, the highest other card counts as 0.",
      "why": "This keeps Coyote's signature twist, which players can see and reason about because everyone else sees the card. It removes all post-bidding draws and reshuffles, so the outcome depends on reading, not on late luck.",
      "fixes": "P2"
    },
    {
      "what": "The game is a fixed 12 hands, and the opener rotates clockwise every hand, so each seat opens equally often (3 times with 4 players, 4 times with 3). Coyote tokens are counted and fewest tokens wins, instead of elimination.",
      "why": "Every player holds every position (opener, middle, last responder) equally often, so no seat has an edge. The length is fixed and short.",
      "fixes": "P3"
    },
    {
      "what": "Elimination is dropped and the game ends after hand 12.",
      "why": "This gives a bounded game length, and all players stay active and informative to the end.",
      "fixes": "P4"
    },
    {
      "what": "The player count is set to 3 or 4.",
      "why": "The bidding lap fits within 4 choices, and there are enough visible cards to give real inference.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Each player sees every card except their own (the bandana).",
    "Strictly rising declarations of the total of all cards in play.",
    "Calling Coyote: an over-declaration costs the declarer, a correct declaration costs the caller.",
    "Coyote tokens as the measure of losing.",
    "Negative cards and the 'Max→0' special that makes the total tricky.",
    "Reading your own card from what others are willing to declare."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (hidden own card, visible others, rising bids, a challenge) is strong inference and bluffing material. It only needs a bounded bidding lap, simpler specials and a symmetric fixed length to fit the platform."
  },
  "variation": {
    "name": "Coyote Lap",
    "summary": "A Coyote game for 3 or 4 players over 12 hands. Each player sees every card but their own and bids on the total in a single lap: declare, raise or call Coyote. Whoever is wrong takes a token, and fewest tokens after 12 hands wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "DECK (33 cards): one -10, two -5, three 0, four each of 1, 2, 3, 4 and 5, three 10, two 15, one 20, and one special card 'Max→0'.\n\nSETUP: Seat players in a fixed clockwise order. Each player starts with 0 Coyote tokens. The player in seat 1 opens hand 1. The game lasts exactly 12 hands.\n\nEACH HAND:\n1. Deal: shuffle the full 33-card deck and deal one card face down to each player.\n2. Bandana: each player is told privately the cards of all other players, but never their own card.\n3. Opening declaration: the opener declares a whole number from -30 to 60, a claim about the TRUE TOTAL of all cards in play this hand.\n4. Responses: each other player, one at a time in clockwise order from the opener, chooses one of two options:\n   (a) RAISE: declare a whole number strictly higher than the current declaration, at most 60. It becomes the current declaration, and this player becomes the current declarer.\n   (b) CALL COYOTE: challenge the current declaration. Bidding stops immediately, and later players do not act this hand.\n   Every declaration is announced to all players as it is made.\n5. Automatic call: if every responder raised, the opener is treated as having called Coyote on the final declaration.\n6. True total: add up the numbers on all cards in play. If the 'Max→0' card is in play, it counts as 0 itself, and the highest-valued other card in play also counts as 0. If several cards tie for highest, only one of them counts as 0. If the highest other card is negative, it still becomes 0.\n7. Resolution: if the true total is LESS than the current declaration, the current declarer takes 1 Coyote token. Otherwise the caller, or the opener in the case of an automatic call, takes 1 Coyote token.\n8. Reveal: all cards, the true total and the token taken are announced to everyone.\n9. Rotate: the next player clockwise opens the next hand.\n\nEND: After hand 12, the game ends.",
    "objective": "After 12 hands, the player with the fewest Coyote tokens wins. If two or more players tie for the fewest, the game is a draw.",
    "expected_effect": "Each hand turns on two inferences. The first is estimating your own unseen card from how high the others are willing to go, since they can see it. The second is predicting whether players later in the lap will call or raise. The opener must declare near the true total: too low and everyone raises safely, leaving the opener stuck with the automatic call; too high and the next player calls. Middle players weigh calling now against passing the risk on. The last responder can raise by a small step only when confident, which shifts the risk onto the opener. Every seat holds every position equally often, so no seat has an edge. Removing post-bidding draws means the outcome follows from reading the bids, not from the deck. Free talk is deliberately left out. The declarations already carry the signal. Spoken claims about another player's card would be pure cheap talk in a contest only one player can win, so they would be ignored or add noise without giving anyone a new decision."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
