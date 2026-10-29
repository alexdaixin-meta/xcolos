# 03 design

- time: 2026-10-28T02:33:59+00:00 (45.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6b9dcf5145b93d85, reply sha256 e4b37b43acefde9e

## Sent

````
Original game: Brusquembille
Players in the original: 2 to 5

Original rules:
Played with 32-card piquet pack, 2-5 players. If 3 or 5 play, remove two Sevens so cards divide evenly. Each player antes to pot and receives 3 cards. Top stock card face-up under stock sets trump and is last card drawn. Eldest leads first trick; any card may be played, no need to follow suit. Highest trump wins trick, otherwise highest of led suit. Trick winner draws first from stock to refill to 3, others follow. Winner leads next. When stock empty, last three tricks require following suit, later rule adds winner of first trick may exchange trump in hand for turned-up trump. After all cards played, count points: Ace 11, Ten 10, King 4, Queen 3, Jack 2, rest 0, plus 1 for a pointless trick in later rules. Most points wins pot. Side-payments: winning a trick containing own Ace gains 2 chips from each opponent, losing own Ace costs 2 chips to each; Ten is 1 chip same way; adjusted for partnerships.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Limits: steps 12 (max 20), choices 2 (max 4), attributes 11 (max 20), rounds 16 (max 40). Random draws per round are 0, since the shuffles, trump and leader are set at setup. Two players, so no talk step is needed. The game is finite and scored by arithmetic. It needs no board, clock or trading. Follow-suit in tricks 14-16 is a simple validity check.

Problem: step 1 says both players see 'the cards in each pile'. Read literally, the unordered contents of the opponent's remaining pile are shown. The opponent's hand is then exactly composition minus cards played minus pile contents. That contradicts setup step 2 ('hand seen only by its owner'): the hidden hand is illusory. If only pile sizes were meant, the rule should say so.

A related ambiguity is the hidden_elements count. It covers 2 hands plus 2 pile orders that are hidden from both players. The designer states 2, and it is unclear whether pile orders count. An engine implementer and a playing model cannot tell which information is actually public. That is a rules-completeness defect.
- change: Rewrite step 1 to say both players see only the NUMBER of cards left in each pile (and the fixed starting composition), not the cards themselves, so that each hand is genuinely private; or, if full pile contents are intended, remove the claim that hands are hidden and state that the game is open-information apart from draw order.
- change: State hidden_elements explicitly: the two hands, plus the pile orders hidden from both (implemented as setup shuffles), so the count is correct for the engine.
The variation that was reviewed: Mirror Brusquembille: CARDS. There are four suits (Spades, Hearts, Diamonds, Clubs) and four ranks. From highest to lowest the ranks are Ace (worth 11 points), Ten (10 points), King (4 points) and Seven (0 points). Each player owns a private 16-card pile containing exactly one Ace, Ten, King and Seven of every suit, worth 100 points in total. Both piles have the same composition, and each player is told it.

SETUP. 1) Shuffle each player's pile separately; its order is hidden from both players. 2) Each player draws the top 3 cards of their own pile as a hand, seen only by its owner, leaving 13 cards in each pile. 3) Draw one suit at random as the trump suit and announce it to both. 4) Choose the first leader at random and announce it. Scores start at 0.

EACH TRICK (16 tricks; the trick number counts 1 to 16):
1. Each player privately sees their own hand. Both see the trump suit, both scores, the trick number, the cards in each pile, and every card played so far.
2. The leader chooses one card from their hand and plays it face up. Any card may be played.
3. The follower chooses one card from their hand and plays it face up. In tricks 1 to 13 any card may be played. In tricks 14, 15 and 16 the follower must play a card of the led suit if they hold one; otherwise any card.
4. Decide the winner in this order:
   (a) If exactly one card is a trump, that card wins.
   (b) If both cards are the same suit (both trumps, or both of the led suit), the higher rank wins. If they are identical (same suit and rank), the leader wins.
   (c) Otherwise (the cards are of different suits and neither is a trump), the leader wins.
5. The winner adds the point values of both cards to their score. If this is trick 16, the winner also adds 1 bonus point.
6. The winner becomes the leader of the next trick.
7. In tricks 1 to 13, the winner draws the top card of their own pile, then the loser draws the top card of their own pile, so both again hold 3 cards. From trick 14 on the piles are empty and no cards are drawn.
8. After trick 16 the game ends.

