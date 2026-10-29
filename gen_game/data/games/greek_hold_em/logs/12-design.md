# 12 design

- time: 2026-10-28T01:55:47+00:00 (66.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 49f72e763b9cfee4, reply sha256 e4f18bcde84a3ad3

## Sent

````
Original game: Greek hold 'em
Players in the original: 2 to 10

Original rules:
Each player is dealt two private hole cards and there is a board of five community cards dealt in stages with betting rounds between. At showdown each remaining player must form the best five-card poker hand using exactly both of their hole cards combined with exactly three cards from the board. The highest standard poker hand wins the pot. Betting, folding, calling and raising follow the same structure as Texas hold 'em and Omaha. If all but one player folds, the last player wins without showdown.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: SCORES: non-pair = a+b+4m (m capped at 3); pair = 2a+6+4m. A pair can have at most one match, because only 3 copies of each rank exist. Ranges: worst 1+2 = 3; best non-pair 5,6 with 3 matches = 11+12 = 23; best pair 6,6 with 1 match = 12+6+4 = 22. After board cards 3 and 4 are shown, each player knows their own score exactly. Only the opponents' scores are unknown.

PAIRWISE LAYER, one pair, my stake s against your stake t: if I score higher I gain min(s,t); if lower I lose min(s,t); if equal, 0. Example table with p = P(I score higher), excluding ties:
- s=0: expected gain 0 against any t.
- s=2, t=0: 0.
- s=2, t=2: 2(2p-1).
- s=4, t=4: 4(2p-1).
- s=4, t=1: 1(2p-1).
No option is strictly better for every opponent action, because the right stake depends on p.

THOUGHTLESS POLICIES under the winner rule:
(a) Always stake 4. Sensible opponents stake high only when strong. The always-4 player then loses up to 4 per opponent when behind and wins about 0 when ahead. It is clearly exploitable and loses, which is fine.
(b) Always stake 0. Its pairwise result is identically 0 every hand whatever anyone does, so it cannot be exploited at all. Its total is pure ante-pot luck. Per hand the ante pot gives the winner +6 (prob 1/3) and each loser -3 (prob 2/3), mean 0, sd about 4.24. Over 10 hands the sd is about 13.4.

Now take two sensible players and one always-0 player. The pairwise game between the two sensible players is symmetric and zero-sum, so each expects 0 from it. The always-0 player also expects 0. All three therefore have identical expected totals, and the always-0 player wins about 1/3 of games, the same as correct play. Skilful staking earns nothing over the 'always pass' policy unless an opponent blunders. Under the min(stakes) rule, anyone can opt out of the reasoning layer at zero cost.

There is also no fold, so a bluff can never win the ante pot. A bluff can only lose stake, which makes deception strictly worse than honest staking.

Seats: fully symmetric and simultaneous, so there is no seat edge. All players can win.

The game fails because the thoughtless 'always pass' policy is unexploitable and matches sensible play in expectation.
- reasoning_over_luck FAILED: With no fold, the 9-chip ante pot goes to the best card score every hand. That alone gives an outcome sd of about 13.4 chips over 10 hands, decided entirely by the deal.

Under the intended good strategy (stake rising with your own score, lowered when opponents' first stakes signal strength), chips flow in the pairwise layer as min(stakes) toward the better hand. That is again card strength.

So when all three play well, both the pot and the transfers go to whoever was dealt better hands, and the winner is decided by the shuffle.

Skill shows only against a player who stakes high when weak. Even then, the always-0 shield gives a non-reasoner the same expectation as a reasoner. There is some inference, from announced first stakes and talk, but no way to turn it into winning a hand you would otherwise lose. You can only shrink or enlarge a transfer that the cards have already decided. Rough estimate: over 80% of the result among competent players is chance.
- change: Add a fold decision: at stake 2, players may fold. Folders forfeit their ante and stakes and cannot win the pot. The ante pot goes to the best score among non-folders, and a lone non-folder wins it without comparison. This makes bluffing and reading signals able to win hands the cards would lose.
- change: Replace the min(stakes) pairwise rule with stakes paid into a common pot. Each player pays their full stake, and the pot goes to the best remaining hand. Staking 0 then forfeits pot equity and is no longer an unexploitable shield.
- change: Require staying in to cost something. For example, a player who does not fold must stake at least the highest first stake announced, or fold. This forces a real call/fold decision against inferred strength.
- change: To cut deal luck, consider 15+ hands or a smaller ante relative to the stakes. Then verify that 'always 0 / always fold', 'always max' and random staking each lose clearly to a sensible strategy over a full game.
The variation that was reviewed: Greek Hold 'em Showdown: SETUP. Three players. Each starts with a chip total of 0; totals may go negative. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. The game lasts exactly 10 hands.

EACH HAND:
1. Deal. Shuffle all 18 cards (the one random event of the hand). Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.
2. Ante. Each player pays 3 chips into the pot, so the pot is 9.
3. First board. Board cards 1 and 2 are turned face up for everyone.
4. Stake 1. All players at the same moment secretly choose a first stake of 0, 1 or 2 chips.
5. All three first stakes are announced.
6. Second board. Board cards 3 and 4 are turned face up.
7. Table talk. All players at the same moment write one short message, which may be true, false or empty. All messages are then shown to everyone. Talk binds no one.
8. Stake 2. All players at the same moment secretly choose a second stake of 0, 1 or 2 chips. A player's stake for the hand is first stake plus second stake, from 0 to 4.
9. Hand scores. Each player's score is computed from their two hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 times the number of matches. A match is a board card whose rank equals a or b; count at most 3 matches, because exactly three board cards may count. All hole cards, stakes and scores are revealed.
10. Ante pot. The player with the uniquely highest score takes the 9-chip pot. If two players tie for highest, each takes 4.5. If all three tie, each takes 3 back.
11. Pairwise settlement. For each of the three pairs of players (1 and 2, 1 and 3, 2 and 3), compare scores. If one score is higher, that player takes from the other an amount equal to the smaller of their two stakes. If the scores are equal, nothing moves.
12. All chip totals are announced.

END. After hand 10 the game ends. Winner: After 10 hands the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Greek hold 'em is a poker variant. Each player holds two private cards and must use exactly both of them with exactly three of five community cards dealt in stages, with Texas hold 'em-style betting, folding and raising between stages. The best hand at showdown, or the last player not to fold, wins the pot.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "The original is real poker. Always folding loses the blinds, always calling loses to value bets, and always raising gets called by strong hands. With proper betting no simple policy wins. The previous variation broke this: under the min(stakes) settlement, staking 0 every hand could not be exploited and matched skilled play in expectation. It also removed folding entirely."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Over many hands, poker skill (fold discipline, value betting, bluffing, reading) beats weaker play. The previous variation lost this. Without a fold, the pot always went to the best cards, and transfers only scaled card outcomes, so over 80% of the result was chance."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Poker is not solved for practical play. A strong player keeps improving through hand reading and bet sizing, and a weak player still wins hands on good cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hole cards are hidden, so players must infer opponents' holdings from their bets, decide whether to call or fold against inferred strength, and bluff. The previous variation had signals but no way to act on them, because a hand could not be won by making the better hand fold."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Hand ranking and pot awards are pure arithmetic once cards and actions are known."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Full poker is too heavy to build: a 52-card deck, standard hand ranking over 10 combinations of three board cards, unlimited re-raising, side pots, and 2 to 10 players. It needs simplification to a small deck, an arithmetic score and a bounded betting structure."
    }
  ],
  "problems": [
    "Previous variation: there was no fold, so the pot always went to the best cards. Bluffing and reading could never win a hand the cards would lose.",
    "Previous variation: the min(stakes) pairwise settlement let 'always stake 0' opt out of the reasoning layer at no cost. That policy was unexploitable and matched skilled play in expectation.",
    "Previous variation: staying in to showdown cost nothing, so there was never a real call-or-fold decision against an opponent's signalled strength.",
    "Previous variation: the 9-chip ante was large relative to stakes of at most 4, and 10 hands were too few. Deal luck dominated the outcome.",
    "Original: full standard poker hand ranking, a 52-card deck, unlimited raises, side pots and up to 10 players exceed what the engine can build reliably."
  ],
  "changes": [
    {
      "what": "Add folding. At the decision after the full board each player chooses Fold, Call or Raise, and a caller facing a raise must call it or fold. Folders lose everything they put in and cannot win the pot. A lone remaining player takes the pot without showing cards.",
      "why": "Hands can now be won by making a better hand fold, and a bluff can succeed. Reading bets can save chips, or win a pot the cards would have lost.",
      "fixes": "Previous variation: there was no fold, so the pot always went to the best cards. Bluffing and reading could never win a hand the cards would lose."
    },
    {
      "what": "Replace the pairwise min(stakes) settlement with a single common pot. Every chip bet goes into the pot, and the pot goes to the best remaining hand.",
      "why": "Not betting no longer shields a player. A player who never bets or always folds bleeds antes and loses every pot that others contest.",
      "fixes": "Previous variation: the min(stakes) pairwise settlement let 'always stake 0' opt out of the reasoning layer at no cost. That policy was unexploitable and matched skilled play in expectation."
    },
    {
      "what": "Staying in costs something. To remain after the full board a player must match the highest first bet, and a Raise adds 2 more that the others must match or fold.",
      "why": "This creates a genuine call/fold decision against inferred strength, and makes value betting and bluffing meaningful.",
      "fixes": "Previous variation: staying in to showdown cost nothing, so there was never a real call-or-fold decision against an opponent's signalled strength."
    },
    {
      "what": "Cut the ante from 3 to 1 per player, so the bets (up to 4 per player) dominate the pot. Raise the game length from 10 to 12 hands.",
      "why": "Most chips now move through decisions rather than the forced ante, and more hands average out the deal.",
      "fixes": "Previous variation: the 9-chip ante was large relative to stakes of at most 4, and 10 hands were too few. Deal luck dominated the outcome."
    },
    {
      "what": "Keep the 18-card deck (ranks 1 to 6, three copies each) and the arithmetic score built on the use-both-hole-cards-plus-three-board idea. Fix the game at 3 players, with one bounded first bet, one fold/call/raise decision and one raise response.",
      "why": "This stays inside the step and choice limits and needs no hand-ranking table or side pots.",
      "fixes": "Original: full standard poker hand ranking, a 52-card deck, unlimited raises, side pots and up to 10 players exceed what the engine can build reliably."
    }
  ],
  "keeps": [
    "Two private hole cards per player, and a hand that must use both hole cards together with at most three board cards.",
    "Community board cards revealed in two stages, with betting between them.",
    "Folding, calling and raising; a lone remaining player wins without showdown.",
    "Bluffing and reading opponents' bets as the core skill.",
    "Chips won and lost across many hands."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "With a real fold, a common pot, a cost to stay in and a small ante, the game becomes compact poker in which inference and bluffing decide pots, and it fits the engine's limits."
  },
  "variation": {
    "name": "Greek Hold 'em Mini",
    "summary": "Three-player, 12-hand mini poker. The deck has 18 cards and hands are scored by arithmetic from both hole cards plus board matches. Each hand has one opening bet, then talk, then a fold/call/raise decision and a response to any raise. Folding, bluffing and reading bets decide who takes each pot.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP. Three players. Each starts with a chip total of 0; totals may go negative and may include fractions from split pots. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. A table 'carry' amount starts at 0. The game lasts exactly 12 hands.\n\nEACH HAND:\n1. Deal. Shuffle all 18 cards; this is the one random event of the hand. Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.\n2. Ante. Each player pays 1 chip into the pot. The pot is 3 plus the current carry, and the carry then resets to 0.\n3. First board. Board cards 1 and 2 are turned face up for everyone.\n4. Opening bet. All players at the same moment secretly choose an opening bet of 0, 1 or 2 chips.\n5. All three opening bets are paid into the pot and announced. Let H be the highest opening bet.\n6. Second board. Board cards 3 and 4 are turned face up.\n7. Table talk. All players at the same moment write one short message, which may be true, false or empty. All messages are then shown to everyone. Talk binds no one.\n8. Decision. All players at the same moment choose one of three options.\n   FOLD: the player is out of the hand and loses everything already paid.\n   CALL: the player pays H minus their own opening bet, so their bet equals H.\n   RAISE: the player pays H minus their own opening bet, plus 2 more.\n9. All decisions are revealed and the payments go into the pot.\n10. Raise response. This step happens only if at least one player chose RAISE and at least one player chose CALL. Each player who chose CALL now chooses, at the same moment, CALL THE RAISE (pay 2 more into the pot) or FOLD (out of the hand, losing everything paid). Players who raised or folded do not act. If two or three players raised, they have paid equal amounts and do not act again.\n11. Raise responses are revealed and payments go into the pot.\n12. Hand scores. Each player's score is computed from their two hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 times the number of matches. A match is a board card whose rank equals a or b. At most 3 matches count, because a hand may use only three board cards. (A pair can have at most one match, since only three copies of each rank exist.) Scores range from 3 to 23.\n13. Showdown. If two or three players are still in the hand, their hole cards and scores are revealed and the pot goes to the highest score among them. If tied players share the highest score, they split the pot equally. If exactly one player is still in, that player takes the whole pot and no cards are revealed. If all three folded, the whole pot becomes the carry and is added to the next hand's pot. If this happens in hand 12, the pot is removed from the game.\n14. Folded players' hole cards are never revealed.\n15. Totals. Each player's total changes by the chips they won minus the chips they paid this hand. All chip totals are announced.\n\nEND. After hand 12 the game ends.",
    "objective": "After 12 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.",
    "expected_effect": "Chips now move mainly through the bets (up to 5 per player per hand against a 1-chip ante), and folding lets players take pots with weaker cards. After the full board each player knows their own score exactly, so the game turns on judging opponents' scores from their opening bets, their talk and their raises.\n\nThe simple policies all lose:\n- Always fold loses at least 1 chip a hand, about -12 over the game. Since the chips are zero-sum apart from the carry, at least one other player must be well ahead of it, so it cannot win.\n- Always call, never fold, pays raises with weak hands and loses to value raising.\n- Always bet 2 and raise gets called by better hands and loses.\n- Random play is exploitable on both counts.\n\nWhen everyone plays well, bluffs and well-timed folds shift pots away from pure card strength, and 12 hands average out much of the deal.\n\nTalk passes both tests. Every pot is contested and only one player can win the game, so interests always conflict. Messages are bluffs or truths about strength. A player who simply believes 'I'm weak, I'll fold' can be trapped by a slow-played strong hand, and one who believes 'I have a pair, fold now' gives up pots to bluffers. Talk is simultaneous, so nobody can tailor their message to another's."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 17,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
