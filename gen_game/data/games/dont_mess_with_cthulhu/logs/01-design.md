# 01 design

- time: 2026-10-28T01:31:46+00:00 (92.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 47780dfe0a6ea643, reply sha256 0f9ccdcb176f7a65

## Sent

````
Original game: Dont Mess With Cthulhu
Players in the original: 3 to 6

Original rules:
Setup: for 4-6 players use 3-4 Investigators vs 2 Cultists, plus extra hidden tokens, shuffle and deal one role face down to each player. Build Investigation deck per player count with Futile cards, Elder Signs equal to player count, and one Cthulhu, shuffle and deal five to each player face down. Each player looks at own cards, notes counts but shuffles so positions unknown, then may lie about contents. Play is four rounds. Each round has actions equal to player count. Active player chooses one face-down Investigation card belonging to another player and reveals it. If Cthulhu is revealed Cultists win instantly. If all Elder Signs revealed Investigators win instantly. Otherwise the owner of the revealed card becomes next Active player. After actions equal to player count, collect remaining face-down cards, reshuffle and redeal evenly, one fewer per player each round. After four rounds without all Signs, Cultists win.
````

## Reply

````
```json
{
  "original_summary": "Don't Mess With Cthulhu is a hidden-role bluffing game. Secret Investigators try to reveal every Elder Sign hidden in players' face-down hands, while secret Cultists try to get Cthulhu revealed or run out the clock. Players take turns cutting one card from another player's hand, and each player may lie about what their own hand holds.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy is safe. An investigator who always cuts the next seat cuts Cthulhu at random and loses about 85% of the time against cultists who steer play. A cultist who cuts at random and makes no false claims gives up control and is soon avoided. Roles are dealt at random, so no seat has a team edge. Who you cut decides who acts next, so choices change the outcome. One weakness: under fully random play the Cultists win about 5 games in 6 (Cthulhu must be the last of the six special cards, a 1-in-6 chance). The game only balances when investigators reason."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Which card comes out of a hand is a random pick, and one unlucky cut ends the game. Results are team results, so a weak player can be carried by teammates or sink them. Over many games, reading claims and choosing whom to cut does shift win rates a lot, but any single game is noisy."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Strong play involves tracking claims against revealed cards, inferring the number and identity of cultists, choosing cuts that keep control with trusted players, and timing a lie. A weak investigator can still win by cutting players who claim signs."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Roles and hand contents are hidden. Every claim is a statement to test against later reveals. Who passes control to whom is evidence about team membership."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The game ends instantly when Cthulhu is revealed (Cultists win) or the last Elder Sign is revealed (Investigators win), otherwise when the cut limit is reached (Cultists win). All of this is counting."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Text and turn-based play suit the engine, but a game round has as many cuts as there are players, which exceeds 4 choices per round. The reshuffle and redeal each round needs a large multi-card deal plus a second random event in the same round. Picking a face-down card by position has to become a random draw from the hand's counts."
    }
  ],
  "problems": [
    "A game round holds one cut per player (up to 6 choices), above the platform's limit of 4 choice steps per round.",
    "The reshuffle-and-redeal between rounds needs a second random event and many dealing steps in one round, beyond the build limits.",
    "Choosing a face-down card by position has no meaning in text: the pick is effectively random and needs to be expressed as one random draw.",
    "Under thoughtless play the Cultists win about 5 games in 6. Balance depends on investigators using the claim information, so claims must happen every turn and be checkable.",
    "The setup is vague about deck composition, extra role tokens per player count, how claims work, and what happens when the target's hand is empty."
  ],
  "changes": [
    {
      "what": "Each engine round is one cut: a simultaneous talk phase, then the active player names a target, then one random card is revealed from the target's hand. The game lasts 4 cuts per player (20 rounds with 5 players, at most 24).",
      "why": "This keeps the original total number of cuts while giving each round only 2 choices and 1 random draw.",
      "fixes": "A game round holds one cut per player (up to 6 choices), above the platform's limit of 4 choice steps per round."
    },
    {
      "what": "Hands are dealt once and never redealt. The original's shrinking hands happen naturally as cards are cut. Cuts may come from any non-empty hand.",
      "why": "This removes the second random event and the bulk redeal. It also makes every claim testable over the whole game, because reveals keep coming from the same fixed hands, which deepens deduction.",
      "fixes": "The reshuffle-and-redeal between rounds needs a second random event and many dealing steps in one round, beyond the build limits."
    },
    {
      "what": "The cut reveals a card drawn uniformly at random from the target's remaining cards, computed from that hand's counts of Signs, Cthulhu and Futile cards.",
      "why": "This matches the original, where the cutter does not know positions, using a single arithmetic draw.",
      "fixes": "Choosing a face-down card by position has no meaning in text: the pick is effectively random and needs to be expressed as one random draw."
    },
    {
      "what": "Each round opens with simultaneous talk: every player writes one message (claims, accusations, requests) without seeing the others, then all messages are shown. Players are told their exact hand counts privately, and hand sizes are public.",
      "why": "Claims become frequent, simultaneous (no copying the first speaker) and checkable against reveals. This gives investigators the information that offsets the Cultists' random-play edge, and gives cultists a reason to bluff.",
      "fixes": "Under thoughtless play the Cultists win about 5 games in 6. Balance depends on investigators using the claim information, so claims must happen every turn and be checkable."
    },
    {
      "what": "Exact setup tables for 4, 5 and 6 players. A hidden extra role token at 4 players keeps the number of cultists uncertain. Fixed rules cover self-targeting, empty hands and the first active player.",
      "why": "This makes the rules complete enough to build and keeps the original's uncertainty about the size of the cult.",
      "fixes": "The setup is vague about deck composition, extra role tokens per player count, how claims work, and what happens when the target's hand is empty."
    }
  ],
  "keeps": [
    "Secret Investigators versus secret Cultists, with team victory.",
    "Five face-down cards per player containing Elder Signs equal to the player count, exactly one Cthulhu, and Futile cards.",
    "Players know their own hand and may lie about it freely.",
    "The active player cuts another player's card, and the owner of the revealed card becomes the next active player.",
    "Instant win conditions: Cthulhu revealed means Cultists win; all Elder Signs revealed means Investigators win; time running out means Cultists win.",
    "Four cuts per player in total."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Its core (hidden roles, lying about hidden hands, control passing to whoever you cut) fits the engine once each cut becomes one round and the redeal is removed."
  },
  "variation": {
    "name": "Don't Cut Cthulhu",
    "summary": "A hidden-team bluffing game in which players cut random cards from each other's fixed secret hands. Investigators must uncover every Elder Sign before Cthulhu surfaces or time runs out.",
    "players": {
      "min": 4,
      "max": 6,
      "suggested": 5
    },
    "rules": "SETUP.\n1. Role tokens: with 4 players, shuffle 3 Investigator and 2 Cultist tokens, deal 1 to each player and set the 5th aside unseen, so there are 1 or 2 Cultists. With 5 players, use 3 Investigators and 2 Cultists. With 6 players, use 4 Investigators and 2 Cultists. Each player privately learns only their own role. Cultists do not learn who the other Cultist is.\n2. Card deck: 5 cards per player in total. The deck holds Elder Signs equal to the number of players, exactly 1 Cthulhu, and the rest Futile cards. With 4 players: 4 Signs, 1 Cthulhu, 15 Futile. With 5 players: 5 Signs, 1 Cthulhu, 19 Futile. With 6 players: 6 Signs, 1 Cthulhu, 23 Futile. Shuffle and deal 5 cards to each player.\n3. Each player is told privately how many Signs, Cthulhu and Futile cards their own hand holds. Everyone can always see how many cards each player has left, how many Signs have been revealed, and how many cuts have been made.\n4. Player 1 is the first active player. Roles are random, so this gives no team an edge.\n\nEACH ROUND (one cut).\n1. Talk: every player writes one short message at the same time without seeing the others. Players may claim anything about their hand or anyone's role, truthfully or not. All messages are then shown to everyone.\n2. Cut: the active player names one other player who has at least 1 card left. You may not name yourself.\n3. Reveal: one card is taken uniformly at random from the named player's remaining cards and revealed to all. It is removed from that hand and does not return.\n4. If it is Cthulhu, the Cultists win immediately.\n5. If it is an Elder Sign, add 1 to Signs revealed. If Signs revealed equals the number of players, the Investigators win immediately.\n6. The named player becomes the active player for the next round.\n7. Add 1 to cuts made. If cuts made equals 4 times the number of players (16, 20 or 24), the game ends and the Cultists win.\n\nTalk is never binding, and no cards or information may be exchanged except through messages.",
    "objective": "Team victory decided by counting. If Cthulhu is revealed, every Cultist wins and every Investigator loses. If the number of revealed Elder Signs reaches the player count before that, every Investigator wins and every Cultist loses. If the cut limit of 4 times the player count is reached first, every Cultist wins. With 4 players the unused role token is never a player and wins nothing. There are no draws.",
    "expected_effect": "Investigators must cut Signs fast while keeping control among players they trust. Cultists must earn trust and then steer cuts toward the Cthulhu holder, or lure cuts onto worthless hands to burn the clock. The players disagree about everything that matters, because the two teams want opposite reveals. A player who simply follows the loudest claim may be cutting a lying Cultist's hand, or handing control to a Cultist, and lose on the spot. Fixed hands let claims be checked against every reveal (a player who claimed 2 Signs and has shown 4 Futile cards is suspect), so careful tracking beats trusting. The talk phase is simultaneous each round so no one can just echo the first speaker. Random cutting favours the Cultists, so the game rewards Investigators who deduce, and Cultists must bluff well to keep their edge once investigators reason. Win rates per side should be checked in playtesting. If Investigators win too rarely with strong play, raise the cut limit to 5 per player."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 24
  }
}
```
````