The total of all points is 201 (200 card points plus the 1-point bonus), so the scores can never be equal. Winner: After 16 tricks, the player with the higher score wins. Because 201 points are shared, a draw is impossible.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Brusquembille is a French trick-taking game for 2 to 5 players using a 32-card piquet pack. Players hold 3 cards each and refill from a stock after every trick. Trumps beat everything and suit need not be followed until the last three tricks. Card points (Ace 11, Ten 10, King 4, Queen 3, Jack 2) decide who takes the pot, and side-payments are made for capturing or losing Aces and Tens.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. 'Always play your highest card' throws Aces and Tens into tricks the opponent can trump. 'Always play your lowest card' hands over every contested trick. A random first leader removes any fixed seat edge. The original's side-payments and pot do not change this, and the mirror variation keeps it, since every policy can lose against an opponent who adapts."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, which cards you draw from a single shared stock largely decides the game: a player who draws many trumps or Aces wins regardless of play. The mirror variation gives both players identical 100-point piles, which removes the gap in total card strength. Only the order of draws stays random, and timing (when to spend trumps, when to sacrifice) can largely overcome it."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Counting cards, deciding when to trump, deciding when to discard a Seven, and planning the follow-suit endgame of the last three tricks all reward deeper play. A weak player still wins tricks and points from the cards they are dealt."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Because each player's remaining cards (hand plus pile) are known as a set, a player can infer which cards the opponent may be holding and how likely each is. Tricks 14 to 16 become a perfect-information endgame that rewards planning ahead. This only works if the pile contents are NOT shown, which was the defect in the previous version."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card points are summed by arithmetic. The previous variation's 201-point total with a 1-point last-trick bonus makes a tie impossible. The original's chip side-payments and partnerships are dropped, because the platform only records who wins."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original has 2 to 5 players, a shared stock, partnership adjustments, chip side-payments and a trump-exchange rule, which is heavy for the engine. The previous variation fit the limits (12 steps, 2 choices, 16 rounds) but failed playability. Its rules said both players see 'the cards in each pile', which reveals the opponent's hand, and it left the hidden-element count unclear."
    }
  ],
  "problems": [
    "P1: Previous variation, step 1 says both players see 'the cards in each pile'. Taken literally, the opponent's hand equals the composition minus cards played minus pile contents, so the 'private' hand is not private and the inference element disappears.",
    "P2: The previous variation left the hidden elements unclear. It stated 2, but there are two private hands plus pile orders hidden from both players, so an implementer could not tell what is public.",
    "P3: Original: drawing from one shared stock lets the luck of the draw decide the total card strength each player receives, so luck swamps skill.",
    "P4: Original: chip side-payments, the pot, partnerships and 3 to 5 player variants cannot be rewarded by a platform that only decides a winner, and they add steps without adding reasoning.",
    "P5: Original: card points can tie, which leaves the winner undefined."
  ],
  "changes": [
    {
      "what": "Step 1 now says both players see only the NUMBER of cards left in each pile (always equal), the fixed starting composition, and every card played so far. They never see the cards in either pile. A sentence spells out what can and cannot be inferred.",
      "why": "Hands become genuinely private. Each player knows the opponent's remaining cards as a set but not which of them are in hand, and that gap is the inference the game rewards.",
      "fixes": "P1"
    },
    {
      "what": "A 'Hidden information' section lists exactly three hidden elements: Player 1's hand (seen by its owner only), Player 2's hand (seen by its owner only), and the order of both piles (hidden from both players, fixed by setup shuffles). It also lists everything that is public.",
      "why": "The engine and the playing models can then tell precisely what is public and what is private, and the reported count is correct.",
      "fixes": "P2"
    },
    {
      "what": "Kept from the previous variation: each player has an identical private 16-card pile (one Ace, Ten, King and Seven of each suit, worth 100 points).",
      "why": "Both players get equal total card strength. Only the draw order is random, and timing can overcome it.",
      "fixes": "P3"
    },
    {
      "what": "Kept: two players only, no chips, pot, side-payments or trump exchange, and the winner is the higher point total.",
      "why": "This fits what the platform can decide and removes steps that add no reasoning.",
      "fixes": "P4"
    },
    {
      "what": "Kept: Queens and Jacks removed, and a 1-point bonus for the last trick, giving 201 points in total.",
      "why": "An odd total makes a draw impossible.",
      "fixes": "P5"
    }
  ],
  "keeps": [
    "Hands of 3 cards refilled after each trick, with the trick winner drawing first",
    "No obligation to follow suit until the last three tricks, which then require following suit",
    "A trump suit fixed at the start; the highest trump wins, otherwise the highest card of the led suit",
    "Card values Ace 11, Ten 10, King 4, with the rank order Ace above Ten above King",
    "A bonus point for winning the last trick",
    "Most card points wins"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation's only playability defect was ambiguous visibility and an unclear hidden-element count. Both are rules-text fixes, and the game stays within all limits with real hidden-hand inference and endgame planning."
  },
  "variation": {
    "name": "Mirror Brusquembille",
    "summary": "A two-player trick-taking game. Each player draws 3-card hands from their own private, identically composed 16-card pile. Trumps beat everything, suit need not be followed until the last three tricks, and the higher card-point total wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. There are four suits (Spades, Hearts, Diamonds, Clubs) and four ranks. From highest to lowest the ranks are Ace (11 points), Ten (10 points), King (4 points) and Seven (0 points). Each player owns a private 16-card pile containing exactly one Ace, Ten, King and Seven of every suit, worth 100 points. Both piles have this same composition, and both players are told it.\n\nHIDDEN INFORMATION. There are exactly three hidden elements.\n(1) Player 1's hand: seen only by Player 1.\n(2) Player 2's hand: seen only by Player 2.\n(3) The order of the cards in both piles: hidden from BOTH players, fixed by the setup shuffles.\nEverything else is public: the trump suit, the leader, the trick number, both scores, the NUMBER of cards left in each pile, and every card played face up so far. No player ever sees the cards in either pile. Because the starting composition is known, each player can work out which cards the opponent still has in hand and pile combined, but not which of them are in hand.\n\nSETUP.\n1) Shuffle each player's pile separately.\n2) Each player takes the top 3 cards of their own pile as their hand, leaving 13 cards in each pile.\n3) Draw one suit at random as the trump suit and announce it.\n4) Choose the first leader at random and announce it.\n5) Both scores start at 0.\n\nEACH TRICK (16 tricks, numbered 1 to 16):\n1. Each player sees their own hand. Both players see the trump suit, both scores, the trick number, the number of cards left in each pile (13 minus the number of tricks already completed in tricks 1 to 13, then 0), and every card played so far. Neither sees the cards inside any pile.\n2. The leader chooses one card from their hand and plays it face up. Any card may be played.\n3. The follower chooses one card from their hand and plays it face up. In tricks 1 to 13 any card may be played. In tricks 14, 15 and 16 the follower must play a card of the led suit if they hold one; otherwise any card.\n4. Decide the winner in this order:\n(a) If exactly one card is a trump, that card wins.\n(b) If both cards are of the same suit, the higher rank wins. If they are identical in suit and rank, the leader wins.\n(c) Otherwise (different suits, neither a trump), the leader wins.\n5. The winner adds the point values of both cards to their score. In trick 16 the winner also adds 1 bonus point.\n6. The winner leads the next trick.\n7. In tricks 1 to 13, the winner draws the top card of their own pile, then the loser draws the top card of their own pile, so both again hold 3 cards. After trick 13 both piles are empty and no more cards are drawn.\n8. After trick 16 the game ends.\n\nThe points total 201 (200 card points plus the 1 bonus point), so the scores cannot be equal.",
    "objective": "After 16 tricks, the player with the higher score wins. Since 201 points are shared, a draw is impossible.",
    "expected_effect": "With pile contents hidden, each player must infer from the composition and the cards played which cards the opponent might be holding. This drives decisions such as leading an Ace into a possible trump, saving trumps, and dumping Sevens on lost tricks. Because both piles are identical, neither player starts with more card strength, so draw order matters less than timing and card counting. In tricks 14 to 16 both hands are fully deducible, so the game ends in a short perfect-information endgame that rewards planning the final tricks with follow-suit in mind. There are two players and no communication step."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 3,
    "random_draws_per_round": 0,
    "rounds": 16
  }
}
```
````
