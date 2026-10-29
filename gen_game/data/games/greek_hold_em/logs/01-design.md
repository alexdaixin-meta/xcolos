# 01 design

- time: 2026-10-28T01:40:11+00:00 (87.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b21760474e42c6f2, reply sha256 04374fe3409b3db2

## Sent

````
Original game: Greek hold 'em
Players in the original: 2 to 10

Original rules:
Each player is dealt two private hole cards and there is a board of five community cards dealt in stages with betting rounds between. At showdown each remaining player must form the best five-card poker hand using exactly both of their hole cards combined with exactly three cards from the board. The highest standard poker hand wins the pot. Betting, folding, calling and raising follow the same structure as Texas hold 'em and Omaha. If all but one player folds, the last player wins without showdown.
````

## Reply

````
```json
{
  "original_summary": "Greek hold 'em is a community-card poker variant. Each player holds two private hole cards, and five shared board cards are revealed in stages with betting rounds between them. At showdown a hand must use exactly both hole cards plus exactly three board cards, and the best standard poker hand takes the pot unless everyone else has folded.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. Always-fold bleeds blinds. Always-raise is beaten by calling it with above-average hands. Always-call is beaten by value betting without bluffing. Position (the dealer button) gives a real seat edge within a hand, but it rotates, so it evens out over many hands."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Over many hands, skill dominates poker. Over the short session a platform can run, the card deal swings single results heavily. Unlimited raising also lets one big all-in pot decide everything."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Hand reading, bluffing, sizing and opponent profiling leave a very high ceiling. A weak player still wins pots with good cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hole cards are hidden. Players must infer opponents' holdings from their bets and the board texture, and plan across betting streets."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "The result is arithmetic in principle. But best-five-card poker evaluation under the exactly-2-plus-exactly-3 constraint (straights, flushes, kickers) is a long rule chain the engine cannot evaluate cheaply. It would lean on a referee to rank hands."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Betting is open-ended sequential raising with a variable number of actions per street, which a flat step list cannot express. There are four betting streets, more than the 4 choice steps allowed per round. Poker hand ranking needs dozens of steps, and side pots add more state."
    }
  ],
  "problems": [
    "P1: Open-ended sequential raise/re-raise loops cannot be built in a flat step list, and four betting streets exceed the 4-choice-step limit.",
    "P2: Standard poker hand ranking (suits, straights, flushes, kickers, best 5 of 7 with the Greek constraint) is far too long a rule chain to compute arithmetically. It would need a referee to decide the winner.",
    "P3: Unlimited bet sizes let one all-in pot decide a short session, so luck swamps skill in the number of hands the platform can play.",
    "P4: Acting position within a betting round gives a seat-based edge in any single hand.",
    "P5: Side pots and all-in handling add state and steps without adding much reasoning."
  ],
  "changes": [
    {
      "what": "Two betting stages per hand instead of four: one after the 3-card flop and one after the last 2 board cards. Each stage is a simultaneous sealed bet of 0–4 chips, followed by a simultaneous call-or-fold for everyone who bet less than the highest bet.",
      "why": "This gives a fixed 4 choice steps per hand while keeping betting, raising (bidding high), calling and folding.",
      "fixes": "P1: Open-ended sequential raise/re-raise loops cannot be built in a flat step list, and four betting streets exceed the 4-choice-step limit."
    },
    {
      "what": "The 52-card deck is replaced by 32 numbered cards (values 1–8, four copies each). Hand strength becomes a single formula: Strength = 20 × min(matches, 3) + 30 × (hole pair ? 1 : 0) + hole1 + hole2, where 'matches' counts board cards equal in value to either hole card.",
      "why": "This keeps the Greek rule that both hole cards always play and at most three board cards count. Pairing the board with your hole cards is what makes a hand strong. It is computable in one calculation.",
      "fixes": "P2: Standard poker hand ranking (suits, straights, flushes, kickers, best 5 of 7 with the Greek constraint) is far too long a rule chain to compute arithmetically. It would need a referee to decide the winner."
    },
    {
      "what": "Bets are capped at 4 chips per stage and the ante is 1. Stacks start at 40. The session is 15 hands, and the winner is the highest stack.",
      "why": "Each hand can move at most 9 chips per player. Many hands decide the game, so consistent reading and betting beats one lucky deal.",
      "fixes": "P3: Unlimited bet sizes let one all-in pot decide a short session, so luck swamps skill in the number of hands the platform can play."
    },
    {
      "what": "All betting decisions are simultaneous polls, so there is no button or acting order.",
      "why": "No seat ever acts with more information than another.",
      "fixes": "P4: Acting position within a betting round gives a seat-based edge in any single hand."
    },
    {
      "what": "There are no side pots. A player who cannot cover a call puts in their whole stack and stays in for the whole pot. A player with 0 chips is eliminated.",
      "why": "This removes side-pot bookkeeping. With a 4-chip cap and 40-chip stacks the case is rare and late.",
      "fixes": "P5: Side pots and all-in handling add state and steps without adding much reasoning."
    }
  ],
  "keeps": [
    "Two private hole cards per player and a shared five-card board revealed in stages.",
    "The Greek constraint: both hole cards always play, and exactly three board cards are used (at most three matches count).",
    "Betting rounds between board reveals, with folding, calling and raising (bidding above others).",
    "Winning a pot either at showdown or when everyone else folds, and bluffing and hand-reading as the core skill."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The hidden-information betting core is excellent for reasoning. Only the open raise loops and poker hand ranking need replacing with fixed simultaneous betting stages and an arithmetic hand score."
  },
  "variation": {
    "name": "Greek Hold 'em Lite",
    "summary": "A fixed-structure poker game for 3–5 players. Each hand has two private cards, a five-card board revealed 3 then 2, and two simultaneous sealed betting stages with call-or-fold. Hand strength is an arithmetic score built from pairing your two hole cards with the board.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "SETUP: Each player starts with 40 chips. The deck has 32 cards: values 1 to 8, four copies of each value. The game lasts 15 hands (rounds). There is no dealer or acting order; every decision is made simultaneously.\n\nEACH HAND:\n1. Ante and deal. Every player still in the game puts 1 chip into the pot (a player with only 1 chip is then all-in). The deck is shuffled. Each player is dealt 2 hole cards, seen only by that player, and 5 board cards are set face down. Any pot left over from the previous hand stays in the pot.\n\n2. Flop. The first 3 board cards are revealed to everyone.\n\n3. Flop bet. Every player in the hand secretly chooses a bet of 0, 1, 2, 3 or 4 chips (never more than their stack). All bets are revealed together and paid into the pot. Call the largest bet H.\n\n4. Flop call or fold. Each player whose bet was less than H chooses simultaneously:\n   - CALL: pay the difference so their bet equals H. If they have fewer chips, they pay their whole stack and stay in.\n   - FOLD: they are out of this hand, and chips already put in stay in the pot.\n   Players who bet H stay in automatically.\n\n5. If only one player remains in the hand, they take the whole pot and the hand ends (skip to step 10).\n\n6. Turn and river. Board cards 4 and 5 are revealed.\n\n7. River bet. This is the same as step 3: a simultaneous secret bet of 0–4 chips by every player still in the hand.\n\n8. River call or fold. This is the same as step 4.\n\n9. Showdown. If only one player remains, they take the pot. Otherwise every remaining player reveals their hole cards and their Strength is computed:\n   - matches = the number of the 5 board cards whose value equals either of the player's hole card values. If both hole cards share a value, a board card of that value counts once.\n   - matches counts at most 3, because a hand uses exactly three board cards.\n   - pair = 1 if the two hole cards have the same value, else 0.\n   - Strength = 20 × min(matches, 3) + 30 × pair + (hole card 1 value) + (hole card 2 value).\n   The highest Strength takes the pot. If several players tie for highest, the pot is split equally among them in whole chips, and any leftover chip stays in the pot for the next hand.\n\n10. Elimination. Any player with 0 chips is eliminated and takes no further part.\n\nEND: The game ends after hand 15, or earlier if only one player has chips left.",
    "objective": "When the game ends, the player with the most chips wins. If two or more players tie for the most chips, those players draw. If only one player has chips left before hand 15, that player wins.",
    "expected_effect": "Play becomes a compact poker duel of inference. A large flop bet after a 6 appears suggests a 6 in hand. A small bet that then calls may be a drawing hand or a trap. Players must size bets to extract value from weaker hands without revealing strength, bluff on boards that look like they hit someone, and fold well. Simple policies all lose to adaptive play: always-4 is called down by better hands, calling stations are value-bet, and always-fold bleeds antes. Capped bets over 15 hands make the deal matter per hand but not for the match, so the stronger reader wins most matches. Simultaneous betting removes positional edge. Talk is deliberately left out. Bets already serve as the signalling and bluffing channel, and a talk phase would cost a choice step beyond the limit without adding a new conflict to reason about."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 15
  }
}
```
````
