# 05 design

- time: 2026-10-28T03:02:59+00:00 (67.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 991a90c6345b2e82, reply sha256 d592af694d021873

## Sent

````
Original game: California Jack
Players in the original: 2 to 2

Original rules:
Use standard 52 card deck. Deal 6 cards to each player, one or three at a time. Place remainder face up as stock; top card's suit is trump. Non-dealer leads first trick. Second player must follow suit if able, else play a trump if able, else any card. A trick is won by the highest trump if any, otherwise by the highest card of the led suit if second player followed suit, otherwise by the leader. Winner leads next trick. Winner draws top exposed stock card, loser draws next card. Continue until stock is gone, then play out final 6 cards with same following rules but no drawing. Each deal awards 1 point each for High (Ace of trump taken), Low (Deuce of trump taken), Jack of trump taken, and Game (most pip value in tricks, where Tens=10, Aces=4, Kings=3, Queens=2, Jacks=1). First to 10 points wins, ties broken in order High, Low, Jack, Game.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: 1. The step budget is not credible. Declared steps_per_round is 16, but the flat per-round list must contain at least the following:
- an info display (1);
- lead and follow choices (2);
- follow-legality enforcement with replacement (about 2);
- trick-winner resolution: trump present, which trump is higher, followed suit, rank compare. The engine has no lookup operation, so ranks A>K>Q>J>10>9>2 must be computed with conditionals (about 3-4 steps).
- card-point lookup for two cards over 7 ranks. Like the rps workaround, this is several steps (about 3-6).
- High/Low/Jack detection (about 1-3);
- log append (1);
- two draws plus a reveal (about 2);
- setting the leader (1);
- end-of-deal scoring under `when` conditions: High, Low and Jack match points for two players, Game with its tie case, and adding card points (about 4-5);
- the deal-2 reset: save the deal-1 record, restore the stock, swap the two hands, clear 2 deal totals, 3 holders and the log, set B as leader (about 6-8).
That is roughly 30-35 steps against a limit of 20.

2. The attribute count is understated. Needed: trump, stock, recorded stock, hand A, hand B, recorded hand A, recorded hand B, current log, deal-1 record, deal points A and B, match points A and B, match card points A and B, High, Low and Jack holders, leader, deal number, led card and followed card. That is about 22, over the limit of 20.

3. There is a rule ambiguity. 'An illegal choice is replaced by the lowest-ranked legal card' has no tiebreak when several suits hold the same lowest rank, for example under rule (c).

The rest is fine. The game is finite (28 rounds) and decided by arithmetic. There are 2 choice steps and 0 random draws per round (one shuffle at setup), and hidden elements in deal 1 are at most 3. With 2 players, the talk question does not apply. Nothing needs a board, clock or judge.
- change: Cut the per-round step list to 20 or fewer, and restate the complexity honestly. Suggested changes:
- Represent each card as a game-list item with stored numeric rank (2=1, 9=2, 10=3, J=4, Q=5, K=6, A=7) and point values, so rank compare and card points are single arithmetic operations instead of conditional ladders.
- Merge High/Low/Jack detection into one step that sets three holders with `if` operations.
- Fold the deal-2 reset into as few `when round==14` operations as the engine allows. A single 'swap hands and restore stock' step should use the recorded lists.
- change: Bring attributes to 20 or fewer. Store only one 'initial deal' record (the original stock plus both hands as one list or object) rather than three separate recorded attributes. Derive deal number from the round number instead of storing it.
- change: Define a full ordering for the illegal-choice replacement, for example: lowest rank, ties broken by suit order Clubs < Diamonds < Hearts < Spades.
The variation that was reviewed: Duplicate California Jack (Open Replay): DECK: 28 cards in 4 suits (Spades, Hearts, Diamonds, Clubs). Each suit has the ranks A, K, Q, J, 10, 9, 2, from highest to lowest. Card points: each 10 = 10, A = 4, K = 3, Q = 2, J = 1, 9 = 0, 2 = 0. That makes 20 per suit and 80 in total.

SETUP: Shuffle the deck once. Deal 4 cards face down to Player A and 4 to Player B. The remaining 20 cards form the stock in shuffled order. The suit of the stock's top card is trump for the whole match. The engine privately records the stock order and both initial hands, which deal 2 reuses.

MATCH: 2 deals of 14 tricks each, one trick per round, 28 rounds in total. Deal 1 is rounds 1-14; Player A leads round 1. Deal 2 is rounds 15-28; Player B leads round 15.

INFORMATION IN DEAL 1 (rounds 1-14): Each round, each player is shown: the trump suit; the current top stock card, or 'stock empty'; the number of cards left in the stock; the complete list, in order, of every card played and every card drawn so far in this deal, with who played or drew it; their own hand only; and the current match points and match card points. The opponent's hand and the stock below the top card are hidden.

INFORMATION IN DEAL 2 (rounds 15-28): Deal 2 is an OPEN deal. Each round, both players are shown: the trump suit; the full remaining stock in order; BOTH players' current hands face up; the complete deal-1 record (the original stock order, both deal-1 initial hands, and the full deal-1 log of plays, draws, trick winners and final deal-1 points); the list of every card played and drawn so far in deal 2; and the current match points and match card points. Nothing is hidden in deal 2.

EACH ROUND (one trick):
1. Show each player the information above.
2. The leader plays any one card from their hand face up.
3. The follower plays one card from their hand face up, obeying these rules in order: (a) play a card of the led suit if they have one; (b) otherwise play a trump if they have one; (c) otherwise play any card. An illegal choice is replaced by the lowest-ranked legal card.
4. Trick winner: if any trump was played, the higher trump wins. Otherwise, if the follower followed suit, the higher card of the led suit wins. Otherwise the leader wins.
5. The winner adds the card points of both cards to their deal card-point total. If the Ace of trump is among the two cards, the winner holds High for this deal. If the Deuce of trump is among them, the winner holds Low. If the Jack of trump is among them, the winner holds Jack.
6. Both played cards are appended to the current deal's log.
7. If the stock is not empty, the winner takes the top stock card into their hand. The next card is revealed and the loser takes it into their hand. Both draws are appended to the log, and the new top card, if any, is revealed. The stock always holds an even number of cards, so both players always draw.
8. The trick winner leads the next trick.
The stock empties after trick 10 of each deal. Tricks 11-14 are then played with 4 cards each and no drawing.

END OF DEAL SCORING (after rounds 14 and 28): Each player gains 1 match point for each of High, Low and Jack they hold. The player with the higher deal card-point total gains 1 match point for Game; if both have 40, nobody scores Game. Each player's deal card points are added to their match card-point total.

DEAL 2 RESET (after round 14 is scored): Save the deal-1 log as the public deal-1 record. Restore the stock to the recorded order, so trump is unchanged. Player A receives Player B's deal-1 initial hand and Player B receives Player A's deal-1 initial hand. Clear deal card points, the High, Low and Jack holders, and the current-deal log. Player B leads round 15. From round 15 onward, all information is shown as described under INFORMATION IN DEAL 2.

END: After round 28 is scored, the match ends. Winner: The player with more match points over both deals wins (each deal awards at most 4). If match points are tied, the player with the higher match card-point total wins (the two totals sum to 160). If that is also tied at 80 each, the match is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "California Jack is a two-player trick-taking game played with a face-up stock. After each trick the winner draws the exposed top card and the loser draws the next card. Each deal awards points for capturing the Ace, Deuce and Jack of trump and for winning the most card points, and the first player to 10 points wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. 'Always play your highest card' wastes trumps and Tens early and hands the opponent the good exposed stock cards. 'Always play low' gives up High, Jack and the Tens. Seat edge: the non-dealer leads first, but the deal alternates. In the previous variation the duplicate replay gave each player each hand with the lead once, which removed the seat edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, a single deal is strongly shaped by who holds the Ace and Jack of trump and by the order of the stock. The match is first to 10, about three deals, which is too few for skill to wash out the cards. The previous variation's duplicate structure fixed this: the same stock and hands are played twice with the players swapped, so the card luck cancels."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still captures some cards and points. A strong player can keep improving in several ways: deciding when to win a trick to take a valuable exposed card and when to lose it, counting trumps, keeping a trump to guard the Ten, and planning the last no-draw tricks once the stock is empty."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The opponent's hand is hidden, and so is every stock card except the top one. Players must infer the opponent's holding from what they drew and played, and must plan whether winning the current trick is worth it, given the visible top card and the unseen card beneath it. In the previous variation the second deal was open, but it rewarded planning against a known record of what happened in deal 1."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners, captured honours, card points and match points all follow by arithmetic from the cards played. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only, with no board. The original 52-card deck with 6-card hands and first-to-10 scoring is long. The previous variation shrank it to 28 cards and 28 rounds but failed the build check: it really needed about 30-35 steps per round against a limit of 20, and about 22 attributes against a limit of 20. It also left a tie unresolved in its replacement rule for illegal plays."
    }
  ],
  "problems": [
    "P1: The original is too long and luck-heavy for the platform. A 52-card deck and first-to-10 means many deals, each dominated by who holds the trump honours.",
    "P2: The previous variation's per-round step list ran to about 30-35 steps (limit 20). Rank comparison and card-point lookup were done by conditional ladders, the follow rule was enforced by replacement afterwards, and the deal-2 reset was spread over many steps.",
    "P3: The previous variation needed about 22 attributes (limit 20). It had separate recorded stock and hands, a separate deal-1 record, three honour-holder attributes and a deal counter.",
    "P4: The previous variation's rule 'an illegal choice is replaced by the lowest-ranked legal card' had no tiebreak when several cards share the lowest rank.",
    "P5: Seat and deal luck. Whoever leads, and whoever is dealt the trump honours, gains an edge that reasoning cannot overcome within a single deal."
  ],
  "changes": [
    {
      "what": "Keep the 28-card deck (A, K, Q, J, 10, 9, 2 in four suits), 4-card hands and a 20-card stock, giving 2 deals of 14 tricks (28 rounds).",
      "why": "This keeps the stock-drawing structure and the honours while making a match short and finite.",
      "fixes": "P1"
    },
    {
      "what": "Keep the duplicate replay. Deal 2 reuses the identical stock, with the two initial hands swapped and the other player leading. Deal 2 is played open.",
      "why": "Each player plays each hand once, with the lead, against the same stock. Card luck and seat edge cancel, and the difference in results comes from play.",
      "fixes": "P5"
    },
    {
      "what": "Each card is a list item carrying three stored numbers: suit, rank value (2=1, 9=2, 10=3, J=4, Q=5, K=6, A=7) and card points (10=10, A=4, K=3, Q=2, J=1, 9=0, 2=0).",
      "why": "The trick winner and the points become single arithmetic expressions instead of conditional ladders. This cuts several steps.",
      "fixes": "P2"
    },
    {
      "what": "Before the follower chooses, one step computes the follower's legal list: led-suit cards if any, else trumps if any, else the whole hand. The follower chooses only from that list.",
      "why": "Illegal plays become impossible, so the replacement steps disappear.",
      "fixes": "P2, P4"
    },
    {
      "what": "Award High, Low and Jack as match points the moment they are captured, in one step: the trick winner gains 1 match point for each of A, 2 and J of trump among the two cards.",
      "why": "Each honour is captured exactly once per deal, so scoring it at capture is equivalent to scoring at the end of the deal. This removes three holder attributes and the end-of-deal honour checks.",
      "fixes": "P2, P3"
    },
    {
      "what": "Use one 'initial deal' record (the stock order plus both hands, stored once). Use one match-long log, so the deal-1 entries stay visible in deal 2 and no separate deal-1 record is needed. Derive the deal from the round number.",
      "why": "Attributes fall to 16.",
      "fixes": "P3"
    },
    {
      "what": "Do the deal-2 reset in two steps that run only after round 14 (on the condition round == 14). The first restores the stock and swaps the hands. The second clears the deal points and makes B the leader.",
      "why": "The reset was the largest step cost.",
      "fixes": "P2"
    },
    {
      "what": "Fix a full card order for the default play: lowest rank value, ties broken by suit order Clubs < Diamonds < Hearts < Spades. Hands are always listed in this order.",
      "why": "Every fallback and listing is unambiguous.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "The face-up stock, where the trick winner takes the exposed top card and the loser takes the next one, so winning or losing a trick on purpose is the central decision.",
    "Trump is set by the suit of the stock's top card.",
    "The follow rule: follow suit, else trump, else any card.",
    "The four scoring items: High (Ace of trump), Low (Deuce of trump), Jack of trump, and Game (most card points, with Ten 10, Ace 4, King 3, Queen 2, Jack 1).",
    "The no-draw endgame once the stock is empty.",
    "The tie-break spirit of the original: honours and Game decide first, card points break ties."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core decision (whether winning a trick is worth the exposed card, given the hidden hand and stock) is real reasoning. With list-item cards, a precomputed legal list, honours scored at capture and a two-step reset, the duplicate format fits the limits."
  },
  "variation": {
    "name": "Duplicate California Jack (Compact)",
    "summary": "California Jack with 28 cards, played as two deals over the same shuffled stock. Players swap hands for the second deal, and the second deal is played open. The first deal tests inference from hidden information. The second tests planning against a known layout and a known score to beat.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 28 cards in 4 suits: Clubs, Diamonds, Hearts, Spades. Each suit has the ranks A, K, Q, J, 10, 9, 2. Each card carries a rank value (2=1, 9=2, 10=3, J=4, Q=5, K=6, A=7; higher wins) and card points (10=10, A=4, K=3, Q=2, J=1, 9=0, 2=0). Each suit holds 20 card points, 80 in total.\n\nCARD ORDER: Whenever cards are listed or a default card is needed, order them by rank value, lowest first, with ties broken by suit order Clubs < Diamonds < Hearts < Spades. Hands are always shown in this order.\n\nSETUP: Shuffle the deck once. Deal 4 cards face down to Player A and 4 to Player B. The other 20 cards form the stock in shuffled order. The suit of the stock's top card is trump for the whole match. The engine privately stores this initial deal (stock order, hand A, hand B) for deal 2. Match points and match card points start at 0 for both players.\n\nMATCH: 28 rounds, one trick per round. Deal 1 is rounds 1-14, and Player A leads round 1. Deal 2 is rounds 15-28, and Player B leads round 15.\n\nINFORMATION: Every round, both players see the following: the trump suit; the top stock card, or 'stock empty'; the number of stock cards left; the match log of every card played and drawn so far, with who played or drew it and who won each trick; both players' match points and match card points; and the current deal card points. In deal 1 (rounds 1-14), each player also sees their own hand only. The opponent's hand and the stock below the top card are hidden. In deal 2 (rounds 15-28), everything is open: both hands face up, the full remaining stock in order, and the stored initial deal.\n\nEACH ROUND:\n1. Show the information above.\n2. The leader chooses any card from their hand and plays it face up.\n3. The engine lists the follower's legal cards: all their cards of the led suit if they have any; otherwise all their trumps if they have any; otherwise their whole hand.\n4. The follower chooses one card from that legal list and plays it face up.\nIf a player gives no valid answer in step 2 or 4, they play the first card of their allowed cards in CARD ORDER.\n5. Both played cards leave the hands.\n6. Trick winner: the follower wins if they played a trump and either the led card is not a trump or the follower's rank value is higher. The follower also wins if they followed the led suit with a higher rank value. In every other case the leader wins.\n7. The winner adds the card points of both cards to their deal card points.\n8. Honours: for each of the Ace of trump, the 2 of trump and the Jack of trump among the two played cards, the winner gains 1 match point at once (High, Low and Jack).\n9. Append both plays and the trick winner to the match log.\n10. If the stock is not empty, the winner takes the top stock card and the loser takes the next one. Both draws are logged and the new top card is revealed. The stock empties after trick 10 of each deal, and tricks 11-14 are played out with no drawing.\n11. The winner leads the next round.\n\nEND OF DEAL (after rounds 14 and 28): The player with more deal card points gains 1 match point for Game. If both have 40, nobody gains it. Each player adds their deal card points to their match card points.\n\nDEAL 2 RESET (after round 14 has been scored): Restore the stock to its stored order, so trump is unchanged. Player A receives Player B's stored initial hand, and Player B receives Player A's stored initial hand. Set both deal card points to 0. Player B leads round 15. The match log is kept, so the whole of deal 1 stays visible.\n\nEND: After round 28 has been scored, the match ends.",
    "objective": "The player with more match points wins. Each deal awards at most 4: High, Low, Jack and Game. If match points are tied, the player with more match card points wins (the two totals add to 160). If both have 80, the match is a draw.",
    "expected_effect": "Because both players play the same stock with each hand, the result measures who played the same cards better rather than who was dealt the trump Ace. In deal 1, players must infer the opponent's hand from draws and plays. They must also decide when to lose a trick on purpose to avoid giving up a Ten or to take a better second card, and when to spend a trump to capture an exposed honour. In deal 2, the player holding each hand knows exactly how that hand fared in deal 1 and what match score they must beat, so play becomes precise planning against a fully visible layout. Simple policies can lose: always-highest wastes trumps, always-lowest gives up High, Jack and the Tens, and always-first-listed is the same as always-lowest. The precomputed legal list removes illegal plays, and all scoring is plain addition."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 2,
    "attributes": 16,
    "hidden_elements": 3,
    "random_draws_per_round": 0,
    "rounds": 28
  }
}
```
````
