# 01 design

- time: 2026-10-27T20:59:57+00:00 (72.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 cb31508abb86347b, reply sha256 fe931cdc08f32dff

## Sent

````
Original game: Big two
Players in the original: 2 to 4

Original rules:
A standard 52-card deck is shuffled and dealt equally: 13 cards each for four players, 17 for three. 2 is highest rank, then A-K-Q-J-10-9-8-7-6-5-4-3. Suits break ties: Spades > Hearts > Clubs > Diamonds. The player with the lowest club or diamond starts by playing any single, pair, triple, or five-card poker hand (straight, flush, full house, four-of-a-kind+single, straight flush). Clockwise, each player must play the same type and same count but higher rank, or pass. If you pass you can re-enter later in same battle. When all others pass, the pile is cleared and the last player to play leads any combination. First to discard all cards wins the round. Scoring for gambling counts cards left in losers hands with doubles for many cards left, holding twos, or losing on twos or bombs.
````

## Reply

````
```json
{
  "original_summary": "Big Two is a climbing and shedding card game for 2 to 4 players with a 52-card deck. Players beat the previous play with a higher combination of the same kind (single, pair, triple or five-card poker hand) or pass, and the first player to empty their hand wins the deal. Losers are penalised for the cards they still hold.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always passing never sheds a card. Always playing the lowest legal card breaks up pairs and runs and wastes the high cards needed to regain the lead. Always playing the highest card spends 2s early and loses control later. The leader of the first deal is fixed by the cards, but the rotating deal start in multi-deal play evens this out."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Hand-splitting, keeping control cards and card counting all matter, so a better player wins more often. A single deal is still heavily driven by the deal: a hand with four 2s and a straight flush usually wins whatever the opponents do. The original only reduces luck through informal gambling scores over many deals."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Beginners can always play a legal card and shed something. Experts improve through card counting, reading passes as weakness, deciding when to break combinations and timing the last bomb. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer what opponents hold from what has been played and from their passes, and must plan the order in which they shed their own hand over many tricks."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner of a deal is whoever empties their hand first, and penalties are counts of the cards left. Everything is arithmetic, and comparing plays is a ranking lookup."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. However, a 52-card deck, 13-card hands, 2 to 4 players and five-card poker hands (straights, flushes, full houses, straight flushes) make the legality checks long, and a deal can run far beyond 40 orbits once it is cut into steps. The gambling scoring is loosely specified ('doubles for many cards left')."
    }
  ],
  "problems": [
    "P1: Five-card poker hands need long legality and comparison checks (flush, full house, straight flush ordering) that exceed what can be built reliably.",
    "P2: A 52-card deck with 13 to 17 card hands makes each deal too long for a 40-round limit and makes the hidden state large.",
    "P3: A single deal is decided too much by who was dealt the 2s and the bombs, so luck swamps skill.",
    "P4: The scoring is vague ('doubles for many cards left, holding twos, losing on bombs'), so there is no exact arithmetic winner over several deals.",
    "P5: The first leader is the holder of the lowest card, which is random and gives a tempo edge in a one-deal game.",
    "P6: Comparing combinations through suit and rank names needs a lookup table that the engine lacks."
  ],
  "changes": [
    {
      "what": "Use a 30-card deck numbered 1 to 30. Card number = 3 × (rank − 1) + suit, with ranks 1 to 10 (rank 10 plays the role of the 2s) and suits 1 to 3. Every comparison is then a comparison of numbers.",
      "why": "Rank and suit order become plain arithmetic, so no lookup table is needed.",
      "fixes": "P6"
    },
    {
      "what": "Allow only singles, pairs, triples and three-card runs. A triple may also be played as a bomb on any single or pair.",
      "why": "This keeps the core tension of Big Two (whether to break a combination, when to bomb) with short legality checks.",
      "fixes": "P1"
    },
    {
      "what": "Play with exactly 3 players, 9 cards each and 3 cards left face-down unseen all deal.",
      "why": "Deals are short enough to fit three into 40 orbits. Card counting becomes reasoning under uncertainty rather than exact elimination.",
      "fixes": "P2"
    },
    {
      "what": "Play a match of 3 deals with an exact penalty per deal. The lowest total penalty wins.",
      "why": "Averaging over deals and penalising every card left rewards damage control with a weak hand, not only winning with a strong one.",
      "fixes": "P3, P4"
    },
    {
      "what": "The first lead of deal 1 goes to seat A, deal 2 to seat B and deal 3 to seat C, instead of to the holder of the lowest card.",
      "why": "Each seat gets the opening tempo exactly once.",
      "fixes": "P5"
    },
    {
      "what": "Add an exact extra penalty for 2s (rank 10) left in hand and double the penalty for a hand of 7 or more cards.",
      "why": "This turns the original's gambling flavour into exact arithmetic and punishes hoarding and passivity.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Hidden hands, with the aim of shedding all your cards first",
    "Climbing play: beat the current combination with the same kind but higher, or pass",
    "Passing does not lock you out of the trick; when everyone else passes, the last player to play clears the pile and leads anything",
    "The highest rank acts as the 2s and suits break ties",
    "Bombs that override smaller plays",
    "Losers penalised by cards left, with extra penalty for unplayed 2s and for big hands"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core climbing and shedding game, with its hidden hands and combination planning, fits once the deck and combinations are shrunk. A three-deal penalty match reduces luck."
  },
  "variation": {
    "name": "Little Two",
    "summary": "A 3-player, 30-card version of Big Two using singles, pairs, triples (which also act as bombs) and three-card runs. It is played as a match of 3 deals, and the lowest total penalty wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "CARDS. There are 30 cards numbered 1 to 30. A card's rank is (card + 2) divided by 3, rounded down, giving ranks 1 to 10. Its suit is card − 3 × (rank − 1), giving suits 1 to 3. A higher card number always beats a lower one. Rank 10 (cards 28, 29, 30) are called 'twos'.\n\nSEATS. The players sit as A, B and C. Turn order is always A, then B, then C, then A again.\n\nMATCH. The match has 3 deals and at most 40 orbits. An orbit is one turn for each seat in order.\n\nDEALING. At the start of each deal, shuffle all 30 cards. Deal 9 to each player, privately. Set the remaining 3 cards aside face-down; nobody sees them during the deal. Every player's card count is public at all times.\n\nCOMBINATIONS. There are four kinds:\n- Single: one card.\n- Pair: two cards of the same rank.\n- Triple: three cards of the same rank.\n- Run: three cards of three consecutive ranks, any suits. Ranks do not wrap around, so 9-10-1 is not a run.\nThe value of a combination is its highest card number.\n\nTHE PILE. The pile holds a current kind and a current value, or is empty.\n- When the pile is empty, the player whose turn it is must lead any combination. They may not pass.\n- When the pile is not empty, the player whose turn it is may pass, or may play a combination of the same kind with a higher value.\n- Bomb: a triple may be played on a single or a pair whatever its value. The pile's kind then becomes triple.\n- A triple on the pile can only be beaten by a higher triple.\n- A run can only be beaten by a higher run.\nPlayed cards are announced to everyone and removed from the game for the rest of the deal.\n\nPASSING AND CLEARING. A player who passes may play again the next time their turn comes in the same trick. The engine records who made the last play. If play comes back round to that player because both others passed since their play, the pile is cleared and that player must lead.\n\nILLEGAL PLAYS. An illegal or malformed play counts as a pass. If the player was required to lead, their lowest-numbered card is played as a single instead.\n\nSTARTING A DEAL. In deal 1, seat A leads first. In deal 2, seat B leads first. In deal 3, seat C leads first. Seats before the leader in the first orbit of a deal do not act in that orbit.\n\nEND OF A DEAL. A deal ends the moment a player plays their last card. That player wins the deal, and the rest of that orbit is skipped. The next deal begins at the start of the next orbit.\n\nPENALTIES. Each non-winner receives a penalty equal to the number of cards left in their hand, plus 1 for each two (rank 10) left in their hand. If they have 7 or more cards left, this penalty is doubled. The deal winner receives 0. Penalties are added to each player's public running total.\n\nEND OF THE MATCH. The match ends after the third deal ends, or at the end of orbit 40, whichever comes first. If orbit 40 ends during a deal, that deal is scored as if it had ended with no winner: every player receives a penalty under the rule above.",
    "objective": "The player with the lowest total penalty after the match ends wins. If two or three players tie for the lowest total, the match is a draw.",
    "expected_effect": "Players must plan how to split their 9 cards into combinations. They must decide when to spend twos and triples to take control, and must count cards to infer who holds the remaining twos, given that 3 cards are unseen. Passes reveal weakness, which invites inference about opponents' hands. Three deals with rotating leads, and penalties scaled by cards left, mean a bad hand can still be played well to limit damage, so skill shows across the match. Talk is left out. The interests are directly opposed with a single winner, so the only shared interest is stopping the current leader, and pre-play messages would mostly be unverifiable claims about hands that add words rather than decisions. The reasoning load already sits in card inference and sequencing."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 3,
    "attributes": 17,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
