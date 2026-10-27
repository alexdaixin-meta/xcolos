# 17 design

- time: 2026-10-27T21:35:06+00:00 (72.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 7e5cf3b318ec25e3, reply sha256 6668c9061567d0b9

## Sent

````
Original game: Durak
Players in the original: 2 to 6

Original rules:
Use 36 cards (6-A). Shuffle and deal 6 each. Turn bottom card face up to set trump suit; it stays as last draw card. Lowest trump attacks first. Attacker plays a card face up. Defender left of attacker must beat it with higher same suit or any trump. If beat, other players clockwise may add new attack cards matching any rank already on table, up to 6 total attacks. Original attacker has priority to add, then clockwise non-defenders. Defender must beat each new card. If defender beats all and no one adds, all table cards go to discard and defender becomes next attacker. If defender fails, they take entire table into hand. Others may then add matching ranks for defender to also take, up to 6. Next attacker is left of defender. After each bout, players draw to 6: main attacker first, then other attackers clockwise, then defender. When talon empty, players out of cards are eliminated. Last player with cards is durak, loser.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Make every random operation go through the engine's seeded shuffle or draw, and use it only at S1, once per deal. Do not use any time-based value, external random source, or unseeded pick. Build the 36-card deck as an ordered game list, Clubs to Spades and rank 6 to 14 within each suit, then shuffle that list with the seeded operation. Deal cards by fixed positions in a fixed order: 8 to player 1, then 8 to player 2, and leave the other 20 in the set-aside list. Every fallback must be computed deterministically from ordered data: the lowest-card replacement for an illegal attack (ties broken by suit order), the default offer of Hearts and Spades, and the default trump of the first offered suit. Make sure nothing iterates over a set or map whose order can change between runs. Check that two runs with the same seed give identical logs.
playing the same seed twice gave different logs: something in the game is not deterministic (a clock, an unseeded draw)

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Durak is a 2–6 player shedding game played with a 36-card deck and a trump suit. An attacker plays cards, and the defender must beat each one with a higher card of the same suit or with a trump, or else pick up the whole table. Players draw back up to six, and the last player still holding cards is the loser (the 'durak').",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every simple policy loses to sensible play. A player who always takes swells their hand and ends as durak. A player who always attacks with their highest card throws away trumps they need later. A player who never adds cards gives up tempo. The first attacker is decided by the deal (lowest trump), so no fixed seat has an edge. With 3–6 players, the seat to the left of a strong attacker is somewhat worse off, but that is minor."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Card counting, saving trumps and choosing when to take all reward skill. However, drawing from the talon after each bout injects a lot of luck, so one deal is noisy. With many players, the loser is partly decided by who happens to gang up on whom."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "There are many levels of play: tracking which cards have been seen, timing trump spends, deliberate takes to collect a rank, and adding cards to strand the defender. A weak player still sheds cards and can survive a hand."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands and the talon are hidden. Good play means inferring what the opponent holds from what they beat, failed to beat, or added, and planning the endgame once the talon is empty."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Whether a card beats another, which ranks may be added, and who runs out of cards are all mechanical facts that can be checked by arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. But open-ended multi-player adding with clockwise priority, drawing order across up to 6 players, and up to 6 attacks per bout far exceed 4 choice steps per round. Repeated talon draws exceed the limit of one random draw per round. The previous variation also failed a determinism test: the same seed gave different logs."
    },
    {
      "criterion": "previous_variation_determinism",
      "verdict": "bad",
      "evidence": "Two runs with the same seed produced different logs. Some part of the previous build used a clock, an unseeded pick, or iteration over an unordered collection: in setup, in a fallback (the lowest-card replacement, the default suit offer or the default trump), or in how hands were listed."
    }
  ],
  "problems": [
    "P1: Non-determinism. Replaying the same seed gave different logs. The likely causes are an unseeded or time-based random pick, a randomness use outside the single setup shuffle, fallbacks that were not computed from ordered data, or hands, discards or announcements listed by iterating over a set or map.",
    "P2: Talon drawing every bout needs many random draws and makes a single deal luck-heavy.",
    "P3: Multi-player adding with clockwise priority and up to 6 attacks per bout needs far more than 4 choice steps per round.",
    "P4: With 3+ players, whether you end as durak depends partly on seat position and on others' choices, not only on your own reasoning.",
    "P5: The deal alone could decide the game if the trump suit is fixed by a random card.",
    "P6: The game needs a guaranteed end inside 40 rounds, and every illegal or missing answer needs a deterministic resolution."
  ],
  "changes": [
    {
      "what": "Randomness happens exactly once: in round 1, the engine's seeded shuffle is applied to the 36-card deck, built as an ordered list (Clubs, Diamonds, Hearts, Spades; ranks 6 to 14 within each suit; card id = suit index × 9 + rank − 6). Cards are dealt by fixed positions: list positions 1–8 to player 1, 9–16 to player 2, and 17–36 to the set-aside list in that order. No other random operation, clock value or external source is used anywhere.",
      "why": "This gives a single seeded source of randomness, so the same seed always produces the same deal.",
      "fixes": "P1: Non-determinism"
    },
    {
      "what": "All hands, the discard pile and the set-aside pile are stored as ordered lists sorted ascending by card id. Every announcement and every fallback reads them in that order. Nothing iterates over a set or map.",
      "why": "This removes order-dependent output and order-dependent fallbacks.",
      "fixes": "P1: Non-determinism"
    },
    {
      "what": "Every fallback is a fixed rule on ordered data. An illegal or missing offer becomes Hearts and Spades. An illegal or missing trump pick becomes the first offered suit in suit order. An illegal or missing attack becomes the attacker's lowest card id. An illegal or missing defence counts as taking. An illegal or missing throw-in counts as passing.",
      "why": "Each fallback is deterministic and reproducible.",
      "fixes": "P1: Non-determinism; P6: guaranteed end and deterministic resolution"
    },
    {
      "what": "Two players, 8 cards each, no drawing. The other 20 cards stay set aside face down and are never used.",
      "why": "This removes talon luck and repeated draws. The set-aside pile keeps a real hidden-information problem: 20 unseen cards, of which 8 are in the opponent's hand.",
      "fixes": "P2: talon luck and repeated draws; P4: seat and coalition effects"
    },
    {
      "what": "Each bout has at most 2 attack cards: one attack, one optional throw-in matching a rank on the table, and up to two defences.",
      "why": "This keeps choice steps at 4 per round while keeping attack, defend, take and add.",
      "fixes": "P3: too many choice steps"
    },
    {
      "what": "Trump is chosen by cut-and-choose. Player 2 offers two different suits; player 1 picks one of them as trump. The player holding the lowest trump attacks first; if neither holds a trump, player 2 attacks first.",
      "why": "Player 2 must offer two suits it can live with, and player 1 chooses after seeing its own hand. Good reasoning can offset a lopsided deal, and the seat roles balance each other.",
      "fixes": "P5: deal deciding the game"
    },
    {
      "what": "The game ends when a hand empties (elimination), with a cap at round 40. At the cap, the player with fewer cards wins; equal counts are a draw.",
      "why": "This guarantees an end with an arithmetic result.",
      "fixes": "P6: guaranteed end and deterministic resolution"
    }
  ],
  "keeps": [
    "The 36-card deck, ranks 6 to Ace",
    "A trump suit that beats all other suits",
    "Beating a card with a higher card of the same suit or with any trump",
    "Attacker adding cards matching ranks already on the table",
    "A defender who fails taking the whole table",
    "A successful defender becoming the next attacker",
    "The lowest trump attacking first",
    "Shedding all your cards to escape being the durak"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "A two-player, no-draw, deterministically seeded Durak keeps the game's core of beating, taking and adding, has real hidden information, and fits the step limits."
  },
  "variation": {
    "name": "Duel Durak (seeded)",
    "summary": "Two-player Durak with 8-card hands, no drawing, and a 20-card hidden set-aside pile. The trump suit is chosen by cut-and-choose. Each bout has one attack, one optional throw-in and up to two defences. The first player to empty their hand wins. All randomness is a single seeded shuffle in round 1.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. 36 cards: suits Clubs (index 0), Diamonds (1), Hearts (2), Spades (3); ranks 6, 7, 8, 9, 10, J=11, Q=12, K=13, A=14. Each card has an id = suit index × 9 + (rank − 6), from 0 to 35. Hands, the discard pile and the set-aside pile are always kept as lists sorted ascending by id, and are always shown and read in that order.\n\nCARD STRENGTH. Card X beats card Y if: (a) X has the same suit as Y and a higher rank; or (b) X is a trump and Y is not a trump.\n\nROUND 1 (setup, no bout).\nStep 1. Build the deck as the ordered list of ids 0 to 35. Shuffle it once with the engine's seeded shuffle. This is the only random operation in the game; no clock or other random source is ever used. Positions 1–8 go to player 1's hand, positions 9–16 to player 2's hand, and positions 17–36 to the set-aside pile. The set-aside pile stays face down for the whole game and is never drawn from. Each player is told only their own hand. Both players are told that each holds 8 cards.\nStep 2. Player 2 names two different suits as the offer. If the answer is missing or illegal, the offer is Hearts and Spades.\nStep 3. Player 1 picks one of the two offered suits as trump. If the answer is missing or illegal, trump is the offered suit with the lower suit index.\nStep 4. The trump suit is announced. The first attacker is the player holding the lowest-rank trump. If neither player holds a trump, player 2 attacks first. The other player is the defender.\n\nROUNDS 2 TO 40 (one bout each, played only while both players hold cards).\nStep 5 (attack). The attacker chooses one card from their hand and plays it face up. If the answer is missing or illegal, the attacker plays their lowest-id card.\nStep 6 (defence 1). The defender either plays one card from their hand that beats the attack card, or says TAKE. A missing or illegal answer counts as TAKE.\nStep 7 (throw-in). The attacker may add one card from their hand whose rank equals the rank of any card now on the table, or PASS. A throw-in is allowed even if the defender said TAKE; in that case the defender will take it too. The attacker may not throw in if this would leave the defender with more cards on the table to beat than cards in hand. A missing or illegal answer counts as PASS.\nStep 8 (defence 2). This step happens only if a card was thrown in and the defender has not said TAKE. The defender either plays one card that beats the thrown-in card, or says TAKE. A missing or illegal answer counts as TAKE.\nStep 9 (resolution).\n- If the defender said TAKE at any point, all cards on the table go into the defender's hand, and the attacker attacks again next bout.\n- Otherwise, all cards on the table go to the discard pile, and the defender becomes the attacker for the next bout.\nStep 10 (announcement). Announce all cards played this bout in order, the result, and both players' hand sizes.\n\nEND.\n- After a bout's resolution, if exactly one player has 0 cards, that player wins.\n- If both players have 0 cards, the game is a draw.\n- If both players still hold cards after round 40, the player with fewer cards wins; equal counts are a draw.\n\nDETERMINISM. Given the same seed, the game must produce identical logs. Every fallback is the fixed rule stated above, computed from the sorted lists.",
    "objective": "The first player whose hand reaches 0 cards after a bout wins. If both reach 0 at the same time, the game is a draw. If round 40 ends with both holding cards, the player with fewer cards wins; equal counts are a draw.",
    "expected_effect": "Without drawing, the game becomes a card-counting duel. Each player knows 8 cards, and play gradually reveals which of the 28 unseen cards are in the opponent's hand rather than set aside. A failed defence or a declined throw-in leaks information about the opponent's hand. The cut-and-choose trump selection makes player 2 offer two suits it can live with, while player 1 reads its own hand to pick between them. Taking on purpose to collect a rank, saving trumps for the last bouts, and throwing in to strand the defender are all rewarded. Simple policies all lose: always TAKE builds a huge hand, always attacking lowest is read and punished, and never throwing in loses tempo. With one seeded shuffle and ordered-list fallbacks, two runs with the same seed should replay identically."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
