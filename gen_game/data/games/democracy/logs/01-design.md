# 01 design

- time: 2026-10-28T02:19:57+00:00 (78.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2b79ee7bdf6ea586, reply sha256 9a5c9a90fc44367e

## Sent

````
Original game: Democracy
Players in the original: 2 to 6

Original rules:
Remove 2s from 52-card deck leaving 48 cards. For 4 players add 2 jokers, for 6 add 1 joker. Rank high to low: 5-4-3-A-K-Q-J-10-9-8-7-6. Points: 5=5, 4=4, 3/A=3, K/Q/J=2, 10/9/8/7=1, 6=0. Joker=0. Each suit totals 25. Deal cards in two days: half the deck each day plus a face-down voting pool of equal size to hand size. Each trick dealer flips one pool card for trump. Each player chooses one hand card face down, then all reveal together. If any trump is played highest trump wins, except 6 of trump beats 5 of trump if both present. If no trump highest rank wins any suit. Tied high with no trump: each takes own card, voting card discarded. Joker cannot be trump; loses to any trump, ties/wins otherwise vs 5s. Winner captures played cards plus voting card. After both days count points per suit; majority 13+ points scores one tribe. First to agreed total tribes wins match.
````

## Reply

````
```json
{
  "original_summary": "Democracy is a 2-6 player trick-taking card game with simultaneous play. Each trick, a face-down 'voting pool' card is flipped to name the trump suit and goes to the trick winner as a prize. Players capture point cards, and whoever holds a majority (13 of 25 points) in a suit wins that suit's 'tribe'. The first player to an agreed number of tribes wins the match.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Play is simultaneous, so no seat leads and no seat has an edge. 'Always play your highest card' loses to any trump and to the 6-of-trump upset. 'Always play lowest' wins almost nothing. Majority scoring means points spread across suits are worth nothing, so choices clearly change who gets tribes."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, timing of trumps and deciding which suit to fight for all reward skill. But one deal of large hands and random trump flips means hand quality swings individual deals. With the flexible 'agreed total tribes' and variable player counts, luck versus skill is not controlled."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Beginners can win tricks with high cards. Strong players track which cards remain, read which suits opponents chase, hold their 6 of trump against a 5, deny majorities, and stop investing in suits already decided."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the voting pool are hidden, and future trumps are unknown. Players must infer opponents' holdings from cards already played and guess what each opponent will commit to the current trick. This is inference plus opponent modelling under simultaneous moves."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick resolution, captured points per suit, the 13+ majority and tribe counts are all arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only and has no board. But it needs player-count-dependent decks with jokers, special joker rules, two 'days' of dealing, an open-ended 'agreed total' match length, and 4 suits times up to 6 players of per-suit tallies (24+ attributes). That breaks the attribute limit and is long."
    }
  ],
  "problems": [
    "Too many tracked numbers: per-suit point tallies for 4 suits across up to 6 players exceed the 20-attribute limit.",
    "Variable deck construction (jokers depending on player count) and joker special rules add rule branches with little strategic value.",
    "Two 'days' of dealing per hand plus an open-ended 'first to an agreed total of tribes' match make length undefined and possibly long.",
    "A single deal's hand quality and the random trump order can decide a match, so luck is not damped.",
    "With 2 players, majorities become a zero-sum race in which the higher capture total almost always also takes the majorities, which reduces the reasoning.",
    "The winner rule has no tie-break, so tied tribe counts are unresolved."
  ],
  "changes": [
    {
      "what": "Fix the game at 3 players with a 24-card deck: 3 suits of 8 cards (5,4,3,A,K,Q,J,6), each suit worth 20 points, with a tribe at 11+ points.",
      "why": "Per-suit tallies become 3 players × 3 suits = 9 attributes. The deck divides evenly into 6-card hands plus a 6-card voting pool. With three players, one rival's gain is not another's loss, so blocking and spoiling matter.",
      "fixes": "Too many tracked numbers: per-suit point tallies for 4 suits across up to 6 players exceed the 20-attribute limit."
    },
    {
      "what": "Remove jokers and the player-count deck variants.",
      "why": "Fewer rule branches; the core trump/majority tension is untouched.",
      "fixes": "Variable deck construction (jokers depending on player count) and joker special rules add rule branches with little strategic value."
    },
    {
      "what": "Play exactly 4 deals of 6 tricks each (24 rounds), one deal per 'day', and end the match after the 4th deal.",
      "why": "Gives a fixed, buildable length.",
      "fixes": "Two 'days' of dealing per hand plus an open-ended 'first to an agreed total of tribes' match make length undefined and possibly long."
    },
    {
      "what": "Score tribes across 4 separate deals and add them up.",
      "why": "Over four deals, a bad hand in one deal can be outweighed by better reasoning in the others, which damps hand luck.",
      "fixes": "A single deal's hand quality and the random trump order can decide a match, so luck is not damped."
    },
    {
      "what": "Add one simultaneous message per trick before cards are chosen.",
      "why": "With three players and only one winner, players can propose 'you take Hearts, I take Spades' deals to stop the leader. They can bluff about their holdings or betray a pact. Promises do not bind, so trust must be read.",
      "fixes": "With 2 players, majorities become a zero-sum race in which the higher capture total almost always also takes the majorities, which reduces the reasoning."
    },
    {
      "what": "Most tribes wins. Tie-break: the highest total captured points in the final deal. If still tied, the tied players draw.",
      "why": "Resolves ties by arithmetic on numbers the engine already tracks. Tallies are reset at the start of each deal, so final-deal tallies remain available at the end.",
      "fixes": "The winner rule has no tie-break, so tied tribe counts are unresolved."
    }
  ],
  "keeps": [
    "The distinctive rank order 5-4-3-A-K-Q-J-6, with point values 5/4/3/3/2/2/1/0.",
    "The face-down voting pool: each trick, its card names the trump suit and is captured by the trick winner.",
    "Simultaneous card play with no leader.",
    "The 'revolution' rule: the 6 of trump beats the 5 of trump when both are played.",
    "The tied-high, no-trump rule: each player keeps their own card and the voting card is discarded.",
    "Majority-per-suit 'tribe' scoring as the match currency."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (hidden hands, simultaneous tricks, random trump from a hidden pool, majority scoring) already demands inference and opponent modelling. It only needs to be shrunk to fit the attribute and length limits and made fixed-length with a clear winner."
  },
  "variation": {
    "name": "Democracy: Three Tribes",
    "summary": "Three players play 4 deals of simultaneous tricks with a 24-card, 3-suit deck. Each trick's trump is flipped from a hidden voting pool, and the winner captures it. Holding 11+ of a suit's 20 points in a deal wins that suit's tribe; most tribes over 4 deals wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "DECK: 24 cards in 3 suits (Hearts, Spades, Diamonds). Each suit has 8 cards. From highest rank to lowest they are: Five (5 points), Four (4), Three (3), Ace (3), King (2), Queen (2), Jack (1), Six (0). Each suit totals 20 points.\n\nMATCH: 4 deals of 6 tricks each, 24 tricks in total.\n\nSTART OF EACH DEAL (tricks 1, 7, 13, 19):\n- Shuffle all 24 cards.\n- Deal 6 cards face down to each player as their private hand.\n- Deal 6 cards face down as the voting pool, in order. Nobody sees the pool.\n- Reset every player's suit tallies to 0.\n\nEACH TRICK:\n1. Flip the next voting-pool card face up. Its suit is the trump suit for this trick, and the card itself is the prize.\n2. Talk: every player writes one short message at the same time, without seeing the others. All three messages are then shown to everyone. Nothing said is binding.\n3. Play: every player secretly chooses one card from their hand, at the same moment. All three cards are revealed together and removed from the hands.\n4. Resolve the trick:\n   (a) If one or more trump-suit cards were played, the highest-ranked trump wins. Exception: if both the Six and the Five of trump were played, the Six wins.\n   (b) If no trump was played, the highest-ranked card wins regardless of suit.\n   (c) If no trump was played and two or more cards tie for highest rank (same rank, different suits), nobody wins the trick. Each player captures their own played card, and the voting card is discarded with no one scoring it.\n5. Score the capture: for each captured card, add its points to the capturing player's tally for that card's suit. Normally the winner captures all 3 played cards plus the voting card.\n6. All played cards and every voting card ever flipped stay visible to everyone for the rest of the deal, along with all suit tallies.\n\nEND OF EACH DEAL (after tricks 6, 12, 18, 24):\n- For each suit, the player whose tally in that suit is 11 or more wins that suit's tribe and adds 1 to their tribe count.\n- A suit with no player at 11+ awards no tribe.\n- Announce everyone's tribe counts.\n\nEND OF MATCH: after trick 24 and its tribe scoring, apply the objective.",
    "objective": "The player with the most tribes after 4 deals wins. If two or more players tie for most tribes, the tied player with the highest sum of their three suit tallies in the 4th deal wins. If they are still tied, the game is a draw among the tied players.",
    "expected_effect": "Players must decide each deal which suit to concentrate on, since points beyond a decided majority, or spread thin, are wasted. They track which cards remain and save trumps for valuable voting cards. They hold a Six of trump to topple a Five, and dump low cards into tricks they expect to lose.\n\nSimple policies lose. Always-highest walks into trumps and Six upsets. Always-lowest captures almost nothing. Random play wastes points across suits.\n\nTalk passes both tests. The players disagree about who gets which suit, because only one player can win the match. A typical proposal is 'you take Hearts, I'll take Spades, we both starve the leader.' A player who simply follows can be betrayed: the proposer may secretly play for the same suit, or let the follower spend high cards so the proposer wins later tricks. Messages can also bluff about which trumps a player holds.\n\nFour deals and the shared, visible information mean a bad hand in one deal can be offset by better counting and better reading of the other two players. Deliberately denying a leader their 11th point is often worth more than taking points yourself."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 2,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 24
  }
}
```
````
