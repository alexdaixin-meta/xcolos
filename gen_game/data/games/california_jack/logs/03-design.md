# 03 design

- time: 2026-10-28T03:01:01+00:00 (58.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 aa922d01c8e70db8, reply sha256 5d5cf1f221b1119c

## Sent

````
Original game: California Jack
Players in the original: 2 to 2

Original rules:
Use standard 52 card deck. Deal 6 cards to each player, one or three at a time. Place remainder face up as stock; top card's suit is trump. Non-dealer leads first trick. Second player must follow suit if able, else play a trump if able, else any card. A trick is won by the highest trump if any, otherwise by the highest card of the led suit if second player followed suit, otherwise by the leader. Winner leads next trick. Winner draws top exposed stock card, loser draws next card. Continue until stock is gone, then play out final 6 cards with same following rules but no drawing. Each deal awards 1 point each for High (Ace of trump taken), Low (Deuce of trump taken), Jack of trump taken, and Game (most pip value in tricks, where Tens=10, Aces=4, Kings=3, Queens=2, Jacks=1). First to 10 points wins, ties broken in order High, Low, Jack, Game.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Most of the game is complete and consistent:
- Follow rules, trick winner, the draw order (the winner takes the seen top card; the next card is revealed and taken by the loser) and end-of-deal scoring are all specified.
- The match is finite at 28 rounds and decided by arithmetic.
- No board, clock or trading is needed, and there are 2 players, so talk is not at issue.
- Stated limits are within bounds: 14 of 20 steps, 2 of 4 choice steps, 18 of 20 attributes, 2 of 3 hidden elements, 0 of 1 random draws, 28 of 40 rounds.
- Trick resolution and the legality of the follow can be a referee-checked rule. Card-point lookup needs if-chains over 7 ranks for 2 cards, which is a heavy load per step but feasible.
- The attribute budget is tight. Two hands, stock, recorded stock, two recorded hands, two deal totals, two match totals, two match-point totals, three holders, leader, trump and two trick cards come to about 19.

The failure is in deal 2. The information state there is undefined. Step 1 shows only cards played and drawn 'so far in this deal'. Yet by the end of deal 1 every stock card has been revealed in order, and each player can deduce the opponent's initial hand: 28 cards minus their own 4 minus the 20 stock cards. Deal 2 is therefore either a perfect-information game, for a player who remembers deal 1, or a partly hidden one, for a player who does not. The rules never say whether the deal-1 record (stock order, both initial hands, deal-1 play) is shown in deal 2. The game's real information structure thus depends on model memory or platform context length, not on the rules. Players with the same rules text can face different games, and the hidden_elements count of 2 is wrong for deal 2.
- change: Define the deal-2 information explicitly. Option 1: at the start of deal 2, show both players the full recorded stock order, both initial hands and the complete deal-1 play log. This states that deal 2 is a perfect-information replay. Set hidden_elements to reflect this, and keep that record in a public attribute shown in step 1 of every deal-2 round.
- change: Option 2, if hidden information in deal 2 is wanted: reshuffle the stock order for deal 2, or reveal stock cards only as they are drawn and forbid reliance on deal 1. Option 1 is cleaner because the platform cannot erase memory.
- change: Recount attributes with the recorded stock, both recorded hands and the deal-1 log included, and confirm the total stays at or under 20. For example, merge the three holder flags into one encoded attribute, or drop the captured piles, since only card-point totals and holders are needed.
The variation that was reviewed: Duplicate California Jack: DECK: 28 cards in 4 suits (Spades, Hearts, Diamonds, Clubs). Each suit has the ranks A, K, Q, J, 10, 9, 2, from highest to lowest. Card points: each 10 = 10, A = 4, K = 3, Q = 2, J = 1, and 9 and 2 = 0. That makes 20 per suit and 80 in total.

SETUP: Shuffle the deck once. Deal 4 cards face down to Player A and 4 to Player B; each player sees only their own hand. The remaining 20 cards form the stock, kept in its shuffled order. Only the top card of the stock is shown. The suit of that top card is trump for the whole match. Record the shuffled stock order and both initial hands; deal 2 reuses them.

MATCH: 2 deals of 14 tricks each, 28 rounds in total, one trick per round. In deal 1 (rounds 1-14) Player A leads the first trick. In deal 2 (rounds 15-28) Player B leads the first trick.

EACH ROUND (one trick):
1. Both players are shown: the trump suit; the current top card of the stock, or 'stock empty'; the number of cards left in the stock; the list of every card played and drawn so far in this deal; their own hand; and the current scores.
2. The leader plays any one card from their hand face up.
3. The follower plays one card from their hand face up and must obey these rules in order: (a) play a card of the led suit if they have one; (b) otherwise play a trump if they have one; (c) otherwise play any card.
4. Trick winner: if any trump was played, the higher trump wins. Otherwise, if the follower followed suit, the higher card of the led suit wins. Otherwise the leader wins.
5. The winner adds both cards to their captured pile for this deal and adds their card points to their deal card-point total. If the Ace of trump is among the two cards, the winner holds High for this deal. If the Deuce of trump is among them, the winner holds Low. If the Jack of trump is among them, the winner holds Jack.
6. If the stock is not empty: the winner takes the top stock card into their hand, which both players already saw. The next card is then revealed, and the loser takes it into their hand, so both players see it. Then the new top card, if any, is revealed. The stock always has an even number of cards, so both players always draw.
7. The trick winner leads the next trick.

When the stock is empty (after trick 10 of a deal), each player has 4 cards. Tricks 11-14 are played with the same rules and no drawing.

END OF DEAL SCORING (after rounds 14 and 28): Each player gains 1 match point for each of High, Low and Jack they hold. The player with the higher deal card-point total gains 1 match point for Game; if both have 40, nobody scores Game. Each player's deal card points are also added to their match card-point total.

DEAL 2 RESET (after round 14 is scored): Restore the stock to the exact recorded order from setup, so the trump is the same. Player A receives Player B's initial 4-card hand from deal 1, and Player B receives Player A's initial hand. Clear captured piles, deal card points and the High, Low and Jack holders. Player B leads round 15.

After round 28 is scored, the match ends. Winner: The player with more match points summed over both deals wins (each deal awards at most 4 match points). If match points are tied, the player with the higher match card-point total over both deals wins (the two totals sum to 160). If that is also tied (80 each), the match is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "California Jack is a two-player trick-taking game played from a face-up stock. Trump is set by the stock's top card, the trick winner takes the visible top card and the loser takes the next one, and points come from capturing the Ace, Deuce and Jack of trump plus a majority of card points ('Game'). The match runs to 10 points.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies all lose to a thinking player. 'Always play your highest card' wastes trumps and tens on worthless stock cards. 'Always play lowest' gives up High, Jack and the tens. Choices decide both trick outcomes and which stock card each player gets, so they matter. The one seat edge is that the non-dealer leads first, and in a single deal the card luck is large."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skill is real: knowing when to win a trick for a good stock card, when to lose one deliberately, and tracking trumps. But with a random 52-card deal and only 4 binary points per deal, whoever is dealt the trump Ace and Deuce collects 2 points without effort. Over a first-to-10 match the luck averages out only slowly."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still scores Low, Jack or Game sometimes. A strong player improves by counting cards, valuing visible stock cards against the cost of trumps, and planning the 6-card endgame. The game is not solved for practical play."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "The opponent's hand and the unrevealed stock are hidden. Players must infer holdings from follows and failures to follow, and plan several tricks ahead about which stock cards to fight for."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners, the holders of High, Low and Jack, and Game all follow from the cards by arithmetic. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based, text-only and has no board. But a 52-card deck with 26 tricks per deal, repeated until someone reaches 10 points, is long and unbounded in rounds. The full deck also strains the attribute and step budgets."
    }
  ],
  "problems": [
    "Card luck dominates a single deal: whoever is dealt the trump Ace and Deuce scores them regardless of skill.",
    "First-to-10 gives a match of unbounded length, and a 52-card deck gives 26 tricks per deal, which is too long for the platform.",
    "The non-dealer leads the first trick, a small built-in seat edge in any single deal.",
    "In the previously tested duplicate variation, deal 2's information state was undefined. Every stock card and both initial hands become deducible by the end of deal 1, but the rules did not say whether that record was shown in deal 2, so the game depended on model memory rather than on the rules.",
    "In the previous variation the attribute budget was almost exhausted (about 19) before any deal-1 record was stored, so storing the record risked going over 20."
  ],
  "changes": [
    {
      "what": "Play a duplicate match of 2 deals. Deal 2 restores the same stock order and gives each player the other's initial hand, and the hand that led first in deal 1 also leads first in deal 2.",
      "why": "Each player plays both hands against the same stock, so who was dealt the trump Ace cancels out. Only how well the cards are played separates the players.",
      "fixes": "Card luck dominates a single deal: whoever is dealt the trump Ace and Deuce scores them regardless of skill."
    },
    {
      "what": "Use a 28-card deck (A K Q J 10 9 2 in four suits), 4-card hands and a 20-card stock, giving 14 tricks per deal and 28 rounds in total.",
      "why": "This keeps every scoring card (Ace, Deuce and Jack of trump, the tens) and the stock-fighting mechanic while fitting the round and attribute limits.",
      "fixes": "First-to-10 gives a match of unbounded length, and a 52-card deck gives 26 tricks per deal, which is too long for the platform."
    },
    {
      "what": "The lead of each hand is fixed: hand A leads in both deals, played by Player A in deal 1 and by Player B in deal 2.",
      "why": "Each player gets the leading position exactly once with the same cards, so the seat edge cancels.",
      "fixes": "The non-dealer leads the first trick, a small built-in seat edge in any single deal."
    },
    {
      "what": "Deal 2 is declared an open-information deal. At its start and in every deal-2 round, both players are shown the full recorded stock order, both deal-1 initial hands, the complete deal-1 play-and-draw log, both current hands face up, and the full remaining stock in order.",
      "why": "Everything in deal 2 is deducible from deal 1 anyway, and the platform cannot erase memory. Showing it explicitly means every player faces the same game whatever they remember. Deal 1 is a hidden-information inference game; deal 2 is a perfect-information planning game in which each player tries to beat the opponent's deal-1 result with that opponent's own cards. Reshuffling instead would break the duplicate fairness.",
      "fixes": "In the previously tested duplicate variation, deal 2's information state was undefined. Every stock card and both initial hands become deducible by the end of deal 1, but the rules did not say whether that record was shown in deal 2, so the game depended on model memory rather than on the rules."
    },
    {
      "what": "Drop the captured piles, since only card-point totals and holders are needed. Merge the High, Low and Jack holder flags into one encoded attribute. Store the deal-1 record as four attributes: recorded stock, both initial hands, and the deal-1 log. The recount comes to 19.",
      "why": "This stores the record deal 2 needs without exceeding 20 attributes.",
      "fixes": "In the previous variation the attribute budget was almost exhausted (about 19) before any deal-1 record was stored, so storing the record risked going over 20."
    }
  ],
  "keeps": [
    "Trump fixed by the top stock card at the start.",
    "Following priority: follow suit if able, else trump if able, else any card.",
    "Trick resolution: highest trump, else highest card of the led suit if followed, else the leader wins.",
    "The trick winner takes the visible top stock card; the loser takes the next card, which is revealed.",
    "A no-draw endgame once the stock is exhausted.",
    "Scoring of High, Low, Jack and Game with the original card-point values (10=10, A=4, K=3, Q=2, J=1).",
    "The tension of deliberately losing a trick to avoid wasting a trump, against winning it to secure a valuable stock card."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game has real inference (hidden hands and stock) and planning (fighting for stock cards). A duplicate format with an explicitly open deal 2 removes card luck and memory dependence within the limits."
  },
  "variation": {
    "name": "Duplicate California Jack (Open Replay)",
    "summary": "A two-deal duplicate match of a 28-card California Jack. Deal 1 is played with hidden hands and a hidden stock. Deal 2 replays the same stock with the hands swapped, with everything shown face up, so each player tries to outscore the opponent's deal-1 result with the opponent's own cards.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 28 cards in 4 suits (Spades, Hearts, Diamonds, Clubs). Each suit has the ranks A, K, Q, J, 10, 9, 2, from highest to lowest. Card points: each 10 = 10, A = 4, K = 3, Q = 2, J = 1, 9 = 0, 2 = 0. That makes 20 per suit and 80 in total.\n\nSETUP: Shuffle the deck once. Deal 4 cards face down to Player A and 4 to Player B. The remaining 20 cards form the stock in shuffled order. The suit of the stock's top card is trump for the whole match. The engine privately records the stock order and both initial hands, which deal 2 reuses.\n\nMATCH: 2 deals of 14 tricks each, one trick per round, 28 rounds in total. Deal 1 is rounds 1-14; Player A leads round 1. Deal 2 is rounds 15-28; Player B leads round 15.\n\nINFORMATION IN DEAL 1 (rounds 1-14): Each round, each player is shown: the trump suit; the current top stock card, or 'stock empty'; the number of cards left in the stock; the complete list, in order, of every card played and every card drawn so far in this deal, with who played or drew it; their own hand only; and the current match points and match card points. The opponent's hand and the stock below the top card are hidden.\n\nINFORMATION IN DEAL 2 (rounds 15-28): Deal 2 is an OPEN deal. Each round, both players are shown: the trump suit; the full remaining stock in order; BOTH players' current hands face up; the complete deal-1 record (the original stock order, both deal-1 initial hands, and the full deal-1 log of plays, draws, trick winners and final deal-1 points); the list of every card played and drawn so far in deal 2; and the current match points and match card points. Nothing is hidden in deal 2.\n\nEACH ROUND (one trick):\n1. Show each player the information above.\n2. The leader plays any one card from their hand face up.\n3. The follower plays one card from their hand face up, obeying these rules in order: (a) play a card of the led suit if they have one; (b) otherwise play a trump if they have one; (c) otherwise play any card. An illegal choice is replaced by the lowest-ranked legal card.\n4. Trick winner: if any trump was played, the higher trump wins. Otherwise, if the follower followed suit, the higher card of the led suit wins. Otherwise the leader wins.\n5. The winner adds the card points of both cards to their deal card-point total. If the Ace of trump is among the two cards, the winner holds High for this deal. If the Deuce of trump is among them, the winner holds Low. If the Jack of trump is among them, the winner holds Jack.\n6. Both played cards are appended to the current deal's log.\n7. If the stock is not empty, the winner takes the top stock card into their hand. The next card is revealed and the loser takes it into their hand. Both draws are appended to the log, and the new top card, if any, is revealed. The stock always holds an even number of cards, so both players always draw.\n8. The trick winner leads the next trick.\nThe stock empties after trick 10 of each deal. Tricks 11-14 are then played with 4 cards each and no drawing.\n\nEND OF DEAL SCORING (after rounds 14 and 28): Each player gains 1 match point for each of High, Low and Jack they hold. The player with the higher deal card-point total gains 1 match point for Game; if both have 40, nobody scores Game. Each player's deal card points are added to their match card-point total.\n\nDEAL 2 RESET (after round 14 is scored): Save the deal-1 log as the public deal-1 record. Restore the stock to the recorded order, so trump is unchanged. Player A receives Player B's deal-1 initial hand and Player B receives Player A's deal-1 initial hand. Clear deal card points, the High, Low and Jack holders, and the current-deal log. Player B leads round 15. From round 15 onward, all information is shown as described under INFORMATION IN DEAL 2.\n\nEND: After round 28 is scored, the match ends.",
    "objective": "The player with more match points over both deals wins (each deal awards at most 4). If match points are tied, the player with the higher match card-point total wins (the two totals sum to 160). If that is also tied at 80 each, the match is a draw.",
    "expected_effect": "Card luck cancels, because each player plays both hands against the same stock with the same lead. Deal 1 rewards inference: reading the opponent's hand from follows and failures to follow, and judging when a visible stock card is worth winning a trick for. Deal 2 is a fully specified perfect-information endgame-planning problem with the deal-1 benchmark in view: a player knows exactly what the opponent achieved with these cards and must plan 14 tricks of stock-fighting to beat it. No player's result depends on what they remember, because all records are displayed. Simple policies (always highest legal card, always lowest, always win when possible) waste trumps or give away tens and High, and lose to deliberate play. Talk does not apply (2 players)."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 2,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 28
  }
}
```
````
