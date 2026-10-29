# 01 design

- time: 2026-10-28T03:32:12+00:00 (62.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 6fe787c03f138556, reply sha256 3b940ffe0108ce84

## Sent

````
Original game: Sedmice
Players in the original: 2 to 4

Original rules:
Sedmice is played with 32 cards (7-A) with 4 cards dealt to each player, rest as talon. Leader plays any card. Following players each play one card. A trick is won by the last player to play a card equal in rank to the led card, or any Seven which is wild. If the current trick winner is an opponent of the original leader, the leader may extend the trick by playing another equal-rank or Seven, then all other players must play another card in order. Extension can repeat. Winner takes all cards of the trick to their side. After each trick all players draw from talon to return to 4 cards until talon empty, then play out remaining hands. Aces and Tens are worth 10 each, plus 10 for last trick, 90 total per deal. Deal winner needs 50+ points. Match is first to 120 points. In 4-player version players form two fixed pairs.
````

## Reply

````
```json
{
  "original_summary": "Sedmice is a Central European trick-taking game for 2 to 4 players with a 32-card deck. A trick goes to the last player who matches the led rank or plays a wild Seven. The leader may keep extending a trick they are losing. Aces and Tens are worth 10 points each, the last trick is worth 10 more, and hands are refilled from a talon.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. If you always follow with a Seven, the opponent leads worthless 8s and 9s to draw your Sevens out, then cashes Aces and Tens. If you always play your lowest card, you lose every contested Ace or Ten. Leading is not a fixed edge, because the follower answers last; the leader's compensation is the extension."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, Seven management and when to extend do matter. But in a short match one deal that gives a player three Sevens and most of the Aces and Tens often decides it. The random refill from the talon adds further variance a player cannot control."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Beginners still take some tricks. Experts improve through counting which ranks are gone, baiting Sevens, timing extensions and saving a Seven for the last trick. The game is not solved."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Opponents' hands and the talon are hidden. Players must infer from what has been played whether the opponent still holds a matching rank or a Seven, and plan which card to give up now to win a later trick."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners follow mechanically from ranks, and points are simple sums of Aces, Tens and the last-trick bonus."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. Three parts break the limits. Unlimited extensions are an unbounded loop of steps. Refilling every hand from the talon after each trick needs several random draws per round. The 4-player fixed-partnership version adds roles and many choice steps."
    }
  ],
  "problems": [
    "Unlimited trick extension creates a loop of unbounded length that a flat step list cannot express, and it can exceed 4 choices per round.",
    "Refilling every hand from the talon after every trick needs several random draws per round, above the limit of 1.",
    "A single lucky deal (many Sevens, Aces and Tens) can decide the match, so luck can swamp skill.",
    "The 4-player partnership version and variable player counts multiply the choice steps and the rules for turn order.",
    "The 'first to 120 across deals, 50+ to win a deal' scoring gives a match of variable length, which is awkward for a fixed number of rounds."
  ],
  "changes": [
    {
      "what": "The leader may extend a trick at most once: one extra card from each player.",
      "why": "This keeps the signature extension decision while bounding each trick to at most 4 card plays.",
      "fixes": "Unlimited trick extension creates a loop of unbounded length that a flat step list cannot express, and it can exceed 4 choices per round."
    },
    {
      "what": "Replace the talon refill with one deal of 8 cards per player at the start of each deal. The 16 undealt cards are set aside face down and never used.",
      "why": "There is only one random event per deal, at its first round. Hidden information remains, because neither player can deduce the other's hand from their own cards.",
      "fixes": "Refilling every hand from the talon after every trick needs several random draws per round, above the limit of 1."
    },
    {
      "what": "Use a guaranteed core deal: each player always receives exactly one Seven, one Ace and one Ten, plus 5 random cards. Play 4 deals, with the first lead alternating.",
      "why": "This caps how lopsided a deal can be and averages luck over four deals. Both players also know the opponent started with at least one Seven, Ace and Ten, which gives a firm basis for inference.",
      "fixes": "A single lucky deal (many Sevens, Aces and Tens) can decide the match, so luck can swamp skill."
    },
    {
      "what": "Restrict the game to 2 players.",
      "why": "A strict head-to-head duel keeps the game within 4 choices per round with no partner roles.",
      "fixes": "The 4-player partnership version and variable player counts multiply the choice steps and the rules for turn order."
    },
    {
      "what": "Fix the length at 4 deals of up to 8 tricks (32 rounds). The higher total of points over all deals wins, and equal totals are a draw.",
      "why": "This gives a fixed, arithmetic winner rule. The game is purely competitive, so no cooperative option collapses under 'higher total wins'.",
      "fixes": "The 'first to 120 across deals, 50+ to win a deal' scoring gives a match of variable length, which is awkward for a fixed number of rounds."
    }
  ],
  "keeps": [
    "The 32-card deck of ranks 7 through Ace, with suits irrelevant.",
    "Sevens are wild and capture any trick.",
    "A trick is won by the last player to match the led rank or play a Seven; otherwise the leader wins it.",
    "The leader's option to extend a trick they are losing.",
    "Aces and Tens are worth 10 each and the last trick is worth 10.",
    "The trick winner leads the next trick."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core decisions (spending Sevens, extending, counting ranks) are rich and survive a bounded extension and a single deal per hand. Only the loop, the refill and the luck needed fixing."
  },
  "variation": {
    "name": "Sedmice Duel",
    "summary": "A two-player Sedmice over 4 deals. Sevens are wild, and the leader may extend a losing trick once. Each deal gives both players a guaranteed Seven, Ace and Ten plus 5 random cards, so counting and baiting decide the game more than the draw does.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS: 32 cards, four each of the ranks 7, 8, 9, 10, J, Q, K, A. Suits do not matter. Aces and Tens are point cards worth 10 each. Sevens are wild.\n\nMATCH: 4 deals. Each deal lasts up to 8 rounds, so the match has 32 rounds. Each round is one trick.\n\nDEALING (first round of each deal): Shuffle the full deck. Each player receives exactly one Seven, one Ace and one Ten. Shuffle the remaining 26 cards and deal 5 more to each player, so each hand has 8 cards. Hands are private. The 16 undealt cards are set aside face down and are never revealed or used in that deal. Both players know the dealing rule.\n\nFIRST LEAD: Player A leads first in deals 1 and 3. Player B leads first in deals 2 and 4. After that, the winner of each trick leads the next one.\n\nA TRICK:\n(1) The leader plays any card face up. Its rank is the 'led rank'.\n(2) The follower plays any card face up. If it matches the led rank or is a Seven, the follower is currently winning. Otherwise the leader wins the trick and it ends.\n(3) If the follower is currently winning, the leader may extend once by playing a second card that matches the led rank or is a Seven. The leader may also decline. If the leader declines or has no such card, the follower wins the trick.\n(4) If the leader extended, the follower must play a second card (any card). If it matches the led rank or is a Seven, the follower wins the trick. Otherwise the leader wins.\nA trick can never be extended more than once.\n\nAFTER EACH TRICK: All cards played in the trick are announced. The winner scores 10 points for each Ace and each Ten among them. Both players always play the same number of cards, so both hands empty together. If the hands are now empty, the winner of this trick also scores 10 points for the last trick, and the deal ends. Any remaining rounds of that deal are skipped. A deal lasts 4 to 8 tricks.\n\nINFORMATION: Each player sees their own hand and every card played. Neither sees the opponent's hand or the set-aside cards.",
    "objective": "After 4 deals, the player with the higher total points across all deals wins. Equal totals are a draw.",
    "expected_effect": "Players must count which ranks and Sevens have been played. Each player knows the opponent held at least one Seven, Ace and Ten, so inference has a firm anchor. Good play includes leading cheap ranks to drain the opponent's Sevens, holding a Seven back for an Ace or Ten trick or for the last-trick bonus, and extending only when the follower is unlikely to have a matching card left. The guaranteed core deal and the four alternating deals keep luck in check, so the better counter and planner should usually win. Talk is omitted: with two strictly opposed players there is nothing to bargain over."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 32
  }
}
```
````
