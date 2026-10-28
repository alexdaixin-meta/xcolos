# 01 design

- time: 2026-10-28T01:42:00+00:00 (98.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ce5f7027c72f7280, reply sha256 0b3822c7f9ef6a01

## Sent

````
Original game: Bastard Brag
Players in the original: 3 to 10

Original rules:
Deal 3 cards face down to each player and an extra 3-card hand to the table, two face down one face up. Ranking: prial (3-3-3 highest), running flush, run, flush, pair, high card, with 3-2-A high and suit tie-break spades>hearts>diamonds>clubs for lives game. Lives version: each player has 3 lives. Clockwise, on turn exchange one card with table (if you take face-up you must leave face-up, if face-down exchange is hidden) or swap whole hand for table hand turning one of yours face up. After first round you may knock to keep hand. After knock each other gets one final exchange. All show, worst hand loses a life, zero lives eliminated, last remains wins. Betting version: ante, two exchange rounds (first must exchange, second may pass), then Brag betting with raises until one remains or two-player pay-double-to-see.
````

## Reply

````
```json
{
  "original_summary": "Bastard Brag is a three-card Brag variant for 3 to 10 players. Players take turns swapping cards with a three-card table hand (two cards face down, one face up), or swap their whole hand, and anyone may knock to end the exchanging. In the lives version the worst hand at each showdown loses a life and the last player left wins; a betting version adds antes and Brag betting.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. Knocking at once with a weak hand gives every rival a final exchange while you cannot improve, so you are often the worst hand. Never knocking lets stronger hands build. Always taking the face-up card shows your hand to everyone. Elimination means no option is risk-free. Seat order matters a little: early seats see fewer exchanges before they can knock, and the last seat gets the final look."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The deal and the blind face-down exchanges add a lot of variance. A single showdown is close to a coin flip between average hands. The lives structure averages over several deals, but the full 52-card ranking with suit tie-breaks rewards card-counting memory more than strategic reasoning."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player can still survive by improving pairs. A strong player can keep improving: tracking which face-up cards each rival took or left, inferring hand strength from blind swaps and whole-hand swaps, and timing the knock relative to rivals' likely holdings."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the face-down table cards are hidden. Public actions (taking a known face-up card, leaving a card face up, swapping blind, swapping the whole hand, knocking) are signals to read, and bluffing a strong hand by knocking is possible."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Hand ranking is a fixed order, the worst hand loses a life, and the last survivor wins. All of it is mechanical. The betting version has a pay-to-see rule that is also arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only and turn-based. However, the 52-card ranking with flushes, running flushes, special 3-2-A and 3-3-3 rules and suit tie-breaks needs many evaluation steps. Up to 10 players exceeds the choice-step limit when a knock triggers final exchanges for everyone. The betting version adds a long raise loop. The game length is unbounded."
    }
  ],
  "problems": [
    "P1: The full 52-card hand ranking (suits, flushes, running flushes, suit tie-breaks) is too costly to evaluate arithmetically within the step limit.",
    "P2: With many players, a knock triggers more final-exchange choices in one round than the 4-choice-step limit allows.",
    "P3: Game length is unbounded: deals can go on with nobody knocking, and many players with 3 lives can exceed 40 rounds.",
    "P4: Luck of the deal is large, and knocking carries no extra risk, so an early knock with a middling hand is a cheap gamble rather than a read of the table.",
    "P5: Fixed seat order gives the same players the first and last looks every deal.",
    "P6: The betting version's open-ended raise loop and pay-to-see rules add many steps and mostly reward bankroll aggression."
  ],
  "changes": [
    {
      "what": "Replace the 52-card deck with 36 cards: four copies each of the values 1 to 9, no suits. Score hands arithmetically by class. Prial (three of a kind) = 300 + value, with 3-3-3 the top prial at 310. Run (three consecutive values) = 200 + top value, with 1-2-3 the top run at 210. Pair = 100 + 10 × pair value + odd card. High card = sum of the three cards.",
      "why": "It keeps Brag's ladder (prial over run over pair over high card) and its two signature quirks (3-3-3 and the 3-2-A-style top run). Each hand becomes one calculation, with no suit evaluation.",
      "fixes": "P1"
    },
    {
      "what": "Limit players to 3 or 4, and treat each round as one player's turn.",
      "why": "One knock then needs at most 1 + 3 = 4 choice steps in a round.",
      "fixes": "P2"
    },
    {
      "what": "Set lives to 3 each with 3 players and 2 each with 4 players. Force a showdown after two full laps of turns in a deal if nobody has knocked. Hard cap the game at 40 rounds, with a lives-based fallback winner.",
      "why": "The game becomes short and always finishes.",
      "fixes": "P3"
    },
    {
      "what": "Penalise the knocker: if the knocker has (or ties for) the worst hand, they lose 2 lives instead of 1. Also, no knocking until every active player has had one turn in the deal.",
      "why": "Knocking becomes a real read of the table: you must judge that your hand beats at least one rival after they each get a final exchange. A bluff-knock becomes a costly gamble.",
      "fixes": "P4"
    },
    {
      "what": "Rotate the starting player one seat clockwise every deal.",
      "why": "This spreads the first-look and last-look positions evenly.",
      "fixes": "P5"
    },
    {
      "what": "Drop the betting version and keep only the lives version.",
      "why": "The lives version already gives an arithmetic winner, and it fits the elimination support.",
      "fixes": "P6"
    },
    {
      "what": "Announce every action publicly in exact terms, without revealing hidden cards: which face-up card was taken and which card was left face up, a blind swap, a whole-hand swap and the card exposed, or a knock.",
      "why": "This turns the original's table-watching into a clean inference task. Players can track which known cards each rival holds and what a blind swap or whole-hand swap implies, and the luck of the deal is offset by information skill.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Three-card hands dealt face down plus a three-card table hand with two cards face down and one face up",
    "Exchange one card with the table: taking the face-up card means leaving your card face up; a face-down exchange is blind and hidden",
    "Swap the whole hand for the table hand, turning one of your old cards face up",
    "Knock to stop exchanging, after which each other player gets one final exchange",
    "Brag hand ladder (prial > run > pair > high card) with 3-3-3 the top prial and the lowest run as the top run",
    "Lives game: the worst hand loses a life, players at zero are eliminated, and the last survivor wins"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (hidden hands, a public face-up card, signalling through exchanges, and knock timing) is genuine inference under uncertainty. It fits the limits once the deck and ranking are simplified and the player count is capped."
  },
  "variation": {
    "name": "Knock Brag",
    "summary": "A 3-4 player lives game of three-card Brag on a suitless 36-card deck. Players swap cards with a partly face-up table hand, read each other's public exchanges, and knock when they judge they are not the worst. A knocker caught with the worst hand loses double.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "DECK: 36 cards, four copies each of the values 1, 2, 3, 4, 5, 6, 7, 8, 9. There are no suits.\n\nLIVES: With 3 players each starts with 3 lives. With 4 players each starts with 2 lives. A player at 0 lives is eliminated and takes no further part.\n\nHAND SCORE (computed for every hand at showdown):\n- Prial (three equal values): 300 + value, except 3-3-3 scores 310.\n- Run (three consecutive values, such as 4-5-6): 200 + highest value, except 1-2-3 scores 210.\n- Pair (exactly two equal): 100 + 10 × the pair value + the odd card.\n- High card (anything else): the sum of the three cards.\nHigher score is better.\n\nDEALING: At the start of each deal the deck is shuffled (one random draw). Each active player gets 3 cards face down; only they see their own cards. Three cards go to the table: table slot U face up (everyone sees it) and table slots D1 and D2 face down (nobody sees them). The first deal starts with seat 1. Each later deal starts with the next active player clockwise from the previous deal's starter.\n\nTURNS: Each round is one turn of the active player. Turns go clockwise among active players. On your turn choose exactly one action:\n(a) TAKE UP: swap one of your cards for the face-up card U. The card you give becomes the new face-up U. Announce: 'X took the face-up [value] and left a face-up [value]'.\n(b) BLIND: swap one of your cards for D1 or D2 (you choose which) without seeing it first. Your card goes face down into that slot. You now see the card you received. Announce: 'X made a blind swap'.\n(c) WHOLE HAND: take all three table cards into your hand; you now see all three. Your old three cards become the table hand. You choose which of them goes face up as U; the other two go face down as D1 and D2. Announce: 'X swapped the whole hand and exposed a [value]'.\n(d) KNOCK: keep your hand and make no exchange. You may knock only when every active player has had at least one turn in the current deal. Announce: 'X knocks'.\n\nAFTER A KNOCK: In the same round, each other active player in clockwise order from the knocker makes one final action of type (a), (b) or (c). They may not knock or pass. Each final action is announced as above. Then the showdown happens.\n\nFORCED SHOWDOWN: If nobody has knocked and every active player has taken 2 turns in the current deal, the showdown happens at once at the end of that round, with no further exchanges and no knocker.\n\nSHOWDOWN: All hands are revealed and scored. Every player with the lowest score (all tied players if several) loses 1 life. If the knocker is among them, the knocker loses 2 lives instead. Players reaching 0 lives are eliminated. If more than one player remains, a new deal begins with the next starter.\n\nEND: The game ends when only one player remains, or at the end of round 40, whichever comes first.",
    "objective": "If only one player remains, that player wins. If round 40 ends with more than one player remaining, the player with the most lives wins. Ties on lives go to the higher hand score at the most recent showdown among the tied players. If still tied, the game is a draw.",
    "expected_effect": "The suitless deck and arithmetic ladder keep Brag's feel while making each showdown a single calculation. Public announcements let players track which known cards rivals hold. A blind swap or whole-hand swap becomes a signal to weigh, for example 'they gave up a 2 face up after taking a whole hand, so they probably hold something better'. The double-life knock penalty turns knocking into the central reasoning decision. You knock only when you believe at least one rival will still be below you after their final exchange, and a bluff-knock to scare rivals into risky blind swaps is possible but costly. Simple policies all lose. Knocking at the first chance is punished by the double loss with a weak hand. Never knocking lets others choose the moment. Always taking the face-up card makes your hand readable. Rotating the starter and forcing a showdown after two laps remove seat advantages and keep games within 40 rounds. Talk is left out: knocking and exchanging are individual decisions with no joint plan to coordinate. A pre-turn message would only be unbinding cheap talk about hand strength, and the game already carries that signal more credibly through costly public actions. Talk would also cost steps the build cannot spare."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
