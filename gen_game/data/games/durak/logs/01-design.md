# 01 design

- time: 2026-10-27T21:06:24+00:00 (109.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 58cffbbcb292a516, reply sha256 c26a6624fd85598b

## Sent

````
Original game: Durak
Players in the original: 2 to 6

Original rules:
Use 36 cards (6-A). Shuffle and deal 6 each. Turn bottom card face up to set trump suit; it stays as last draw card. Lowest trump attacks first. Attacker plays a card face up. Defender left of attacker must beat it with higher same suit or any trump. If beat, other players clockwise may add new attack cards matching any rank already on table, up to 6 total attacks. Original attacker has priority to add, then clockwise non-defenders. Defender must beat each new card. If defender beats all and no one adds, all table cards go to discard and defender becomes next attacker. If defender fails, they take entire table into hand. Others may then add matching ranks for defender to also take, up to 6. Next attacker is left of defender. After each bout, players draw to 6: main attacker first, then other attackers clockwise, then defender. When talon empty, players out of cards are eliminated. Last player with cards is durak, loser.
````

## Reply

````
```json
{
  "original_summary": "Durak is a Russian shedding card game for 2 to 6 players with a 36-card deck and a trump suit. Attackers lead cards, the defender must beat each one or pick up the whole table, and players refill from a talon. When the talon is empty, players who run out of cards are safe, and the last player still holding cards is the durak (fool), the only loser.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy works. 'Always take' grows your hand until you are the durak. 'Always defend with the cheapest card' and 'always attack low' are beaten by players who save trumps and pick their moment to take. Choices clearly change the outcome. The seat with the lowest trump attacks first, which is a small, deal-dependent edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Over many games strong players beat weak ones. A single game, though, swings heavily on the deal: how many trumps and high trumps you get, and what you draw from the talon. The outcome is also binary (durak or not), so one bad deal decides a whole match."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card counting, inferring the opponent's hand from what they could not beat, timing a deliberate take, and choosing which rank to add are deep skills. A weak player still escapes often enough to score."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, and the trump and discards are public. Good play requires inferring what the opponent holds from what they beat, how they beat it and when they took, and planning several bouts ahead in the endgame."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Who holds cards at the end is a matter of fact. Legality of a beat (same suit higher, or trump) is mechanical."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Up to 6 attack cards per bout, added by several players in priority order, means far more than 4 choice steps per round. Refilling every player to 6 from a talon is several draw events per bout. Rotating attacker and defender among up to 6 players, with elimination, is a long rule chain. A full game with a 36-card talon runs well past 40 bouts once several games are needed to tame luck."
    }
  ],
  "problems": [
    "P1: A bout can contain up to 6 attack cards, each added by any of several players, so one round needs far more than 4 choice steps.",
    "P2: Refilling every hand to 6 from the talon after each bout is many draws per round and makes a game too long to repeat within 40 rounds.",
    "P3: Multi-player rotation (who attacks, who may add, who is next) and elimination of emptied players is a long rule chain that is hard to build correctly.",
    "P4: A single game is a binary verdict (durak or not) heavily driven by the deal of trumps. Luck swamps skill over one game, which is a lottery trap.",
    "P5: The first attacker is fixed by the deal (lowest trump), a seat edge that is not balanced within a game.",
    "P6: There is no rule for illegal moves or for a game that drags on, both of which an automated engine needs."
  ],
  "changes": [
    {
      "what": "Cap each bout at 2 attack cards: one lead and at most one added card of a rank already on the table. The defender answers each.",
      "why": "This keeps the attack, beat-or-take and add-a-matching-rank structure in exactly 4 choice steps per round.",
      "fixes": "P1"
    },
    {
      "what": "Remove the talon. Each deal gives 6 cards to each player from a shuffled 36-card deck. The other 24 cards stay hidden and unused, and a randomly chosen suit is trump. There is no drawing during a deal.",
      "why": "This leaves one random event per deal and short deals. It plays Durak's most skilful phase, the no-talon endgame, with 24 unseen cards so the opponent's hand must still be inferred.",
      "fixes": "P2"
    },
    {
      "what": "Make it a two-player game.",
      "why": "Attacker and defender simply alternate, with no rotation, priority order or elimination chain. Zero-sum play also avoids the cooperation trap entirely.",
      "fixes": "P3"
    },
    {
      "what": "Play 4 deals. At the end of each deal the player still holding cards takes a penalty equal to the number of cards left, and the lower total penalty wins.",
      "why": "Four deals average out hand luck. The margin scoring rewards losing a bad deal narrowly and winning a good one cleanly, so skill shows even on poor hands.",
      "fixes": "P4"
    },
    {
      "what": "The first attacker alternates by deal: Player 1 attacks first in deals 1 and 3, Player 2 in deals 2 and 4.",
      "why": "Any first-move edge is shared exactly.",
      "fixes": "P5"
    },
    {
      "what": "Define defaults for illegal moves: an illegal attack plays your lowest card, an illegal defence counts as taking, and an illegal add counts as passing. Each deal is capped at 10 bouts, with a hand-size-difference penalty if the cap is reached, and the game is capped at 40 rounds.",
      "why": "The engine always has a legal continuation and a guaranteed end.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "36-card deck (6 to Ace in four suits) with a trump suit",
    "Attacker leads; the defender must beat with a higher card of the same suit or with a trump, or take the whole table",
    "Attackers may add cards matching a rank already on the table",
    "A successful defence discards the table and makes the defender the next attacker; a failed defence keeps the same attacker",
    "Shedding objective: being left holding cards is what loses",
    "Hidden hands, with inference from what the opponent beats, how and when they take"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Durak, a hidden-hand attack-and-defend shedding duel with trumps and rank matching, fits in 4 choices per bout once the game is two-player and talon-free. Several deals with margin scoring turn a luck-heavy single verdict into a skill test."
  },
  "variation": {
    "name": "Duel Durak",
    "summary": "A two-player, talon-free Durak played over 4 short deals. Each round is one bout: an attack card, a beat-or-take answer, an optional added card of a matching rank, and a second beat-or-take answer. Cards left in hand at the end of a deal are penalty points, and the lower total wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. The deck has 36 cards: four suits (Clubs, Diamonds, Hearts, Spades), each with ranks 6, 7, 8, 9, 10, J (11), Q (12), K (13), A (14).\n\nBEATING. A card X beats a card Y if (a) X is the same suit as Y and of higher rank, or (b) X is a trump and Y is not a trump. A trump beats a lower trump. Nothing else beats.\n\nSTRUCTURE. The game has 4 deals. Each round of the game is one bout. The game lasts at most 40 rounds.\n\nSTARTING A DEAL. At the start of each deal, shuffle all 36 cards and deal 6 cards face down to each player. Only the owner sees their hand. The remaining 24 cards are set aside face down, unseen by both players and unused for this deal. Choose the trump suit at random, each suit with chance 1/4, and announce it. Player 1 is the attacker in the first bout of deals 1 and 3. Player 2 is the attacker in the first bout of deals 2 and 4. The other player is the defender. The bout counter for the deal starts at 0.\n\nA BOUT (one round), in order:\n1. ATTACK. The attacker chooses one card from their hand and places it face up on the table. If the named card is not in their hand, their lowest-ranked card is played instead (ties broken by suit order Clubs, Diamonds, Hearts, Spades).\n2. DEFENCE. The defender either names a card from their hand that beats the attack card, which is placed face up on the table, or says TAKE. A named card that is not in their hand or does not beat the attack card counts as TAKE.\n3. ADD. This step happens only if the defender beat the first card and both players still hold at least one card. The attacker may place one more card from their hand whose rank matches the rank of either card already on the table, or say PASS. A card that does not match a rank on the table, or is not in hand, counts as PASS.\n4. SECOND DEFENCE. This step happens only if a card was added. The defender either names a card from their hand that beats the added card, or says TAKE. Illegal answers count as TAKE.\n5. RESOLVE. If the defender said TAKE at any point, the defender puts every card on the table into their hand, and the same player attacks again next bout. Otherwise all table cards are discarded face up, out of play, and the defender becomes the attacker for the next bout. All plays and the resulting hand sizes are announced to both players. Add 1 to the bout counter.\n\nENDING A DEAL. After a bout, the deal ends if either player has no cards, or if the bout counter has reached 10. Penalties are scored as follows:\n- If exactly one player has no cards, the other player (the durak) adds the number of cards in their hand to their penalty total.\n- If both have no cards, nobody scores a penalty.\n- If the deal ended by reaching 10 bouts with both players holding cards, the player holding more cards adds the difference in hand sizes to their penalty total. If the hand sizes are equal, nobody scores.\nThen the next deal begins.\n\nENDING THE GAME. The game ends when the 4th deal has ended. If round 40 finishes while a deal is still in progress, that deal is scored as if it had reached its bout cap, and the game ends.",
    "objective": "After the game ends, the player with the lower total penalty wins. If the totals are equal, the game is a draw.",
    "expected_effect": "Every bout poses real decisions. The attacker picks which card to lead, judging what the opponent can beat. The defender weighs spending a trump against taking cards back. Adding a matching rank is the main weapon, because it can force a take or strip the defender's last answer. With 24 unseen cards, each player must infer the opponent's holdings from what they beat, which suit they beat with, and when they chose to take, and must plan the last few bouts so as not to be stuck holding cards. Simple policies lose. Always TAKE lets the opponent shed every card. Always defending with the cheapest legal card burns cards predictably. Always PASS gives up the forcing add. Margin penalties over 4 deals mean a skilled player limits the damage on poor hands and maximises it on good ones, so the better player usually wins even when the trump deals are uneven. The alternating first attack removes any seat edge. There is no talk: with two players and zero-sum interests, talk adds nothing to reason with beyond bluffing that hidden hands already provide."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
