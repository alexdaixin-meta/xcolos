# 01 design

- time: 2026-10-28T01:31:46+00:00 (81.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 255e1aa64d13125b, reply sha256 709098bb806759fc

## Sent

````
Original game: Salem 1692
Players in the original: 4 to 12

Original rules:
Each player gets face-down Tryal cards; any Witch card makes you a Witch forever, even if later lost. One Town Hall power each. Deal 3 playing cards. Put Conspiracy in deck and Night at bottom; set Black Cat aside. At Dawn, Witches eyes-open secretly give Black Cat to any player. First player is Black Cat holder. On your turn you must either draw 2 cards (Black cards revealed and resolved instantly) or play any number of cards on others, never yourself. Green cards are one-shot, Blue stay, Red are accusations. At 7 accusations the accuser reveals one of that player's Tryal cards; if Witch revealed, that player dies. When Conspiracy is drawn, reveal one Tryal on Black Cat holder, then each player takes one unrevealed Tryal from left, becoming Witch if they gain a Witch card. When Night is drawn, all close eyes, Witches choose a kill, Constable chooses a save; if different player, victim dies. Witches win when all non-Witches dead; Town wins when all Witch Tryal cards are revealed.
````

## Reply

````
```json
{
  "original_summary": "Salem 1692 is a 4-12 player hidden-role card game. Secret Witches try to kill the townsfolk, and the Town plays accusation cards on players until it has revealed every Witch Tryal card. Night kills and Constable saves, a Conspiracy card that passes Tryal cards around, and many card types make it chaotic.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Choices matter: whom you accuse, whom Witches kill, whom the Constable saves. But card draws decide a lot. The Conspiracy card can turn innocents into Witches at random, and black cards resolve without anyone choosing. The first-player and Black Cat rules create seat effects."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading people pays off, but the random hand decides whether you can accuse at all. A random Conspiracy can flip teams. Random Tryal reveals mean even a correct accusation of a Witch often shows an innocent card first."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Social deduction has deep headroom: bluffing, reading accusation patterns, timing claims. Weak players can still win as part of a team."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hidden roles, secret night actions and accusation patterns all require inference about who is lying."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The win conditions (all Witch cards revealed, or all non-Witches dead) follow mechanically from what happened."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "There are dozens of distinct card effects, Blue cards that stay in play, Town Hall powers, multi-card Tryal hands, Conspiracy passing, a shuffled deck with Night placed at the bottom, and up to 12 players. This far exceeds 20 steps, 4 choices and 3 hidden elements per round."
    }
  ],
  "problems": [
    "P1: Too many card types, persistent effects and special powers to build within the step and attribute limits.",
    "P2: Luck swamps skill: the hand dealt decides who can accuse, Conspiracy reassigns teams at random, and Tryal reveals are random draws.",
    "P3: Multi-card Tryal hands and a deck with several random draws per turn break the one-draw-per-round and three-hidden-element limits.",
    "P4: Accusations are spent cards from a random hand rather than deliberate choices, so the core deduction decision is often unavailable.",
    "P5: The player count (up to 12) and an unbounded length make games long and hard to balance."
  ],
  "changes": [
    {
      "what": "Replace all playing cards with one simultaneous accusation poll each round. Every living player names one other living player and receives one accusation token per vote, and tokens accumulate across rounds.",
      "why": "This keeps Salem's accumulating accusations and trial threshold while making every accusation a deliberate, readable choice.",
      "fixes": "P1, P4"
    },
    {
      "what": "When a player reaches a threshold of 3 tokens as the unique leader, they are tried and their role revealed. A Witch means the Town wins; an innocent is hanged. All tokens then reset.",
      "why": "This replaces random Tryal-card reveals with a single deterministic reveal, so being right is rewarded and being wrong costs a townsperson.",
      "fixes": "P2, P3"
    },
    {
      "what": "One hidden role per player, dealt once: 1 Witch, 1 Constable, the rest Townsfolk. Conspiracy and team-swapping are removed.",
      "why": "Teams no longer change at random, and the hidden state stays one strong element.",
      "fixes": "P2, P3"
    },
    {
      "what": "Add one random event per round, the Gossip. The engine draws one living player, who privately learns whether the next living player clockwise is the Witch. Nobody else is told who was drawn.",
      "why": "This adds Salem-style information that can be bluffed. A true claim must be about the claimant's own left neighbour, which constrains lies and makes counter-claims analysable. It uses exactly one random draw.",
      "fixes": "P2, P3"
    },
    {
      "what": "Night happens every round. Every living player privately names a night target, but only the Witch's (kill) and the Constable's (protect, not self) choices count. If they differ, the victim dies and their role is revealed.",
      "why": "This keeps Night and the Constable save. Polling everyone hides who the active roles are.",
      "fixes": "P1"
    },
    {
      "what": "Limit the game to 5-6 players and at most 6 rounds. The Witch wins at parity (living Witch at least equal to living others) or by surviving round 6.",
      "why": "Games are short and bounded, and the balance can be tuned for one Witch.",
      "fixes": "P5"
    },
    {
      "what": "Add a simultaneous talk phase before accusations: each living player writes one message at the same time, and all are shown.",
      "why": "Claims, counter-claims and bluffs about the Gossip are the heart of the deduction.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Secret Witch versus Town hidden roles",
    "Accusations that accumulate up to a threshold that triggers a trial and reveal",
    "Night: the Witch chooses a kill, the Constable chooses a save, and the victim dies only if the choices differ",
    "Town wins by exposing the Witch; the Witch wins by thinning out the Town",
    "Paranoia from information that may be a lie (Gossip in place of the Black Cat and Conspiracy chaos)"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core (hidden Witch, cumulative accusations, Night kill versus Constable save) fits the limits once the card machinery is replaced with polls and one private random clue per round."
  },
  "variation": {
    "name": "Salem 1692: Gossip and Gallows",
    "summary": "One secret Witch hides among 5-6 villagers. Each round one random villager privately learns a rumour about a neighbour. Everyone talks, then accuses, and accusations pile up toward a trial. At night the Witch kills unless the Constable guesses the target.",
    "players": {
      "min": 5,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP. Seat players in a circle, numbered 1..N (N = 5 or 6). Deal hidden roles at random: exactly 1 Witch, 1 Constable, and the rest Townsfolk. Each player sees only their own role. Every player starts alive with 0 accusation tokens. The game lasts at most 6 rounds.\n\nEACH ROUND, in this order:\n1. GOSSIP DRAW. The engine draws one living player uniformly at random as the Gossip. Only that player is told they were drawn.\n2. GOSSIP RESULT. The Gossip is privately told whether the next living player clockwise from them is the Witch (\"Witch\" or \"not the Witch\"). Nobody else learns who the Gossip was or what they heard. A Witch may be drawn and will simply learn that their neighbour is not the Witch.\n3. TALK. Every living player writes one short message at the same time, without seeing the others. Then all messages are shown to everyone. Players may claim, accuse, lie or stay vague. Nothing said is binding.\n4. ACCUSATION. All living players simultaneously name one other living player (never themselves). Each named player gains 1 accusation token per vote.\n5. ANNOUNCE. All votes and every player's token total are made public.\n6. TRIAL CHECK. If one player has strictly more tokens than every other player AND has at least 3 tokens, that player is tried. If two or more players tie for the most tokens, nobody is tried this round and tokens carry over.\n7. TRIAL. The tried player's role is revealed to all.\n   - If they are the Witch, the game ends immediately and the Town wins.\n   - Otherwise they are hanged (eliminated). All players' tokens then reset to 0.\n8. PARITY CHECK. If the number of living Witches (1) is at least the number of living non-Witches, the game ends and the Witch wins.\n9. NIGHT. Every living player privately names one living player as their night target. Only two choices count:\n   - The Witch's choice is the kill. It must be a living non-Witch.\n   - The Constable's choice is the protection. It must be a living player other than the Constable.\n   Everyone else's choice is ignored. This hides who the active roles are. If the Constable is dead, there is no protection.\n10. NIGHT RESOLUTION. If the kill target differs from the protection target, the kill target dies and their role is revealed. If they are the same, nobody dies, and it is announced only that the night passed peacefully.\n11. PARITY CHECK. Repeat the check in step 8.\n12. ROUND END. If this was round 6 and the Witch is still alive, the game ends and the Witch wins. Otherwise start the next round.\n\nDead players take no further part, receive no tokens and are skipped when finding the next living player clockwise.",
    "objective": "Team game. The Town (Constable and all Townsfolk, alive or dead) wins together if the Witch is tried and revealed. The Witch wins if, after a trial or a night, living non-Witches are no more numerous than the living Witch (1 versus 1), or if the Witch is still alive at the end of round 6. There are no draws.",
    "expected_effect": "Accusations become the central deliberate choice, and the cumulative threshold of 3 means a vote must be coordinated, which Witch bluffs can disrupt. Players disagree because the Witch wants an innocent hanged while each townsperson wants the real Witch hanged. They also disagree among themselves about whom to trust: a true Gossip claim can only concern the claimant's own left neighbour, a Witch can fake such a claim to frame that neighbour, and the framed innocent knows the claim is false and will counter-claim. A townsperson who just follows the first loud accuser risks hanging an innocent, which costs the Town a member and moves the Witch toward parity (a 5-player game can be lost in two rounds of errors). Night kills reveal roles and create a guessing duel between the Witch and Constable over whom the Constable expects the Witch to target. Simple policies lose: random accusers hang innocents, and a silent Witch or one who always kills the loudest accuser becomes predictable. Roles are team-based and the game is short, so the deal decides which side you play, not who wins."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 3,
    "attributes": 13,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 6
  }
}
```
````
