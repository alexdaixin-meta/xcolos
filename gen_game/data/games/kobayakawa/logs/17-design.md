# 17 design

- time: 2026-10-27T08:58:31+00:00 (94.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ccee4b906d074bd1, reply sha256 df2c86c44658a6f4

## Sent

````
Original game: Kobayakawa
Players in the original: 3 to 6

Original rules:
Each player gets 4 kamons and one hidden card from a 1-15 deck; one card is revealed as Kobayakawa. Place 8 kamons in the center pot. Each round has a Draw phase: in turn order each player either draws from deck to keep one of the two cards discarding the other face-up, or blindly replaces the Kobayakawa card. Then Fight phase: in order each player chooses to bet 1 kamon to fight or pass. Only fighters reveal. The fighter with the lowest card adds the Kobayakawa value to his total; highest total wins. Winner takes all bet kamons plus 1 from center. Ties broken by earlier turn order. If sole fighter, wins without revealing. Winner becomes start player. Players with 0 kamons are eliminated. Continue until 2 kamons remain in center; last round costs 2 kamons to fight and winner takes both remaining. Most kamons at end wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Cut the per-round procedure by at least 3-4 steps while keeping the core bluff-and-fight loop. Candidates:
(1) Drop the SHIFT option and the Alternate card. The Kobayakawa is dealt once per round and never replaced, which removes the shift check, the alternate deal and its announcement.
(2) Merge the two-stage draw: replace KEEP/DRAW followed by the OLD/NEW choice with one simultaneous choice, KEEP or SWAP. SWAP takes the reserve card blind and discards the old card face up. This removes the separate private look and the second poll.
(3) Remove the round-10 special cases: use the same minimum stake and centre feed every round, and always carry a tied pot (split ties only at game end, or simply let a final tie remain in the pot).
(4) Optionally drop the simultaneous TALK step, or fold the reveal announcements into the fight prompt.
Also blunt reckless fighting so that always choosing the last option (HIGH) is not a near-50% strategy. For example, when two or more players fight, a losing HIGH fighter could lose one extra kamon to the centre. Or the Kobayakawa bonus could go only to the lowest card when that fighter fought LOW.
the game was built and behaves as specified, but evaluation found design flaws:
- the built game has 22 steps per round, over the limit of 20
- against random seats the results were {'seat 2': 22, 'seat 3': 21, 'seat 1': 17}
- a thoughtless policy `first@seat1`: won 0, lost 60, drew 0
- a thoughtless policy `first@seat2`: won 0, lost 60, drew 0
- a thoughtless policy `last@seat1`: won 30, lost 30, drew 0
- a thoughtless policy `last@seat2`: won 20, lost 39, drew 1

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Kobayakawa is a 3-6 player bluffing game played with cards numbered 1-15. Each player holds one hidden card and may draw to improve it or replace the shared Kobayakawa card. Players then bet a kamon to fight or pass. The lowest fighting card adds the Kobayakawa value, and the highest total takes the bets plus one kamon from the centre. The player with the most kamons at the end wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the original and the previous variation, the centre pays out to any fight winner, including a sole fighter. A blind always-fight policy therefore collects that payout whenever the others pass. In testing, 'last' (always fight) won 30 of 60 games from seat 1 against random play, about half when a third would be fair. Always-keep-and-pass ('first') lost every game, which is fine. The random-seat spread (17/22/21) shows a mild seat skew."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Choosing when to fight depends on your card, the face-up Kobayakawa value and the cards others discarded. Fighting with a weak card against selective players loses stakes. Fighting a middling card when you are likely to be the lowest fighter under a high Kobayakawa wins pots. Luck in the deal is redrawn every round, so it averages out over many rounds."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Reading what a SWAP means, estimating where your card ranks given the visible discards, and deciding who will fight together form an open-ended inference problem. A weak player still wins pots whenever they hold strong cards."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Cards are hidden and only fighters reveal. The 'lowest card gets the bonus' twist means the value of a card depends on what you infer the others hold and whether they will fight."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Totals, the pot and kamon counts are all arithmetic on dealt numbers."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original runs a turn-ordered draw and fight, has a Kobayakawa-replacement option and a special final round. The previous build needed 22 steps per round, over the limit of 20."
    }
  ],
  "problems": [
    "P1: The previous build used 22 steps per round, over the limit of 20, because of the shift option, the two-stage draw, the round-10 special cases and the talk step.",
    "P2: Always fighting wins about half the time against random play, because the centre pays even a sole uncontested fighter. A blind aggressor collects that free kamon every time the others pass, and the others never do while it is always in.",
    "P3: Tie-breaking by turn order and a rotating start player give seats unequal standing (random-seat results 17/22/21).",
    "P4: Sequential turn order in the original lets later players react to earlier ones, which the engine handles poorly and which favours late seats."
  ],
  "changes": [
    {
      "what": "Remove the option to replace the Kobayakawa card. Merge the draw into one simultaneous KEEP or SWAP choice: SWAP takes your face-down reserve card blind and discards your old card face up.",
      "why": "This cuts the shift check, the alternate deal, the private look and the second poll, while keeping the improve-your-card decision and the information leaked by discards.",
      "fixes": "P1"
    },
    {
      "what": "Use the same rules every round: no special final round, a stake of 1 every round, and a fixed 10 rounds.",
      "why": "Removes the special-case steps.",
      "fixes": "P1"
    },
    {
      "what": "Drop the talk step.",
      "why": "Card claims are cheap and unenforceable, the bluffing already lives in the fight decision, and the step budget is tight.",
      "fixes": "P1"
    },
    {
      "what": "The centre pays 1 kamon only to the winner of a contested fight (two or more fighters). A sole fighter just takes back their own stake and gains nothing.",
      "why": "Blind aggression no longer harvests free kamons when the others pass. Against random play, always-fight's expected gain falls from clearly ahead to only slightly ahead (about +0.33 vs +0.21 per round), and against selective players it loses stakes. Always-pass still loses because the centre feeds the active players.",
      "fixes": "P2"
    },
    {
      "what": "Both choices are made by all players at the same moment, and there is no start player.",
      "why": "No seat moves first or last, so no seat has a built-in edge.",
      "fixes": "P3, P4"
    },
    {
      "what": "Fight ties are broken by the lower card, not by seat.",
      "why": "The tie-break is deterministic and independent of seat.",
      "fixes": "P3"
    }
  ],
  "keeps": [
    "Cards 1-15, one hidden card each, and a face-up Kobayakawa card.",
    "Improving your card by a blind draw, with the old card discarded face up.",
    "Betting 1 kamon to fight or passing for free.",
    "The signature twist: the lowest fighting card adds the Kobayakawa value.",
    "The highest fighting total takes the stakes plus a kamon from a finite centre.",
    "Most kamons at the end wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core bluff-and-fight loop is good reasoning material. It only needed trimming to fit the step limit and a payout fix so blind aggression stops paying."
  },
  "variation": {
    "name": "Kobayakawa Duel Rounds",
    "summary": "Players secretly improve one hidden card, then all decide at once whether to stake a kamon. The lowest fighting card gets the face-up Kobayakawa bonus, and the highest total takes the pot. Only contested fights draw a kamon from the centre.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "rules": "SETUP: Each player starts with 5 kamons. The centre starts with 10 kamons. The game lasts exactly 10 rounds.\n\nEACH ROUND:\n1. Deal. Shuffle a fresh deck of 15 cards numbered 1 to 15. Deal each player one face-down hand card, which only they see. Deal each player one face-down reserve card, which nobody sees. Turn one card face up: this is the Kobayakawa card, value K. Announce K.\n2. Draw choice. All players at the same moment choose KEEP or SWAP. A SWAP player discards their hand card face up and takes their reserve card as their new hand card, then looks at it. Reserve cards of KEEP players are not used. Announce every discarded card and who discarded it.\n3. Fight choice. All players at the same moment choose FIGHT or PASS. A player with 0 kamons must PASS. Each FIGHT player puts 1 kamon into the pot.\n4. Resolve.\n   - No fighters: nothing happens.\n   - Exactly one fighter: that player takes their own kamon back. Their card is not revealed and the centre pays nothing.\n   - Two or more fighters: all fighters reveal their cards. Each fighter's total is their card, except that the fighter with the lowest card adds K to it. The fighter with the highest total wins. If totals tie, the tied fighter with the lower card wins. The winner takes the whole pot. If the centre has at least 1 kamon, the winner also takes 1 kamon from the centre. Losing fighters lose their stake.\n5. Announce all fighters, revealed cards, totals, the winner, and every player's kamon count.\n6. After round 10 the game ends.",
    "objective": "After round 10, the player with the most kamons wins. If two or more players tie for most, the game is a draw.",
    "expected_effect": "Blind always-fight now gains only slightly against random play and loses to selective fighters, because a lone fighter no longer collects from the centre. Always-pass loses because the centre steadily feeds active players. Winning requires judging whether your card is strong given K: a low card under a high K is strong only if you will be the lowest fighter. Players must also read the face-up discards (a SWAP of a 3 suggests a different hand than a SWAP of a 9) and predict who will fight. Simultaneous choices and a card-based tie-break remove seat advantages. Talk is omitted: the bluff lives in the fight decision, and unenforceable card claims would add steps without adding reasoning."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 2,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
