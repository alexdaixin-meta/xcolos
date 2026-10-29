# 01 design

- time: 2026-10-28T02:31:52+00:00 (74.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 a9f1b9a640320aac, reply sha256 5adcbf49bf74f67b

## Sent

````
Original game: Brusquembille
Players in the original: 2 to 5

Original rules:
Played with 32-card piquet pack, 2-5 players. If 3 or 5 play, remove two Sevens so cards divide evenly. Each player antes to pot and receives 3 cards. Top stock card face-up under stock sets trump and is last card drawn. Eldest leads first trick; any card may be played, no need to follow suit. Highest trump wins trick, otherwise highest of led suit. Trick winner draws first from stock to refill to 3, others follow. Winner leads next. When stock empty, last three tricks require following suit, later rule adds winner of first trick may exchange trump in hand for turned-up trump. After all cards played, count points: Ace 11, Ten 10, King 4, Queen 3, Jack 2, rest 0, plus 1 for a pointless trick in later rules. Most points wins pot. Side-payments: winning a trick containing own Ace gains 2 chips from each opponent, losing own Ace costs 2 chips to each; Ten is 1 chip same way; adjusted for partnerships.
````

## Reply

````
```json
{
  "original_summary": "Brusquembille is a 17th-century French trick-taking game for 2 to 5 players, the ancestor of Briscola, played with a 32-card piquet pack. Players hold 3 cards and refill from a stock after each trick, with no duty to follow suit until the last three tricks, and they score card points (Ace 11, Ten 10, King 4, Queen 3, Jack 2) to win the pot, with side-payments for Aces and Tens.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. 'Always play your highest card' throws Aces and Tens into tricks the opponent captures with a trump. 'Always play your lowest' gives up every valuable lead. Seat order matters little, because the leader and the follower each have both advantages and drawbacks, and the lead passes to whoever wins each trick."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, ducking and timing your trumps clearly matter. But all players refill blind from one shared stock, so one player can draw most of the Aces, Tens and trumps. The total card points each player ever holds is pure luck, and over a single deal that swamps much of the skill."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still wins tricks and scores points. A strong one keeps improving: tracking which trumps and Aces remain, choosing when to sacrifice a zero card, and baiting the opponent into spending trumps."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the stock order are hidden. Good play means inferring the opponent's likely holdings from cards already played and planning trump use over several tricks."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The trick winner follows from a fixed rank and trump rule, and the result is a sum of fixed card values."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only with no board. But 3 to 5 players, removing Sevens, chip side-payments with partnership adjustments, a trump-exchange variant and optional later rules make it long and messy. A single shared stock that refills several hands also adds draw handling for every player."
    }
  ],
  "problems": [
    "P1: Shared blind stock: who draws the Aces, Tens and trumps is luck, and it can decide the game regardless of play.",
    "P2: Rule bloat: chip side-payments for Aces and Tens, partnership adjustments, the trump-exchange rule and the pointless-trick bonus duplicate what card points already measure and add many steps.",
    "P3: With 3 to 5 players the number of sequential choices and draws per trick grows, and kingmaking appears, without adding new reasoning.",
    "P4: Ties in total points are possible, and the original leaves them unresolved.",
    "P5: Card counts per player (removing Sevens for 3 or 5 players) and the 32-card shared pack are awkward for an engine that handles decks by list operations."
  ],
  "changes": [
    {
      "what": "Each player gets a private 16-card draw pile of identical composition: Ace, Ten, King and Seven of each of the four suits. The two piles are shuffled independently, and players refill only from their own pile.",
      "why": "Both players hold exactly the same cards over the whole game, 100 card points each, so luck affects only the order of arrival, not the quantity. Since a player knows the opponent's full 16-card set, counting cards becomes exact reasoning about which of the opponent's remaining cards are in hand now.",
      "fixes": "P1"
    },
    {
      "what": "Two players only.",
      "why": "Keeps each trick to 2 sequential choices, avoids kingmaking, and makes the mirrored-pile fairness clean.",
      "fixes": "P3"
    },
    {
      "what": "Remove chip side-payments, partnerships, the trump exchange and the pointless-trick point. Add 1 bonus point for winning the 16th trick.",
      "why": "Card points already reward capturing Aces and Tens. The last-trick point makes the total 201, which is odd, so a draw is impossible.",
      "fixes": "P2"
    },
    {
      "what": "Fix the tie rule: identical cards (same suit and rank, now possible) are won by the leader.",
      "why": "Resolves the new duplicate case and gives a small edge to leading, which offsets the follower's information advantage.",
      "fixes": "P4"
    },
    {
      "what": "Choose the trump suit and the first leader at random at setup, and shuffle the piles at setup. No random events happen during play.",
      "why": "All randomness happens once at the start, which fits the engine's deck handling.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Hands of 3 cards refilled after every trick, trick winner draws first",
    "Any card may be played with no need to follow suit, until the last three tricks, which require following suit",
    "A trump suit fixed for the game: the highest trump wins, otherwise the highest card of the led suit",
    "Piquet card points: Ace 11, Ten 10, King 4, Seven 0; rank order Ace > Ten > King > Seven",
    "The trick winner leads the next trick",
    "Most card points wins"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The trick-taking core needs counting, ducking and trump timing, which is real reasoning. Mirrored private piles remove the draw-luck that hurts it, and the game fits within the step limits."
  },
  "variation": {
    "name": "Mirror Brusquembille",
    "summary": "A two-player Brusquembille in which each player draws from a private pile holding exactly the same 16 cards in a different random order. Hands of 3, a fixed trump, no duty to follow suit until the end, and most card points wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. There are four suits (Spades, Hearts, Diamonds, Clubs) and four ranks. From highest to lowest the ranks are Ace (worth 11 points), Ten (10 points), King (4 points) and Seven (0 points). Each player owns a private 16-card pile containing exactly one Ace, Ten, King and Seven of every suit, worth 100 points in total. Both piles have the same composition, and each player is told it.\n\nSETUP. 1) Shuffle each player's pile separately; its order is hidden from both players. 2) Each player draws the top 3 cards of their own pile as a hand, seen only by its owner, leaving 13 cards in each pile. 3) Draw one suit at random as the trump suit and announce it to both. 4) Choose the first leader at random and announce it. Scores start at 0.\n\nEACH TRICK (16 tricks; the trick number counts 1 to 16):\n1. Each player privately sees their own hand. Both see the trump suit, both scores, the trick number, the cards in each pile, and every card played so far.\n2. The leader chooses one card from their hand and plays it face up. Any card may be played.\n3. The follower chooses one card from their hand and plays it face up. In tricks 1 to 13 any card may be played. In tricks 14, 15 and 16 the follower must play a card of the led suit if they hold one; otherwise any card.\n4. Decide the winner in this order:\n   (a) If exactly one card is a trump, that card wins.\n   (b) If both cards are the same suit (both trumps, or both of the led suit), the higher rank wins. If they are identical (same suit and rank), the leader wins.\n   (c) Otherwise (the cards are of different suits and neither is a trump), the leader wins.\n5. The winner adds the point values of both cards to their score. If this is trick 16, the winner also adds 1 bonus point.\n6. The winner becomes the leader of the next trick.\n7. In tricks 1 to 13, the winner draws the top card of their own pile, then the loser draws the top card of their own pile, so both again hold 3 cards. From trick 14 on the piles are empty and no cards are drawn.\n8. After trick 16 the game ends.\n\nThe total of all points is 201 (200 card points plus the 1-point bonus), so the scores can never be equal.",
    "objective": "After 16 tricks, the player with the higher score wins. Because 201 points are shared, a draw is impossible.",
    "expected_effect": "Both players hold the same 100 points of cards over the game, so the result depends on capturing and protecting points, not on drawing them. Each player knows exactly which of the opponent's 16 cards are still unplayed, so good play means narrowing down which 3 the opponent holds now. It also means saving trumps to capture the opponent's Aces and Tens, leading Sevens to probe, and holding high cards for the forced follow-suit tricks 14 to 16, when the remaining cards in each hand are fully known. Simple policies lose. 'Always highest' wastes trumps on Sevens and walks Aces into enemy trumps. 'Always lowest' lets the opponent safely cash Aces and Tens. Random play loses to counting. Shuffle order still matters a little, through when trumps arrive, but holdings are equal, so skill dominates."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 16
  }
}
```
````
