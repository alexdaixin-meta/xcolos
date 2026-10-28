# 10 design

- time: 2026-10-28T01:52:37+00:00 (129.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 a394bddf665535c9, reply sha256 98059acaede5de3c

## Sent

````
Original game: Greek hold 'em
Players in the original: 2 to 10

Original rules:
Each player is dealt two private hole cards and there is a board of five community cards dealt in stages with betting rounds between. At showdown each remaining player must form the best five-card poker hand using exactly both of their hole cards combined with exactly three cards from the board. The highest standard poker hand wins the pot. Betting, folding, calling and raising follow the same structure as Texas hold 'em and Omaha. If all but one player folds, the last player wins without showdown.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rebalance the betting so that always betting the maximum is not a dominant strategy. Options:
(1) Remove the fold option. Every player still in the hand matches H, possibly all-in, and the showdown always decides. Bets then raise the stakes but cannot win pots alone, so card strength matters.
(2) Alternatively, make folding cheap and over-betting costly. For example, a folder recovers half of what they bet, or the highest bettor's excess over the second-highest bet is returned and not at risk.
(3) Shrink the bet range, for example 0–2, and increase the ante or the pair and match weights so the showdown dominates the outcome.
(4) Order the options so that 'last' is not automatically the most aggressive choice.
Then re-run the thoughtless-policy checks: first and last at each seat should win at roughly the random rate. Also check that seat 1 has no edge.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the last option as seat 1 wins 95% of decided matches against random seats
- against random seats the results were {'seat 1': 23, 'seat 3': 20, 'seat 2': 15, 'seats 1 and 2': 1, 'seats 1 and 3': 1}
- a thoughtless policy `first@seat1`: won 32, lost 27, drew 1
- a thoughtless policy `first@seat2`: won 39, lost 20, drew 1
- a thoughtless policy `last@seat1`: won 56, lost 3, drew 1
- a thoughtless policy `last@seat2`: won 50, lost 9, drew 1

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Greek hold 'em is a community-card poker variant for 2 to 10 players. Each player holds two private cards and must make a five-card hand from exactly both hole cards plus exactly three of the five board cards. Several rounds of Texas-style betting (bet, call, raise, fold) take place as the board is revealed. The best hand at showdown, or the last player not to fold, takes the pot.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the tested adaptation the most aggressive option dominated. Always taking the last option won 56-3 from seat 1 and 50-9 from seat 2 against random seats, 95% of decided matches. The cause was folding: aggression wins pots outright whenever opponents fold, whatever the cards. Even always taking the first option beat random play (39-20 from seat 2). Seat 1 won 23 matches against 15 for seat 2, which points to an edge from the order of the betting turns."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Real poker rewards skill over many hands. In the adaptation, however, a policy with no thought (always bet the maximum) beat random players almost every time. Results therefore measured willingness to push, not judgement of hand strength or of opponents."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Poker has deep headroom: bet sizing by hand strength, reading opponents' betting, bluffing and slow-playing. A weak player still wins individual hands through the cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hole cards are hidden and the board arrives in stages. Players must estimate their hand's relative strength and infer opponents' holdings from their bets. The board-reading this needs is the core of the game."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "The winner follows from chip counts. However, full poker hand ranking with a choice of three board cards out of five is a long rule chain, which invites evaluation errors on the platform."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is text-only and turn-based. But open-ended raising rounds, up to 10 players, sequential action order and full hand evaluation exceed the step and choice limits. Sequential betting also produced a seat effect."
    }
  ],
  "problems": [
    "Folding lets aggression win pots without a showdown, so always betting the maximum beats random or passive opponents regardless of cards (last@seat1 won 56-3).",
    "The last option in each list was the most aggressive one, so the 'always last' thoughtless policy equalled 'always max', the dominant line.",
    "Sequential betting gave seat 1 an edge (23 wins against 15 for seat 2), because acting order mattered.",
    "Open-ended raise and re-raise rounds need too many steps and choices for the engine.",
    "Full poker hand ranking with a free choice of three of five board cards is a long rule chain that is error-prone to build and to evaluate.",
    "With folds and a single shared pot, a winning bet takes everything the opponents committed. Over-betting is therefore cheap when it works and is never punished by a careful opponent who simply declines to match."
  ],
  "changes": [
    {
      "what": "Remove folding. Every player always reaches the showdown. Instead of matching one shared bet, each player chooses their own stake, and every pair of players settles on the smaller of their two stakes: the better hand takes that amount from the worse.",
      "why": "Bets can no longer win without cards. Betting high with a weak hand costs exactly as much as it wins with a strong one, so blind maximum betting has zero expected value. A player who stakes high only when strong beats it, by staking low when weak and taking the full amount when the blind bettor is weak.",
      "fixes": "Folding lets aggression win pots without a showdown, so always betting the maximum beats random or passive opponents regardless of cards (last@seat1 won 56-3)."
    },
    {
      "what": "Stakes are capped at 0 to 2 per betting phase (0 to 4 per hand). A fixed ante pot of 9, 3 from each player, always goes to the best hand.",
      "why": "The ante pot is common to all, so it dilutes the extra variance that an always-maximum player takes on in a highest-total race. The small, bounded stakes keep any one hand from swinging the match.",
      "fixes": "With folds and a single shared pot, a winning bet takes everything the opponents committed. Over-betting is therefore cheap when it works and is never punished by a careful opponent who simply declines to match."
    },
    {
      "what": "Both betting phases are simultaneous polls. The stage-1 stakes are announced before stage 2.",
      "why": "No seat acts first or last, which removes the order advantage. Revealing stage-1 stakes keeps a reason to read and to manage signals: bluff high early, or slow-play low early and raise late.",
      "fixes": "Sequential betting gave seat 1 an edge (23 wins against 15 for seat 2), because acting order mattered."
    },
    {
      "what": "Replace the raise rounds with exactly two simultaneous stake choices per hand (options listed 0, 1, 2).",
      "why": "This fits the engine: two choice steps plus talk. Always-last (stake 2) is now a zero-expectation gamble that careful betting exploits, not a winning policy.",
      "fixes": "Open-ended raise and re-raise rounds need too many steps and choices for the engine."
    },
    {
      "what": "Replace poker hand ranking with an arithmetic hand score. The score is the sum of the two hole ranks, plus 6 if the hole cards are a pair, plus 4 for each board card that matches a hole rank, counting at most 3 board cards.",
      "why": "Scoring is computable in one step with no referee. It keeps the Greek rule (both hole cards always count, at most three board cards count), and pairs and board matches trade off at comparable value.",
      "fixes": "Full poker hand ranking with a free choice of three of five board cards is a long rule chain that is error-prone to build and to evaluate."
    },
    {
      "what": "Fix the game at 3 players. Add one simultaneous table-talk message per hand, after the full board is revealed and before the final stake.",
      "why": "Three players keeps pairwise settlement small. Talk adds bluffing and reading, because only one player can win and each wants rivals to misjudge the matchup.",
      "fixes": "Sequential betting gave seat 1 an edge (23 wins against 15 for seat 2), because acting order mattered."
    }
  ],
  "keeps": [
    "Two private hole cards per player, both of which always count, and a shared board of which at most three cards can count: the Greek hold 'em constraint.",
    "A staged board reveal with betting before and after the rest of the board appears.",
    "Antes, a showdown, and chips moving from weaker hands to stronger ones in proportion to what was bet.",
    "Hidden information, bet sizing by hand strength, bluffing and slow-playing, and reading opponents from their bets and revealed hands.",
    "A chip race over many hands with the highest total as the winner."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The betting failure came from folding, sequential action and aggressive option order. A no-fold, pairwise-settled, simultaneous stake structure fixes all three while keeping the hold 'em feel, and it fits the limits."
  },
  "variation": {
    "name": "Greek Hold 'em Showdown",
    "summary": "This is a 3-player, 10-hand poker race with no folding. Each player holds two private cards that both count, and up to three board cards can add to a hand. The board is revealed in two stages, with a simultaneous stake before and after the second reveal. Every pair of players settles at the smaller of their two stakes, so betting big pays only when your hand really is stronger.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP. Three players. Each starts with a chip total of 0; totals may go negative. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. The game lasts exactly 10 hands.\n\nEACH HAND:\n1. Deal. Shuffle all 18 cards (the one random event of the hand). Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.\n2. Ante. Each player pays 3 chips into the pot, so the pot is 9.\n3. First board. Board cards 1 and 2 are turned face up for everyone.\n4. Stake 1. All players at the same moment secretly choose a first stake of 0, 1 or 2 chips.\n5. All three first stakes are announced.\n6. Second board. Board cards 3 and 4 are turned face up.\n7. Table talk. All players at the same moment write one short message, which may be true, false or empty. All messages are then shown to everyone. Talk binds no one.\n8. Stake 2. All players at the same moment secretly choose a second stake of 0, 1 or 2 chips. A player's stake for the hand is first stake plus second stake, from 0 to 4.\n9. Hand scores. Each player's score is computed from their two hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 times the number of matches. A match is a board card whose rank equals a or b; count at most 3 matches, because exactly three board cards may count. All hole cards, stakes and scores are revealed.\n10. Ante pot. The player with the uniquely highest score takes the 9-chip pot. If two players tie for highest, each takes 4.5. If all three tie, each takes 3 back.\n11. Pairwise settlement. For each of the three pairs of players (1 and 2, 1 and 3, 2 and 3), compare scores. If one score is higher, that player takes from the other an amount equal to the smaller of their two stakes. If the scores are equal, nothing moves.\n12. All chip totals are announced.\n\nEND. After hand 10 the game ends.",
    "objective": "After 10 hands the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.",
    "expected_effect": "With no folding, bets can only win through better cards, so always staking the maximum is a zero-expectation gamble. Careful players exploit it by staking 0 with weak hands and 4 with strong ones, while always staking 0 just bleeds antes. Simultaneous polls remove any seat advantage. Skill shows in judging relative hand strength after the partial and full board. It also shows in reading the announced first stakes and the revealed hands of earlier hands, to spot bluffers and slow-players. Players must manage their own signals too: a high first stake can scare rivals into small second stakes, and a low first stake can disguise a monster. Late in the match, trailing players must take calculated risks. Talk passes both tests because only one player can win and every player wants rivals to misjudge the matchup. A strong hand wants opponents to stake high, and a weak hand wants them to stake low. A player who simply follows another's claim ('I have nothing, bet small') can lower their stake against a strong hand and lose value, or raise into a bluff-free monster and lose up to 4 chips to that player."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
