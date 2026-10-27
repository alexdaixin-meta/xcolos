# 01 design

- time: 2026-10-27T08:36:22+00:00 (68.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 3e96996b613c293f, reply sha256 78513627fd80d1bb

## Sent

````
Original game: Kobayakawa
Players in the original: 3 to 6

Original rules:
Each player gets 4 kamons and one hidden card from a 1-15 deck; one card is revealed as Kobayakawa. Place 8 kamons in the center pot. Each round has a Draw phase: in turn order each player either draws from deck to keep one of the two cards discarding the other face-up, or blindly replaces the Kobayakawa card. Then Fight phase: in order each player chooses to bet 1 kamon to fight or pass. Only fighters reveal. The fighter with the lowest card adds the Kobayakawa value to his total; highest total wins. Winner takes all bet kamons plus 1 from center. Ties broken by earlier turn order. If sole fighter, wins without revealing. Winner becomes start player. Players with 0 kamons are eliminated. Continue until 2 kamons remain in center; last round costs 2 kamons to fight and winner takes both remaining. Most kamons at end wins.
````

## Reply

````
```json
{
  "original_summary": "Kobayakawa is a 3-6 player micro-bluffing game. Each round every player holds one hidden card from a 1-15 deck and a public Kobayakawa card is shown. Players either redraw their card or blindly replace the Kobayakawa card, then pay a chip to fight or pass; among the fighters, the lowest card gains the Kobayakawa value, and the highest resulting total takes the pot plus one chip from the centre.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Always passing keeps the starting 4 kamons while the centre hands out about 8, so it usually loses, and always fighting bleeds chips on weak cards. Simple policies therefore lose. However, ties are broken by earlier turn order, which gives a built-in seat edge. Acting in turn order also hands later players information about earlier draws and fights."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading discards, judging whether a low card plus the Kobayakawa value beats the field, and folding marginal hands are real skills. But there are only about 7 rounds, and each is one card deal, so card luck carries a lot of weight."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still win rounds whenever they hold a high card. Strong players gain by estimating opponents' cards from discards and fight behaviour, and by timing Kobayakawa swaps."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Every card is hidden until the fight. Face-up discards, Kobayakawa swaps and willingness to fight all leak information. The 'lowest card gets the bonus' twist means both very low and very high cards can be strong, which forces inference about what others hold."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Card totals, the pot and chip counts are all arithmetic. The winner is simply who holds the most kamons."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based text with no board. But each player may draw from the deck during the round, which means several random draws per round against a limit of one. The seat-ordered sequential phases also add steps."
    }
  ],
  "problems": [
    "Each player's individual draw from the deck is a separate random event, so a round has several random draws, over the platform limit of one.",
    "Ties go to the earlier seat, a built-in positional advantage.",
    "Sequential turn order lets later players act on earlier players' revealed choices, which is another seat edge and costs extra steps.",
    "Only about 7 rounds of single-card deals, so luck has a large share of the outcome.",
    "There is no channel for the table bluffing that the game's theme invites; all signalling is through actions taken in seat order."
  ],
  "changes": [
    {
      "what": "Each round begins with one shuffle-and-deal. Every player gets a hand card and a face-down reserve card, plus a face-up Kobayakawa card and a face-down alternate Kobayakawa card. 'Drawing' reveals your reserve to you; 'Shift' replaces the Kobayakawa with the alternate.",
      "why": "This keeps the draw-or-replace decision while using exactly one random event per round.",
      "fixes": "Each player's individual draw from the deck is a separate random event, so a round has several random draws, over the platform limit of one."
    },
    {
      "what": "Ties for the highest total no longer go to a seat. The tied pot stays in place and carries into the next round. In the final round it is split evenly and any remainder is discarded.",
      "why": "This removes the positional advantage, and it makes ties a meaningful risk.",
      "fixes": "Ties go to the earlier seat, a built-in positional advantage."
    },
    {
      "what": "The draw decision and the fight decision are each made simultaneously by all players.",
      "why": "No seat sees others' choices first. Information still flows, because discards and Shift votes are revealed before the fight.",
      "fixes": "Sequential turn order lets later players act on earlier players' revealed choices, which is another seat edge and costs extra steps."
    },
    {
      "what": "The centre pot is raised to 11 kamons, giving 10 rounds: 9 normal rounds plus a final round with a fight cost of 2.",
      "why": "More hands let skill in folding, bluffing and inference outweigh individual deals.",
      "fixes": "Only about 7 rounds of single-card deals, so luck has a large share of the outcome."
    },
    {
      "what": "A simultaneous one-message talk phase is added after cards are settled and before the fight.",
      "why": "Only one player can take the pot, so claims such as 'I hold 15' are a contested bluff. Others must judge them against the discards and the Kobayakawa value.",
      "fixes": "There is no channel for the table bluffing that the game's theme invites; all signalling is through actions taken in seat order."
    }
  ],
  "keeps": [
    "A 1-15 deck, with one hidden card per player per round.",
    "The public Kobayakawa card, and the twist that the lowest fighter adds its value.",
    "The choice between improving your own card (with the discard shown face up) and blindly replacing the Kobayakawa.",
    "Paying a kamon to fight or passing for free; a sole fighter wins without revealing.",
    "The winner takes the stakes plus one centre kamon; the final round costs 2 and pays out the remaining centre.",
    "Elimination at 0 kamons; most kamons wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Kobayakawa is already a compact hidden-information bluffing game. It needs only a one-draw-per-round restructure, seat-neutral ties and simultaneous phases to fit the platform and reward inference."
  },
  "variation": {
    "name": "Kobayakawa: Simultaneous Duel",
    "summary": "Each round every player holds a hidden card from 1-15 and may redraw or vote to shift the public Kobayakawa card. After one round of simultaneous table talk, everyone simultaneously fights or passes. Among the fighters, the lowest card adds the Kobayakawa value, and the highest total takes the pot. Most kamons after 10 rounds wins.",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "rules": "SETUP: Each player starts with 4 kamons. The centre holds 11 kamons. The pot starts at 0. The game lasts 10 rounds, or ends sooner if only one player remains.\n\nEACH ROUND:\n1. DEAL (the round's only random event). Shuffle a deck of cards numbered 1 to 15. Each active player receives one HAND card, seen only by that player, and one RESERVE card, face down and unseen by anyone. Two more cards are dealt: the KOBAYAKAWA, face up for all to see, and the ALTERNATE, face down.\n2. ANNOUNCE. The engine announces the round number, the Kobayakawa value, the current pot, every player's kamon count, and the fight cost: 1 in rounds 1-9, 2 in round 10.\n3. DRAW CHOICE (simultaneous). Each active player secretly chooses one of three options:\n   - KEEP: keep your hand card.\n   - DRAW: look at your reserve card.\n   - SHIFT: vote to replace the Kobayakawa.\n4. Each player who chose DRAW privately sees their reserve card.\n5. KEEP CHOICE (simultaneous, drawers only). Each drawer chooses to keep either OLD (the hand card) or NEW (the reserve card). The kept card becomes the hand card. The other card is discarded face up for everyone to see.\n6. REVEAL. The engine announces each player's draw choice and all face-up discards.\n7. SHIFT. If at least one player chose SHIFT, the alternate card replaces the Kobayakawa and its value is announced. Otherwise the original Kobayakawa stays.\n8. TALK (simultaneous). Every active player writes one short message without seeing the others. All messages are then shown to everyone. Talk is not binding, and claims may be false.\n9. FIGHT CHOICE (simultaneous). Each active player chooses FIGHT or PASS. A player with fewer kamons than the fight cost must PASS.\n10. STAKE. Each fighter pays the fight cost into the pot. The engine then moves centre kamons into the pot: 1 in rounds 1-9, and all remaining centre kamons in round 10.\n11. SCORE.\n   - If nobody fights, the pot stays where it is and carries into the next round.\n   - If exactly one player fights, that player takes the whole pot and their card is not revealed.\n   - If two or more fight, all fighters' cards are revealed. Each fighter's total equals their card value, except that the fighter with the lowest card adds the Kobayakawa value to their card. The fighter with the highest total takes the whole pot.\n12. TIES. If two or more fighters share the highest total, nobody takes the pot and it carries into the next round. In round 10, the pot is instead divided equally among the tied fighters, rounding down, and any remainder is removed from the game.\n13. ELIMINATION. Any player with 0 kamons is eliminated.\n14. END CHECK. The game ends after round 10, or as soon as only one active player remains.",
    "objective": "When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one player is left before round 10, that player wins.",
    "expected_effect": "Players must judge whether their card wins, which is either a high card or the lowest card among fighters plus the Kobayakawa value. To do so they reason from face-up discards, Shift votes and messages. Shifting is a gamble, since a low card loves a high Kobayakawa, and it reveals intent. Talk passes both tests. Players disagree because only one fighter takes each pot, so everyone wants rivals to pass on hands that would beat theirs and to fight on hands that would lose. A player who simply believes the claim 'I hold 14, don't fight' and folds a lowest-card hand that would have won with a Kobayakawa of 11 loses the pot. Because claims are not binding, they must be checked against the discards. Always passing loses ground as rivals collect the 11 centre kamons, and always fighting bleeds kamons on weak cards. Simultaneous choices and carry-over ties remove every seat advantage, and 10 hands with variable fight decisions let folding discipline and bluff-reading outweigh the deal."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
