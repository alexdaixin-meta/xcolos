# 14 design

- time: 2026-10-28T01:58:13+00:00 (87.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 577d3ea832cb07e6, reply sha256 d677c16bc6e7e917

## Sent

````
Original game: Greek hold 'em
Players in the original: 2 to 10

Original rules:
Each player is dealt two private hole cards and there is a board of five community cards dealt in stages with betting rounds between. At showdown each remaining player must form the best five-card poker hand using exactly both of their hole cards combined with exactly three cards from the board. The highest standard poker hand wins the pot. Betting, folding, calling and raising follow the same structure as Texas hold 'em and Omaha. If all but one player folds, the last player wins without showdown.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: Once board cards 3-4 are turned, each player knows their exact final score. The only unknown is the 2 opponents' hole cards. The decision tree is very shallow: one open from {0,1,2}, one simultaneous FOLD/CALL/RAISE, and one CALL/FOLD response.

Because the decision is simultaneous and the response faces about 15% pot-odds thresholds, bluff raises almost never generate folds. Raising is essentially value-only, and good play collapses to near-fixed strength thresholds that any competent model finds quickly. There is little room for opponent modelling to change outcomes.

Rough variance estimate:
- Per-hand swing for a contested player: ±4-5 chips, so σ ≈ 4 per hand and ≈ 14 over 12 hands.
- Realistic skill edge of a good player over a mediocre one: about 0.3-0.5 chips per hand, or 4-6 over the game.
- Edge/σ ≈ 0.3-0.4, giving a skilled player roughly 40-45% to win against two weaker players versus a 33% baseline.

That is not clearly favoured, and card luck decides most games. When all three play the intended threshold strategy, the result is decided purely by which player is dealt the best hands across 12 deals. Good play cannot overcome a bad deal here.

There is something to infer (opening bets made after seeing half the board, card removal from the 18-card deck, talk). But the payoff to that inference is small relative to the shuffle.
- change: Reduce card luck structurally. Either (a) play 36 hands (within the 40 limit) so the per-game edge/σ roughly doubles, or (b) use duplicate dealing: store each shuffle and replay it for 3 consecutive hands with hole hands rotated among seats, so each player plays every hand once. This needs list attributes within the 20 limit.
- change: Keep real uncertainty at the decision. Turn only board card 3 before step 7/8 and reveal board card 4 at showdown, so scores are not fully known when deciding and both bluffing and hand-reading matter.
- change: Give raises fold equity. Make the raise 4 instead of 2, and/or make the step-8 decision sequential in a seat order that rotates each hand. Raises then come before others act, players respond with information, and opponent modelling is rewarded beyond fixed hand-strength thresholds.
- change: After the changes, re-verify that always-open-2/always-raise and never-fold still lose most games to sensible play, and that a threshold-plus-reading player beats a pure threshold player clearly (e.g. ≥55% in 3-player simulation).
The variation that was reviewed: Greek Hold 'em Mini: SETUP. Three players. Each starts with a chip total of 0; totals may go negative and may include fractions from split pots. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. A table 'carry' amount starts at 0. The game lasts exactly 12 hands.

EACH HAND:
1. Deal. Shuffle all 18 cards; this is the one random event of the hand. Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.
2. Ante. Each player pays 1 chip into the pot. The pot is 3 plus the current carry, and the carry then resets to 0.
3. First board. Board cards 1 and 2 are turned face up for everyone.
4. Opening bet. All players at the same moment secretly choose an opening bet of 0, 1 or 2 chips.
5. All three opening bets are paid into the pot and announced. Let H be the highest opening bet.
6. Second board. Board cards 3 and 4 are turned face up.
7. Table talk. All players at the same moment write one short message, which may be true, false or empty. All messages are then shown to everyone. Talk binds no one.
8. Decision. All players at the same moment choose one of three options.
   FOLD: the player is out of the hand and loses everything already paid.
   CALL: the player pays H minus their own opening bet, so their bet equals H.
   RAISE: the player pays H minus their own opening bet, plus 2 more.
9. All decisions are revealed and the payments go into the pot.
10. Raise response. This step happens only if at least one player chose RAISE and at least one player chose CALL. Each player who chose CALL now chooses, at the same moment, CALL THE RAISE (pay 2 more into the pot) or FOLD (out of the hand, losing everything paid). Players who raised or folded do not act. If two or three players raised, they have paid equal amounts and do not act again.
11. Raise responses are revealed and payments go into the pot.
12. Hand scores. Each player's score is computed from their two hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 times the number of matches. A match is a board card whose rank equals a or b. At most 3 matches count, because a hand may use only three board cards. (A pair can have at most one match, since only three copies of each rank exist.) Scores range from 3 to 23.
13. Showdown. If two or three players are still in the hand, their hole cards and scores are revealed and the pot goes to the highest score among them. If tied players share the highest score, they split the pot equally. If exactly one player is still in, that player takes the whole pot and no cards are revealed. If all three folded, the whole pot becomes the carry and is added to the next hand's pot. If this happens in hand 12, the pot is removed from the game.
14. Folded players' hole cards are never revealed.
15. Totals. Each player's total changes by the chips they won minus the chips they paid this hand. All chip totals are announced.

END. After hand 12 the game ends. Winner: After 12 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Greek hold 'em is a poker variant. Each player holds two private hole cards and must use both of them with exactly three of five community cards, with Texas hold 'em style betting rounds between the board stages. The previous XColos adaptation, Greek Hold 'em Mini, cut it to three players, an 18-card numeric deck, 12 hands, a simultaneous 0/1/2 opening bet, a simultaneous FOLD/CALL/RAISE decision after the whole board was visible, and a raise response.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy dominates. Always-raise gets called by strong hands, and never-fold pays off value bets. Seats were symmetric because all decisions were simultaneous, and choices do change pots."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Over 12 hands, σ ≈ 14 chips against a realistic skill edge of 4-6 chips gives edge/σ ≈ 0.3-0.4. A skilled player wins about 40-45% against two weaker players, versus 33% by chance. Card luck decides most games."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "With every board card visible before the main decision, each player knew their exact final score. Good play collapses to fixed strength thresholds that a competent model finds quickly, leaving little to improve beyond that."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Opponents' hole cards were hidden, but the simultaneous decision made bluff raises almost never win a fold, so reads hardly changed outcomes. The payoff to inference was small next to the shuffle."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Hand scores follow from a stated formula, and pots and totals are plain arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is text-only and turn-based, with one shuffle per hand, a small numeric deck and no board geometry. It fits within the step and attribute limits."
    }
  ],
  "problems": [
    "P1: Luck swamps skill. 12 hands is too few, and edge/σ ≈ 0.35 means the deal decides most games.",
    "P2: No uncertainty at the decision. All four board cards were visible before the main bet, so each player knew their exact score and the only open question was opponents' hole cards. Play reduced to fixed thresholds.",
    "P3: Bets had no fold equity. The decision was simultaneous and the raise of 2 was small against the pot, so bluffs almost never won a fold and raising was value-only.",
    "P4: No positional or sequential information. Nobody acted after seeing what others did within a betting round, so opponent modelling had little to work with.",
    "P5: The talk step cost time and steps but added little. Claims are free and unverifiable, and the bets themselves already carry the signal.",
    "P6: The carry rule (all three fold) and the multi-stage opening-bet-then-raise structure added steps and edge cases without adding decisions worth making."
  ],
  "changes": [
    {
      "what": "Play 36 hands instead of 12.",
      "why": "Per-game edge/σ grows with the square root of the number of hands, about 1.7× from length alone. Combined with the larger per-hand edge from the other changes, a skilled player should be clearly favoured. Duplicate dealing was rejected because replaying a shuffle with rotated hole hands tells players the other hands they held earlier, which leaks hidden information.",
      "fixes": "P1"
    },
    {
      "what": "Only board cards 1-3 are face up when betting; board card 4 stays face down until showdown.",
      "why": "A hand can still gain 4 points if card 4 matches, so draws, card-removal reasoning and bluffing against possible improvement all matter. Hand strength is no longer certain.",
      "fixes": "P2"
    },
    {
      "what": "Replace the simultaneous opening bet and FOLD/CALL/RAISE decision with one sequential betting round. Each player, in an order that rotates each hand, chooses CHECK, BET 2 or BET 4 until someone bets. Later players then CALL or FOLD, and players who checked earlier respond with CALL or FOLD.",
      "why": "A bet of 2 or 4 into a pot of 3 gives real fold equity. A bluff of 4 needs both others to fold only about 57% of the time, and a bluff of 2 about 40%. Players act on others' visible actions. Bet sizing becomes a signal that can be honest or deceptive. Check-then-call traps and stealing from the last seat become real options.",
      "fixes": "P3"
    },
    {
      "what": "The first actor rotates every hand, so each seat acts first 12 times, second 12 times and last 12 times.",
      "why": "Sequential order creates positional information to exploit, and the rotation keeps seats balanced.",
      "fixes": "P4"
    },
    {
      "what": "Remove the table-talk step.",
      "why": "In this zero-sum poker game talk is cheap and unverifiable. Bets already serve as costly, credible communication. Dropping talk shortens a 36-hand game and saves steps.",
      "fixes": "P5"
    },
    {
      "what": "Remove the carry and the separate raise stage. Because a bettor can never fold, the pot always goes to someone.",
      "why": "This simplifies the build. The step count per hand falls to 15 and choice steps to at most 4 while keeping every meaningful decision.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Two private hole cards per player, both of which must be used.",
    "Exactly three board cards count, so a hand scores at most three matches.",
    "Community cards revealed in stages, with betting while some cards are still unknown.",
    "Betting, calling and folding, with the last player in winning without a showdown.",
    "The compact 18-card numeric deck and the established scoring formula, which keep it a game of hand strength, reads and bluffs."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game's core of hidden hole cards, a partly hidden board, and betting with bluff and fold equity is good strategic material. The previous version's flaws (too few hands, no uncertainty at the decision, no fold equity) are fixable within the limits."
  },
  "variation": {
    "name": "Greek Hold 'em Mini II",
    "summary": "This is a three-player, 36-hand numeric poker game. Each hand has one sequential betting round, played with three board cards visible and a fourth board card still hidden. Bets of 2 or 4 into a pot of 3, a rotating action order and an unseen last card make bluffing, hand-reading and position matter. The longer game lets skill outweigh the shuffle.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP. Three players, numbered 1, 2 and 3. Each starts with a chip total of 0. Totals may go negative and may include fractions from split pots. The deck has 18 cards: ranks 1, 2, 3, 4, 5 and 6, three copies of each, with no suits. The game lasts exactly 36 hands. In hand h, the FIRST ACTOR is player ((h - 1) mod 3) + 1. The SECOND ACTOR is the next player after the first actor (wrapping from 3 to 1), and the THIRD ACTOR is the remaining player.\n\nEACH HAND:\n1. Deal. Shuffle all 18 cards; this is the only random event of the hand. Deal 2 hole cards face down to each player and 4 board cards face down to the table. Each player sees only their own hole cards.\n2. Ante. Each player pays 1 chip into the pot. The pot starts at 3.\n3. Board. Board cards 1, 2 and 3 are turned face up for everyone. Board card 4 stays face down.\n4. First actor's choice: CHECK, BET 2 or BET 4. A bet is paid into the pot at once, and the choice is announced to all.\n5. Second actor's choice, announced to all. If nobody has bet yet, the choices are CHECK, BET 2 or BET 4. If a bet has been made, the choices are CALL (pay the same amount as the bet into the pot) or FOLD (leave the hand, losing everything already paid).\n6. Third actor's choice, with the same options as the second actor, announced to all.\n7. Response. This step happens only if a bet was made after at least one player checked. Each player who checked before the bet chooses, at the same moment, CALL (pay the bet amount) or FOLD. The choices are then revealed. Only one bet is ever made in a hand: there are no raises, and the bettor never acts again.\n8. Final board. Board card 4 is turned face up.\n9. Hand scores. Each player's score is computed from their hole cards (ranks a and b) and the 4 board cards. Score = a + b, plus 6 if a equals b, plus 4 for each match. A match is a board card whose rank equals a or b. At most 3 matches count, because a hand may use only three board cards.\n10. Showdown. The players still in the hand are those who did not fold. If exactly one player is still in, that player takes the whole pot and no hole cards are revealed. If two or three are still in, their hole cards and scores are revealed, and the pot goes to the highest score among them. Players tied for the highest score split the pot equally. If everyone checked, all three go to showdown.\n11. Folded players' hole cards are never revealed.\n12. Totals. Each player's total changes by the chips they won minus the chips they paid this hand. All three totals are announced.\n13. All cards return to the deck for the next shuffle.\n\nThe sum of all totals is always 0.\n\nEND. After hand 36 the game ends.",
    "objective": "After 36 hands, the player with the highest chip total wins. If two or three players share the highest total, the game is a draw among them.",
    "expected_effect": "Players can no longer know their exact score when they bet. Card 4 can add 4 points, so paired-with-board hands and hands needing a match play differently. Bets now carry real fold equity: a 4-chip bluff into 3 needs folds only about 57% of the time. This rewards bluffing, check-calling traps, stealing from the third seat after two checks, and reading bet size as a strength signal. Position rotates, so no seat is favoured.\n\nSimple policies all lose. Always-check/always-call gets value-bet without ever winning folds. Always-bet-4/always-call bleeds chips when strong hands call. Always-fold-to-bets is stolen from every hand. Random play loses to all of these.\n\nSo the outcome is not decided by the deal when everyone plays well. Even when all three play sensible threshold strategies, sequential bets with a hidden last card mean a player who reads opponents' bet sizes and frequencies, and adjusts bluffing to who still has to act, should gain more than a pure threshold player. A rough estimate is a skill edge of 0.5-0.8 chips per hand, about 18-29 over the game, against σ ≈ 20, for about a 55-65% win rate against two weaker players. This should be confirmed by 3-player simulation.\n\nThe chip lead also creates multi-hand planning. A leader late in the game can tighten up, but the ante makes passivity costly. Trailing players must take calculated risks.\n\nTalk is left out. Bets are the costly, credible signals here. Free messages in a zero-sum poker game would only add words, so they fail the reasoning test even though interests conflict."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
